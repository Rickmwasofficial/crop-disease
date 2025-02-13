from flask import Flask, request, jsonify, send_from_directory
import tensorflow as tf
import numpy as np
import io
import os

app = Flask(__name__)

# Load the model
model = tf.keras.models.load_model('crop_disease_efficientnet_finetuned_V1.keras')

# Class names
class_names = [
    'Gray Leaf Spot',
    'Common Rust',
    'Healthy',
    'Northern Leaf Blight'
]

def process_image_and_predict(file_bytes):
    """
    Process image bytes and make predictions using the model
    """
    # Decode image from bytes
    img = tf.image.decode_image(file_bytes, channels=3)
    
    # Resize the image
    img = tf.image.resize(img, size=[224, 224])
    
    # Rescale to [0,1]
    img = tf.cast(img, tf.float32) / 255.0
    
    # Add batch dimension
    img = tf.expand_dims(img, axis=0)
    
    # Make prediction
    predictions = model.predict(img, verbose=0)
    
    # Get predicted class and confidence
    predicted_class_index = tf.argmax(predictions[0]).numpy()
    predicted_class = class_names[predicted_class_index]
    confidence = float(predictions[0][predicted_class_index])
    
    return predicted_class, confidence, predictions

@app.route('/')
def serve_index():
    return send_from_directory('../Frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../Frontend', filename)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if image was provided
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Read the file
        img_bytes = file.read()
        
        # Validate crop name
        crop_name = request.form.get('crop_name', '').strip()
        if not crop_name:
            return jsonify({'error': 'Crop name is required'}), 400
        
        # Process image and get predictions
        predicted_class, confidence, preds = process_image_and_predict(img_bytes)
        
        # Print predictions for debugging
        print("Predictions:", preds)
        
        # Prepare response
        result = {
            'crop': crop_name,
            'disease': predicted_class,
            'confidence': float(confidence)  # Ensure confidence is JSON serializable
        }
        
        return jsonify(result)
    
    except tf.errors.InvalidArgumentError as e:
        return jsonify({'error': 'Invalid image format or corrupted image file'}), 400
    except Exception as e:
        print(f"Error processing request: {str(e)}")  # Log the error
        return jsonify({'error': 'An error occurred processing the image'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
