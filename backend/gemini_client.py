# gemini_client.py - FINAL, DEFINITIVE VERSION

import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image
import json

SYSTEM_PROMPT = """You are a sneaker recognition expert. From the image, identify the sneaker's official Brand, Model, and Colorway. Also provide a plausible style code (SKU). Return ONLY a valid JSON object with keys: 'name', 'brand', and 'style_code'. Example: {"name": "Nike Air Jordan 1 Retro High OG 'Lost & Found'", "brand": "Nike", "style_code": "DZ5485-612"}"""

def identify_sneaker(project_id: str, location: str, image_bytes: bytes):
    """
    Identifies a sneaker using the Vertex AI SDK with the most stable model.
    """
    try:
        # Initialize the Vertex AI client
        vertexai.init(project=project_id, location=location)
        
        # Load the model
        # THIS IS THE FINAL, CORRECTED MODEL NAME
        model = GenerativeModel(
            "gemini-1.0-pro-vision", 
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
        
        # Robustness checks
        if not response.candidates or not response.candidates[0].content.parts:
            print("Error: The AI response was empty or malformed.")
            return None

        # Extract and parse the JSON response safely
        json_text = response.candidates[0].content.parts[0].text.strip()
        sneaker_data = json.loads(json_text)
        
        return sneaker_data

    except Exception as e:
        print(f"An error occurred in the Vertex AI client: {e}")
        return None