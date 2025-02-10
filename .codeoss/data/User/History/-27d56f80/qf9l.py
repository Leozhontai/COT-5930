import os
from flask import Flask, redirect, request, abort
from storage import upload_file, get_list_of_files

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
            file_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{file}"  # Public URL
            index_html += f'<li><a href="{file_url}" target="_blank"><img src="{file_url}" width="100"></a></li>'

    index_html += "</ul>"
    return index_html

@app.route('/upload', methods=["POST"])
def upload():
    file = request.files.get('form_file')
    if not file:
        return "Error: No file uploaded.", 400

    file_name = file.filename.strip()  # Remove unwanted spaces

    # Save file locally before uploading
    file.save(file_name)

    # Upload file to Google Cloud Storage
    upload_file(BUCKET_NAME, file_name)

    # Remove local file after uploading to GCS
    os.remove(file_name)

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
