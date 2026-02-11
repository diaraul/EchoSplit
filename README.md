# EchoSplit AI: Source Separation Web Application

**Developed by Raul Diaz** *Data Science (Music Tech Emphasis) | University of Oregon*

## Project Overview
EchoSplit is a full-stack web application designed for musicians and producers to isolate stems from audio files. Using Deep Learning models, the application splits songs into vocals and accompaniment with high precision.

## Technical Challenges Solved
* **TensorFlow Threading & Scope:** Resolved complex TypeError issues involving TensorFlow's graph execution within a multi-threaded Flask environment.
* **Dynamic Resource Management:** Implemented automated file cleanup protocols and Windows-optimized subprocess handling to ensure server stability.
* **Scalable Architecture:** Built a container-ready backend to handle audio signal processing workloads efficiently.

## Installation & Setup
To run this project locally, follow these steps:

### 1. Prerequisites
* **Python 3.10** (Required for TensorFlow/Spleeter compatibility)
* **FFmpeg**: Must be installed and added to your system PATH for audio processing.

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/diaraul/EchoSplit.git

# Create a virtual environment
python -m venv echo-env

# Activate the environment
# On Windows:
.\echo-env\Scripts\activate
# On Mac/Linux:
source echo-env/bin/activate

# Install dependencies
pip install -r requirements.txt 