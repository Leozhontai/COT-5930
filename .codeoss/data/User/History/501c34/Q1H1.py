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
#   generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

PROMPT = "describe the image. end your response in json"

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File '{path}' not found. Ensure the correct file path is provided.")

    file = genai.upload_file(path, mime_type=mime_type)
    print(f"✅ Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# 🔹 Prevent auto-execution when `gemini.py` is imported
if __name__ == "__main__":
    response = model.generate_content(
        [upload_to_gemini('licensed-image.jpeg', mime_type="image/jpeg"), "\n\n", PROMPT]
    )

    print(response.text)
