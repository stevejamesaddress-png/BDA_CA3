# =====================================================
# File: Dockerfile.app
# Author: Steven James L00196960
# Builds the web application image 
# =====================================================
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py ./
COPY src/templates/index.html ./templates/index.html

ENV PYTHONUNBUFFERED=1

# this is just a note of expected port
#it does nothing truley 
EXPOSE 5001

# Using the standard Flask development server for simplicity
CMD ["python", "app.py"]