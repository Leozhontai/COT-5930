import os
import google.generativeai as genai

# ✅ Securely load API key from environment variable
genai.configure(api_key=os.environ.get("GEMINI_API"))

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

PROMPT = """
You are an AI model that analyzes images and generates descriptive metadata.

Please examine the uploaded image and return a **JSON response** with the following fields:

1️⃣ **title** → A short, meaningful title summarizing the image.  
2️⃣ **description** → A detailed, natural-language description explaining what is happening in the image.

⚠️ **Strictly format the response in JSON** with the following structure:

{
  "title": "Your generated title here",
  "description": "Your generated description here"
}

Ensure that:
- The response is **valid JSON** and contains **no extra text**.
- The **title** is concise (3-7 words).
- The **description** is detailed (2-3 sentences).
"""

def upload_to_gemini(path, mime_type="image/jpeg"):
    """Uploads the given file to Gemini AI."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"✅ Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def generate_image_description(image_path):
    """Generates an image description using Gemini AI."""
    file = upload_to_gemini(image_path)
    
    response = model.generate_content([file, "\n\n", PROMPT])
    
    print("🔹 Gemini AI Output:", response.text)  # ✅ Debugging step
    
    return response.text  # Returns JSON response
