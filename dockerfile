# Base image con CUDA runtime
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Installazione pacchetti base
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-venv \
    python3-pip \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Usa python3.10 come default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Installa Torch con supporto CUDA 12.1
RUN pip install torch==2.0.1+cu121 torchvision==0.15.2+cu121 torchaudio==2.0.2 \
    --extra-index-url https://download.pytorch.org/whl/cu121

WORKDIR /app

# Copia requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installa libreria RunPod
RUN pip install runpod

# Copia il codice sorgente
COPY . .

# RunPod NON usa uvicorn, ma la sua libreria runpod serve
CMD ["python", "-u", "handler.py"]
