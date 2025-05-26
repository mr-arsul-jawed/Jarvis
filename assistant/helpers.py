import datetime
import webbrowser
from requests import get
from .speech import speak, takecommand
import requests
import os
from dotenv import load_dotenv
import pywhatkit
import PyPDF2
from assistant.speech import speak, takecommand
load_dotenv()
import wikipedia
import smtplib
import urllib.parse


# Constants
CITY = "Kolkata"
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CONTACTS = {
    "shahid": os.getenv("CONTACT_SHAHID")

}




def wish():
    # Get current time and temperature
    temp, description = get_temperature(CITY)
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    hour = int(datetime.datetime.now().hour)

    # Greet based on time
    if 0 <= hour < 12:
        speak("Good morning! i'm jarvis.")
    elif 12 <= hour < 15:
        speak("Good afternoon! i'm jarvis.")
    else:
        speak("Good evening! i'm jarvis.")

    # Speak current time
    speak(f"Sir, it's {current_time}.")

    # Speak weather info
    if temp is not None:
        temp_msg = f"The current temperature is {temp} degrees Celsius and today's weather is {description}."
        speak(temp_msg)
    else:
        speak("Sorry, I couldn't fetch the current temperature.")
    

 
def find_me():
    try:
        speak("Give me a second, let me check where we are.")

        response = requests.get("https://ipinfo.io/json")
        data = response.json()

        city = data.get("city")
        region = data.get("region")
        country = data.get("country")
        loc = data.get("loc")

        if city and region and country:
            speak(f"Sir, based on the current network, we appear to be in {city}, {region}, {country}.")

            speak("Would you like me to open this location on Google Maps for you?")

            confirm = takecommand().lower()
            if any(phrase in confirm for phrase in ["yes", "open map", "sure", "open it","show me the map"]):
                webbrowser.open(f"https://www.google.com/maps?q={loc}")
                speak("I've opened the location in Google Maps.")
            else:
                speak("Alright, let me know if you need directions or help getting somewhere.")
        else:
            speak("Sorry, I couldn't determine your location.")
    except Exception as e:
        speak("Sorry, I couldn't fetch your current location.")
        print("Error:", e)

def pdf_reader():
    book = open(r"c:\\Users\arsul\Downloads\websocket.pdf",'rb')
    # pdfReader = PyPDF2.PdfFileReader(book)
    pdfReader = PyPDF2.PdfReader(book)
    # pages = pdfReader.numPages
    pages = len(pdfReader.pages)
    speak(f"Total numbers of pages in this pdf {pages}")
    speak("Sir, Please enter the page number i have to read")

    pg = int(input("Please enter the page number:___"))
    # page = pdfReader.getPage(pg)
    page = pdfReader.pages[pg]
    speak(f"Reading page number {pg}")
    # text = page.extractText()
    text = page.extract_text()
    speak(text)


def send_whatsapp_message():
    speak("To whom should I send the message?")
    name = takecommand().lower()

    phone_number = CONTACTS.get(name)

    if not phone_number:
        speak(f"Sorry, I couldn't find {name} in your contact list.")
        return

    speak("What is the message?")
    message = takecommand()

    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute + 2  # schedule 2 minutes later

    try:
        pywhatkit.sendwhatmsg(phone_number, message, hour, minute)
        speak(f"Message to {name} has been scheduled successfully.")
    except Exception as e:
        speak("Sorry, I couldn't send the WhatsApp message.")
        print(e)

def get_temperature(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return temp, description
    else:
        return None, None
    
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

def search_wikipedia():
    # speak("What should I search on Wikipedia?")
    query = takecommand()

    if query and query != "none":
        speak(f"Searching Wikipedia for {query}...")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find anything on Wikipedia with that title.")
        except Exception as e:
            speak("Sorry, I ran into an error while searching Wikipedia.")
            print("Wikipedia error:", e)


# def get_next_notes_file(folder="Note_file", base_name="notes", ext=".txt"):
#     # Ensure the folder exists, create if it doesn't
#     if not os.path.exists(folder):
#         os.makedirs(folder)
    
#     i = 1
#     while True:
#         filename = f"{base_name}_{i}{ext}"
#         filepath = os.path.join(folder, filename)
#         if not os.path.exists(filepath):
#             return filepath
#         i += 1


folder_name = "Note_file"
file_name = "notes_1.txt"

# Create the full path
NOTES_FILE = os.path.join(os.getcwd(), folder_name, file_name)

def take_note():
    # NOTES_FILE = get_next_notes_file()
    speak("What should I write down?")
    note = takecommand()
    with open(NOTES_FILE, "a") as f:
        f.write(note + "\n")
    speak(f"I've made a note of that in {NOTES_FILE}.")


def read_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            content = f.read()
            if content:
                speak("Here are your notes.")
                speak(content)
            else:
                speak("You have no notes yet.")
    else:
        speak("You have no notes yet.")


# def duckduckgo_instant_answer(query):
#     try:
#         encoded_query = urllib.parse.quote_plus(query)
#         url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json"
#         response = requests.get(url)
#         data = response.json()

#         if data.get("AbstractText"):
#             speak(data["AbstractText"])
#         elif data.get("Definition"):
#             speak(data["Definition"])
#         elif data.get("RelatedTopics"):
#             for topic in data["RelatedTopics"]:
#                 if isinstance(topic, dict) and topic.get("Text"):
#                     speak("Here's something I found:")
#                     speak(topic["Text"])
#                     break
#             else:
#                 speak("Sorry, I couldn't find an instant answer.")
#         else:
#             speak("Sorry, I couldn't find an instant answer.")
#     except Exception as e:
#         speak("Sorry, something went wrong while searching.")
#         print("Error:", e)

def send_email(to_email, subject, message, from_email, password, smtp_server="smtp.gmail.com", smtp_port=587):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(from_email, to_email, email_message)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")
        print(e)

def system_command(command):
    command = command.lower()
    if "open notepad" in command:
        os.system("notepad")
        speak("Opening Notepad.")
    elif "shutdown" in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif "screenshot" in command:
        import pyautogui
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken and saved.")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    else:
        speak("Sorry, I don't recognize that system command.")
    
def help_menu():
    commands = """
    I can help you with these tasks:
    - Tell time and date
    - Get weather updates
    - Search Google or Wikipedia
    - Play YouTube videos
    - Send WhatsApp messages
    - Read PDFs
    - Take and read notes
    - Tell jokes and motivational quotes
    - Set reminders
    - Send emails
    - Open Notepad, shutdown, take screenshots
    Just ask me what you want!
    """
    speak(commands)