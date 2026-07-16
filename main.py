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


def task_compare(tasks, comparitor_task = None):
    print("Running task_compare...")
    if comparitor_task == None:
        comparitor_task = tasks[0]
    comparitor_task.is_dotted = True
    for task in tasks:
        if task == comparitor_task:
            continue
        if task.is_completed == True:
            continue
        while True:
            choice = input(
                f"Would you rather: 1. {comparitor_task.name}, "
                f"or: 2. {task.name}?"
                )
            if choice in ("1", "2"):
                break
            print("Please enter 1 or 2")
        if choice == "2":
            task.is_dotted = True
            comparitor_task = task


def task_complete(tasks):
    print("Running complete_tasks...")
    dotted_tasks: list[Task] = []
    for task in tasks:
        if task.is_dotted == True:
            dotted_tasks.append(task)
    final_dotted_task = find_task(tasks, dotted_tasks[len(dotted_tasks)-1].id)
    print(final_dotted_task.name)
    while True:
        choice = input(
            f"Your current task is {final_dotted_task.name}. Have you "
            f"completed it? (y)es or (n)o.\n"
            ).strip().lower()
        if choice in ("y", "n"):
            break
        print("Please enter y or n")
    if choice == "y":
        final_dotted_task.is_completed = True
        return final_dotted_task 
        # next_unflagged_task = tasks[tasks.index(final_dotted_task)+1]
        # return next_unflagged_task #Should go in compare function
    else: # needs more feature! Currently does not return anything
        final_dotted_task = None
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
