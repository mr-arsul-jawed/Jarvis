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




