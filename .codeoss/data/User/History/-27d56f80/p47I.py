import os
from flask import Flask, redirect, request, send_file
from google.cloud import storage

os.makedirs('files', exist_ok = True)

app = Flask(__name__)

def get_list_of_files(bucket_name):
    """Lists all the blobs in the bucket."""
    print("\n")
    print("get_list_of_files: "+bucket_name)

    blobs = storage_client.list_blobs(bucket_name)
    print(blobs)
    files = []
    for blob in blobs:
        files.append(blob.name)

    return files

def upload_file(bucket_name, file_name):
    """Send file to bucket."""
    print("\n")
    print("upload_file: "+bucket_name+"/"+file_name)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_filename(file_name)

    return 

def download_file(bucket_name, file_name):
    """ Retrieve an object from a bucket and saves locally"""  
    print("\n")
    print("download_file: "+bucket_name+"/"+file_name)
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)
    blob.download_to_filename(file_name)
    blob.reload()
    print(f"Blob: {blob.name}")
    print(f"Bucket: {blob.bucket.name}")
    print(f"Storage class: {blob.storage_class}")
    print(f"Size: {blob.size} bytes")
    print(f"Content-type: {blob.content_type}")
    print(f"Public URL: {blob.public_url}")

    return



@app.route('/')
def index():
    index_html="""
<form method="post" enctype="multipart/form-data" action="/upload" method="post">
  <div>
    <label for="file">Choose file to upload</label>
    <input type="file" id="file" name="form_file" accept="image/jpeg"/>
  </div>
  <div>
    <button>Submit</button>
  </div>
</form>"""    

    for file in list_files():
        index_html += "<li><a href=\"/files/" + file + "\">" + file + "</a></li>"

    return index_html

@app.route('/upload', methods=["POST"])
def upload():
    file = request.files['form_file']  # item name must match name in HTML form
    file.save(os.path.join("./files", file.filename))

    return redirect("/")

@app.route('/files')
def list_files():
    files = os.listdir("./files")
    jpegs = []
    for file in files:
        if file.lower().endswith(".jpeg") or file.lower().endswith(".jpg"):
            jpegs.append(file)
    
    return jpegs

@app.route('/files/<filename>')
def get_file(filename):
  return send_file('./files/'+filename)

if __name__ == '__main__':
    app.run(debug=True)