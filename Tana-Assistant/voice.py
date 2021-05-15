import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
from playsound import playsound
import glob
import tasks
# TODO:
# ui will call speech function loop which makes use of functions that call the taskapi and wolfram/wiki api
# have a try catch function for error handeling of unknown words
#


def remove_mp3():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for fl in glob.glob(dir_path+"\\*.mp3"):
        # Do what you want with the file
        os.remove(fl)


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
    command = ""
    try:
        command = r.recognize_google(audio)
        print("You said: " + command)
    except sr.UnknownValueError:
        print("Google Speech Recognition did not understand audio")
    except sr.RequestError as e:
        print("Request Failed; {0}".format(e))
    return command


def numbered_list(list):
    numbered_list = [f"{i+1} {list[i]}" for i in range(len(list))]
    return(numbered_list)


def handle_command(command):

    if ("list" and ("today" or "today's") in command):
        listening = True

        response_list = numbered_list(tasks.list_tasks_time()["title"])
        response_string = ", ".join(response_list)
        response = "Today's tasks are " + response_string
        respond(response)

    elif "time" in command:
        listening = True
        respond(ctime())

    elif "stop listening" in command:
        listening = False
        print('Listening stopped')
        return listening
    else:
        listening = True
        respond("Sorry didn't get that")
    return listening


def main_loop():
    time.sleep(2)
    respond("Hi Torja, what can I do for you?")
    listening = True
    while listening == True:
        command = listen()
        listening = handle_command(command)
    remove_mp3()


main_loop()
# numbered_list(tasks.list_tasks_time()["title"])
