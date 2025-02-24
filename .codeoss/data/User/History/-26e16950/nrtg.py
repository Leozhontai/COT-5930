import os
import json
from flask import Flask, request, redirect, abort, send_file
from google.cloud import storage
from gemini import generate_image_metadata  # Import function from gemini.py

# Google Cloud Storage Bucket Name
BUCKET_NAME = "cot5930"
storage_client = storage.Client()

def upload_file(bucket_name, file_name):
    """Uploads an image and its AI-generated metadata to Google Cloud Storage."""
    print(f"\n🚀 Uploading {file_name} to {bucket_name}")

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_name)  # Upload image
        print(f"✅ Successfully uploaded {file_name}")

        # Call Gemini AI to generate title & description
        metadata_json = generate_image_metadata(file_name)
        if metadata_json is None:
            print("❌ Skipping JSON upload due to invalid response.")
            return  # Exit if Gemini response is invalid

        # Save JSON metadata locally
        json_file_name = os.path.splitext(file_name)[0] + ".json"
        json_path = json_file_name  

        with open(json_path, "w") as json_file:
            json.dump(metadata_json, json_file, indent=4)

        # Debugging: Print saved JSON
        print(f"\n📁 JSON File Contents:\n{metadata_json}")

        # Upload JSON metadata to GCS in the same location as the image
        json_blob = bucket.blob(json_file_name)
        json_blob.upload_from_filename(json_path)
        print(f"✅ JSON metadata uploaded: {json_file_name}")

        # Remove local JSON file
        os.remove(json_path)

        # Remove local image after upload
        os.remove(file_name)

    except Exception as e:
        print(f"❌ Error uploading {file_name}: {e}")

app = Flask(__name__)

@app.route('/')
def index():
    index_html = """
    <h2>Upload and View Files</h2>
    <form method="post" enctype="multipart/form-data" action="/upload">
      <div>
        <label for="file">Choose file to upload:</label>
        <input type="file" id="file" name="form_file" accept="image/jpeg"/>
      </div>
      <div>
        <button>Submit</button>
      </div>
    </form>
    <h3>Uploaded Images:</h3>
    <ul>
    """

    # Fetch files from Google Cloud Storage
    blobs = storage_client.list_blobs(BUCKET_NAME)
    files = [blob.name for blob in blobs]

    image_files = [file for file in files if file.lower().endswith(('.jpeg', '.jpg'))]

    for image in image_files:
        json_file = image.replace(".jpeg", ".json").replace(".jpg", ".json")
        title = "No title available"
        description = "No description available"

        # Check if the corresponding JSON file exists
        if json_file in files:
            json_blob = storage_client.bucket(BUCKET_NAME).blob(json_file)
            json_data = json_blob.download_as_text()
            try:
                metadata = json.loads(json_data)
                title = metadata.get("title", "No title available")
                description = metadata.get("description", "No description available")
            except json.JSONDecodeError:
                pass  # Ignore errors and use default title/description

        # Display image with title and description
        index_html += f"""
        <li>
            <a href="/files/{image}" target="_blank">
                <img src="/files/{image}" width="200" alt="Uploaded Image">
            </a>
            <p><strong>{title}</strong></p>
            <p><em>{description}</em></p>
        </li>
        """

    index_html += "</ul>"
    return index_html

@app.route('/upload', methods=["POST"])
def upload():
    file = request.files['form_file']  # Retrieve file from form
    file_name = file.filename.strip()

    # Save file locally before uploading
    file.save(file_name)

    # Upload image + metadata
    upload_file(BUCKET_NAME, file_name)

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
