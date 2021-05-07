from PySimpleGUI.PySimpleGUI import No
from gtasks_api import GtasksAPI
from urllib.parse import urlparse
import pendulum
from pyasn1.type.univ import Boolean
gtasks = GtasksAPI('credentials.json', 'token.pickle')
if gtasks.auth_url:
    gtasks.finish_login(
        "4/1AY0e-g7dIkNYHc30rRzhSzRr8iQIV3JDVUNxQz1tELSX4Dqcm-a20bpIfOo")


# returns a list of dictionaries with the data needed for application
def parse_response(task_title=None, task_list_title=None):
    task_info = {"task_list_id": "", "task_list_title": "",
                 "task_ids": [], "task_titles": [], "status": [], "due": []}
    task_all_info = []

    task_lists = gtasks.service.tasklists().list().execute()  # get all the task lists
    for task_list in task_lists["items"]:
        task_info["task_list_id"] = task_list["id"]
        task_info["task_list_title"] = task_list["title"]

        tasks = gtasks.service.tasks().list(
            tasklist=task_list["id"], showCompleted=False).execute()
        # go through the tasks of a specific list and add it do the info
        for task in tasks["items"]:
            task_info["task_ids"].append(task["id"])
            task_info["task_titles"].append(task["title"])
            task_info["status"].append(task["status"])
            if "due" in task:
                task_info["due"].append(task["due"])
        task_all_info.append(task_info.copy())
        task_info = {"task_list_id": "", "task_list_title": "",
                     "task_ids": [], "task_titles": [], "status": [], "due": []}

        return task_all_info


# +++++++++++++++++++++++++++++++++++++++++++++++
    # mark _ as completed
    # mark _ from _ as completed
    # mark all from _ as completed

# get task id and tasklist id from a task title
    # list all of tasklist and loop through everything until something matches
# get task id and tasklist id from a task title and task list title
    # last all of task lists and look for matches from there
# get task ids of all tasks and task list of a task list title
    # list all task lists and return all id
# ======================================================


def task_list_get_first_id():
    task_lists = gtasks.service.tasklists().list().execute()  # get all the task lists
    return (task_lists["items"][1]["id"])


# get task ids of all tasks and task list of a task list title
    # list all task lists and return all id
def task_get_id_list(task_list_title):
    # LET THIS ALSO RETURN ALL OF THE IDS UNDERNEATH THAT TASK LIST
    id_info = {"task_list_id": "", "task_ids": ""}
    task_lists = gtasks.service.tasklists().list().execute()  # get all the task lists
    for task_list in task_lists["items"]:
        if (task_list["title"] == task_list_title):
            task_list_id = task_list["id"]
            break  # get the first matching one

    # get tasks under that tasklist
    task_ids = []
    task_list_info = gtasks.service.tasks().list(tasklist=task_list_id).execute()
    for task in task_list_info["items"]:
        task_ids.append(task["id"])
    id_info["task_list_id"] = task_list_id
    id_info["task_ids"] = task_ids
    # CHANGE where this method is being referenced
    return(id_info["task_list_id"])

# enter a task title and defaults to first list get the id (needed for deleting)
# gets the first id of a given task if there are more than one
# below method


def task_get_id(task_title, task_list_title=None):
    task_id = "-1"
    if (task_list_title):
        task_list_id = task_get_id_list(task_list_title=task_list_title)
    else:
        # use first task list if not task list anme
        task_list_id = task_list_get_first_id()
    task_list_info = gtasks.service.tasks().list(tasklist=task_list_id).execute()
    for task in task_list_info["items"]:
        if (task["title"] == task_title):
            task_id = task["id"]
    return task_id


# return ids of tasks between two dates
# due min today for todays tasks, due Max = today to move tasks from before
# defaults to returning todays tasks
# return id, title, duedate
# return a filtered dictionary
def list_tasks_time_updated(dueMin=pendulum.today(), dueMax=pendulum.tomorrow()):
    tasks_due_before_time = []
    tasks_due_before_time_sorted = {
        "id": [], "self_link": [], "title": [], "due": []}
    task_list_ids = []
    task_lists = gtasks.service.tasklists().list().execute()
    valid_tasks = []
    # get the ids each task list
    for task_list in task_lists["items"]:
        task_list_ids.append(task_list["id"])
    for id in task_list_ids:
        # query each tasklist by id
        valid_tasks = (gtasks.service.tasks().list(
            tasklist=id, showCompleted=False, dueMin=dueMin, dueMax=dueMax).execute())
        # extract the tasks from the task list (gets rid of tasklist info)
        if "items" in valid_tasks:
            for task in valid_tasks["items"]:
                tasks_due_before_time.append(task)
    tasks_due_before_time.sort(key=lambda x: x["due"])
    for task in tasks_due_before_time:
        tasks_due_before_time_sorted["id"].append(task["id"])
        tasks_due_before_time_sorted["self_link"].append(task["selfLink"])
        tasks_due_before_time_sorted["title"].append(task["title"])
        tasks_due_before_time_sorted["due"].append(task["due"])
    return tasks_due_before_time_sorted


def list_tasks(task_list_title):
    task_titles = []
    task_list_id = task_get_id_list(task_list_title)
    task_list_info = gtasks.service.tasks().list(tasklist=task_list_id).execute()
    for task in task_list_info["items"]:
        task_titles.append(task["title"])
    return task_titles


def create_task(title, task_list_id=task_list_get_first_id(), due_date=str(pendulum.today())):
    body = {"title": title, "due": due_date}
    gtasks.service.tasks().insert(tasklist=task_list_id, body=body).execute()


def create_task_list(title):
    gtasks.service.tasklists().insert(body={"title": title}).execute()


def delete_task_list(title):
    gtasks.service.tasklists().delete(tasklist=task_get_id_list(title)).execute()


def delete_task(task_list_title, task_title):
    gtasks.service.tasks().delete(tasklist=task_get_id_list(
        task_list_title), task=task_get_id(task_title, task_list_title)).execute()


def update_due_task():
    # find ids of late tasks
    late_tasks_info = list_tasks_time_updated(
        dueMin=None, dueMax=pendulum.today())
    late_task_lists_ids = []
    late_tasks_ids = late_tasks_info["id"]
    late_task_urls = late_tasks_info["self_link"]
    late_tasks_titles = late_tasks_info["title"]
    # get which task list a task belongs to by parsing the selflink
    for url in late_task_urls:
        url_parsed = urlparse(url)
        task_list_id = url_parsed.path.split("/")[4]
        late_task_lists_ids.append(task_list_id)

    for i in range(len(late_task_lists_ids)):
        body = {"title": late_tasks_titles[i], "due": str(
            pendulum.today()), "id": late_tasks_ids[i]}
        gtasks.service.tasks().update(
            tasklist=late_task_lists_ids[i], task=late_tasks_ids[i], body=body).execute()


# update previous implementations using the new parse response function (save as new file and split pane)

# mark all of todays tasks as completed
# desired complete task function functionality
    # mark _ as completed
    # mark _ from _ as completed
    # mark all from _ as completed
    # mark all as completed
    # mark a specific task as completed (just title or specify task list)
    # mark all of a specific tasklist tasks as completed
    # mark all of today's tasks as completed

# fix delete functions

# change title to title and other namings and naming conventions of functions and do only one thing

# NEXT STEPS
# convert the date on text to speech end from today
# 1. how would to get finish_login string for other users
# MVC?
# things to expand upon: pep8 style, documentation that auto generates using https://pdoc3.github.io/pdoc/
