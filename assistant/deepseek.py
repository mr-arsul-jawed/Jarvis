import requests
from assistant.speech import speak
from dotenv import load_dotenv
import os

load_dotenv() 

API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deekseek.com/search"  # hypothetical URL

def search_deepseek(query):
    params = {
        "api_key": API_KEY,
        "q": query
    }
    response = requests.get(BASE_URL, params=params)
    print("Status code:", response.status_code)
    print("Response text:", response.text)   
    if response.status_code == 200:
        data = response.json()
        # Parse the response as needed and return useful info
        return data.get("results", [])
    else:
        return None

def handle_deepseek_search(query):
    results = search_deepseek(query)
    if results:
        # Speak first result or summarize
        speak(f"Here’s what I found: {results[0]['title']}")
        # Optionally read more info
    else:
        speak("Sorry, I couldn't find anything on DeekSeek.")
