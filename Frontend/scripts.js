document.getElementById('submit-btn').addEventListener('click', async () => {
    // DOM Elements
    const cropImageInput = document.getElementById('crop-image');
    const cropNameInput = document.getElementById('crop-name');
    const errorMessage = document.getElementById('error-message');
    const resultsSection = document.getElementById('results');
    const imgSection = document.getElementById('img-display');
    const submitBtn = document.getElementById('submit-btn');

    // Reset UI states
    errorMessage.hidden = true;
    resultsSection.innerHTML = '';
    imgSection.innerHTML = '<div class="preview-placeholder"><i class="fas fa-seedling placeholder-icon"></i><p class="placeholder-text">Image preview will appear here</p></div>';

    // Get form values
    const cropImage = cropImageInput.files[0];
    const cropName = cropNameInput.value.trim();

    // Validation
    let isValid = true;
    if (!cropImage) {
        showError('Please upload an image of the affected crop.');
        isValid = false;
    } else if (!['image/jpeg', 'image/png', 'image/gif'].includes(cropImage.type)) {
        showError('Please upload a valid image file (JPEG, PNG, or GIF).');
        isValid = false;
    }
    
    if (!cropName) {
        showError('Please enter the name of the crop.');
        isValid = false;
    }

    if (!isValid) return;

    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
        <span class="btn-content">
            <i class="fas fa-spinner fa-spin btn-icon"></i>
            Analyzing...
        </span>
    `;

    try {
        // Upload image
        const uploadFormData = new FormData();
        uploadFormData.append('image', cropImage);
        
        const uploadResponse = await fetch('https://turbo-space-dollop-4j75xv9p9jvxf77xg-5000.app.github.dev/upload', {
            method: 'POST',
            body: uploadFormData,
        });

        if (!uploadResponse.ok) {
            throw new Error(await uploadResponse.json().error || 'Image upload failed');
        }

        // Get prediction
        const { image_path } = await uploadResponse.json();
        const predictionResponse = await fetch('https://turbo-space-dollop-4j75xv9p9jvxf77xg-5000.app.github.dev/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image_path, crop_name: cropName }),
        });

        if (!predictionResponse.ok) {
            throw new Error(await predictionResponse.json().error || 'Prediction failed');
        }

        // Display results
        const result = await predictionResponse.json();
        updateImagePreview(result.img_url);
        displayResults(cropName, result);

    } catch (error) {
        showError(error.message || 'Failed to connect to the server. Please try again.');
        console.error('API Error:', error);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `
            <span class="btn-content">
                <i class="fas fa-microscope btn-icon"></i>
                Analyze Crop Health
            </span>
        `;
    }
});

// Helper functions
function showError(message) {
    const errorElement = document.getElementById('error-message');
    errorElement.textContent = message;
    errorElement.hidden = false;
    errorElement.setAttribute('aria-live', 'assertive');
}

function updateImagePreview(imgUrl) {
    const imgSection = document.getElementById('img-display');
    imgSection.innerHTML = imgUrl 
        ? `<div class="image-preview-container">
            <img src="${imgUrl}" alt="Analyzed crop image" class="analysis-image">
            <div class="image-overlay">Analysis Preview</div>
           </div>`
        : '<p class="error-text">Image preview unavailable</p>';
}

function displayResults(cropName, result) {
    const resultsSection = document.getElementById('results');
    resultsSection.innerHTML = `
        <div class="results-content">
            <h3 class="results-title">Diagnostic Report</h3>
            <div class="results-grid">
                <div class="result-card">
                    <h4 class="card-title"><i class="fas fa-seedling"></i> Crop Identification</h4>
                    <p class="card-value">${cropName}</p>
                </div>
                <div class="result-card">
                    <h4 class="card-title"><i class="fas fa-disease"></i> Disease Detected</h4>
                    <p class="card-value">${result.disease}</p>
                </div>
                <div class="result-card">
                    <h4 class="card-title"><i class="fas fa-percentage"></i> Confidence Level</h4>
                    <p class="card-value">${result.confidence}</p>
                </div>
            </div>
            <div class="insights-container">
                <h4 class="insights-title"><i class="fas fa-microscope"></i> AI Analysis</h4>
                <div class="markdown-content">${marked.parse(result.gemini)}</div>
            </div>
            <div class="insights-container">
                <h4 class="insights-title"><i class="fas fa-lightbulb"></i> Actionable Insights</h4>
                <div class="markdown-content">${marked.parse(result.meaningful_insights)}</div>
            </div>
        </div>
    `;
}