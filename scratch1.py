import speech_recognition as sr
from time import ctime
import time
import os
import webbrowser
from gtts import gTTS
import geocoder
from weather import Weather, Unit
import sys
import subprocess


def speak(audioString):
    print(audioString)
    tts = gTTS \
        (text=audioString, lang='en')
    tts.save('audio.mp3')
    os.system("mpg321 audio.mp3")


def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition Server")

    return data


def shodan(data):
    if "how are you" in data:
        speak("I am fine")
    if "what time is it" in data:
        speak(ctime())
    if "where is" in data:
        data = data.split(" ")
        location = data[2]
        speak("Hold on Chris, I will show you where " + location + " is.")
        webbrowser.open("https://www.google.pl/maps/place/" + location)
    if "open website" in data:
        data = data.split(" ")
        site = data[2]
        speak("Hold on Chris.")
        webbrowser.open("https://" + site + ".com")
    if "goodbye" in data:
        speak("goodbye")
        sys.exit(0)
    if "shut down" in data:
        speak("OK Chris, see you next time")
        cmdCommand = "shutdown -h now"
        process = subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)

    if "current weather" in data:
        g = geocoder.ip('me')
        place = (g.lat)
        place2 = (g.lng)
        position = (str(place) + "," + str(place2))
        weather = Weather(Unit.CELSIUS)
        lookup = weather.lookup_by_latlng(place, place2)
        forecasts = lookup.forecast
        for forecast in forecasts:
            speak("Date is: " + forecast.date)
            speak("Weather condition: " + forecast.text)
            speak("Max temperature: " + forecast.high + " Celsius degrees")
            speak("Min temperature: " + forecast.low + " Celsius degrees")
            break
    if "weather forecast" in data:
        g = geocoder.ip('me')
        place = (g.lat)
        place2 = (g.lng)
        position = (str(place) + "," + str(place2))
        weather = Weather(Unit.CELSIUS)
        lookup = weather.lookup_by_latlng(place, place2)
        forecasts = lookup.forecast
        for forecast in forecasts:
            speak("Date is: " + forecast.date)
            speak("Weather condition: " + forecast.text)
            speak("Max temperature: " + forecast.high + " Celsius degrees")
            speak("Min temperature: " + forecast.low + " Celsius degrees")



time.sleep(2)
speak("Hi Chris, what can I do for you?")
while 1:
    data = recordAudio()
    shodan(data)
