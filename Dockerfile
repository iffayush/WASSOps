FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget unzip git && \
    rm -rf /var/lib/apt/lists/*

# Install nuclei 3.4.6
RUN wget https://github.com/projectdiscovery/nuclei/releases/download/v3.4.6/nuclei_3.4.6_linux_amd64.zip && \
    unzip nuclei_3.4.6_linux_amd64.zip && \
    mv nuclei /usr/local/bin/nuclei && \
    chmod +x /usr/local/bin/nuclei && \
    rm nuclei_3.4.6_linux_amd64.zip README.md LICENSE.md

# Download nuclei templates
RUN git clone https://github.com/projectdiscovery/nuclei-templates.git /nuclei-templates

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY main.py .
COPY scan.py .

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 