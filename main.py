from dataclasses import dataclass

@dataclass
class Task:
    name: str
    completed: bool = False
    dotted: bool = False
    id: int | None = None

tasks: list[Task] = []

def compare_tasks(tasks):
    print("Running compare_tasks...")
    comparitor = 0
    tasks[comparitor].dotted = True
    for task in tasks:
        if task.id == comparitor:
            continue
        while True:
            choice = input(f"Would you rather: 1. {tasks[comparitor].name}, or: 2. {task.name}?")
            if choice in ("1", "2"):
                break
            print("Please enter 1 or 2")


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

    print(tasks)





if __name__ == "__main__":
    main()
