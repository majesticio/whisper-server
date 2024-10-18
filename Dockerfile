FROM nvidia/cuda:11.8.0-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    python3 \
    python3-pip \
    ffmpeg \
    curl \
    tzdata \
    cuda-toolkit-11-8 \
    && rm -rf /var/lib/apt/lists/*

# Set timezone to UTC to avoid tzdata configuration prompt
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

RUN git clone https://github.com/ggerganov/whisper.cpp.git /whisper.cpp

WORKDIR /whisper.cpp

RUN sh ./models/download-ggml-model.sh base.en

# Build whisper.cpp with CUDA support and specify the architecture (adjust compute_89 for your GPU)
RUN make clean && CUDA_DOCKER_ARCH=compute_89 GGML_CUDA=1 make -j

RUN pip3 install Flask gunicorn httpx

COPY server.py /whisper.cpp/server.py

EXPOSE 8888

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8888", "server:app"]
