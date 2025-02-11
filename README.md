# Crop Disease Detection with AgricureAI

![AgricureAI Logo](path/to/logo.png)

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Dataset](#dataset)
6. [Model Details](#model-details)
7. [Technology Stack](#technology-stack)
8. [Contributing](#contributing)
9. [License](#license)
10. [Authors](#authors)

---

## Introduction

AgricureAI is an AI-powered web application designed to help farmers diagnose crop diseases using image recognition technology. By uploading images of affected crops, users can receive accurate predictions about the type of disease affecting their plants. This tool aims to improve agricultural productivity by providing timely and actionable insights.

---

## Features

- **Image Upload**: Users can upload images of affected crops directly from their devices.
- **Real-Time Predictions**: The application processes the uploaded image and provides a prediction about the disease within seconds.
- **User-Friendly Interface**: A simple and intuitive frontend ensures ease of use for all users.
- **Scalable Backend**: Built with Flask, the backend can handle multiple requests efficiently.
- **Advanced AI Model**: Utilizes state-of-the-art deep learning models (e.g., EfficientNet) for accurate disease detection.

---

## Installation

### Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (optional but recommended)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/crop-disease-detection.git
   cd crop-disease-detection

Model Details
The AI model used in this project is based on the EfficientNet architecture, fine-tuned for crop disease detection. The following versions were trained and tested:

crop_disease_efficientnet_V1.keras : Baseline model without data augmentation.
crop_disease_efficientnet_finetuned_V1.keras : Fine-tuned model with additional layers.
crop_disease_efficientnet_data_aug_V2.keras : Model with data augmentation techniques applied.
crop_disease_efficientnet_finetuned_data_aug_V2.keras : Final model with both fine-tuning and data augmentation.
The selected model (crop_disease_efficientnet_finetuned_data_aug_V2.keras) achieved the highest accuracy during testing.

Technology Stack
Frontend :
HTML, CSS, JavaScript
Fetch API for communicating with the backend
Backend :
Flask (Python web framework)
TensorFlow/Keras for AI model inference
Model :
EfficientNet architecture
Trained using the PlantVillage dataset
Tools :
Git for version control
Docker (optional) for containerization
Contributing
We welcome contributions to improve AgricureAI! To contribute:

Fork the repository.
Create a new branch for your feature or bug fix.
Commit your changes and push them to your fork.
Submit a pull request for review.
Please ensure your code adheres to the existing style and includes appropriate tests.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Authors
Mark Munyao - Frontend and Backend Integration github: marky376
Erick Mwangi - Model Training and Dataset Preparation github: 
Feel free to reach out to us if you have any questions or feedback!

Acknowledgments
Special thanks to the creators of the PlantVillage dataset for providing high-quality labeled data.
Thanks to the TensorFlow and Flask communities for their excellent tools and documentation.
Thank you for using AgricureAI! We hope this tool helps farmers worldwide in diagnosing crop diseases more effectively.
