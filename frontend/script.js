// --- CONFIGURATION ---
// IMPORTANT: You will replace this placeholder with your actual Render backend URL after you deploy it.
const API_BASE_URL = 'https://your-backend-name.onrender.com';

// --- DOM Elements ---
const imageDropArea = document.getElementById('image-drop-area');
const imageUpload = document.getElementById('image-upload');
const identifyBtn = document.getElementById('identify-btn');
// ... (the rest of your script.js file is exactly the same as before) ...
// ... (no other changes are needed in this file) ...

// --- The rest of your script.js code goes here ---
const imagePreviewContainer = document.getElementById('image-preview-container');
const imagePreview = document.getElementById('image-preview');
const uploadPrompt = document.getElementById('upload-prompt');
const uploadSection = document.getElementById('upload-section');
const resultsSection = document.getElementById('results-section');
const loaderContainer = document.getElementById('loader-container');
const progressText = document.getElementById('progress-text');
const resultContent = document.getElementById('result-content');
const sneakerNameEl = document.getElementById('sneaker-name');
const sneakerSkuEl = document.getElementById('sneaker-sku');
const resultImage = document.getElementById('result-image');
const priceListings = document.getElementById('price-listings');
const errorMessage = document.getElementById('error-message');
const errorText = document.getElementById('error-text');
const resetBtn = document.getElementById('reset-btn');
const priceChartCanvas = document.getElementById('price-chart');

let file = null;
let priceChart = null;

// --- Event Listeners ---
imageDropArea.addEventListener('click', () => imageUpload.click());
imageDropArea.addEventListener('dragover', (e) => { e.preventDefault(); imageDropArea.classList.add('bg-gray-50', 'dark:bg-gray-700', 'border-blue-500'); });
imageDropArea.addEventListener('dragleave', () => imageDropArea.classList.remove('bg-gray-50', 'dark:bg-gray-700', 'border-blue-500'));
imageDropArea.addEventListener('drop', (e) => { e.preventDefault(); imageDropArea.classList.remove('bg-gray-50', 'dark:bg-gray-700', 'border-blue-500'); if (e.dataTransfer.files.length) { handleFile(e.dataTransfer.files[0]); } });
imageUpload.addEventListener('change', (e) => { if (e.target.files.length) { handleFile(e.target.files[0]); } });
identifyBtn.addEventListener('click', identifyAndAnalyze);
resetBtn.addEventListener('click', resetUI);

// --- Core Functions ---
function handleFile(inputFile) {
    if (inputFile && inputFile.type.startsWith('image/')) {
        file = inputFile;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            uploadPrompt.classList.add('hidden');
            imagePreviewContainer.classList.remove('hidden');
            identifyBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    } else {
        showError("Please upload a valid image file."); file = null;
    }
}

function resetUI() {
    file = null;
    imageUpload.value = '';
    uploadPrompt.classList.remove('hidden');
    imagePreviewContainer.classList.add('hidden');
    imagePreview.src = '';
    identifyBtn.disabled = true;
    uploadSection.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    loaderContainer.classList.add('hidden');
    resultContent.classList.add('hidden');
    errorMessage.classList.add('hidden');
    if(priceChart) { priceChart.destroy(); }
}

async function identifyAndAnalyze() {
    if (!file) { showError("No image selected."); return; }

    // --- Show loading state ---
    uploadSection.classList.add('hidden');
    resultsSection.classList.remove('hidden');
    loaderContainer.classList.remove('hidden');
    progressText.textContent = 'Uploading and identifying...';
    resultContent.classList.add('hidden');
    errorMessage.classList.add('hidden');

    try {
        const base64Image = await fileToBase64(file);

        // --- Make API call to the backend ---
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: base64Image })
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.error || `Request failed with status ${response.status}`);
        }

        const data = await response.json();
        
        // --- Populate UI with data from backend ---
        progressText.textContent = 'Analysis complete!';
        
        // Sneaker Info
        const { sneaker_info, price_listings, price_history } = data;
        sneakerNameEl.textContent = sneaker_info.name;
        sneakerSkuEl.textContent = `Style Code: ${sneaker_info.style_code}`;
        resultImage.src = URL.createObjectURL(file);

        // Price Listings
        displayPriceListings(price_listings);
        
        // Price Chart
        displayPriceChart(price_history);
        
        // --- Show final results ---
        loaderContainer.classList.add('hidden');
        resultContent.classList.remove('hidden');

    } catch (err) {
        console.error("Error during analysis:", err);
        showError(err.message || "An unknown error occurred during analysis.");
        loaderContainer.classList.add('hidden');
    }
}

// --- Display Functions ---
function displayPriceListings(listings) {
    priceListings.innerHTML = ''; // Clear previous results
    if (!listings || listings.length === 0) {
        priceListings.innerHTML = '<p>No price listings found.</p>';
        return;
    }
    
    listings.forEach(source => {
        const listingEl = document.createElement('div');
        listingEl.className = 'flex items-center justify-between p-4 bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700';
        listingEl.innerHTML = `
            <div class="flex items-center gap-4">
                <img src="${source.logo}" alt="${source.name} logo" class="w-8 h-8 rounded-full">
                <div>
                    <p class="font-semibold text-lg">${source.name}</p>
                    <p class="text-sm text-gray-500 dark:text-gray-400">${source.condition} - Size ${source.size}</p>
                </div>
            </div>
            <div class="text-right">
                <p class="text-xl font-bold text-green-600 dark:text-green-400">$${source.price.toFixed(2)}</p>
            </div>
        `;
        priceListings.appendChild(listingEl);
    });
}

function displayPriceChart(history) {
    if(priceChart) { priceChart.destroy(); }
    
    priceChart = new Chart(priceChartCanvas, {
        type: 'line',
        data: {
            labels: history.labels,
            datasets: [{
                label: 'Average Sale Price',
                data: history.data,
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                fill: true,
                tension: 0.4,
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    ticks: {
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 8 // Show fewer labels on the x-axis for readability
                    }
                },
                y: { ticks: { callback: value => '$' + value } }
            }
        }
    });
}

// --- Helper Functions ---
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}
        
function showError(message) {
    uploadSection.classList.add('hidden');
    resultsSection.classList.remove('hidden');
    loaderContainer.classList.add('hidden');
    resultContent.classList.add('hidden');
    errorMessage.classList.remove('hidden');
    errorText.textContent = message;
}

// --- Initial State ---
identifyBtn.disabled = true;