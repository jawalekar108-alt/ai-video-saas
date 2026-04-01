# Production Dockerfile for AI Video SaaS (Streamlit + yt-dlp + Node + FFmpeg)

FROM python:3.11-slim

# Environment settings
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies (production stack)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    git \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node LTS (required by yt-dlp modern extraction)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs

# Verify installs
RUN node -v && npm -v && ffmpeg -version

# Create non‑root user (security best practice)
RUN useradd -m -u 1000 appuser
WORKDIR /app

# Copy dependency files first (Docker cache optimization)
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install --upgrade yt-dlp

# Copy application
COPY . .

# Change ownership
RUN chown -R appuser:appuser /app
USER appuser

# Streamlit production settings
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Production start command
CMD streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false


# ==============================
# Recommended additional files:
# ==============================

# docker-compose.yml
# ------------------
# version: '3.9'
# services:
#   ai-video-saas:
#     build: .
#     container_name: ai-video-saas
#     ports:
#       - "8501:8501"
#     restart: always
#     environment:
#       - PYTHONUNBUFFERED=1
#     volumes:
#       - .:/app


# .dockerignore
# -------------
# __pycache__
# *.pyc
# *.pyo
# *.pyd
# .Python
# venv
# .venv
# env
# .env
# .git
# .gitignore
# node_modules
# *.log
# data/
# videos/
# downloads/


# Production recommendations:
# --------------------------
# Add later if scaling SaaS:
# - Redis (job queue)
# - Postgres (metadata)
# - Celery/RQ (background jobs)
# - Nginx (reverse proxy)
# - S3 (video storage)
# - Whisper fallback transcription
# - caching layer

# Typical production structure:
# app/
# ├── app.py
# ├── services/
# │     ├── youtube.py
# │     ├── transcript.py
# │     ├── summarizer.py
# │     └── storage.py
# ├── utils/
# ├── workers/
# ├── Dockerfile
# ├── docker-compose.yml
# └── requirements.txt
