import httpx
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

PRELOADED_MODEL_PATH = 'models/ggml-base.en.bin'  

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    temp_audio_path = f"/dev/shm/{file.filename}"  # Using in-memory temp storage
    file.save(temp_audio_path)

    result = subprocess.run(
        ['./main', '-m', PRELOADED_MODEL_PATH, '-f', temp_audio_path, '-nt', '--output-txt'],
        capture_output=True,
        text=True
    )

    print(f"STDOUT: {result.stdout}")
    print(f"STDERR: {result.stderr}")
    print(f"Return Code: {result.returncode}")

    os.remove(temp_audio_path)

    if result.returncode != 0:
        return jsonify({'error': 'Transcription failed', 'details': result.stderr}), 500

    transcription = result.stdout.strip()

    return jsonify({'transcription': transcription})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
