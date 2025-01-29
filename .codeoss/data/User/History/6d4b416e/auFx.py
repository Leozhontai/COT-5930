import os
import time
from flask import Flask, request, redirect, url_for, render_template
from google.cloud import datastore, storage
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Google Cloud Clients
datastore_client = datastore.Client()
storage_client = storage.Client()

BUCKET_NAME = "your-gcs-bucket-name"  # Replace with your actual GCS bucket name

def upload_to_gcs(file, filename):
    """Uploads a file to Google Cloud Storage and stores metadata in Datastore."""
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_file(file, content_type=file.content_type)
    file_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

    # Store file metadata in Datastore
    entity = datastore.Entity(key=datastore_client.key("photos"))
    entity.update({
        "name": filename,
        "url": file_url,
        "user": "anonymous",
        "timestamp": int(time.time())
    })
    datastore_client.put(entity)

    return file_url

def get_uploaded_files():
    """Fetches the list of uploaded images from Datastore."""
    query = datastore_client.query(kind="photos")
    query.order = ["-timestamp"]  # Order by most recent uploads
    return list(query.fetch())

@app.route("/", methods=["GET", "POST"])
def index():
    """Renders the homepage with upload form and image list."""
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        
        filename = secure_filename(file.filename)
        file_url = upload_to_gcs(file, filename)

        return redirect(url_for("index"))

    # Fetch uploaded images
    files = get_uploaded_files()
    return render_template("index.html", files=files)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
