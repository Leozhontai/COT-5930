import os
import json
import google.generativeai as genai

# Securely configure API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is not set. Please set it as an environment variable.")

genai.configure(api_key=API_KEY)

# Define the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Prompt to ensure a structured JSON response
PROMPT = """You are an AI that analyzes images and generates structured JSON output. 
For the given image, provide a JSON response with:
{
   "title": "A short, meaningful title summarizing the image",
   "description": "A detailed explanation of what is in the image."
}
Ensure that the response is **valid JSON** and contains **only the JSON object**, without additional text.
"""

def generate_image_metadata(image_path):
    """Uploads an image to Gemini AI and retrieves a structured JSON response with title & description."""
    try:
        # Upload image to Gemini AI
        gemini_file = genai.upload_file(image_path, mime_type="image/jpeg")
        print(f"✅ Uploaded image to Gemini AI: {image_path}")

        # Generate AI response
        response = model.generate_content([gemini_file, "\n\n", PROMPT])

        # Debugging: Print raw API response
        print(f"\n🔍 Gemini API Raw Response:\n{response.text}")

        # Convert to JSON
        metadata_json = json.loads(response.text)  # Ensure JSON format
        print(f"✅ Parsed JSON Output:\n{metadata_json}")

        return metadata_json

    except json.JSONDecodeError:
        print("❌ ERROR: Gemini AI response is not valid JSON!")
        return None  # Return None if JSON is invalid

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

