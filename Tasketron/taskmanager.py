import uuid
import json
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, category, difficulty, due_date):
        task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "category": category,
            "difficulty": difficulty,
            "due_date": due_date,
            "completed": False
        }
        self.tasks.append(task)

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]

    def mark_completed(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["completed"] = True

    def save_tasks(self, filename="tasks.json"):
        with open(filename, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def load_tasks(self, filename="tasks.json"):
        try:
            with open(filename, "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []
