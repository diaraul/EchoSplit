import os
import time
import shutil
from flask import Flask, render_template, request
from spleeter.separator import Separator

app = Flask(__name__)

# Folder Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #this line registers upload folder w Flask (web server)

# Ensure folders exist on startup, if they exist, exist_ok = True
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)


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

    if file:
        # 2. Save the file
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_path)

        print(f"AI is starting work on: {file.filename}")

        # --- THE FIX IS HERE ---
        # We create the separator INSIDE the function so the
        # TensorFlow 'Graph' doesn't get out of scope.
        try:
            from spleeter.separator import Separator
            # Use default settings to avoid the 'codec' error from earlier
            local_separator = Separator('spleeter:2stems')
            local_separator.separate_to_file(input_path, OUTPUT_FOLDER)
        except Exception as e:
            return f"AI Error: {str(e)}"
        # -----------------------

        # 3. Create links to the output (Spleeter defaults to .wav)
        song_name = os.path.splitext(file.filename)[0]
        vocal_path = f"/static/output/{song_name}/vocals.wav"
        music_path = f"/static/output/{song_name}/accompaniment.wav"

        return f"""
        <h1>Split Complete!</h1>
        <p><a href="{vocal_path}" download>Download Vocals</a></p>
        <p><a href="{music_path}" download>Download Music</a></p>
        <br><a href="/">Split another song</a>
        """

if __name__ == '__main__':
    # Protection for Windows Multiprocessing and Debug mode
    print("--- EchoSplit AI Server Starting ---")
    app.run(debug=True, port=6006, use_reloader=False)

