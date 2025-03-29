# Use official Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into the container
COPY . .

# Set environment variable for port
ENV PORT=8080

# Use gunicorn to run the Flask app
# Make sure your Flask app is in `gemini.py` and the Flask instance is named `app`
CMD ["gunicorn", "--bind", ":8080", "gemini:app"]
