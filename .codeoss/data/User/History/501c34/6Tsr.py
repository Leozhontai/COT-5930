import os
import google.generativeai as genai
import json

# Configure API key
genai.configure(api_key=os.environ['GEMINI_API'])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

# Define the Gemini model
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
)

# Define the structured prompt
PROMPT = """You are an AI that analyzes images and generates structured JSON output. 
For the given image, provide a JSON response with:
{
   "title": "A short, meaningful title summarizing the image",
   "description": "A detailed explanation of what is in the image."
}
Ensure that the response is **valid JSON** and contains **only the JSON object**, without additional text.
"""

def upload_to_gemini(path, mime_type="image/jpeg"):
    """Uploads an image to Gemini AI and returns a file reference."""
    if not os.path.exists(path):
        print(f"❌ ERROR: File '{path}' not found.")
        return None

    file = genai.upload_file(path, mime_type=mime_type)
    print(f"✅ Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def generate_image_metadata(image_path):
    """Uploads an image and gets a structured JSON response with title & description."""
    gemini_file = upload_to_gemini(image_path)
    
    if gemini_file is None:
        return None

    response = model.generate_content([gemini_file, "\n\n", PROMPT])

    # Debugging: Print raw API response
    print(f"\n🔍 Gemini API Raw Response:\n{response.text}")

    try:
        metadata_json = json.loads(response.text)  # Ensure JSON format
        print(f"✅ Parsed JSON:\n{metadata_json}")
        return metadata_json

    except json.JSONDecodeError:
        print("❌ ERROR: Gemini AI response is not valid JSON!")
        return None  # Return None if JSON is invalid
