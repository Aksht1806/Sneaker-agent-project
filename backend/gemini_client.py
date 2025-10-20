# gemini_client.py - FINAL ROBUST VERSION

import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image
import json

SYSTEM_PROMPT = """You are a sneaker recognition expert. From the image, identify the sneaker's official Brand, Model, and Colorway. Also provide a plausible style code (SKU). Return ONLY a valid JSON object with keys: 'name', 'brand', and 'style_code'. Example: {"name": "Nike Air Jordan 1 Retro High OG 'Lost & Found'", "brand": "Nike", "style_code": "DZ5485-612"}"""

def identify_sneaker(project_id: str, location: str, image_bytes: bytes):
    """
    Identifies a sneaker using the Vertex AI SDK, with added safety checks.
    """
    try:
        # Initialize the Vertex AI client
        vertexai.init(project=project_id, location=location)
        
        # Load the model
        model = GenerativeModel(
            "gemini-1.5-pro-001",
            system_instruction=[SYSTEM_PROMPT]
        )
        
        # Load the image data
        image = Image.from_bytes(image_bytes)
        
        # Prepare the prompt
        prompt_parts = [
            "Identify this sneaker and provide details in JSON format.",
            image,
        ]

        # Generate the content
        response = model.generate_content(prompt_parts)
        
        # --- ROBUSTNESS CHECKS ADDED ---
        # 1. Check if the response has any 'candidates' (answers) at all.
        if not response.candidates:
            print("Error: The AI response contained no candidates.")
            return None

        # 2. Check if the first candidate has any 'parts' (content).
        first_candidate = response.candidates[0]
        if not first_candidate.content.parts:
            print("Error: The first candidate had no content parts.")
            return None
        # --- END OF CHECKS ---

        # Extract and parse the JSON response safely
        json_text = first_candidate.content.parts[0].text.strip()
        sneaker_data = json.loads(json_text)
        
        return sneaker_data

    except Exception as e:
        print(f"An error occurred in the Vertex AI client: {e}")
        return None