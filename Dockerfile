# Use NVIDIA CUDA base image for GPU support
FROM nvidia/cuda:11.8.0-runtime-ubuntu20.04

# Set non-interactive mode for tzdata
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    python3 \
    python3-pip \
    ffmpeg \
    curl \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Set timezone to UTC to avoid tzdata configuration prompt
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

# Clone the whisper.cpp repository
RUN git clone https://github.com/ggerganov/whisper.cpp.git /whisper.cpp

# Set the working directory
WORKDIR /whisper.cpp

# Download the base.en model
RUN sh ./models/download-ggml-model.sh base.en

# Build the whisper.cpp project
RUN make -j

# Install Flask for the API and Gunicorn for production serving
RUN pip3 install Flask gunicorn

# Copy the server.py to the container
COPY server.py /whisper.cpp/server.py

# Expose the port for the Flask API
EXPOSE 8888

# Use Gunicorn to serve the Flask application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8888", "server:app"]
