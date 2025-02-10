import os
from flask import Flask, redirect, request, send_file
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

    # List files in GCS bucket
    for file in get_list_of_files(BUCKET_NAME):
        index_html += f'<li><a href="/files/{file}">{file}</a></li>'

    index_html += "</ul>"
    return index_html

@app.route('/upload', methods=["POST"])
def upload():
    file = request.files['form_file']  # Retrieve file from form
    file_path = os.path.join("./", file.filename)
    file.save(file_path)  # Save locally before upload

    # Upload to Google Cloud Storage
    upload_file(BUCKET_NAME, file_path)

    # Remove local file after upload
    os.remove(file_path)

    return redirect("/")

@app.route('/files/<filename>')
def get_file(filename):
    """Download file from Google Cloud Storage and serve it."""
    file_path = os.path.join("./", filename)

    # Download the file locally
    download_file(BUCKET_NAME, filename)

    return send_file(file_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
