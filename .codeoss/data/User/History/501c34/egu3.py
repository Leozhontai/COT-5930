import os
import google.generativeai as genai
import json

# Configure Gemini API key
API_KEY = os.getenv("GEMINI_API")
if not API_KEY:
    raise ValueError("❌ ERROR: GEMINI_API key is not set. Run 'export GEMINI_API=\"your-api-key\"'.")

genai.configure(api_key=API_KEY)

PROMPT = """Analyze the given image and respond ONLY in JSON format.
Ensure the response follows this exact structure:

{
   "title": "A short, meaningful title summarizing the image",
   "description": "A detailed explanation of what is in the image."
}

DO NOT include any extra text, explanations, or formatting—only return a valid JSON object.
"""

def generate_image_metadata(image_path):
    """Uploads an image and gets structured JSON metadata."""
    if not os.path.exists(image_path):
        print(f"❌ ERROR: File '{image_path}' not found.")
        return None

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([image_path, PROMPT])

        metadata_json = json.loads(response.text.strip())
        return metadata_json

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None
