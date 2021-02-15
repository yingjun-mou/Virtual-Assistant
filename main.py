# Tony a virtual assistant program that gets the date, current time,
# responds back with a random greeting, and returns information on a person.

# pip install pyaudio
# pip install SpeechRecognition
# pip install gTTS
# pip install wikipedia
from time import sleep

import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia
import pygame

# Igonore any waning messages
warnings.filterwarnings('ignore')


# Record audio and return it as a string
def recordAudio():
    # Record the audio
    r = sr.Recognizer()  # create a recognizer object
    r.energy_threshold = 800
    # Open the microphone and start recording
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('Hi, say something :)')
        # timeout is the time wait for the next word = 5
        # phrase_time_limit = 10
        audio = r.listen(source)

    # Use Googles speech recognition
    data = ''
    try:
        data = r.recognize_google(audio)
        print('You siad: ' + data)
    except sr.UnknownValueError:  # Check for unknown errors
        print('Google Speech Recognition could not understand the audio, unknown error')
    except sr.RequestError as e:
        print('Request results from Google Speech Recognition service error' + str(e))

    return data


# A function to get the virtual assistant response
def assistantResponse(text):
    print(text)

    # Convert text to speech
    myobj = gTTS(text=text, lang='en', slow=False)

    # Save the converted audio to a file
    filename = 'assistant_response.mp3'
    myobj.save(filename)

    # Play the converted file
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # sleep(10)  # prevent from killing
    # os.remove(filename)


# FEATURE 01: WAKING
# A function for wake words or phrases
def wakeWord(text):
    WAKE_WORDS = ['hey tony', 'okay tony', 'tony']  # A list of wake words

    text = text.lower()

    # Check if the user input contains a wake word/phrase
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    return False


# FEATURE 02: RANDOM GREETING RESPONSE
def greeting(text):
    # Possible greeting inputs
    GREETING_INPUTS = ['hi', 'hey', 'hola', 'wassup', 'hello', 'what\'s up']

    # Greeting responses
    GREETING_RESPONSES = ['hey there', 'howday', 'whats good', 'hello']

    # If the users input is a greeting, then return a randomly chosen greeting response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'

    # If no greeting was detected then return an empty string
    return ''


# FEATURE 03: GET CURRENT DATE
# A function to get the current date
def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day

    month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']

    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
                      '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th',
                      '20th', '21st', '22nd', '23th', '24th', '25th', '26th', '27th', '28th',
                      '29th', '30th', '31st', ]

    return 'Today is ' + weekday + ' ' + month_name[monthNum - 1] + ' the ' + ordinalNumbers[dayNum - 1] + '. '


# FEATURE 04: GET CURRENT TIME
# A function to get the current time
def getTime():
    now = datetime.datetime.now()
    meridiem = ''
    if now.hour >= 12:
        meridiem = 'p.m'
        hour = now.hour - 12
    else:
        meridiem = 'a.m'
        hour = now.hour

    # Convert minute into a proper string
    if now.minute < 10:
        minute = '0' + str(now.minute)
    else:
        minute = str(now.minute)

    return 'It is ' + str(hour) + ':' + minute + ' ' + meridiem + '. '



# FEATURE 05: GET PERSON
# A function to get the item name from the text
def getPerson(text):
    wordList = text.split()  ## Splitting the text into a list of words

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i + 1].lower() == 'is':
            return wordList[i + 2] + ' ' + wordList[i + 3]


# FEATURE 06: GET ITEM
# A function to get the item name from the text
def getItem(text):
    wordList = text.split()  ## Splitting the text into a list of words

    for i in range(0, len(wordList)):
        if i + 2 <= len(wordList) - 1 and wordList[i].lower() == 'what' and wordList[i + 1].lower() == 'is':
            return wordList[i + 2]


if __name__ == '__main__':
    while True:
        # (Always) Record the audio
        text = recordAudio()
        response = ''
        # Check for the wake words
        if(wakeWord(text) == True):
            # Check for greetings by the user
            response = response + greeting(text)

            # Check to see if the user said anything having to do with the date
            if('date' in text):
                get_date = getDate()
                response = response + ' ' + get_date

            # Check if user asks about time
            if('time' in text):
                response = response + ' ' + getTime()

            # Check to see if the user said 'who is'
            if('who is' in text):
                person = getPerson(text)
                wiki = wikipedia.summary(person, sentences=2, auto_suggest=False, redirect=False)
                response = response + ' ' + wiki

            # Check to see if the user said 'what is'
            if ('what is' in text):
                item = getItem(text)
                wiki = wikipedia.summary(item, sentences=2, auto_suggest=False, redirect=False)
                response = response + ' ' + wiki

            assistantResponse(response)
