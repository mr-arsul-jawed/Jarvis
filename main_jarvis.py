from assistant.speech import speak, takecommand
from assistant.helpers import wish, tell_time, tell_date, google_search, tell_ip
from assistant.email_utils import check_notifications

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
            speak("I cannot help with that. Please ask something else.")

if __name__ == "__main__":
    main()
