import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import simpledialog

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
    engine.stop()

def get_text_input_fallback():
    speak("You can type your response instead.")
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    response = simpledialog.askstring("Input Needed", "Please type your response:")
    if response is None:
        return ""
    return response.strip().lower()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            speak("Sorry, I didn’t hear anything.")
            return get_text_input_fallback()
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except sr.WaitTimeoutError:
        print("Timeout: No speech detected.")
        speak("Sorry, I didn’t hear anything.")
        return ""
    except sr.UnknownValueError:
        print("Speech not understood.")
        speak("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        speak("Sorry, I couldn't reach the speech service.")
        return ""
    except Exception:
        speak("Say that again please...")
        return "none"
    return query.lower()
