import os
import google.generativeai as genai

genai.configure(api_key=os.environ['GEMINI_API'])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
)

PROMPT = """Generate a JSON response with the following format:
{
   "title": "A short caption describing the image",
   "description": "A detailed description of the image"
}
Ensure the response is **valid JSON** and contains **only the JSON object**, with no additional text.
"""

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini and gets a JSON response."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File '{path}' not found. Ensure the correct file path is provided.")

    file = genai.upload_file(path, mime_type=mime_type)
    print(f"✅ Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def get_image_caption(file_path):
    """Generates a title and description for the image using Gemini AI."""
    gemini_file = upload_to_gemini(file_path, mime_type="image/jpeg")
    response = model.generate_content([gemini_file, "\n\n", PROMPT])

    # Debugging: Print API response
    print(f"\n🔍 Gemini API Raw Response:\n{response.text}")

    try:
        metadata_json = json.loads(response.text)  # Ensure JSON format
        return metadata_json
    except json.JSONDecodeError:
        print("❌ ERROR: Gemini response is not valid JSON!")
        return None  # Return None if JSON is invalid
