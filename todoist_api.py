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


def get_filter_tasks(query: str | None = None) -> list:
    """Return the active tasks matching a Todoist filter query.

    `query` defaults to TODOIST_FILTER from .env. get_tasks/filter_tasks
    return an iterator of *pages*, each page costing a network request, so
    flatten them here and hand the app a plain list.
    """
    query = query or os.environ.get("TODOIST_FILTER", "").strip()
    api = get_api()
    pages = api.filter_tasks(query=query) if query else api.get_tasks()
    return [task for page in pages for task in page]


if __name__ == "__main__":
    # Smoke test: `python todoist_api.py` proves the token is wired up.
    # A missing token is a setup mistake, not a bug, so show the message
    # rather than a traceback.
    import sys

    try:
        tasks = get_filter_tasks()
    except RuntimeError as exc:
        sys.exit(str(exc))
    print(f"Token works. {len(tasks)} active task(s) found.")
    for task in tasks[:5]:
        print(f"  - {task.content}")
