import os
from flask import Flask, redirect, request, send_file, abort
from storage import upload_file, get_list_of_files, download_file

# Google Cloud Storage Bucket Name
BUCKET_NAME = "cot5930"

app = Flask(__name__)

@app.route('/')
def index():
    index_html = """
    <h2>Upload and View Files</h2>
    <form method="post" enctype="multipart/form-data" action="/upload">
      <div>
        <label for="file">Choose file to upload:</label>
        <input type="file" id="file" name="form_file" accept="image/jpeg, image/png"/>
      </div>
      <div>
        <button type="submit">Submit</button>
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
    file = request.files.get('form_file')
    if not file:
        return "Error: No file uploaded.", 400

    file_path = file.filename  # Save file with its original name

    # Save file locally before uploading
    file.save(file_path)

    # Upload file to Google Cloud Storage
    upload_file(BUCKET_NAME, file_path)

    # Remove local file after uploading to GCS
    os.remove(file_path)

    return redirect("/")

@app.route('/files/<filename>')
def get_file(filename):
    """Download file from Google Cloud Storage and serve it."""
    file_path = filename  # No local storage, only used for serving

    # Try to download the file from GCS
    if not download_file(BUCKET_NAME, filename):
        return abort(404, description="File not found in Google Cloud Storage.")

    return send_file(file_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
