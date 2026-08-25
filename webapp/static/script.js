let selectedFile = null;
let currentDiseasePage = null;

const imageInput = document.getElementById('imageInput');
const loader = document.getElementById('loader');
const resultArea = document.getElementById('resultArea');
const statusText = document.getElementById('statusText');
const causeText = document.getElementById('causeText');
const treatmentText = document.getElementById('treatmentText');
const detailBtn = document.getElementById('detailBtn');

imageInput.addEventListener('change', (e) => {
    selectedFile = e.target.files[0];
});

async function checkHealth() {
    if (!selectedFile) {
        alert("Please upload a chili leaf image first.");
        return;
    }

    loader.classList.remove('hidden');
    resultArea.classList.add('hidden');

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Prediction failed');
        }

        const data = await response.json();

        statusText.textContent = data.title;
        statusText.className = data.disease === 'Healthy'
            ? "text-3xl font-black mb-4 text-green-600"
            : "text-3xl font-black mb-4 text-red-600";

        causeText.textContent = data.cause;
        treatmentText.textContent = data.quick_tip;

        currentDiseasePage = data.page;

        loader.classList.add('hidden');
        resultArea.classList.remove('hidden');

    } catch (error) {
        loader.classList.add('hidden');
        alert("Something went wrong while analyzing the image. Please try again.");
        console.error(error);
    }
}

detailBtn.addEventListener('click', () => {
    if (currentDiseasePage) {
        window.location.href = `/disease/${currentDiseasePage}`;
    }
});