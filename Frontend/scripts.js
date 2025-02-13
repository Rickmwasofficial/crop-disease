document.getElementById('submit-btn').addEventListener('click', async () => {
    const cropImageInput = document.getElementById('crop-image');
    const cropNameInput = document.getElementById('crop-name');
    const errorMessage = document.getElementById('error-message');
    const resultsSection = document.getElementById('results');

    errorMessage.style.display = 'none'; // Correct: style.display
    resultsSection.innerHTML = '';

    const cropImage = cropImageInput.files[0];
    const cropName = cropNameInput.value.trim(); // Correct: cropNameInput.value

    if (!cropImage) {
        errorMessage.textContent = 'Please upload an image of the affected crop.';
        errorMessage.style.display = 'block'; // Correct: style.display
        return;
    }

    const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!validImageTypes.includes(cropImage.type)) {
        errorMessage.textContent = 'Please upload a valid image file (JPEG, PNG, or GIF).';
        errorMessage.style.display = 'block'; // Correct: style.display
        return;
    }

    if (!cropName) {
        errorMessage.textContent = 'Please enter the name of the crop.';
        errorMessage.style.display = 'block'; // Correct: style.display
        return;
    }

    resultsSection.innerHTML = '<p style="font-weight: bold;">Processing your request...</p>';

    try {
        const formData = new FormData();
        formData.append('image', cropImage);
        formData.append('crop_name', cropName);

        const response = await fetch('https://musical-zebra-g4qjgrwvw4673v9gq-5000.app.github.dev/predict', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            resultsSection.innerHTML = 
                <h3>Prediction Result:</h3>
                <p><strong>Crop:</strong> ${cropName}</p>
                <p><strong>Disease Detected:</strong> ${result.disease}</p> <p><strong>Confidence:</strong> ${result.confidence}</p>
            ; // Access the correct property: result.disease
        } else {
            resultsSection.innerHTML = <p>Error: ${result.error || 'An unknown error occurred.'}</p>;
        }

    } catch (error) {
        resultsSection.innerHTML = <p>Error: Failed to connect to the server. Please try again.</p>;
        console.error('Error during API call:', error);
    }

});
