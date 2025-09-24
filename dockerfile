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

WORKDIR /app

# Copia requirements
COPY requirements.txt .

# copia la cartella DeepSpeed (se esiste nella root della repo)
COPY DeepSpeed/ ./DeepSpeed/

# ------------------------------
# Installa pacchetti di sistema (inclusi per insightface)
# ------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    python3-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install insightface==0.7.3 --no-build-isolation

RUN pip install --no-cache-dir -r requirements.txt --verbose

# Installa libreria RunPod
RUN pip install runpod

# Copia il codice sorgente
COPY . .

# RunPod NON usa uvicorn, ma la sua libreria runpod serve
CMD ["python", "-u", "handler.py"]
