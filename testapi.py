from PySimpleGUI.PySimpleGUI import No
from gtasks_api import GtasksAPI
import pendulum
gtasks = GtasksAPI('credentials.json', 'token.pickle')
if gtasks.auth_url:
    gtasks.finish_login(
        "4/1AY0e-g7dIkNYHc30rRzhSzRr8iQIV3JDVUNxQz1tELSX4Dqcm-a20bpIfOo")


'''
get id of a given task list name
'''


def get_id(task_list_name):
    task_lists = gtasks.service.tasklists().list().execute()  # get all the task lists
    for task_list in task_lists["items"]:
        if (task_list["title"] == task_list_name):
            task_list_id = task_list["id"]
    return task_list_id


# list tasks due before that date
def list_tasks_time(time="2021-05-10T14:43:18.000Z"):

    tasks_due_before_time = []
    task_list_ids = []
    task_lists = gtasks.service.tasklists().list().execute()
    valid_tasks = []

    # get the ids of
    for task_list in task_lists["items"]:
        task_list_ids.append(task_list["id"])

    for id in task_list_ids:
        valid_tasks = (gtasks.service.tasks().list(
            tasklist=id, showCompleted=False, dueMax=time).execute())
        for task in valid_tasks["items"]:
            print(task["title"])

    return None


def list_tasks_by_date(date="Today"):
    task_titles = []
    task_lists = gtasks.service.tasklists().list().execute()
    tasks_all = []

    for task_list in task_lists["items"]:
        task_list_id = task_list["id"]
        task_info = gtasks.service.tasks().list(tasklist=task_list_id).execute()
        tasks_all += task_info["items"]
    # get all of the tasks into one list
    # filter them by date and status needaction
    tasks_with_due = [
        item for item in tasks_all if item["status"] != "completed" and "due" in item]

    for item in tasks_with_due:
        if ("due" in item):

            item["due"] = pendulum.parse(item["due"])

    # print(tasks_with_due)
    sorted_x = sorted(tasks_with_due, key=lambda i: i["due"])
    # for task in sorted_x:

    # print(task["title"])
    # if ("due" in task):
    # print(task["due"])
    # print(type(task["due"]))

    return None


def list_tasks(task_list_name):

    task_titles = []
    task_list_id = get_id(task_list_name)

    task_list_info = gtasks.service.tasks().list(tasklist=task_list_id).execute()
    for task in task_list_info["items"]:
        task_titles += (task["title"])

    return task_titles


test_list = {'kind': 'tasks#taskLists', 'etag': '"LTg4NzY2NDEzOA"', 'items': [{'kind': 'tasks#taskList', 'id': 'MTA5MzE5NzQ5Nzc0MzUxMzc3Mzk6MDow', 'etag': '"NzU4ODMzMzUz"', 'title': 'Current', 'updated': '2021-03-13T20:15:36.914Z', 'selfLink': 'https://www.googleapis.com/tasks/v1/users/@me/lists/MTA5MzE5NzQ5Nzc0MzUxMzc3Mzk6MDow'}, {'kind': 'tasks#taskList', 'id': 'NnNmMndZelBKZ1IwckZCWA', 'etag': '"NjMxNzk0NTc3"', 'title': 'Misc', 'updated': '2021-05-01T02:01:04.779Z', 'selfLink': 'https://www.googleapis.com/tasks/v1/users/@me/lists/NnNmMndZelBKZ1IwckZCWA'}, {'kind': 'tasks#taskList', 'id': 'bi11WE5URnBINUxONDlKSg', 'etag':
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      '"NjMxNTc4MTg4"', 'title': 'School', 'updated': '2021-05-01T01:57:29.044Z', 'selfLink': 'https://www.googleapis.com/tasks/v1/users/@me/lists/bi11WE5URnBINUxONDlKSg'}, {'kind': 'tasks#taskList', 'id': 'S3doa083M0Y0VnpyMzVqUA', 'etag': '"NjAzNzY1OTU5"', 'title': 'Work', 'updated': '2021-04-30T18:13:56.817Z', 'selfLink': 'https://www.googleapis.com/tasks/v1/users/@me/lists/S3doa083M0Y0VnpyMzVqUA'}]}

list_tasks_by_date()
list_tasks_time()
# print(list_tasks("Current"))


# BREAK DOWN NEXT STEPS
# convert the date on text to speech end from today
# 1. how would to get finish_login string for other users
# list today's tasks - test with clearing a task
# . create a task for tommorrow
# . create a task list
# . remove a task
# . remove a tasklist
# update a task
# update a tasklist
# change to classes?
# things to expand upon: pep8 style, documentation that auto generates using https://pdoc3.github.io/pdoc/
