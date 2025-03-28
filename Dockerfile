# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port Cloud Run expects
EXPOSE 8080

# Set environment variable for Flask
ENV PORT 8080

# Start the Flask app
CMD ["python", "gemini.py"]
