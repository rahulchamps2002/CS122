import json
import uuid
from datetime import datetime

class TaskManager:
    def __init__(self, filename="data/tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, title, description, category, due_date, priority):
        task = {
            "id": str(uuid.uuid4()),
            "title": title.strip(),
            "description": description.strip(),
            "category": category.strip(),
            "due_date": due_date.strip(),
            "priority": priority.strip(),
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save_tasks()

    def toggle_complete(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["completed"] = not t["completed"]
        self.save_tasks()

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []
