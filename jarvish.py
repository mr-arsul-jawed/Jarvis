import pyttsx3
import speech_recognition as sr
import datetime
# import os
# import cv2
import random
from requests import get

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

# Text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# To convert voice into text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=5)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception as e:
        speak("Say that again please...")
        return "none"
    return query.lower()

# To wish
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Jarvis, sir. Please tell me how I can help you.")

# To notify and read notifications
def check_notifications():
    # Example notification
    notification = "You have a new email from your boss."
    
    speak("You have a new notification. Would you like me to read it?")
    permission = takecommand()
    
    if "yes" in permission or "sure" in permission or "okay" in permission:
        speak(notification)
    else:
        speak("Okay, I won't read it.")

# if __name__ == "__main__":
wish()
check_notifications()
