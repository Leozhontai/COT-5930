FROM python:3.10-slim-buster

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set the port Cloud Run expects
EXPOSE 8080

# Start the app
CMD ["python3", "app.py"]
