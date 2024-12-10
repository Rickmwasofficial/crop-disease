// scripts.js
document.getElementById('submit-btn').addEventListener('click', function () {
  const cropImage = document.getElementById('crop-image').files[0];
  const cropName = document.getElementById('crop-name').value.trim();
  const errorMessage = document.getElementById('error-message');

  if (!cropImage) {
      alert('Please upload an image of the affected crop.');
      return;
  }

  const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];
  if (!validImageTypes.includes(cropImage.type)) {
      errorMessage.style.display = 'block';
      errorMessage.textContent = 'Please upload a valid image file (JPEG, PNG, GIF).';
      return;
  }

  if (!cropName) {
      alert('Please enter the name of the crop.');
      return;
  }

  errorMessage.style.display = 'none'; // Hide error
  alert(`Image and crop name submitted successfully!\nCrop: ${cropName}`);
  // Here, you would send the data to the AI backend for processing
});
