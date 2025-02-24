import os
import json
from flask import Flask, redirect, request, send_file, abort
from google.cloud import storage
import gemini  # Import your existing Gemini functions

# Google Cloud Storage Bucket Name
BUCKET_NAME = "cot5930"
storage_client = storage.Client()

def get_list_of_files(bucket_name):
    """Lists all the blobs in the bucket."""
    print("\nFetching file list from bucket:", bucket_name)
    try:
        blobs = storage_client.list_blobs(bucket_name)
        return [blob.name for blob in blobs]
    except Exception as e:
        print(f"❌ Error listing files: {e}")
        return []

def upload_file(bucket_name, file_name):
    """Uploads an image and its metadata to Google Cloud Storage."""
    print("\nUploading file:", file_name)

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_name)  # Upload image
        print(f"✅ Successfully uploaded {file_name}")

        # Call Gemini AI *only* after upload
        try:
            gemini_file = gemini.upload_to_gemini(file_name, mime_type="image/jpeg")
            response = gemini.model.generate_content([gemini_file, "\n\n", gemini.PROMPT])

            # Save the response as a JSON file
            metadata = response.text
            json_file_name = os.path.splitext(file_name)[0] + ".json"
            json_path = json_file_name  # Save JSON locally
            
            # Save the JSON response to a local file
            with open(json_path, "w") as json_file:
                json_file.write(metadata)

            # Upload JSON metadata to GCS
            json_blob = bucket.blob(json_file_name)
            json_blob.upload_from_filename(json_path)
            print(f"✅ JSON metadata uploaded: {json_file_name}")

            # Remove local JSON file
            os.remove(json_path)

        except Exception as e:
            print(f"❌ Gemini Error: {e}")

        # Remove local image after upload
        os.remove(file_name)

    except Exception as e:
        print(f"❌ Error uploading {file_name}: {e}")

def download_file(bucket_name, file_name):
    """Downloads a file from Google Cloud Storage."""
    print(f"\nDownloading {file_name} from {bucket_name}")

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        if not blob.exists():
            print(f"❌ ERROR: File '{file_name}' does not exist in GCS.")
            return False  # File not found

        blob.download_to_filename(file_name)
        print(f"✅ Successfully downloaded {file_name}")
        return True
    except Exception as e:
        print(f"❌ Error downloading {file_name}: {e}")
        return False

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
    <h3>Available Files:</h3>
    <ul>
    """

    # Fetch files from Google Cloud Storage
    files = get_list_of_files(BUCKET_NAME)
    if not files:
        index_html += "<li>No files found in storage.</li>"
    else:
        for file in files:
            index_html += f'<li><a href="/files/{file}">{file}</a></li>'

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

@app.route('/files')
def list_files():
    """Fetches and filters only JPEG files from GCS."""
    files = get_list_of_files(BUCKET_NAME)
    return [file for file in files if file.lower().endswith(".jpeg") or file.lower().endswith(".jpg")]

@app.route('/files/<filename>')
def get_file(filename):
    """Downloads the file from GCS and serves it."""
    if not download_file(BUCKET_NAME, filename):
        return abort(404, description="File not found in Google Cloud Storage.")

    return send_file(filename, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
