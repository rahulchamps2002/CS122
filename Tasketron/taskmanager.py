import uuid
from TitleBanner import show_banner
import json
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self):
        print("\n📝 Add New Task")
        title = input("Title: ")
        description = input("Description: ")
        category = input("Category: ")
        difficulty = input("Difficulty (Easy/Medium/Hard): ")
        due_date = input("Due Date (YYYY-MM-DD): ")

        task = {
            "id": str(uuid.uuid4()),
            "title": title.strip(),
            "description": description.strip(),
            "category": category.strip(),
            "difficulty": difficulty.strip(),
            "due_date": due_date.strip(),
            "completed": False
        }

        self.tasks.append(task)
        print("✅ Task added successfully.\n")

    def find_task(self, num):
        if self.tasks[num-1]:
            task = self.tasks[num-1]
            return task
        print("❌ Task not found.")
        return None

    def delete_task(self, filename="tasks.json"):
        self.list_tasks()
        print("\n🗑️ Delete Task")
        number = input("Enter task number to delete: ")
        task = self.find_task(int(number))

        if task:
            self.tasks.remove(task)
            self.save_tasks(filename)  # Save changes to file
            print("✅ Task deleted and file updated.\n")


    def update_task(self):
        print("\n🔄 Update Task")
        num = input("Enter task number to mark as completed: ")
        task = self.find_task(int(num))

        if task:
            task["completed"] = True
            print(f"✅ Task '{task['title']}' marked as completed.\n")

    def list_tasks(self):
        print("\n📋 Current Tasks")
        tasknum = 1
        if not self.tasks:
            print("No tasks available.\n")
            return
        for task in self.tasks:
            status = "✔️" if task["completed"] else " "
            print(f"{tasknum} [{status}] {task['title']} - Due: {task['due_date']} | Difficulty: {task['difficulty']}")
            tasknum += 1
        print()

    def list_tasks_sorted_by_date(self):
        tasknum = 1
        print("\n📅 Tasks Sorted by Due Date")
        if not self.tasks:
            print("No tasks available.\n")
            return

        try:
            sorted_tasks = sorted(
                self.tasks,
                key=lambda t: datetime.strptime(t["due_date"], "%Y-%m-%d")
            )
        except ValueError:
            print("⚠️ One or more tasks have invalid date format. Use YYYY-MM-DD.\n")
            return

        for task in sorted_tasks:
            status = "✔️" if task["completed"] else " "
            print(f"{tasknum}. [{status}] {task['title']} - Due: {task['due_date']} | Difficulty: {task['difficulty']}")
            tasknum += 1
        print()

    def save_tasks(self, filename="tasks.json"):
        with open(filename, "w") as f:
            json.dump(self.tasks, f, indent=2)
    print("💾 Tasks saved successfully.\n")

    def load_tasks(self, filename="tasks.json"):
        try:
            with open(filename, "r") as f:
                self.tasks = json.load(f)
            print("📂 Tasks loaded successfully.\n")
        except FileNotFoundError:
            print("⚠️ No saved tasks found. Starting fresh.\n")


def run():
    manager = TaskManager()

    while run:
        show_banner()
        print("Menu:")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Choice: ")
        if choice == "1":
            manager.add_task()
            manager.save_tasks()
        elif choice == "2":
            manager.list_tasks_sorted_by_date()
        elif choice == "3":
            manager.update_task()
            manager.save_tasks()
        elif choice == "4":
            manager.delete_task()
            manager.save_tasks()
        elif choice == "5":
            print("Goodbye from Tasketron.\n")
            break
        else:
            print("Invalid choice. Try again.\n")

run()
