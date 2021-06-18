import spacy
from spacy.matcher import Matcher


nlp = spacy.load("en_core_web_sm")


voice_input = "Hey Tana can you make a task help mom with groceries task under mom's groceries"
doc = nlp(voice_input)


matcher = Matcher(nlp.vocab)


def get_task_api_command(verb):
    command_words = {
        "create": "Create", "make": "Create", "procure": "Create", "generate": "Create",
        "list": "List", "detail": "List", "tell": "List",
        "update": "Update", "clear": "Clear", "finish": "Clear"
    }

    try:
        command = command_words[verb]
    except:
        command = "-1"
    return command


def extract_first_verb(matcher, doc):
    pattern = [[{"POS": "VERB"}]]

    matcher.add("get_verb", pattern)
    matches = matcher(doc)
    # for match_id, start, end in matches:
    #     matched_span = doc[start:end]
    #     return matched_span.text

    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # get string representation
        span = doc[start:end]  # the matched span

        return match_id, string_id, start, end, span.text


#!get the command
# print(get_task_api_command(verb))


def extract_index_last_prep(matcher, doc):
    pattern = [[{"TAG": "IN"}]]
    matcher.add("get_prep", pattern)
    matches = matcher(doc)

    return (matches)[-1][2]  # last preposition's end index

    # return matches[-1][2]


def extract_first_key(matcher, doc):
    patterns = [
        [{"TEXT": "list"}],
        [{"TEXT": "lists"}],
        [{"TEXT": "task"}],
        [{"TEXT": "tasks"}],
    ]
    matcher.add("keyword", patterns)
    matches = matcher(doc)

    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]  # the matched span
        if (string_id == "keyword"):
            return start, end, span.text

#!extract out the verb, compare its synonyms to a list of other synonyms (or get siimmilarity)- genertaaes a command, read after key words [task,list] and then get the last preposition if command isn't update
#!outputs: first verb, first key word, words after key word and before last preposition,  words after last preposition


def extract_details(matcher, doc):
    patterns = [
        [{"TEXT": "list"}],
        [{"TEXT": "lists"}],
        [{"TEXT": "task"}],
        [{"TEXT": "tasks"}],
    ]
    matcher.add("keyword", patterns)

    pattern = [[{"TAG": "IN"}]]
    matcher.add("get_prep", pattern)
    pattern = [[{"POS": "VERB"}]]

    matcher.add("get_verb", pattern)
    matches = matcher(doc)

    details = {"first_verb": [], "key_word": [],
               "end_index_key_word": [], "index_last_prep": 0}

    # print(matches)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]  # the matched span
        if (len(details["first_verb"]) < 1 and string_id == "get_verb"):
            details["first_verb"].append(span.text)

        if (len(details["key_word"]) < 1 and string_id == "keyword"):
            details["key_word"].append(span.text)
            details["end_index_key_word"].append(end-1)

        if (string_id == "get_prep"):
            details["index_last_prep"] = end-1
        # print(start, end, span.text)

    return details


details = extract_details(matcher, doc)

print(details)
