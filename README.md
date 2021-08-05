# Tana
> A Windows Voice Assistant for better Google Tasks management 

## Table of Contents
* [Usage](#usage)
* [Setup](#setup)
* [Main Technologies](#technologies-used)

## Usage
**Update**: Have a bunch of overdue tasks and don't want to spend time manually clicking each one to update? just ask Tana to *update* tasks.

**Create**: Easily create new tasks or lists using the *create/make/generate/procure* key word. 

**List**: Want to hear all your tasks for today or from a specific list just ask Tana to *list/tell* you what your tasks are. 

**Clear**: Done all your tasks for the day? too tired to click through each one to complete it Tana can clear all your tasks for the day or an individual task or all tasks from a list. Just use the key words *clear/finish*. 

**General Questions**: Curious mind? Need to know the weather? ask whatever question and Tana will do its best to answer. 

## Main Technologies
- [Python](https://www.python.org/) 
    - [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/)
    - [SpaCy](https://spacy.io/)
    - [Google Speech API](https://cloud.google.com/text-to-speech)
    - [Google Tasks API](https://developers.google.com/tasks)
    - [Wolfram API](https://products.wolframalpha.com/api/)


## Setup

*prerequisites: have git, python, and pip setup on a Windows machine*
```bat
git pull https://github.com/Torja99/Tana.git
cd Tana
pip install -U requirements.txt
cd Tana-Assistant/
python app.py
```

