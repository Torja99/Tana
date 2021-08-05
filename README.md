# Tana
> A Windows Voice Assistant for better Google Tasks management 
## Table of Contents
* [Usage](#usage)
* [Setup](#setup)
* [Main Technologies](#main-technologies)

## Usage

**Update**: Have a bunch of overdue tasks and don't want to spend time manually clicking each one to update? just ask Tana to *update* tasks.

https://user-images.githubusercontent.com/22987998/128398479-70683ae3-6c84-4674-b1fe-b02e0c53aee6.mp4

**Create**: Easily create new tasks or lists using the *create/make/generate/procure* key word. 

https://user-images.githubusercontent.com/22987998/128401037-b3a8437b-3508-48f4-8cb1-3e6daae7f9c7.mp4

**List**: Want to hear all your tasks for today or from a specific list just ask Tana to *list/tell* you what your tasks are. 

https://user-images.githubusercontent.com/22987998/128401150-773de99b-3c61-447c-96b1-805872db5a3a.mp4

**Clear**: Done all your tasks for the day? too tired to click through each one to complete it Tana can clear all your tasks for the day or an individual task or all tasks from a list. Just use the key words *clear/finish*. 

https://user-images.githubusercontent.com/22987998/128401129-6eecd034-9d05-4a25-b1cf-07a8c83e73e1.mp4

**General Questions**: Curious mind? Need to know the weather? ask whatever question and Tana will do its best to answer. 

https://user-images.githubusercontent.com/22987998/128401218-813d73b4-c8c5-493d-a6f1-fbd5bd817d8b.mp4

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
cd Tana/
pip install -U requirements.txt
cd Tana-Assistant/
python app.py
```

