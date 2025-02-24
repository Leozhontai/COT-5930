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

PROMPT = """You are an AI that analyzes images and generates structured JSON output. 
For the given image, provide a JSON response with:
{
   "title": "A short, meaningful title summarizing the image",
   "description": "A detailed explanation of what is in the image."
}
Ensure that the response is **valid JSON** and contains **only the JSON object**, without additional text.
"""

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  # print(file)
  return file

response = model.generate_content(
    [upload_to_gemini('licensed-image.jpeg', mime_type="image/jpeg"), "\n\n", PROMPT]
)

# print(response)
print(response.text)