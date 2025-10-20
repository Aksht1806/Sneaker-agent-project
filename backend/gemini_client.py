# gemini_client.py - FINAL VERSION using Vertex AI SDK

import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image
import json

SYSTEM_PROMPT = """You are a sneaker recognition expert. From the image, identify the sneaker's official Brand, Model, and Colorway. Also provide a plausible style code (SKU). Return ONLY a valid JSON object with keys: 'name', 'brand', and 'style_code'. Example: {"name": "Nike Air Jordan 1 Retro High OG 'Lost & Found'", "brand": "Nike", "style_code": "DZ5485-612"}"""

def identify_sneaker(project_id: str, location: str, image_bytes: bytes):
    """
    Identifies a sneaker using the Vertex AI SDK, which is more robust.
    """
    try:
        # Initialize the Vertex AI client
        vertexai.init(project=project_id, location=location)
        
        # Load the model
        model = GenerativeModel(
            "gemini-1.5-pro-001", # A specific, stable version of the model
            system_instruction=[SYSTEM_PROMPT]
        )
        
        # Load the image data for the model
        image = Image.from_bytes(image_bytes)
        
        # Prepare the prompt
        prompt_parts = [
            "Identify this sneaker and provide details in JSON format.",
            image,
        ]

        # Generate the content
        response = model.generate_content(prompt_parts)
        
        # Extract and parse the JSON response
        json_text = response.text.strip()
        sneaker_data = json.loads(json_text)
        
        return sneaker_data

    except Exception as e:
        print(f"An error occurred in the Vertex AI client: {e}")
        return None