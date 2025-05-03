import json

from flask import Flask, render_template, request, redirect, url_for
from logic.task_manager import TaskManager


app = Flask(__name__)
manager = TaskManager()

@app.route('/')
def index():
    return render_template("index.html", tasks=manager.tasks)

@app.route('/add', methods=['POST'])
def add_task():
    manager.add_task(
        request.form["title"],
        request.form["description"],
        request.form["category"],
        request.form["due_date"],
        request.form["priority"]
    )
    return redirect('/')

@app.route('/toggle/<task_id>')
def toggle(task_id):
    manager.toggle_complete(task_id)
    next_page = request.args.get("next", "/")
    return redirect(next_page)

@app.route('/delete/<task_id>')
def delete(task_id):
    manager.delete_task(task_id)
    next_page = request.args.get("next", "/")
    return redirect(next_page)

@app.route('/calendar')
def calendar():
    events = [{
        "id": task["id"],
        "title": task["title"],
        "start": task["due_date"],
        "description": task["description"],
        "completed": task["completed"]
    } for task in manager.tasks]

    return render_template("calendar.html", calendar_events=json.dumps(events))


if __name__ == '__main__':
    app.run(debug=True)
