from urllib.parse import urlparse
import pendulum
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/tasks']
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('tasks', 'v1', credentials=creds)


def list_task_lists(maxResults):
    results = service.tasklists().list(maxResults=maxResults).execute()
    items = results.get('items', [])

    if not items:
        print('No task lists found.')
    else:
        print('Task lists:')
        for item in items:
            print(u'{0} ({1})'.format(item['title'], item['id']))


'''
returns tasklist id of a tasklist title otherwise gives first tasklist id
'''


def get_task_list_id(task_list_title=None):
    task_lists = service.tasklists().list().execute()  # get all the task lists
    task_list_id = None
    if (task_list_title):
        for task_list in task_lists["items"]:
            if (task_list["title"] == task_list_title):
                task_list_id = task_list["id"]
                break  # get the first matching one
    else:
        task_list_id = task_lists["items"][0]["id"]
    return (task_list_id)


# gets id of  first task matching that task title
def get_task_info_from_task_title(task_title):
    # get
    tasks_info = {
        "id": [], "list_id": []}
    task_list_id = get_task_list_id(task_title)
    task_lists = service.tasklists().list().execute()
    for task_list in task_lists["items"]:
        task_list_id = task_list["id"]
        tasks = service.tasks().list(tasklist=task_list_id, showCompleted=False).execute()
        # get all tasks under a task list

        if "items" in tasks:
            for task in tasks["items"]:
                if task["title"] == task_title:
                    tasks_info["id"] = task["id"]
                    break
        if tasks_info["list_id"]:
            break
    tasks_info["list_id"] = task_list_id
    return tasks_info


def get_task_info_from_task_list_and_task_title(task_title, task_list_title):
    task_info = {
        "id": "", "list_id": ""}
    task_info["list_id"] = get_task_list_id(task_list_title)

    tasks = service.tasks().list(
        tasklist=task_info["list_id"], showCompleted=False).execute()
    # get all tasks under a task list

    if "items" in tasks:
        for task in tasks["items"]:
            if task["title"] == task_title:
                task_info["id"] = task["id"]
                break
    return (task_info)


'''
return tasks titles under a task list
'''


def list_tasks(task_list_title):
    # may need to update to include id information
    tasks_info = {
        "id": [], "title": []}
    task_list_id = get_task_list_id(task_list_title)
    task_list_info = service.tasks().list(
        tasklist=task_list_id, showCompleted=False).execute()
    if "items" in task_list_info:
        for task in task_list_info["items"]:
            tasks_info["id"].append(task["id"])
            tasks_info["title"].append(task["title"])
    return tasks_info


'''
returns task titles between two dates in sorted order of due date
'''


def list_tasks_time(dueMin=pendulum.today(), dueMax=pendulum.tomorrow()):
    tasks_due_before_time = []
    tasks_due_before_time_sorted = {
        "id": [], "self_link": [], "title": [], "due": []}
    task_list_ids = []
    task_lists = service.tasklists().list().execute()
    valid_tasks = []
    # get the ids each task list
    for task_list in task_lists["items"]:
        task_list_ids.append(task_list["id"])
    for id in task_list_ids:
        # query each tasklist by id
        valid_tasks = (service.tasks().list(
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


'''
changes task due date to today for tasks that were due before today
'''


def update_due_task():
    # find ids of late tasks
    late_tasks_info = list_tasks_time(
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
        service.tasks().update(
            tasklist=late_task_lists_ids[i], task=late_tasks_ids[i], body=body).execute()


'''
creates a tasklist given its title
'''


def create_task_list(title):

    service.tasklists().insert(body={"title": title}).execute()


'''
creates a new task which defaults to todays date as due date, if no title place in first list
'''


def create_task(task_title, task_list_title=None, due_date=str(pendulum.today())):
    # find id of task tak title
    if task_list_title:
        task_list_id = get_task_list_id(task_list_title=task_list_title)
    else:
        task_list_id = get_task_list_id()
    body = {"title": task_title, "due": due_date}
    print(due_date)
    service.tasks().insert(tasklist=task_list_id, body=body).execute()


'''
complete a task: no parameters = complete todays tasks

task list title = complete all under that one those
task name = complete first one with that name
task lis title and name = complete first one with that name
# do above 3 
# make a requirements txt file 

'''


def clear_todays_tasks():
    # get info of todays tasks
    todays_tasks = list_tasks_time()
    todays_task_lists_ids = []
    todays_tasks_ids = todays_tasks["id"]
    todays_tasks_urls = todays_tasks["self_link"]
    todays_tasks_titles = todays_tasks["title"]
    # get which task list a task belongs to by parsing the selflink
    for url in todays_tasks_urls:
        url_parsed = urlparse(url)
        task_list_id = url_parsed.path.split("/")[4]
        todays_task_lists_ids.append(task_list_id)

    for i in range(len(todays_task_lists_ids)):
        body = {"id": todays_tasks_ids[i], "title": todays_tasks_titles[i],
                "status": "completed"}
        service.tasks().update(
            tasklist=todays_task_lists_ids[i], task=todays_tasks_ids[i], body=body).execute()


def clear_all_tasks_from_task_list(task_list_title):
    task_list_id = get_task_list_id(task_list_title=task_list_title)
    # get all task ids from a list
    task_info = list_tasks(task_list_title=task_list_title)
    task_ids = task_info["id"]
    task_titles = task_info["title"]
    for i in range(len(task_ids)):
        body = {"id": task_ids[i], "title": task_titles[i],
                "status": "completed"}
        service.tasks().update(
            tasklist=task_list_id, task=task_ids[i], body=body).execute()


def clear_task(task_title):
    task_info = get_task_info_from_task_title(task_title)
    task_id, task_list_id = task_info["id"], task_info["list_id"]

    body = {"id": task_id, "title": task_title,
            "status": "completed"}
    service.tasks().update(
        tasklist=task_list_id, task=task_id, body=body).execute()
    # find matching title


def clear_task_from_list(task_title, task_list_title):
    task_info = get_task_info_from_task_list_and_task_title(
        task_title, task_list_title)
    task_id, task_list_id = task_info["id"], task_info["list_id"]

    print(task_id)
    print(task_list_id)
    body = {"id": task_id, "title": task_title,
            "status": "completed"}
    service.tasks().update(
        tasklist=task_list_id, task=task_id, body=body).execute()


clear_task_from_list("digital diploma", "TEST")
