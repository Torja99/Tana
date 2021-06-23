from logging import exception
import spacy
from spacy.matcher import Matcher


def get_task_api_command(verb):
    command_words = {
        "create": "Create", "make": "Create", "procure": "Create", "generate": "Create",
        "list": "List", "detail": "List", "tell": "List",
        "update": "Update", "clear": "Clear", "finish": "Clear"
    }

    try:
        command = command_words[verb]
    except:
        command = -1
    return command


def get_matches(voice_input):

    matcher = Matcher(nlp.vocab)

    patterns = [
        [{"TEXT": "list"}],
        [{"TEXT": "lists"}],
        [{"TEXT": "task"}],
        [{"TEXT": "tasks"}],
    ]
    matcher.add("key_words", patterns)

    pattern = [[{"TAG": "IN"}]]
    matcher.add("prepositions", pattern)

    pattern = [[{"POS": "VERB"}]]
    matcher.add("verbs", pattern)

    pattern = [[{"TEXT": "clear"}]]
    matcher.add("exceptions", pattern)

    matches = matcher(doc)

    details = format_matches(matches)

    return details


def format_matches(matches):
    details = {"key_words": [], "verbs": [],
               "prepositions": [], "exceptions": []}
    for (match_id, start, end) in matches:
        string_id = nlp.vocab.strings[match_id]

        match_data = (doc[start:end], start, end)
        if (string_id == "key_words"):
            details["key_words"].append(match_data)

        if (string_id == "prepositions"):
            details["prepositions"].append(match_data)

        if (string_id == "verbs"):
            details["verbs"].append(match_data)

        if (string_id == "exceptions"):
            details["exceptions"].append(match_data)

    return details


#!change to manipulate details
def check_details_exceptions(details):
    if (details["verbs"]):  # check if verbs first entry is good
        first_verb_text = str(details["verbs"][0][0])
        command = get_task_api_command(first_verb_text)
    else:
        command = -1

    first_key_word_text = str(details["key_words"][0][0])
    first_key_word = details["key_words"][0]
    first_key_word_index = details["key_words"][0][1]
    if (details["exceptions"]):
        exception = details["exceptions"][0]
        exception_index = details["exceptions"][0][1]

    if (command == -1):  # first verb no good (either doesn't exist or no verbs at all)
        if (first_key_word_text == "list"):
            # insert list as first verb
            details["verbs"].insert(0, first_key_word)
            details["key_words"].remove(first_key_word)

        elif(exception_index < first_key_word_index):
            details["verbs"].insert(0, exception)
            details["exceptions"].remove(exception)
            del(exception)

    return details


nlp = spacy.load("en_core_web_sm")
voice_input = (
    "hey tana create a task called help mom")
doc = nlp(voice_input)
details = get_matches(voice_input)
print(details)
print(check_details_exceptions(details))


#!check to see if the first verb is within the dict
#! if not then check if list is the first key word (take list as verb )
#! or if clear is in exceptions and is before the first key word (take clear as verb)
#! else throw exception
