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

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
  "timeout_millis": 60000
}

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

@app.route("/", methods=["GET"])
def home():
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

# Cloud Run needs the app to listen on port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
