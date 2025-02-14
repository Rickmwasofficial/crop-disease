document.getElementById('submit-btn').addEventListener('click', async () => {
    const cropImageInput = document.getElementById('crop-image');
    const cropNameInput = document.getElementById('crop-name');
    const errorMessage = document.getElementById('error-message');
    const resultsSection = document.getElementById('results');

    errorMessage.style.display = 'none';
    resultsSection.innerHTML = '';

    const cropImage = cropImageInput.files[0];
    const cropName = cropNameInput.value.trim();

    // Validation checks
    if (!cropImage) {
        errorMessage.textContent = 'Please upload an image of the affected crop.';
        errorMessage.style.display = 'block';
        return;
    }

    const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!validImageTypes.includes(cropImage.type)) {
        errorMessage.textContent = 'Please upload a valid image file (JPEG, PNG, or GIF).';
        errorMessage.style.display = 'block';
        return;
    }

    if (!cropName) {
        errorMessage.textContent = 'Please enter the name of the crop.';
        errorMessage.style.display = 'block';
        return;
    }

    resultsSection.innerHTML = '<p style="font-weight: bold;">Processing your request...</p>';

    try {
        // First, upload the image to save it on the server
        const uploadFormData = new FormData();
        uploadFormData.append('image', cropImage);
        
        // Upload the image first
        const uploadResponse = await fetch('https://turbo-space-dollop-4j75xv9p9jvxf77xg-5000.app.github.dev/upload', {
            method: 'POST',
            body: uploadFormData,
        });

        const uploadResult = await uploadResponse.json();

        if (!uploadResponse.ok) {
            throw new Error(uploadResult.error || 'Failed to upload image');
        }

        // Now send the prediction request with the saved image path
        const predictionResponse = await fetch('https://turbo-space-dollop-4j75xv9p9jvxf77xg-5000.app.github.dev/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image_path: uploadResult.image_path,
                crop_name: cropName
            }),
        });

        const result = await predictionResponse.json();

        if (predictionResponse.ok) {
            resultsSection.innerHTML = `
                <h3>Prediction Result:</h3>
                <p><strong>Crop:</strong> ${cropName}</p>
                <p><strong>Disease Detected:</strong> ${result.disease}</p>
                <p><strong>Confidence:</strong> ${result.confidence}</p>
                <p>${marked.parse(result.gemini)}</p>
            `;
        } else {
            resultsSection.innerHTML = `<p>Error: ${result.error || 'An unknown error occurred.'}</p>`;
        }

    } catch (error) {
        resultsSection.innerHTML = `<p>Error: ${error.message || 'Failed to connect to the server. Please try again.'}</p>`;
        console.error('Error during API call:', error);
    }
});