"""Todoist access for the AutoFocus app.

Authentication uses a *personal* API token, not OAuth: this app only ever
talks to one account (yours), so there is no need for a client id/secret or
a callback flow. Get the token from Todoist:

    Settings -> Integrations -> Developer -> API token

Put it in a `.env` file in the project root (see `.env.example`). That file
is gitignored and must never be committed. If the token does leak, revoke it
on the same Todoist settings page - deleting the commit is not enough, the
value stays in git history.
"""

import os

from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI

from task import Task

# Reads .env from the project root into os.environ. Real environment
# variables win, so exporting TODOIST_API_TOKEN in the shell overrides .env.
load_dotenv()

TOKEN_VAR = "TODOIST_API_TOKEN"


def get_token() -> str:
    """Return the personal API token, or explain how to set one up."""
    token = os.environ.get(TOKEN_VAR, "").strip()
    if not token:
        raise RuntimeError(
            f"No {TOKEN_VAR} found.\n"
            f"Copy .env.example to .env and paste your token from Todoist: "
            f"Settings -> Integrations -> Developer -> API token."
        )
    return token


def get_api() -> TodoistAPI:
    """Return an authenticated Todoist client."""
    return TodoistAPI(get_token())


def to_task(todoist_task) -> Task:
    """Convert one Todoist API task into the app's own Task record.

    Only the fields the app actually uses are kept, so the rest of the
    code never has to know what a Todoist task object looks like.

    A task with no due date has `due` set to None; recurrence and the date
    itself both live on that `due` object.
    """
    due = todoist_task.due
    return Task(
        name=todoist_task.content,
        id=todoist_task.id,
        due_date=due.date if due else None,
        is_recurring=bool(due and due.is_recurring),
    )


def get_filter_tasks(query: str | None = None) -> list[Task]:
    """Return the active tasks matching a Todoist filter query.

    `query` defaults to TODOIST_FILTER from .env. get_tasks/filter_tasks
    return an iterator of *pages*, each page costing a network request, so
    flatten them here and hand the app a plain list of app Tasks.

    Everything Todoist returns here is active, so is_completed stays False;
    is_dotted is the app's own state and always starts False.
    """
    query = query or os.environ.get("TODOIST_FILTER", "").strip()
    api = get_api()
    pages = api.filter_tasks(query=query) if query else api.get_tasks()
    return [to_task(task) for page in pages for task in page]

def todoist_complete_task(task_id):
    """For recurring tasks, this schedules the next occurrence. For 
    non-recurring tasks, it marks them as completed.
    This method is idempotent for non-recurring tasks (an action that can 
    be performed multiple times without changing the final result beyond 
    the initial application).
    Recurring tasks with a [period]! in Todoist - idempotent.
    Recurring tasks without the ! will tick over to the next instance every time.
    """
    api = get_api()
    api.complete_task(task_id)

def todoist_copy_task(task_id):
    """Creates a duplicate of a task in Todoist."""
    api = get_api()
    task = api.get_task(task_id)
    new_task = api.add_task(
        task.content, 
        description=task.description,
        project_id=task.project_id,
        section_id=task.section_id, 
        parent_id=task.parent_id, 
        labels=task.labels, 
        priority=task.priority, 
        due_string=task.due.string if task.due else None,
        duration=task.duration.amount if task.duration else None,
        duration_unit=task.duration.unit if task.duration else None, 
        assignee_id=task.assignee_id,
        order=task.order, 
        deadline_date=task.deadline.date if task.deadline else None)
    return new_task.id

# if __name__ == "__main__":
   
#     # task_id = "6hMvJ6c573m36RC3"
#     # api = get_api()
#     # task = api.get_task(task_id)
#     # print("Original task: ", task)
#     # copied_task_id = todoist_copy_task(task_id)
#     # new_task = api.get_task(copied_task_id)
#     # print("New task: ", new_task)

