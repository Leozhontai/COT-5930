gcloud auth list
gcloud config list project
Updated property [core/project].
gcloud services enable   artifactregistry.googleapis.com   cloudbuild.googleapis.com   run.googleapis.com
ls
mkdir ~/helloworld-python
cd ~/helloworld-python
touch main.py
cloudshell edit main.py
touch requirements.txt
cloudshell edit requirements.txt
touch Procfile
cloudshell edit Procfile
ls
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
rm -r venv/
REGION="europe-west9"
ls
gcloud run deploy helloworld-python   --source .   --platform managed   --region $REGION   --allow-unauthenticated
gcloud artifacts repositories delete cloud-run-source-deploy   --location $REGION
gcloud run services delete helloworld-python   --platform managed   --region $REGION
PROJECT_ID=$(gcloud config get-value core/project)
echo $PROJECT_ID
gcloud projects delete $PROJECT_ID
gcloud services enable datastore.googleapis.com storage.googleapis.com
gsutil mb gs://your-gcs-bucket-name
pip install flask google-cloud-storage google-cloud-datastore gunicorn
FROM python:3.9
gcloud auth list
touch Dockerfile
gcloud config list project
gcloud services enable   artifactregistry.googleapis.com   cloudbuild.googleapis.com   run.googleapis.com
ls
cloudshell edit Procfile
ls
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
touch requirements.txt
pip install -r requirements.txt
python main.py
ls
python main.py
127.0.0.1 - - [29/Jan/2025 03:45:24] "GET /upload?__debugger__=yes&cmd=resource&f=debugger.js HTTP/1.1" 200 -
127.0.0.1 - - [29/Jan/2025 03:45:24] "GET /upload?__debugger__=yes&cmd=resource&f=console.png&s=0GW4AoBQWJKPyG0hUITf HTTP/1.1" 200 -
127.0.0.1 - - [29/Jan/2025 03:45:24] "GET /upload?__debugger__=yes&cmd=resource&f=console.png HTTP/1.1" 200 -
127.0.0.1 - - [29/Jan/2025 03:45:40] "GET /upload?__debugger__=yes&cmd=printpin&s=0GW4AoBQWJKPyG0hUITf HTTP/1.1" 200 -
127.0.0.1 - - [29/Jan/2025 03:46:01] "GET /?authuser=0 HTTP/1.1" 200 -
127.0.0.1 - - [29/Jan/2025 03:46:04] "POST /upload HTTP/1.1" 500 -
Traceback (most recent call last):
IsADirectoryError: [Errno 21] Is a directory: './files/'
127.0.0.1 - - [29/Jan/2025 03:46:04] "GET /upload?__debugger__=yes&cmd=resource&f=style.css HTTP/1.1" 304 -
127.0.0.1 - - [29/Jan/2025 03:46:04] "GET /upload?__debugger__=yes&cmd=resource&f=debugger.js HTTP/1.1" 304 -
127.0.0.1 - - [29/Jan/2025 03:46:04] "GET /upload?__debugger__=yes&cmd=resource&f=console.png&s=0GW4AoBQWJKPyG0hUITf HTTP/1.1" 304 -
127.0.0.1 - - [29/Jan/2025 03:48:07] "POST /upload HTTP/1.1" 302 -
127.0.0.1 - - [29/Jan/2025 03:48:07] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [29/Jan/2025 03:48:08] "GET /files/1_0_0_20161219140623097.jpg HTTP/1.1" 200 -
127.0.0.1 - - [29/Jan/2025 03:48:43] "POST /upload HTTP/1.1" 302 -
127.0.0.1 - - [29/Jan/2025 03:48:43] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [29/Jan/2025 03:48:44] "GET /files/iPhone%2016%20Pro%20Wallpapers%20_%20HD%20&%204K%20Wallpapers%20for%20Apple%20iPhone.jpeg HTTP/1.1" 200 -
127.0.0.1 - - [29/Jan/2025 03:50:35] "GET /files/iPhone%2016%20Pro%20Wallpapers%20_%20HD%20&%204K%20Wallpapers%20for%20Apple%20iPhone.jpeg HTT









python main.py
REGION="europe-west9"
ls
gcloud run deploy project-cot5930
REGION="europe-west9"
gcloud config set run/region $REGION
gcloud run deploy project-cot5930   --source .   --platform managed   --region $REGION   --allow-unauthenticated
gcloud run services list
git init  # Initialize a Git repository
git add .  # Stage all files for commit
git commit -m "Initial commit"  # Commit with a message
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/Leozhontai/COT-5930
git push -u origin main
git init
git add .
git commit -m "Initial commit"
git config --global user.email "leozhontai561@gmail.com" 
git config --global user.name "Leozhontai"
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/Leozhontai/COT-5930
git push -u origin main
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/Leozhontai/COT-5930
git push -u origin main
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/Leozhontai/COT-5930
git push -u origin main
