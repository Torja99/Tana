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


'''
returns task titles between two dates
'''


def list_tasks_time_updated(dueMin=pendulum.today(), dueMax=pendulum.tomorrow()):
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


def create_task_new(task_title, task_list_title=None, due_date=str(pendulum.today())):
    # find id of task tak title
    if task_list_title:
        task_list_id = get_task_list_id(task_list_title=task_list_title)
    else:
        task_list_id = get_task_list_id()
    body = {"title": task_title, "due": due_date}
    print(due_date)
    service.tasks().insert(tasklist=task_list_id, body=body).execute()
