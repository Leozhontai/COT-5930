FROM python:3.10-slim-buster

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all other files in the current folder
COPY . .

# Expose port Cloud Run expects
EXPOSE 8080

# Start your Flask app
CMD ["python3", "app.py"]
