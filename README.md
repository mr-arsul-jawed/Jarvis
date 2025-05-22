# Jarvis Personal Voice Assistant

Jarvis is a Python-based personal voice assistant that can perform tasks like telling time, checking emails, performing Google searches, fetching your IP address, and more — all via voice commands.

## Features
- Voice interaction with speech recognition and text-to-speech
- Check new emails and read subjects/bodies aloud
- Tell current time and date
- Perform Google searches via voice command
- Fetch and announce your public IP address
- Fallback to typed input when speech recognition fails

## Folder Structure

jarvis_project/
│
├── assistant/
│ ├── init.py
│ ├── jarvis.py
│ ├── speech.py
│ ├── email_utils.py
│ ├── utils.py
├── .env
├── requirements.txt
├── README.md


## Setup

1. Clone or download this repository.

2. Create a `.env` file in the root directory with your email credentials:


**Note:** For Gmail, create an App Password if you have 2FA enabled.

3. Install dependencies:

bash
pip install -r requirements.txt

python -m assistant.jarvis
Dependencies
pyttsx3

SpeechRecognition

python-dotenv

requests

pyaudio (for microphone input)

imaplib (built-in)

email (built-in)

pip install pipwin
pipwin install pyaudio

License
MIT License
