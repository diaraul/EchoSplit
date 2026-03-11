# EchoSplit AI: Multi-Stem Source Separation

**Developed by Raul Diaz** *Data Science Student (Music Tech Emphasis) | University of Oregon*

## 🎵 Project Overview
EchoSplit is an end-to-end web application that leverages Deep Learning to perform high-fidelity audio source separation. Unlike basic vocal removers, EchoSplit provides **5-stem isolation**, extracting:
* **Vocals**
* **Drums**
* **Bass**
* **Piano**
* **Other Accompaniment**

The backend utilizes the Spleeter library to analyze spectrograms and reconstruct isolated audio signals in real-time.


## 🛠 Technical Hurdles & Engineering Solutions
* **Dependency Synchronization:** Successfully resolved a critical dependency conflict between legacy ML requirements (Spleeter/Typer) and modern web frameworks (Flask 2.2). This was achieved by pinning a "bridge version" of the **Click (7.1.2)** and **Werkzeug (2.0.3)** libraries to maintain system-wide stability.
* **FFmpeg Binary Integration:** Orchestrated system-level audio processing by integrating FFmpeg binaries directly into the application environment, ensuring the application can run regardless of local Windows PATH configurations.
* **Resource Efficiency:** Configured the TensorFlow backend to handle intensive U-Net model computations on CPU-bound hardware, ensuring accessibility for users without dedicated GPUs.

## 🚀 Installation & Setup

### 1. Prerequisites
* **Python 3.10** (Required for TensorFlow/Spleeter compatibility)
* **FFmpeg**: Required for audio decoding/encoding.
    * **Download:** [gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/) (Download `ffmpeg-git-full.7z`).
    * **Setup:** Place `ffmpeg.exe` and `ffprobe.exe` directly in the `EchoSplit` root directory alongside `api.py`. I recommend placing the original folder in `C:\ffmpeg`.

### 2. Environment Setup
```bash
# Clone the repository
git clone [https://github.com/diaraul/EchoSplit.git](https://github.com/diaraul/EchoSplit.git)

# Navigate to project
cd EchoSplit

# Create a virtual environment
python -m venv echo-env

# Activate the environment
# On Windows:
.\echo-env\Scripts\activate
# On Mac/Linux:
source echo-env/bin/activate

# Install dependencies
pip install -r requirements.txt
