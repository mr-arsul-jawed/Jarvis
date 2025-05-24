import datetime
import webbrowser
from requests import get
from .speech import speak, takecommand
import requests
import os
from dotenv import load_dotenv
import pywhatkit
import PyPDF2

load_dotenv()

CITY = "Kolkata"
API_KEY = os.getenv("OPENWEATHER_API_KEY")
# print("API Key:", API_KEY)


CONTACTS = {
    "shahid": os.getenv("CONTACT_SHAHID")

}


def wish():
    
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        # greet = "Good morning sir"
        speak("Good morning sir")
    elif 12 <= hour < 15:
        # greet = "Good afternoon sir"
        speak("Good afternoon sir")
    else:
        # greet = "Good evening sir"
        speak("Good evening sir")
    
    response = takecommand().lower()
    
    if response and response != "none":
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Sir, it's {current_time}.")
        temp, description = get_temperature(CITY)
        if temp is not None:
          temp_msg = f"The current temperature is {temp} degrees Celsius and today's weather will be {description}."
          speak(temp_msg)
        else:
          speak("Sorry, I couldn't fetch the current temperature.")
    else:
     speak("I am Jarvis, sir. Please tell me how I can help you.")

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
            if "yes_open_map" in confirm or "sure" in confirm:
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
    book = open(r"C:\Users\arsul\Downloads\websocket.pdf",'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"Total numbers of pages in this pdf {pages}")
    speak("Sir, Please enter the page number i have to read")

    pg = int(input("Please enter the page number"))
    page = pdfReader.getPage(pg)
    text = page.extractText()
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
    # print("Weather API Status:", response.status_code)
    # print("Weather API Response:", response.text)
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




