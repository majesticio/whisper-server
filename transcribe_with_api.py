import requests
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Send an audio file for transcription.')
parser.add_argument('audio_file', type=str, help='Path to the audio file')
parser.add_argument('--host', type=str, default='http://localhost:8888', help='API host URL (default: http://localhost:8888)')

# Parse the arguments
args = parser.parse_args()

url = f"{args.host}/transcribe"  # API endpoint for transcription
audio_file = args.audio_file  # Get the audio file path from the argument

# Send the audio file to the API
with open(audio_file, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, files=files)

# Check if the request was successful
if response.status_code == 200:
    transcription = response.json().get('transcription', 'No transcription available')
    print(transcription.strip())  # Print only the transcription text
else:
    print(f"Error: {response.status_code}, {response.text}")
