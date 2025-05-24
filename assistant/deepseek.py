import requests
from assistant.speech import speak
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com/v1/chat/completions"

def search_deepseek(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ],
        "stream": False
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)
    print("Status code:", response.status_code)
    print("Response text:", response.text)

    if response.status_code == 200:
        data = response.json()
        # Extract the assistant's reply from the response
        answer = data["choices"][0]["message"]["content"]
        return answer
    else:
        return None

def handle_deepseek_search(query):
    answer = search_deepseek(query)
    if answer:
        speak(f"Here’s what I found: {answer}")
    else:
        speak("Sorry, I couldn't find anything on DeepSeek.")
