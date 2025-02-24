import os
import google.generativeai as genai
import json
import re  # Import regex for extracting valid JSON

# Configure Gemini AI API key
API_KEY = os.getenv("GEMINI_API")
if not API_KEY:
    raise ValueError("❌ ERROR: GEMINI_API key is not set. Run 'export GEMINI_API=\"your-api-key\"'.")

genai.configure(api_key=API_KEY)

# Define the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
)

# Define the structured prompt to enforce proper JSON response
PROMPT = """Analyze the given image and respond ONLY in JSON format.
Ensure the response follows this exact structure:

{
   "title": "A short, meaningful title summarizing the image",
   "description": "A detailed explanation of what is in the image."
}

DO NOT include any extra text, explanations, or formatting—only return a valid JSON object.
"""

def upload_to_gemini(path, mime_type="image/jpeg"):
    """Uploads an image to Gemini AI and returns a file reference."""
    if not os.path.exists(path):
        print(f"❌ ERROR: File '{path}' not found.")
        return None

    try:
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"✅ Uploaded file '{file.display_name}' as: {file.uri}")
        return file
    except Exception as e:
        print(f"❌ ERROR: Failed to upload file: {e}")
        return None

def generate_image_metadata(image_path):
    """Uploads an image and gets a structured JSON response with title & description."""
    gemini_file = upload_to_gemini(image_path)

    if gemini_file is None:
        return None

    try:
        response = model.generate_content([gemini_file, "\n\n", PROMPT])

        # Debugging: Print raw API response
        print(f"\n🔍 Gemini API Raw Response:\n{response.text}")

        # Extract only the valid JSON part using regex
        json_match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if not json_match:
            print("❌ ERROR: No valid JSON detected in response.")
            return None

        clean_json = json_match.group(0)  # Extract matched JSON part
        metadata_json = json.loads(clean_json)  # Convert to Python dict

        print(f"✅ Parsed JSON:\n{metadata_json}")

        # Convert JSON to text format
        text_metadata = f"Title: {metadata_json['title']}\nDescription: {metadata_json['description']}"
        return text_metadata

    except json.JSONDecodeError:
        print("❌ ERROR: Gemini AI response is not valid JSON!")
        return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

