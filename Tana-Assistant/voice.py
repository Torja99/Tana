import speech_recognition as sr
from time import ctime
from gtts import gTTS
from playsound import playsound
import tasks
import nlp_command as nc
import wolfram
import custom_logger


def respond(audio_text):
    tts = gTTS(text=audio_text, lang='en')
    id = str(ctime()).split(":")
    id = " ".join(id)
    id = id.replace(" ", "")
    file_name = f"temp-audio/{id}_speech.mp3"

    tts.save(file_name)
    playsound(file_name)


def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            custom_logger.log.info("I am listening...")
            audio = r.listen(source)
        command = ""
    except OSError as ex:
        return f"Device Error; {ex}"
    try:
        command = r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Audio Error"
    except sr.RequestError as ex:
        return f"Request Failed; {ex}"
    return command


def numbered_list(list):
    numbered_list = [f"{i+1} { list[i]}" for i in range(len(list))]
    return numbered_list


def handle_command(command):
    custom_logger.log.info(f"Command: {command}")

    if (command == "goodbye" or command == "stop"):
        response = "Goodbye!"
        return response

    # need at least 2 words in command to unpack
    if (command == "Audio Error" or len(command.split()) <= 1):
        response = "Sorry didn't get that"
        return response

    nlp = nc.nlp

    doc = nlp(command)
    details = nc.get_matches(doc)
    custom_logger.log.info(f"details:{details}")

    details = nc.check_details_exceptions(details)
    custom_logger.log.info(details)

    #!when key words or verbs are empty (even after checking for exceptions) send it to wolfram (the verb case is handled in check details exceptions command)
    if (not details["key_words"] or not details["verbs"]):
        response = wolfram.wolfram_query(command)
        return response

    first_verb_text = str(details["verbs"][0][0])
    action = nc.get_task_api_command(first_verb_text)

    #!can get rid of this if statement

    if (action == "List"):
        if (details["date"]):

            response_list = (tasks.list_tasks_time()["title"])
            response_list_numbered = numbered_list(response_list)
            response_string = ", ".join(response_list_numbered)
            response = f"Today's tasks are {response_string}"
            return response

        elif(details["prepositions"]):
            end_index_last_prep = details["prepositions"][-1][2]

            task_list_title = str(doc[end_index_last_prep:])

            task_list_title = tasks.task_list_verifier(task_list_title)

            if (task_list_title):
                response_list = (
                    tasks.list_tasks(task_list_title)["title"])

                if not response_list:
                    response = f"No tasks remaining from {task_list_title}!"
                    return response

                response_list_numbered = numbered_list(response_list)

                response_string = ", ".join(response_list_numbered)
                response = f"Tasks from {task_list_title} include {response_string}"
                return response
            else:
                response = "Invalid task list name"
                return response
        else:
            response = "Sorry didn't get that"
            return response

    elif (action == "Create"):

        first_key_word_index = details["key_words"][0][2]
        key_word_text = str(details["key_words"][0][0])

        if(details["prepositions"]):
            end_index_last_prep = details["prepositions"][-1][2]

            task_list_title = str(doc[end_index_last_prep:])

            task_list_title = tasks.task_list_verifier(task_list_title)
            if (task_list_title):
                task_title = str(
                    doc[first_key_word_index:end_index_last_prep-1])

                tasks.create_task(task_title, task_list_title)
                response = f"New task {task_title} under list {task_list_title} created"
                return response

            else:
                response = "Invalid list name"
            return response

        elif(key_word_text == "task"):

            task_title = str(doc[first_key_word_index:])

            if (task_title):
                tasks.create_task(task_title)

                response = f"New task {task_title} created"
                return response
            else:
                response = "Invalid task name"
                return response

        elif(key_word_text == "list"):

            task_list_title = str(doc[first_key_word_index:]).title()

            if (task_list_title):
                tasks.create_task_list(task_list_title)

                response = f"New list {task_list_title} created"
                return response
            else:
                response = "Invalid list name"
                return response
        else:
            response = "Sorry didn't get that"
            return response

    elif (action == "Clear"):
        first_key_word_index = details["key_words"][0][2]
        key_word_text = str(details["key_words"][0][0])

        if(details["prepositions"]):

            if (key_word_text == "task"):
                end_index_last_prep = details["prepositions"][-1][2]

                task_list_title = str(doc[end_index_last_prep:])

                task_list_title = tasks.task_list_verifier(task_list_title)
                if (task_list_title):
                    task_title = str(
                        doc[first_key_word_index:end_index_last_prep-1])

                    tasks.clear_task_from_list(task_title, task_list_title)
                    response = f"Task {task_title} cleared from {task_list_title}"
                    return response

                else:
                    if (key_word_text == "task"):
                        task_title = str(doc[first_key_word_index:])
                        if (task_title):
                            tasks.clear_task(task_title)
                            response = f"Task {task_title} cleared"
                            return response
                        else:
                            response = "Invalid task name"
                            return response

            if (key_word_text == "tasks"):
                end_index_last_prep = details["prepositions"][-1][2]

                task_list_title = str(doc[end_index_last_prep:])

                task_list_title = tasks.task_list_verifier(task_list_title)

                if (task_list_title):
                    tasks.clear_all_tasks_from_task_list(task_list_title)
                    response = f"Tasks from {task_list_title} cleared"
                    return response
                else:
                    response = "Invalid task list name"
                    return response

        if (key_word_text == "tasks"):
            if(details["date"]):
                tasks.clear_todays_tasks()
                response = "Today's tasks cleared"
                return response

            else:
                response = "Sorry didn't get that"
                return response

        if (key_word_text == "task"):
            task_title = str(doc[first_key_word_index:])
            if (task_title):
                tasks.clear_task(task_title)
                response = f"Task {task_title} cleared"
                return response
            else:
                response = "Invalid task name"
                return response

    elif (action == "Update"):
        tasks.update_due_task()
        response = "Overdue tasks are now due today!"
        return response

    else:

        response = "Sorry didn't get that"
        return response
