from flask import Flask, request, jsonify, send_from_directory
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os

app = Flask(__name__)

#Replace the 'crop_disease_model.h5' with the path to the trained model file.
model = tf.keras.models.load_model('crop_disease_model.h5')


class_names = ['Healthy', 'Disease1', 'Disease2', 'Disease3']


# Serve the index.html file
@app.route('/')
def serve_index():
    return send_from_directory('Frontend', 'index.html')

# Serve static files (CSS, JS, images) from the 'Frontend' directory
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('Frontend', filename)

# API endpoint to make predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        img = Image.open(io.BytesIO(file.read()))
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        crop_name = request.form.get('crop_name', '').strip()
        if not crop_name:
            return jsonify({'error': 'Crop name is required'}), 400
        

        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions, axis=1)[0]
        predicted_class = class_names[predicted_class_index]
        confidence = float(predictions[0][predicted_class_index])

        result = {
            'crop': crop_name,
            'disease': predicted_class,
            'confidence': confidence
        }

        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
