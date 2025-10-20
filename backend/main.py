# main.py - FINAL VERSION using Vertex AI SDK

from flask import Flask, request, jsonify
from flask_cors import CORS
import gemini_client
import scraper
import base64
from io import BytesIO
from PIL import Image
import os

# --- ACTION REQUIRED ---
# Find your Project ID in the Google Cloud Console and paste it here.
# It usually looks like 'gen-ai-project-123456' or similar.
# Make sure this is the same project you initialized with 'gcloud init'.
GCP_PROJECT_ID = "gen-lang-client-0524943717"
GCP_PROJECT_LOCATION = "us-central1" # You can leave this as is.
# --- END ACTION ---

if "PASTE_YOUR_GCP_PROJECT_ID_HERE" in GCP_PROJECT_ID:
    raise ValueError("Please replace 'PASTE_YOUR_GCP_PROJECT_ID_HERE' with your actual GCP Project ID in main.py")

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze_sneaker():
    if not request.json or 'image' not in request.json:
        return jsonify({'error': 'Missing image data in request'}), 400

    try:
        base64_data = request.json['image'].split(',')[1]
        image_bytes = base64.b64decode(base64_data)
        
        sneaker_data = gemini_client.identify_sneaker(
            project_id=GCP_PROJECT_ID,
            location=GCP_PROJECT_LOCATION,
            image_bytes=image_bytes
        )
        
        if not sneaker_data:
            return jsonify({'error': 'Could not identify the sneaker from the image.'}), 500

        price_listings = scraper.get_mock_price_listings()
        price_history = scraper.get_mock_price_history()

        response_data = {
            'sneaker_info': sneaker_data,
            'price_listings': price_listings,
            'price_history': price_history
        }
        
        return jsonify(response_data)

    except Exception as e:
        print(f"An unexpected error occurred in main.py: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500

# NOTE: The if __name__ == '__main__': block has been removed for production.
# Gunicorn will be used to run the 'app' object directly.