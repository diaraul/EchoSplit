FROM python:3.10-slim

# Install system dependencies for audio and ML
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-create folders for uploads and AI results
RUN mkdir -p uploads static/output

COPY . .

# Main entry point
CMD ["python", "api.py"]
