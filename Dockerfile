FROM python:3.10-slim-buster

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose the port Cloud Run uses
EXPOSE 8080

# Start the Flask app using main.py
CMD ["python3", "main.py"]

