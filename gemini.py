import os
import google.generativeai as genai
import json
import re
from flask import Flask, request, jsonify

app = Flask(__name__)  # Added for Flask

# ✅ Original Setup
API_KEY = os.getenv("GEMINI_API")
if not API_KEY:
    raise ValueError("❌ ERROR: GEMINI_API key is not set.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

PROMPT = """Analyze the given image and respond ONLY in JSON format.
Ensure the response follows this exact structure:

{
   "title": "A short, meaningful title summarizing the image",
   "description": "A detailed explanation of what is in the image."
}

DO NOT include any extra text, explanations, or formatting—only return a valid JSON object.
"""

def upload_to_gemini(path, mime_type="image/jpeg"):
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
    gemini_file = upload_to_gemini(image_path)
    if gemini_file is None:
        return None
    try:
        response = model.generate_content([gemini_file, "\n\n", PROMPT])
        print(f"\n🔍 Gemini API Raw Response:\n{response.text}")
        json_match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if not json_match:
            print("❌ ERROR: No valid JSON detected in response.")
            return None
        metadata_json = json.loads(json_match.group(0))
        print(f"✅ Parsed JSON:\n{metadata_json}")
        return metadata_json
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

# ✅ NEW: Flask-only for Cloud Run compatibility

@app.route("/", methods=["GET"])
def health_check():
    return "✅ Gemini Image Metadata API is running!"

@app.route("/analyze", methods=["POST"])
def analyze_image():
    if 'file' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['file']
    path = os.path.join("/tmp", file.filename)
    file.save(path)

    result = generate_image_metadata(path)
    if result is None:
        return jsonify({"error": "Failed to analyze image"}), 500

    return jsonify(result)

# ✅ Keep original CLI functionality if run locally
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Use it like: python gemini.py yourimage.jpg
        image_path = sys.argv[1]
        generate_image_metadata(image_path)
    else:
        # Only needed for Cloud Run
        app.run(host="0.0.0.0", port=8080)
