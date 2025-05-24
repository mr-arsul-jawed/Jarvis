from assistant.speech import speak, takecommand
from assistant.helpers import wish, tell_time, tell_date, google_search, tell_ip, find_me, pdf_reader
from assistant.email_utils import check_notifications
from assistant.deepseek import search_deepseek
from assistant.deepseek import handle_deepseek_search






# This is mainly for testing purposes
def main():
    wish()

    while True:
        query = takecommand()
        query = query.lower()  # Convert once and reuse

        if any(phrase in query for phrase in ["time", "current time", "what time is it"]):
            speak("Sure, let me check the time for you.")
            tell_time()

        elif any(phrase in query for phrase in ["date", "current date", "what's the current date"]):
            speak("Sure, let me check the date for you.")
            tell_date()

        elif any(phrase in query for phrase in ["search on google", "google search", "find on google"]):
            google_search()

        elif any(phrase in query for phrase in ["check email", "check_emails"]):
            speak("Checking for new emails...")
            check_notifications()

        elif any(phrase in query for phrase in ["fetch ip", "get my ip", "what is my ip", "ip address"]):
            speak("Fetching your IP address...")
            tell_ip()

        elif any(phrase in query for phrase in ["where am i", "where are we", "what's my location", "current location", "where are we located"]):
            find_me()

        elif any(phrase in query for phrase in ["read pdf", "pdf reader", "open pdf"]):
            pdf_reader()

        elif any(phrase in query for phrase in ["search on deep", "search on deekseek", "search on ai"]):
            search_query = takecommand()
            handle_deepseek_search(search_query)

        elif any(phrase in query for phrase in ["shutdown","goodbye", "sleep"]):
            speak("Bye, Sir! and take care.")
            break

        else:
            speak("I cannot help with that. Please ask something else.")


if __name__ == "__main__":
    main()
