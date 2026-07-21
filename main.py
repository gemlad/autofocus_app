import sys

from dataclasses import dataclass

@dataclass
class Task:
    name: str
    is_completed: bool = False
    is_dotted: bool = False
    id: int | None = None

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

def quit_no_save():
    while True:
        choice = input(
            f"Are you sure you want to quit without saving?"
            f"(y)es (to quit) or (n)o (don't quit)\n"
            ).strip().lower()
        if choice in ("y", "n"):
            break
        print("Please enter y (to quit) or n (don't quit)")
    if choice == "y":
        sys.exit("Autofocus App terminated. Nothing was saved.")

def find_task(tasks, task_id):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise ValueError(f"No task found with id {task_id}")
    return task

def find_previous_dot_task(tasks, latest_completed_task=None):
    """ previous_dot_task is the dotted task before the latest completed task.

        Returns previous_dot_task from the task list.
    """
    if latest_completed_task == None:
        # TODO: sort out edge case
        # raise ValueError("No latest_completed_task")
        previous_dot_task = None
        return(previous_dot_task)
    if latest_completed_task.is_completed == False:
        raise ValueError(f"{latest_completed_task.name} has not been completed.")

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
    

def find_resume_from_task(tasks, latest_completed_task = None):
    """ resume_from_task is the next uncompleted, undotted task on the list after the latest completed task.
        
        Returns resume_from_task from the task list. 
    """
    if latest_completed_task == None:
        # TODO: sort out edge case
        # raise ValueError("No latest_completed_task")
        resume_from_task = tasks[0]
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
    # TODO: resume comparing after completion. Agreed names:
    # previous_dot_task - the dot before latest_completed_task; becomes the new comparator
    # resume_from_task  - the task after latest_completed_task in `tasks`; where scanning resumes
    # If previous_dot_task is None (no earlier dot), restart from the top instead.
    print("Running task_compare...")
    if previous_dot_task == None:
        previous_dot_task = tasks[0]
    previous_dot_task.is_dotted = True
    if resume_from_task == None:
        return
    for task in tasks[tasks.index(resume_from_task):]:
        if task == previous_dot_task:
            continue
        if task.is_completed == True:
            continue
        while True:
            choice = get_input(
                f"Would you rather: 1. {previous_dot_task.name}, "
                f"or: 2. {task.name}? (Press 'q' to quit)\n"
                )
            if choice in ("1", "2"):
                break
            print("Please enter 1 or 2. (Press 'q' to quit)")
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
        latest_dot_task = find_task(tasks, dotted_tasks[len(dotted_tasks)-1].id)
        while True:
            choice = get_input(
                f"Your current task is {latest_dot_task.name}. Have you "
                f"completed it? (y)es or (n)o. (Press 'q' to quit)\n"
                ).strip().lower()
            if choice in ("y", "n"):
                break
            print("Please enter y or n")
        if choice == "y":
            latest_dot_task.is_completed = True
            latest_completed_task = latest_dot_task
            return latest_completed_task
    print("You have completed your tasks!")
    quit_no_save()

    # else: # needs more feature! Currently does not return anything
    #     print("App terminated - do the task then run again!")




        

def main():
    print("\n\n     AutoFocus App\n\n")

    # Load json tasks

    # Poll Todoist - compare, add new tasks to app task list, update completed tasks in app task list
    # Compare tasks
    # Show task to complete
    # Complete task
    # Update todoist

    #rerun from poll Todoist.

    # Any time: save (including update Todoist) and quit, save without quit, or quit without saving

    tasks: list[Task] = [
    Task("Wrestle a bear",id=23),
    Task("Write a review of North & South",id=54),
    Task("Solve world peace",id=654),
    Task("Have a nap",id=654654),
    Task("Become a mighty pirate",id=4987)    
    ]
    
    latest_completed_task = None
    resume_from_task = tasks[0]
    
    while True:
        previous_dot_task = find_previous_dot_task(tasks, latest_completed_task)
        resume_from_task = find_resume_from_task(tasks, latest_completed_task)
        task_compare(tasks, previous_dot_task = previous_dot_task, resume_from_task = resume_from_task)
        latest_completed_task = task_complete(tasks)

## Testing code
    # for task in tasks:
    #     if task.is_dotted == True:
    #         print(task.name)

    # completed_task = task_complete(tasks)
    # print("Completed task is ", completed_task) #testing

    # print(tasks)  #testing


if __name__ == "__main__":
    main()
