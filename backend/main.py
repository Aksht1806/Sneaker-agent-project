# main.py - FINAL ROBUST VERSION

from flask import Flask, request, jsonify
from flask_cors import CORS
import gemini_client
import scraper
import base64
from io import BytesIO
from PIL import Image
import os

# Your Project ID should already be here.
GCP_PROJECT_ID = "gen-lang-client-0524943717"
GCP_PROJECT_LOCATION = "us-central1"

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze_sneaker():
    if not request.json or 'image' not in request.json:
        return jsonify({'error': 'Missing image data in request'}), 400

    try:
        base64_data = request.json['image'].split(',')[1]
        image_bytes = base64.b64decode(base64_data)
        
        # Call the gemini client to get sneaker data
        sneaker_data = gemini_client.identify_sneaker(
            project_id=GCP_PROJECT_ID,
            location=GCP_PROJECT_LOCATION,
            image_bytes=image_bytes
        )
        
        # --- FINAL ROBUSTNESS CHECK ADDED ---
        # If the gemini_client returned None (meaning the AI failed),
        # stop here and send a professional error message to the frontend.
        if sneaker_data is None:
            print("Main.py: identify_sneaker returned None. Sending error to frontend.")
            return jsonify({'error': 'The AI could not identify this sneaker. Please try a clearer image.'}), 500
        # --- END OF CHECK ---

        # The code below will ONLY run if sneaker_data is valid.
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