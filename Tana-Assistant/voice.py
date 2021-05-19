from google.auth.crypt import verify_signature
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
        print(fl)
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
    numbered_list = [f"{i+1} { list[i]}" for i in range(len(list))]
    return(numbered_list)

# check if diff permuations of task list are in list of tasks and return an appropriate one


def task_list_verifier(task_list_title):
    task_list_titles = tasks.list_task_lists()

    if(task_list_title.title() in task_list_titles):
        task_list_title = task_list_title.title()
    elif (task_list_title.lower() in task_list_titles):
        task_list_title = task_list_title.lower()
    elif(task_list_title.upper() in task_list_titles):
        task_list_title = task_list_title.upper()
    else:
        task_list_title = None
    return(task_list_title)


def handle_command(command):

    if ("list" and ("today" or "today's") in command):
        listening = True

        response_list = (tasks.list_tasks_time()["title"])
        response_list_numbered = numbered_list(response_list)
        response_string = ", ".join(response_list_numbered)
        response = f"Today's tasks are {response_string}"
        respond(response)

    elif ("list" in command and "create" not in command):
        listening = True
        words_in_command = command.split(" ")

        task_list_title = words_in_command[len(words_in_command)-1]

        task_list_title = task_list_verifier(task_list_title)

        if (task_list_title):
            response_list = (
                tasks.list_tasks(task_list_title)["title"])
            response_list_numbered = numbered_list(response_list)
            response_string = ", ".join(response_list_numbered)
            response = f"Tasks from {task_list_title} include {response_string}"
            respond(response)
        else:
            respond("Invalid task list name")

    elif ("update" in command):
        listening = True
        tasks.update_due_task()
        response = "Overdue tasks are now due today!"
        respond(response)

    elif ("create" and "list" in command):
        listening = True

        words_in_command = command.split(" ")
        task_list_title = words_in_command[len(words_in_command)-1]
        tasks.create_task_list(task_list_title.title())
        response = f"New list {task_list_title} created"
        respond(response)

    elif ("create" and "task" in command and "list" not in command):
        listening = True

        words_in_command = command.split(" ")
        task_title_index = words_in_command.index("task") + 1
        task_title = words_in_command[task_title_index]

        if (task_title_index == len(words_in_command)-1):
            tasks.create_task(task_title)
            response = f"New task {task_title} created"
            respond(response)
        else:
            task_list_title = words_in_command[len(words_in_command)-1]
            task_list_title = task_list_verifier(task_list_title)
            if (task_list_title):
                tasks.create_task(task_title, task_list_title)
                response = f"New task {task_title} under list {task_list_title} created"
                respond(response)
            else:
                respond("Invalid task list name")

    elif ("clear" and ("today" or "today's") in command):
        listening = True
        tasks.clear_todays_tasks()
        response = "Today's tasks cleared"
        respond(response)

    elif (("clear" and "all" in command) and ("today" or "today's") not in command):
        listening = True

        words_in_command = command.split(" ")
        task_list_title = words_in_command[len(words_in_command)-1]
        task_list_title = task_list_verifier(task_list_title)
        if (task_list_title):
            tasks.clear_all_tasks_from_task_list(task_list_title)
            response = f"Tasks from {task_list_title} cleared"
            respond(response)
        else:
            response = "Invalid task list name"
            respond(response)

    elif ("clear" and ("from" or "under") in command):
        listening = True

        words_in_command = command.split(" ")
        task_title_index = words_in_command.index(
            "clear") + 1  # task title is after clear keyword
        task_title = words_in_command[task_title_index]

        # task list title is last word
        task_list_title = words_in_command[len(words_in_command)-1]
        task_list_title = task_list_verifier(task_list_title)
        if (task_list_title):
            tasks.clear_task_from_list(task_title, task_list_title)
            response = f"Task {task_title} cleared from {task_list_title}"
            respond(response)
        else:
            respond("Invalid task list name")

    elif ("clear" in command):
        listening = True

        words_in_command = command.split(" ")
        task_title = words_in_command[len(words_in_command)-1]
        tasks.clear_task(task_title)
        response = f"Task {task_title} cleared"
        respond(response)

    elif "stop" in command:
        listening = False
        print("Done listening")
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


main_loop()
