import sys

from task import Task
from todoist_client import get_filter_tasks
from todoist_client import todoist_complete_task
from todoist_client import todoist_copy_task

tasks: list[Task] = []

QUIT_SENTINEL = "q"

def get_input(prompt):
    """Drop-in replacement for input(). Every prompt in the app should
    call this instead of input() directly, so 'q' always works.
    """
    response = input(prompt).strip()
    if response.lower() == QUIT_SENTINEL:
        quit_no_save()
        # quit_no_save() calls sys.exit() if the user confirms, so
        # execution only reaches here if they said "n" (don't quit).
        # In that case, ask again.
        return get_input(prompt)
    return response

def quit_no_save(): # O says: quit(save = True) might be a good implementation
    while True:
        choice = input(
            f"Are you sure you want to quit?\n"
            f"Y - quit\n"
            f"N - don't quit\n"
            ).strip().lower()
        if choice in ("y", "n"):
            break
        print("Please enter y (to quit) or n (don't quit)")
    if choice == "y":
        sys.exit("Autofocus App terminated.")

def update_tasks(tasks = []):
    try:
        todoist_tasks = get_filter_tasks()
    except RuntimeError as exc:
        sys.exit(str(exc))
    seen = set()  
    tasks = [
        x for x in tasks + todoist_tasks 
        if x.id not in seen and not seen.add(x.id)
        ] #adds new tasks from todoist
    tasks_ids = [x.id for x in tasks]
    todoist_tasks_ids = [x.id for x in todoist_tasks]
    completed = [x for x in tasks_ids if x not in todoist_tasks_ids]
    for x in completed:
        task = find_task(tasks, x)
        task.is_completed = True 
        #marks tasks completed in Todoist as completed in app
    return tasks


def find_task(tasks, task_id):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise ValueError(f"No task found with id {task_id}")
    return task

def find_previous_dot_task(tasks, latest_completed_task=None):
    """ previous_dot_task is the dotted task before the latest completed task.
        Returns previous_dot_task from the task list.
    """
    previous_dot_task = tasks[0]
    if latest_completed_task == None:
        for task in tasks[::-1]:
            if task.is_completed == True:
                continue
            if task.is_dotted == False:
                continue
            if task.is_dotted == True:
                previous_dot_task = task
                return previous_dot_task
    elif latest_completed_task.is_completed == False:
        raise ValueError(f"{latest_completed_task.name} has not been completed.")
    elif latest_completed_task.is_completed == True:
        for task in tasks[tasks.index(latest_completed_task) -1::-1]:
            if task.is_completed == True:
                continue
            elif task.is_completed == False and task.is_dotted == False:
                continue
            elif task.is_completed == False and task.is_dotted == True:
                previous_dot_task = task
                return(previous_dot_task)
            else:
                raise ValueError(f"Task {task.name} metadata corrupted")
    return previous_dot_task
    

def find_resume_from_task(tasks, latest_completed_task = None, previous_dot_task = None):
    """ resume_from_task is the next uncompleted, undotted task on the list
        after the latest completed task.
        Returns resume_from_task from the task list. 
    """
    if latest_completed_task == None:
        # TODO: sort out edge case
        # raise ValueError("No latest_completed_task")
        resume_from_task = tasks[tasks.index(previous_dot_task)+1]
        return(resume_from_task)
    if latest_completed_task.is_completed == False:
        raise ValueError(f"{latest_completed_task.name} has not been completed.")

    for task in tasks[tasks.index(latest_completed_task):]:
        if task.is_completed == False and task.is_dotted == False:
            resume_from_task = task
            return(resume_from_task)
        elif task.is_completed == False and task.is_dotted == True:
            raise ValueError(f"Task {task.name} is dotted but not completed, and a task was completed before it.")
        elif task.is_completed == True:
            continue
        else:
            raise ValueError(f"Task {task.name} metadata corrupted")
    resume_from_task = None
    return(resume_from_task)


def task_compare(tasks, previous_dot_task = None, resume_from_task = None):
    """ Compares a comparator task with the next suitable task.
        The comparator and next suitable task will change.

        Doesn't return anything but changes the tasks' metadata in the list
    """
    print("Running task_compare...")
    if resume_from_task == None:
        return
    if previous_dot_task == None:
        previous_dot_task = tasks[tasks.index(resume_from_task)]
        previous_dot_task.is_dotted = True
    for task in tasks[tasks.index(resume_from_task):]:
        if task == previous_dot_task:
            continue
        if task.is_completed == True:
            continue
        while True:
            choice = get_input(
                f"Would you rather: \n"
                f"1. {previous_dot_task.name}, or\n"
                f"2. {task.name}?\n"
                f"(Q to quit)\n"
                )
            if choice in ("1", "2"):
                break
            print("\nPlease enter 1 or 2. (Q to quit)")
        if choice == "2":
            task.is_dotted = True
            previous_dot_task = task

def task_complete(tasks):
    """Shows the task ready to be completed, and if the user inputs that they have completed it, 
        marks it as completed in the metadata. 
    
        Returns latest_completed_task.
    """
    print("Running task_complete...")
    dotted_tasks: list[Task] = []
    for task in tasks:
        if task.is_dotted == True and task.is_completed == False:
            dotted_tasks.append(task)
    while len(dotted_tasks) > 0:
        # latest_dot_task = find_task(tasks, dotted_tasks[len(dotted_tasks)-1].id)
        latest_dot_task = dotted_tasks[len(dotted_tasks)-1]
        while True:
            choice = get_input(
                f"Your current task is {latest_dot_task.name}. Have you "
                f"completed it? \n\n"
                f"C or Y for fully completed\n"
                f"N for not completed\n"
                f"P for partially completed\n"
                f"Q to quit\n"
                ).strip().lower()
            if choice in ("c", "y", "n", "p"):
                break
            print("Please enter c, n or p (q to quit)\n")
        if choice == "n":
            ## TODO: add choices
            print("Finding a different task...")
            latest_dot_task.is_dotted = False
            return
        if choice == "p":
            todoist_copy_task(latest_dot_task.id)

        todoist_complete_task(latest_dot_task.id)
        latest_dot_task.is_completed = True
        latest_completed_task = latest_dot_task
        return latest_completed_task
        

    sys.exit("You have completed your tasks! Autofocus App terminated.")
    
        

def main():
    print("\n\n     AutoFocus App\n\n")

    tasks = []
    latest_completed_task = None
    resume_from_task = None

    
    while True:
        tasks = update_tasks(
            tasks
            )
        previous_dot_task = find_previous_dot_task(
            tasks, 
            latest_completed_task
            )
        resume_from_task = find_resume_from_task(
            tasks, 
            latest_completed_task, 
            previous_dot_task
            )
        task_compare(
            tasks, 
            previous_dot_task = previous_dot_task, 
            resume_from_task = resume_from_task
            )
        latest_completed_task = task_complete(
            tasks
            )

## Testing code
    # for task in tasks:
    #     if task.is_dotted == True:
    #         print(task.name)

    # completed_task = task_complete(tasks)
    # print("Completed task is ", completed_task) #testing

    # print(tasks)  #testing


if __name__ == "__main__":
    main()
