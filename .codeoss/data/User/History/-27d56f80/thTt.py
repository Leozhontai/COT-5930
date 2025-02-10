import os
from flask import Flask, redirect, request, send_file, abort
from storage import upload_file, get_list_of_files, download_file

# Google Cloud Storage Bucket Name
BUCKET_NAME = "cot5930"

app = Flask(__name__)

@app.route('/')
def index():
    index_html = """
    <form method="post" enctype="multipart/form-data" action="/upload">
      <div>
        <label for="file">Choose file to upload</label>
        <input type="file" id="file" name="form_file" accept="image/jpeg"/>
      </div>
      <div>
        <button>Submit</button>
      </div>
    </form>
    <ul>
    """

    # Fetch files from Google Cloud Storage
    for file in list_files():
        index_html += f'<li><a href="/files/{file}">{file}</a></li>'

    index_html += "</ul>"
    return index_html

@app.route('/upload', methods=["POST"])
def upload():
    file = request.files['form_file']  # Retrieve file from form
    file_name = file.filename.strip()

    # Save file locally before uploading
    file.save(file_name)

    # Upload to Google Cloud Storage
    upload_file(BUCKET_NAME, file_name)

    # Remove local file after upload
    os.remove(file_name)

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
