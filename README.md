
# Whisper cpp



## Setup
### Build with Dockerfile
`sudo docker build -t whisper-api-gpu .`

### Start the container
```
sudo docker run -d --gpus all --restart unless-stopped \             
  -p 8888:8888 \
  whisper-api-gpu
```

### Run the container persistantly
> From the project directory -->
```bash
sudo docker run -d --gpus all --restart unless-stopped \                 
  -p 8888:8888 \
  whisper-api-gpu
```

## Usage
The transcribe endpoint is accessible via port `8888`

`curl -F 'file=@recordings/audio-new.wav' http://localhost:8888/transcribe`

Example output:

`{"transcription":" This is a test of the emergency broadcast system, many and all notifications must go through a proper function.\n"}`

##### record some audio
`ffmpeg -f alsa -i default -10 audio.wav`
