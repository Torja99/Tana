import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
from playsound import playsound
import glob
# TODO:
# ui will call speech function loop which makes use of functions that call the taskapi and wolfram/wiki api
# have a try catch function for error handeling of unknown words
#


def remove_mp3():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for fl in glob.glob(dir_path+"\\*.mp3"):
        # Do what you want with the file
        os.remove(fl)
    print("succ")


def respond(audio_text):
    print(audio_text)
    tts = gTTS(text=audio_text, lang='en')
    id = str(ctime()).split(":")
    id = " ".join(id)
    id = id.replace(" ", "")
    file_name = id + "_speech.mp3"

    tts.save(file_name)
    playsound(file_name)


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening...")
        audio = r.listen(source)
    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition did not understand audio")
    except sr.RequestError as e:
        print("Request Failed; {0}".format(e))
    return data


def digital_assistant(data):
    if "how are you" in data:
        listening = True
        respond("I am well")

    elif "time" in data:
        listening = True
        respond(ctime())

    elif "stop listening" in data:
        listening = False
        print('Listening stopped')
        return listening
        # listening = True
        # print("Sorry didn't get that")
        # respond("sorry")
    else:
        listening = True
        respond("Sorry didn't get that")
    return listening


def main_loop():
    time.sleep(2)
    respond("Hi Torja, what can I do for you?")
    listening = True
    while listening == True:
        data = listen()
        listening = digital_assistant(data)
    remove_mp3()


main_loop()
