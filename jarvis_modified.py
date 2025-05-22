import pyttsx3
import speech_recognition as sr
import datetime
# import random
import webbrowser
from requests import get
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os
import pyaudio
# import time
import sys
sys.stdout.flush()


load_dotenv()



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#here: speak function
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
    engine.stop()

#Here: take command from the user
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
    except Exception as e:
        speak("Say that again please...")
        return "none"
    return query.lower()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Jarvis, sir. Please tell me how I can help you.")

def get_text_input_fallback():
    """Fallback function when speech recognition fails."""
    speak("You can type your response instead.")
    response = input("Type your response here: ")
    return response.strip().lower()

def get_user_confirmation(prompt):
    speak(prompt)
    print(f"Prompt: {prompt}")
    for _ in range(2):  # Try twice before giving up
        response = takecommand()
        if any(word in response for word in ["yes", "sure", "okay", "read full email", "yes please", "yes, please"]):
            return True
        elif any(word in response for word in ["no", "not now", "later", "skip"]):
            return False
        else:
            speak("I didn’t catch that. Could you please repeat?")
    speak("I'll skip it for now.")
    return False

def check_new_email():
    # Email account credentials
    username = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')

    # Connect to Gmail's IMAP server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login to the account
    imap.login(username, password)

    # Select inbox folder
    imap.select("inbox")

    # Search for all unseen emails
    status, messages = imap.search(None, 'UNSEEN')

    mail_ids = messages[0].split()

    if len(mail_ids) == 0:
        return None

    # Fetch the most recent unread email
    latest_email_id = mail_ids[-1]

    status, msg_data = imap.fetch(latest_email_id, "(RFC822)")

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            # Decode email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            # Decode sender email
            from_ = msg.get("From")

            # Extract email body
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            return {
                "subject": subject,
                "from": from_,
                "body": body
            }

    imap.close()
    imap.logout()

def check_notifications():
    email_data = check_new_email()
    if email_data is None:
        speak("You have no new emails.")
        return
    
    if get_user_confirmation(f"You have a new email from {email_data['from']}. Would you like me to read the subject?"):
        speak(f"The subject is: {email_data['subject']}")
        if get_user_confirmation("Would you like me to read the body?"):
            speak(email_data['body'])
        else:
            speak("Okay, I won't read the body.")
    else:
        speak("Okay, I won't read it.")


def tell_time():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {time}")

def tell_date():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    speak(f"Today's date is {date}")

def google_search():
    speak("What should I search on Google?")
    query = takecommand()
    if query != "none":
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Here are the search results for {query}")

#here: find the ip address
def tell_ip():
    try:
        ip = get('https://api.ipify.org').text
        speak(f"Your public IP address is {ip}")
    except Exception as e:
        speak("Sorry, I couldn't fetch your IP address right now.")

def main():
    wish()
    while True:
        query = takecommand()
        if "time" in query or "current time" in query:
            speak("Sure, let me check the time for you.")
            tell_time()
        elif "date" in query:
            speak("Sure, let me check the date for you.")
            tell_date()
        elif "search" in query:
            google_search()
        elif "check_email" in query or "check email" in query or "check notifications" in query:
            speak("Checking for new emails...")
            check_notifications()
        elif "ip" in query or "ip_address" in query or "fetch ip" in query:
            speak("Fetching your IP address...")
            tell_ip()
        elif "exit" in query or "stop" in query or "shutdown" in query:
            speak("Goodbye, Sir!")
            break
        else:
            speak("I can not help with that. Please ask something else.")

# Run the assistant
main()
