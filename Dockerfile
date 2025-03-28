# Use official Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port (Cloud Run default)
EXPOSE 8080

# Command to run your app (adjust if needed)
CMD ["python", "gemini.py"]
