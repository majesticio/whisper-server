
# Whisper cpp
------------
*this only works with 16-bit WAV files*
>convert a file to 16-bit WAV:


`ffmpeg -i input.mp3 -ar 16000 -ac 1 -c:a pcm_s16le output.wav`


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
`ffmpeg -f alsa -i default -ac 1 -ar 16000 -t 10 output.wav`

- `-f alsa`: Specifies the audio input format. For Linux systems using ALSA for audio, default is often the standard input device. Replace this if using a different audio input device.
- `-i default`: Input device. This can be replaced with the name of your specific audio input device.
- `-ac 1`: Sets the number of audio channels. 1 is for mono, use 2 for stereo.
- `-ar 16000`: Sets the audio sampling rate to 16kHz (standard for CD-quality audio). You can change it depending on your requirements.
- `-t 00:01:00`: Duration of the recording (in this case, 1 minute).
output.wav: The output file name in .wav format.


Convert a file:

`ffmpeg -i input.mp3 -ar 16000 -ac 1 -c:a pcm_s16le output.wav`

#### Special thanks to the authors of whisper.cpp

https://github.com/ggerganov/whisper.cpp