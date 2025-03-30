FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install flask

ENV PORT=8080
CMD ["python", "app.py"]
