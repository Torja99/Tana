from PySimpleGUI.PySimpleGUI import No
from gtasks_api import GtasksAPI
import pendulum
gtasks = GtasksAPI('credentials.json', 'token.pickle')
if gtasks.auth_url:
    gtasks.finish_login(
        "4/1AY0e-g7dIkNYHc30rRzhSzRr8iQIV3JDVUNxQz1tELSX4Dqcm-a20bpIfOo")


def get_id_first_task_list():
    task_lists = gtasks.service.tasklists().list().execute()  # get all the task lists

    return (task_lists["items"][1]["id"])


def get_id_task_list(task_list_name):
    task_lists = gtasks.service.tasklists().list().execute()  # get all the task lists

    for task_list in task_lists["items"]:
        if (task_list["title"] == task_list_name):
            task_list_id = task_list["id"]

    return task_list_id


# enter a task name and defaults to first list get the id (needed for deleting)
# gets the first id of a given task if there are more than one
def get_id_task(task_name, task_list_name=None):
    task_id = "-1"
    task_list_id = get_id_first_task_list()

    if (task_list_name):
        task_list_id = get_id_task_list(task_list_name=task_list_name)
    print(task_list_id)
    task_list_info = gtasks.service.tasks().list(tasklist=task_list_id).execute()

    for task in task_list_info["items"]:
        if (task["title"] == task_name):
            task_id = task["id"]
            break
    return task_id


# list tasks due before that date
def list_tasks_time(time="2021-05-10T14:43:18.000Z"):
    dueMin = pendulum.today()
    tasks_due_before_time = []
    tasks_due_before_time_sorted = []
    task_list_ids = []
    task_lists = gtasks.service.tasklists().list().execute()
    valid_tasks = []

    # get the ids each task list
    for task_list in task_lists["items"]:
        task_list_ids.append(task_list["id"])

    for id in task_list_ids:
        # query each tasklist by id
        valid_tasks = (gtasks.service.tasks().list(
            tasklist=id, showCompleted=False, dueMin=dueMin, dueMax=time).execute())
        # extract the tasks from the task list (gets rid of tasklist info)
        for task in valid_tasks["items"]:
            tasks_due_before_time.append(task)

    tasks_due_before_time.sort(key=lambda x: x["due"])

    for task in tasks_due_before_time:
        tasks_due_before_time_sorted.append(task["title"])

    return tasks_due_before_time_sorted


def list_tasks(task_list_name):
    task_titles = []
    task_list_id = get_id_task_list(task_list_name)
    task_list_info = gtasks.service.tasks().list(tasklist=task_list_id).execute()

    for task in task_list_info["items"]:
        task_titles.append(task["title"])

    return task_titles


def create_task(title, task_list_id=get_id_first_task_list(), due_date=str(pendulum.today())):
    body = {"title": title, "due": due_date}
    gtasks.service.tasks().insert(tasklist=task_list_id, body=body).execute()


def create_task_list(title):

    gtasks.service.tasklists().insert(body={"title": title}).execute()


def delete_task_list(title):
    gtasks.service.tasklists().delete(tasklist=get_id_task_list(title))


def delete_task(task_list_title, task_title):
    gtasks.service.tasks().delete(tasklist=get_id_task_list(
        task_list_title), task=get_id_task(task_title, task_list_title))


# move all due before today to today

# mark all of todays tasks as completed

# fix delete functions

# NEXT STEPS
# convert the date on text to speech end from today
# 1. how would to get finish_login string for other users
# MVC?
# things to expand upon: pep8 style, documentation that auto generates using https://pdoc3.github.io/pdoc/
