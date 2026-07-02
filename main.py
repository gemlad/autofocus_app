from dataclasses import dataclass

@dataclass
class Task:
    name: str
    completed: bool = False
    dotted: bool = False
    id: int | None = None

tasks: list[Task] = []

def find_task(tasks, task_id):
    return next((t for t in tasks if t.id == task_id), None)


def compare_tasks(tasks):
    print("Running compare_tasks...")
    comparitor = 0
    tasks[comparitor].dotted = True
    for task in tasks:
        if task.id == comparitor:
            continue
        while True:
            choice = input(
                f"Would you rather: 1. {tasks[comparitor].name}, "
                f"or: 2. {task.name}?"
                )
            if choice in ("1", "2"):
                break
            print("Please enter 1 or 2")
        if choice == "2":
            task.dotted = True
            comparitor = task.id


def complete_task(tasks):
    print("Running complete_tasks...")
    dotted_tasks: list[Task] = []
    for task in tasks:
        if task.dotted == True:
            dotted_tasks.append(task)
    last_dotted = find_task(tasks, dotted_tasks[len(dotted_tasks)-1].id)
    if last_dotted is not None:
        print(last_dotted.name)
    while True:
        choice = input(
            f"Your current task is {last_dotted.name}. Have you "
            f"completed it? (y)es or (n)o.\n"
            ).strip().lower()
        if choice in ("y", "n"):
            break
        print("Please enter y or n")
    if choice == "y":
        last_dotted.completed = True
        return last_dotted
    else:
        last_dotted = None
        print("App terminated - do the task then run again!")


def main():
    print("AutoFocus App")
    tasks: list[Task] = [
    Task("Wrestle a bear"),
    Task("Write a review of War & Peace"),
    Task("Solve world peace"),
    Task("Have a nap"),
    Task("Become a mighty pirate")    
    ]
 
    for i, task in enumerate(tasks, start=0):
        task.id = i

    compare_tasks(tasks)    

    for task in tasks:
        if task.dotted == True:
            print(task.name)

    last_completed = complete_task(tasks)
    print(last_completed)

    print(tasks)


if __name__ == "__main__":
    main()
