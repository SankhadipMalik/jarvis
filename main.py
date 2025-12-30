import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import wikipedia

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "<your api key>"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(api_key="your api key"),
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def search_info(query):
    query = query.strip().lower()

    # exact confusing cases
    if query in ["who", "what is who"]:
        speak("Do you mean World Health Organization?")
        print("Clarification needed: WHO")
        return

    # too short query
    if len(query.split()) < 2:
        speak("Please ask a complete question")
        return

    try:
        summary = wikipedia.summary(query, sentences=2)
        print("\n--- INFO ---")
        print(summary)
        print("------------\n")
        speak(summary)

    except wikipedia.exceptions.DisambiguationError as e:
        speak("Your question is ambiguous. Please be more specific.")
        print("Options:", e.options[:5])

    except Exception as e:
        print("Wikipedia error:", e)
        speak("I could not find information on that")




def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    elif c.startswith("play"):
        song = c.replace("play", "").strip()

        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak("Song not found in my library")

    elif "news" in c:
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            if not articles:
                speak("No news found")
                return

            for article in articles[:5]:
                title = article.get("title")
                if title:
                    speak(title)
        else:
            speak("Unable to fetch news")

    elif c.startswith(("what is", "who is", "tell me about")):
        query = c
        query = query.replace("what is", "")
        query = query.replace("who is", "")
        query = query.replace("tell me about", "")
        query = query.strip()
        search_info(query)

    else:
        speak("I am searching on Google")
        webbrowser.open(f"https://www.google.com/search?q={c}")





if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for wake word...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)

            word = r.recognize_google(audio)
            print("Heard:", word)

            if "jarvis" in word.lower():
                speak("hello sankha,jarvis is active , command me")

                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=6)

                command = r.recognize_google(audio)
                print("Command:", command)

                processCommand(command)

        except sr.WaitTimeoutError:
            # silence timeout — ignore
            pass

        except sr.UnknownValueError:
            # speech not understood — ignore
            pass

        except Exception as e:
            print("Error:", e)


      



