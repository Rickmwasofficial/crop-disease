from flask import Flask, request, jsonify, send_from_directory, url_for
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import os
from werkzeug.utils import secure_filename
import time
import requests
import json
from training.chatbot import get_disease_insights
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv('GEMINI_API'))

# Create the gemini model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
}

gemi = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  system_instruction="""
    Return a direct, formatted markdown response without any introductory sentences or acknowledgments. 
    When given information about a crop disease:
    - Start immediately with a level 2 heading '## Causes'
    - Follow with the causes of the disease in clear, simple language
    - Then add a level 2 heading '## Solutions'
    - List practical solutions with bullet points
    - Add a level 2 heading '## Prevention'
    - Provide prevention measures with bullet points
    - End with a level 2 heading '## Sources'
    - List 2-3 credible sources as links

    If the crop is healthy, start with a level 2 heading '## Maintaining Healthy {crop}' and provide advice.
    Use simple, accessible language throughout.
    """,
)

chat_session = gemi.start_chat(
  history=[
    
  ]
)

# Configuration
UPLOAD_FOLDER = 'uploaded_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Load the model
model = tf.keras.models.load_model('crop_disease_efficientnet_finetuned_V1.keras')

# Class names
class_names = [
    'Gray Leaf Spot',
    'Common Rust',
    'Healthy',
    'Northern Leaf Blight'
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            # Create unique filename using timestamp
            timestamp = int(time.time() * 1000)
            filename = f"{timestamp}_{secure_filename(file.filename)}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the file
            file.save(filepath)
            
            return jsonify({
                'message': 'File uploaded successfully',
                'image_path': filepath
            })
        
        return jsonify({'error': 'Invalid file type'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to serve uploaded images
@app.route('/uploaded_images/<filename>')
def serve_uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'image_path' not in data:
            return jsonify({'error': 'No image path provided'}), 400

        image_path = data['image_path']
        crop_name = data.get('crop_name', '').strip()

        if not crop_name:
            return jsonify({'error': 'Crop name is required'}), 400

        if not os.path.exists(image_path):
            return jsonify({'error': 'Image file not found'}), 404

        img = tf.io.read_file(image_path)

        # Extract the filename from the full path
        filename = os.path.basename(image_path)
        image_url = f"https://turbo-space-dollop-4j75xv9p9jvxf77xg-5000.app.github.dev/uploaded_images/{filename}"
        print(f"Predict endpoint generated URL: {image_url}")

        # Decode the image into a tensor
        img = tf.image.decode_image(img, channels=3)  # Ensure 3 channels (RGB)

        # Resize the image to the expected input shape
        img = tf.image.resize(img, size=[224, 224])

        # Rescale the image to [0, 1]
        img_1 = img / 255.0

        # Expand dimensions to fit model input
        img = tf.expand_dims(img, axis=0)

        # Make prediction
        preds = model.predict(img, verbose=0)

        # Print predictions for debugging
        # print("Predictions:", preds)

        # Get the class index with the highest probability
        predicted_class_index = tf.argmax(preds[0])
        predicted_class = class_names[predicted_class_index]
        confidence = float(preds[0][predicted_class_index])

        # Clean up - optionally remove the uploaded file
        # os.remove(image_path)  


        gemini_response = chat_session.send_message(f'The crop is {crop_name} and the disease is {predicted_class}').text
        meaningful_insights= get_disease_insights(predicted_class)

        return jsonify({
            'crop': crop_name,
            'disease': predicted_class,
            'confidence': confidence,
            "meaningful_insights": meaningful_insights,
            "gemini": gemini_response,
            "img_url": image_url
        })

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def serve_index():
    return send_from_directory('../Frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../Frontend', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)