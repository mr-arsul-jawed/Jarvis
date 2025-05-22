import datetime
import webbrowser
from requests import get
from .speech import speak, takecommand

def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning")
    elif 12 <= hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Jarvis, sir. Please tell me how I can help you.")

def tell_time():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {time}")

def tell_date():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    speak(f"Today's date is {date}")

def google_search():
    speak("What should I search on Google?")
    query = takecommand()
    if query != "none" and query != "":
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Here are the search results for {query}")

def tell_ip():
    try:
        ip = get('https://api.ipify.org').text
        speak(f"Your public IP address is {ip}")
    except Exception:
        speak("Sorry, I couldn't fetch your IP address right now.")
