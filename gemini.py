from flask import Flask, request, jsonify
import os
import google.generativeai as genai
import json
import re

app = Flask(__name__)

# Configure Gemini AI API key
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
        return None
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        return file
    except Exception:
        return None

def generate_image_metadata(image_path):
    gemini_file = upload_to_gemini(image_path)
    if gemini_file is None:
        return None
    try:
        response = model.generate_content([gemini_file, "\n\n", PROMPT])
        json_match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if not json_match:
            return None
        clean_json = json_match.group(0)
        return json.loads(clean_json)
    except Exception:
        return None

@app.route("/")
def home():
    return "✅ Gemini Image Metadata API is running!"

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    uploaded_file = request.files["file"]
    temp_path = os.path.join("/tmp", uploaded_file.filename)
    uploaded_file.save(temp_path)

    result = generate_image_metadata(temp_path)
    if result is None:
        return jsonify({"error": "Failed to analyze image"}), 500

    return jsonify(result)

# Required for Cloud Run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
