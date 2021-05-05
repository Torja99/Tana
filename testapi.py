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
    task_list_id = get_id(task_list_name)
    task_list_info = gtasks.service.tasks().list(tasklist=task_list_id).execute()

    for task in task_list_info["items"]:
        task_titles.append(task["title"])

    return task_titles


test_list = {'kind': 'tasks#taskLists', 'etag': '"LTg4NzY2NDEzOA"', 'items': [{'kind': 'tasks#taskList', 'id': 'MTA5MzE5NzQ5Nzc0MzUxMzc3Mzk6MDow', 'etag': '"NzU4ODMzMzUz"', 'title': 'Current', 'updated': '2021-03-13T20:15:36.914Z', 'selfLink': 'https://www.googleapis.com/tasks/v1/users/@me/lists/MTA5MzE5NzQ5Nzc0MzUxMzc3Mzk6MDow'}, {'kind': 'tasks#taskList', 'id': 'NnNmMndZelBKZ1IwckZCWA', 'etag': '"NjMxNzk0NTc3"', 'title': 'Misc', 'updated': '2021-05-01T02:01:04.779Z', 'selfLink': 'https://www.googleapis.com/tasks/v1/users/@me/lists/NnNmMndZelBKZ1IwckZCWA'}, {'kind': 'tasks#taskList', 'id': 'bi11WE5URnBINUxONDlKSg', 'etag':
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      '"NjMxNTc4MTg4"', 'title': 'School', 'updated': '2021-05-01T01:57:29.044Z', 'selfLink': 'https://www.googleapis.com/tasks/v1/users/@me/lists/bi11WE5URnBINUxONDlKSg'}, {'kind': 'tasks#taskList', 'id': 'S3doa083M0Y0VnpyMzVqUA', 'etag': '"NjAzNzY1OTU5"', 'title': 'Work', 'updated': '2021-04-30T18:13:56.817Z', 'selfLink': 'https://www.googleapis.com/tasks/v1/users/@me/lists/S3doa083M0Y0VnpyMzVqUA'}]}

# print(list_tasks("Current"))
# print("====================================")
print(list_tasks_time())


# BREAK DOWN NEXT STEPS
# convert the date on text to speech end from today
# 1. how would to get finish_login string for other users
# list today's tasks - test with clearing a task
# change filter of todays tasks to have a due min
# function to move all due tasks from yesterday to today
# . create a task for tommorrow
# . create a task list
# . remove a task
# . remove a tasklist
# update a task
# update a tasklist
# change to classes?
# things to expand upon: pep8 style, documentation that auto generates using https://pdoc3.github.io/pdoc/
