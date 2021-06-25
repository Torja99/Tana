import speech_recognition as sr
from time import ctime
import os
from gtts import gTTS
from playsound import playsound
import glob
import tasks
import nlp_command as nc


def remove_mp3():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for fl in glob.glob(dir_path+"\\*.mp3"):
        print(fl)
        # Do what you want with the file
        os.remove(fl)


def respond(audio_text):
    # plays audio text and responds with it
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
        # print("You said: " + command)  # remove after
    except sr.UnknownValueError:
        return "Audio Error"
    except sr.RequestError as e:
        return "Request Failed; {0}".format(e)
    return command


def numbered_list(list):
    numbered_list = [f"{i+1} { list[i]}" for i in range(len(list))]
    return numbered_list

# check if diff permutations of task list are in list of tasks and return an appropriate one


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
    return task_list_title



def handle_command(command):

    if (len(command) <= 2):  # need at least 3 words in command to unpack
        response = "Sorry didn't get that"
        respond(response)
        return response

    nlp = nc.nlp

    doc = nlp(command)
    details = nc.get_matches(doc)
    first_verb_text = str(details["verbs"][0][0])
    action = nc.get_task_api_command(first_verb_text)

    if (details["key_words"]):

        details = nc.check_details_exceptions(details)

        print(details)

    #!no valid actions change to running the wiki/wolfram command
    if (action == -1):

        response = "Sorry didn't get that"
        respond(response)
        return response

    else:

        if (action == "List"):
            if (details["date"]):

                response_list = (tasks.list_tasks_time()["title"])
                response_list_numbered = numbered_list(response_list)
                response_string = ", ".join(response_list_numbered)
                response = f"Today's tasks are {response_string}"
                respond(response)
                return response

            elif(details["prepositions"]):
                end_index_last_prep = details["prepositions"][-1][2]

                task_list_title = str(doc[end_index_last_prep:])

                task_list_title = task_list_verifier(task_list_title)

                if (task_list_title):
                    response_list = (
                        tasks.list_tasks(task_list_title)["title"])
                    response_list_numbered = numbered_list(response_list)
                    response_string = ", ".join(response_list_numbered)
                    response = f"Tasks from {task_list_title} include {response_string}"
                    respond(response)
                    return response
                else:
                    response = "Invalid task list name"
                    respond(response)
                    return response

        elif (action == "Create"):

            first_key_word_index = details["key_words"][0][2]
            key_word_text = str(details["key_words"][0][0])

            if(details["prepositions"]):
                end_index_last_prep = details["prepositions"][-1][2]

                task_list_title = str(doc[end_index_last_prep:])

                task_list_title = task_list_verifier(task_list_title)
                if (task_list_title):
                    task_title = str(
                        doc[first_key_word_index:end_index_last_prep-1])

                    tasks.create_task(task_title, task_list_title)
                    response = f"New task {task_title} under list {task_list_title} created"
                    respond(response)
                    return response

                else:
                    response = "Invalid list name"
                    respond(response)
                return response

            elif(key_word_text == "task"):

                task_title = str(doc[first_key_word_index:])

                if (task_title):
                    tasks.create_task(task_title)

                    response = f"New task {task_title} created"
                    respond(response)
                    return response
                else:
                    response = "Invalid task name"
                    respond(response)
                    return response

            elif(key_word_text == "list"):

                task_list_title = str(doc[first_key_word_index:]).title()

                if (task_list_title):
                    tasks.create_task_list(task_list_title)

                    response = f"New list {task_list_title} created"
                    respond(response)
                    return response
                else:
                    response = "Invalid list name"
                    respond(response)
                    return response

        elif (action == "Clear"):
            first_key_word_index = details["key_words"][0][2]
            key_word_text = str(details["key_words"][0][0])

            if(details["prepositions"]):

                if (key_word_text == "task"):
                    end_index_last_prep = details["prepositions"][-1][2]

                    task_list_title = str(doc[end_index_last_prep:])

                    task_list_title = task_list_verifier(task_list_title)
                    if (task_list_title):
                        task_title = str(
                            doc[first_key_word_index:end_index_last_prep-1])

                        tasks.clear_task_from_list(task_title, task_list_title)
                        response = f"Task {task_title} cleared from {task_list_title}"
                        respond(response)
                        return response

                    else:
                        if (key_word_text == "task"):
                            task_title = str(doc[first_key_word_index:])
                            if (task_title):
                                tasks.clear_task(task_title)
                                response = f"Task {task_title} cleared"
                                respond(response)
                                return response
                            else:
                                response = "Invalid task name"
                                respond(response)
                                return response

                if (key_word_text == "tasks"):
                    end_index_last_prep = details["prepositions"][-1][2]

                    task_list_title = str(doc[end_index_last_prep:])

                    task_list_title = task_list_verifier(task_list_title)

                    if (task_list_title):
                        tasks.clear_all_tasks_from_task_list(task_list_title)
                        response = f"Tasks from {task_list_title} cleared"
                        respond(response)
                        return response
                    else:
                        response = "Invalid task list name"
                        respond(response)
                        return response

            if (key_word_text == "tasks"):
                if(details["date"]):
                    tasks.clear_todays_tasks()
                    response = "Today's tasks cleared"
                    respond(response)
                    return response

                else:
                    response = "Sorry didn't get that"
                    respond(response)
                    return response

            if (key_word_text == "task"):
                task_title = str(doc[first_key_word_index:])
                if (task_title):
                    tasks.clear_task(task_title)
                    response = f"Task {task_title} cleared"
                    respond(response)
                    return response
                else:
                    response = "Invalid task name"
                    respond(response)
                    return response

        elif (action == "Update"):

            tasks.update_due_task()
            response = "Overdue tasks are now due today!"
            respond(response)
            return response

        else:

            response = "Sorry didn't get that"
            respond(response)
            return response


