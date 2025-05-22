from assistant.speech import speak, takecommand
from assistant.helpers import wish, tell_time, tell_date, google_search, tell_ip
from assistant.email_utils import check_notifications
from assistant.deepseek import search_deepseek
from assistant.deepseek import handle_deepseek_search





# This is mainly for testing purposes
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
        elif "search_on_google" in query or "findongoogle" in query or "search on google" in query:
            speak("What would you like to search on Google?")
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
        if any(phrase in query for phrase in ["search on deep", "search on deekseek", "search on ai"]):
            # speak("What would you like to search on DeepSeek?")
            search_query = takecommand()
            handle_deepseek_search(search_query)
        else:
            speak("I cannot help with that. Please ask something else.")

if __name__ == "__main__":
    main()
