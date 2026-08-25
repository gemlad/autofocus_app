"""The Task record the whole app passes around.

Lives in its own module so both `main.py` and `todoist_client.py` can import
it. It can't live in main.py: running `python main.py` loads that file as
`__main__`, so `from main import Task` elsewhere would load a *second*
copy of main.py and re-run it.
"""

from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Task:
    name: str
    is_completed: bool = False
    is_dotted: bool = False
    # Todoist ids are strings ("6X4rfFVCjhmWM9fB"), not ints.
    id: str | None = None
    # None for tasks with no due date. A plain `date` for "due Tuesday",
    # a `datetime` when the task is due at a specific time.
    due_date: date | datetime | None = None
    # True for "every day", "every 2 weeks" etc. Completing one of these in
    # Todoist rolls it forward instead of closing it, so the app will need
    # to treat them differently later on.
    is_recurring: bool = False
