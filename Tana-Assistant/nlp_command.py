import spacy
from spacy.matcher import Matcher
import custom_logger


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


def get_matches(doc):

    matcher = Matcher(nlp.vocab)

    patterns = [
        [{"TEXT": "list"}],
        [{"TEXT": "lists"}],
        [{"TEXT": "task"}],
        [{"TEXT": "tasks"}],
    ]
    matcher.add("key_words", patterns)

    pattern = [[{"POS": "ADP"}]]
    matcher.add("prepositions", pattern)

    pattern = [[{"POS": "VERB"}]]
    matcher.add("verbs", pattern)

    pattern = [
        [{"TEXT": "clear"}],
        [{"TEXT": "update"}]
    ]
    matcher.add("exceptions", pattern)

    matches = matcher(doc)

    details = format_matches(doc, matches)

    return details


def get_dates(doc):  # dates is a list
    for ent in doc.ents:
        if (ent.label_ == "DATE"):
            return ent.text


def format_matches(doc, matches):
    details = {"key_words": [], "verbs": [],
               "prepositions": [], "exceptions": [], "date": ""}

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

    details["date"] = get_dates(doc)

    return details


def check_details_exceptions(details):
    if (not details["key_words"]):
        return details

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
        elif(not details["exceptions"]):
            return details

        elif(exception_index < first_key_word_index):
            details["verbs"].insert(0, exception)
            details["exceptions"].remove(exception)

    # verb can not be a key word
    if (details["verbs"][0] == first_key_word):
        details["key_words"].remove(first_key_word)

    return details


nlp = spacy.load("en_core_web_sm")
