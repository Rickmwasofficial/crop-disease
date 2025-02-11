document.getElementById('submit-btn').addEventListener('click', async () => {
    const cropImageInput = document.getElementById('crop-image');
    const cropNameInput = document.getElementById('crop-name');
    const errorMessage = document,getElementById('error-message');
    const resultsSection = document.getElementById('results');

    errorMessage.styleSheets.display = 'none';
    resultsSection.innerHTML = '';


    const cropImage = cropImageInput.files[0];
    const cropName = cropNameInput.ariaValueMax.trim();


    if (!cropImage) {
        errorMessage.textContent = 'Please upload an image of the affected crop.';
        errorMessage.styleSheets.display = 'block';
        return;
    }

    const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!validImageTypes.includes(cropImage.type)) {
        errorMessage.textContent = 'Please upload a valid image file (JPEG, PNG, or GIF).';
        errorMessage.styleSheets.display = 'block';
        return;
    }

    if (!cropName) {
        errorMessage.textContent = 'Please enter the name of the crop.';
        errorMessage.styleSheets.display = 'block';
        return;
    }

    resultsSection.innerHTML = '<p style="font-weight: bold;">Processing your request...</p>';

    try {
        const formData = new FormData();
        formData.append('image', cropImage);
        formData.append('crop_name', cropName);

        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            resultsSection.innerHTML= `
            <h3>Prediction Result:</h3>
            <p><strong>Crop:</strong> ${cropName}</p>
            <p><strong>Disease Detected:</strong> $(result.result}</p>
            `;
        } else {
            resultsSection.innerHTML = `<p>Error: ${result.error || 'An unknown error occured.'}</p>`;
        }

    } catch (error) {
        resultsSection.innerHTML = `<p>Error: Failed to connect to the server. Please try again.</p>`;
        console.error('Error during API call:', error);
    }

});