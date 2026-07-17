from dataclasses import dataclass

@dataclass
class Task:
    name: str
    is_completed: bool = False
    is_dotted: bool = False
    id: int | None = None

tasks: list[Task] = []

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
        raise ValueError("No latest_completed_task")
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
        raise ValueError("No latest_completed_task")
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
        resume_from_task = tasks[0]
    # TODO: create a new task list of 'suitable tasks'
    for task in tasks[tasks.index(resume_from_task):]:
        if task == previous_dot_task:
            continue
        if task.is_completed == True:
            continue
        while True:
            choice = input(
                f"Would you rather: 1. {previous_dot_task.name}, "
                f"or: 2. {task.name}?"
                )
            if choice in ("1", "2"):
                break
            print("Please enter 1 or 2")
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
        if task.is_dotted == True:
            dotted_tasks.append(task)
    latest_dot_task = find_task(tasks, dotted_tasks[len(dotted_tasks)-1].id)
    print(latest_dot_task.name)
    while True:
        choice = input(
            f"Your current task is {latest_dot_task.name}. Have you "
            f"completed it? (y)es or (n)o.\n"
            ).strip().lower()
        if choice in ("y", "n"):
            break
        print("Please enter y or n")
    if choice == "y":
        latest_dot_task.is_completed = True
        latest_completed_task = latest_dot_task
        return latest_completed_task

    else: # needs more feature! Currently does not return anything
        latest_dot_task = None
        print("App terminated - do the task then run again!")




        

def main():
    print("AutoFocus App")
    tasks: list[Task] = [
    Task("Wrestle a bear",id=23),
    Task("Write a review of War & Peace",id=54),
    Task("Solve world peace",id=654),
    Task("Have a nap",id=654654),
    Task("Become a mighty pirate",id=4987)    
    ]
 
    task_compare(tasks)    

## Testing code
    for task in tasks:
        if task.is_dotted == True:
            print(task.name)

    completed_task = task_complete(tasks)
    print("Completed task is ", completed_task) #testing

    print(tasks)  #testing


if __name__ == "__main__":
    main()
