"""
EchoSplit AI | Neural Audio Isolation
Developer: Raul Diaz (University of Oregon)
Algorithm: Spleeter U-Net 5-Stem
"""

import os
import sys
import time
import shutil
from flask import Flask, render_template, request, jsonify
from spleeter.separator import Separator
import zipfile
from flask import send_file
import io

base_path = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] += os.pathsep + base_path

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'm4a'}

# Folder Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #this line registers upload folder w Flask (web server)

# Ensure folders exist on startup, if they exist, exist_ok = True
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_old_files(max_age_seconds=3600):
    """Deletes files and folders older than 1 hour to save disk space."""
    now = time.time()
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            # If the file/folder is older than the max_age, delete it
            if os.stat(file_path).st_mtime < now - max_age_seconds:
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    print(f"--- Auto-Cleaned: {filename} ---")
                except Exception as e:
                    print(f"Error cleaning {filename}: {e}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # 1. Clean up old files (keep it at 1 hour/3600s for safety)
    cleanup_old_files(3600)

    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        # 2. Save the file
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_path)

        print(f"AI is starting 5-stem separation on: {file.filename}")

        # We create the separator INSIDE the function so the
        # TensorFlow 'Graph' doesn't get out of scope.
        try:
            # Use default settings to avoid the 'codec' error
            local_separator = Separator('spleeter:5stems')
            local_separator.separate_to_file(input_path, OUTPUT_FOLDER)

            # Create paths for all 5 stems
            song_name = os.path.splitext(file.filename)[0]
            stems = ['vocals', 'drums', 'bass', 'piano', 'other']

            file_data = []
            for stem in stems:
                # We use the relative path that the web browser understands
                file_url = f"/static/output/{song_name}/{stem}.wav"
                file_data.append({
                    "name": stem,
                    "url": file_url
                })

            return jsonify({
                "success": True,
                "files": file_data
            })

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        # This handles cases where the file extension isn't allowed
        return jsonify({"success": False, "error": "File type not supported. Please upload MP3, WAV, or FLAC."}), 400

@app.route('/download_all/<song_name>')
def download_all(song_name):
    # Path to the folder containing the 5 stems
    song_folder = os.path.join(OUTPUT_FOLDER, song_name)

    if not os.path.exists(song_folder):
        return jsonify({"success": False, "error": "Stem folder not found"}), 404

    # Create a buffer to hold the zip data in memory (faster than writing to disk)
    memory_file = io.BytesIO()

    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(song_folder):
            for file in files:
                # Security check: skip hidden system files
                if file.startswith('.') or not file.endswith('.wav'):
                    continue

                file_path = os.path.join(root, file)
                # Add file to zip, using just the filename (no full paths inside zip)
                zf.write(file_path, arcname=file)

    memory_file.seek(0)

    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{song_name}_EchoSplit_stems.zip"
    )

if __name__ == '__main__':
    # Protection for Windows Multiprocessing and Debug mode
    print("--- EchoSplit AI Server Starting ---")
    app.run(debug=True, port=6006, use_reloader=False)

