from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Use /dev/shm for in-memory file saving
    temp_audio_path = f"/dev/shm/{file.filename}"
    file.save(temp_audio_path)

    # Run Whisper to transcribe the audio
    result = subprocess.run(
        ['./main', '-m', 'models/ggml-base.en.bin', '-f', temp_audio_path, '--output-txt'],
        capture_output=True,
        text=True
    )

    # Log stdout and stderr for debugging
    print(f"STDOUT: {result.stdout}")
    print(f"STDERR: {result.stderr}")
    print(f"Return Code: {result.returncode}")

    # Check if the transcription was successful
    if result.returncode != 0:
        return jsonify({'error': 'Transcription failed', 'details': result.stderr}), 500

    # Read the transcription from the output .txt file
    output_txt_path = temp_audio_path + ".txt"
    if not os.path.exists(output_txt_path):
        return jsonify({'error': 'Transcription output not found'}), 500

    with open(output_txt_path, 'r') as transcript_file:
        transcription = transcript_file.read()

    # Clean up temporary files from /dev/shm
    os.remove(temp_audio_path)
    os.remove(output_txt_path)

    return jsonify({'transcription': transcription})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
