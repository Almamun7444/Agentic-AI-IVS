"""
ekta REAL MINI JARVIS বানাবো।

Eta korte parbe:
✅ browser open
✅ voice talk
✅ weather check
✅ WhatsApp message
✅ PC control
✅ AI response

🧠 FIRST — Architecture

Jarvis system:

Voice Input
   ↓
Speech → Text
   ↓
OpenAI Brain
   ↓
Decision
   ↓
Python Function (Tool)
   ↓
Real Action

"""

from openai import OpenAI
from dotenv import load_dotenv

import os
import webbrowser
import pyttsx3
import speech_recognition as sr
import pywhatkit
import pyautogui
import requests

# -------------------------
# LOAD API KEYS
# -------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# -------------------------
# VOICE ENGINE
# -------------------------

engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# -------------------------
# LISTEN FUNCTION
# -------------------------

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except:
        return ""

# -------------------------
# TOOLS
# -------------------------

def open_youtube():
    webbrowser.open("https://youtube.com")
    speak("Opening YouTube")

def open_google():
    webbrowser.open("https://google.com")
    speak("Opening Google")

def search_youtube(video):
    pywhatkit.playonyt(video)
    speak(f"Playing {video} on YouTube")

def send_whatsapp(number, message):

    pywhatkit.sendwhatmsg_instantly(
        number,
        message
    )

    speak("WhatsApp message sent")

def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    data = requests.get(url).json()

    temp = data["main"]["temp"]

    weather = data["weather"][0]["description"]

    speak(f"{city} temperature is {temp} degree Celsius with {weather}")

def type_message(text):
    pyautogui.write(text)

# -------------------------
# AI BRAIN
# -------------------------

def ask_ai(user_input):

    response = client.chat.completions.create(

        model="gpt-5",

        messages=[

            {
                "role": "system",
                "content": """
You are Jarvis AI.

Return ONLY one action.

Possible actions:

open_youtube
open_google
weather
youtube_search
whatsapp
type

Examples:

User: open youtube
Output: open_youtube

User: weather in Dhaka
Output: weather:Dhaka

User: play alan walker
Output: youtube_search:alan walker
"""
            },

            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response.choices[0].message.content

# -------------------------
# MAIN LOOP
# -------------------------

speak("Jarvis activated")

while True:

    command = listen()

    if command == "":
        continue

    ai_response = ask_ai(command)

    print("AI Decision:", ai_response)

    # -------------------------
    # ACTIONS
    # -------------------------

    if ai_response == "open_youtube":
        open_youtube()

    elif ai_response == "open_google":
        open_google()

    elif ai_response.startswith("weather:"):

        city = ai_response.split(":")[1]

        get_weather(city)

    elif ai_response.startswith("youtube_search:"):

        video = ai_response.split(":")[1]

        search_youtube(video)

    elif ai_response.startswith("type:"):

        text = ai_response.split(":")[1]

        type_message(text)

    elif ai_response.startswith("whatsapp:"):

        parts = ai_response.split(":")

        number = parts[1]

        message = parts[2]

        send_whatsapp(number, message)

    elif "exit" in command:
        speak("Goodbye")
        break