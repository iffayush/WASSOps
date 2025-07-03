FROM python:3.11-slim

# Install system packages
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    git \
    make \
    && apt-get clean

# Install Nuclei
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    wget \
    && apt-get clean && \
    curl -LO https://github.com/projectdiscovery/nuclei/releases/download/v3.4.6/nuclei_3.4.6_linux_amd64.zip && \
    unzip nuclei_3.4.6_linux_amd64.zip && \
    mv nuclei /usr/local/bin/nuclei && \
    chmod +x /usr/local/bin/nuclei && \
    nuclei --update-templates


# Set workdir and copy code
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
