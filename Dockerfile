# Use a lightweight version of Python 3.11
FROM python:3.11-slim

# Install FFmpeg on the Linux server
RUN apt-get update && apt-get install -y ffmpeg

# Set up your project folder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Turn on the Flask server
CMD gunicorn main:app --bind 0.0.0.0:$PORT