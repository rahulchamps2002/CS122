import tkinter as tk
from tkinter import ttk, messagebox
from taskmanager import TaskManager

manager = TaskManager()
manager.load_tasks()

def refresh_table():
    for row in task_table.get_children():
        task_table.delete(row)
    for task in manager.tasks:
        task_table.insert('', 'end', iid=task["id"], values=(
            task["title"], task["due_date"], task["difficulty"], "✔" if task["completed"] else "✘"
        ))

def delete_selected_task():
    selected = task_table.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a task to delete.")
        return
    task_id = selected[0]
    manager.delete_task(task_id)
    manager.save_tasks()
    refresh_table()

def complete_selected_task():
    selected = task_table.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a task to complete.")
        return
    task_id = selected[0]
    manager.mark_completed(task_id)
    manager.save_tasks()
    refresh_table()


def add_task_window():
    def save_new_task():
        manager.add_task(
            title_entry.get(),
            desc_entry.get(),
            category_entry.get(),
            difficulty_box.get(),
            due_entry.get()
        )
        manager.save_tasks()
        refresh_table()
        new_window.destroy()

    new_window = tk.Toplevel(root)
    new_window.title("Add Task")

    tk.Label(new_window, text="Title").grid(row=0, column=0)
    title_entry = tk.Entry(new_window)
    title_entry.grid(row=0, column=1)

    tk.Label(new_window, text="Description").grid(row=1, column=0)
    desc_entry = tk.Entry(new_window)
    desc_entry.grid(row=1, column=1)

    tk.Label(new_window, text="Category").grid(row=2, column=0)
    category_entry = tk.Entry(new_window)
    category_entry.grid(row=2, column=1)

    tk.Label(new_window, text="Difficulty").grid(row=3, column=0)
    difficulty_box = ttk.Combobox(new_window, values=["Easy", "Medium", "Hard"])
    difficulty_box.grid(row=3, column=1)

    tk.Label(new_window, text="Due Date (YYYY-MM-DD)").grid(row=4, column=0)
    due_entry = tk.Entry(new_window)
    due_entry.grid(row=4, column=1)

    tk.Button(new_window, text="Save", command=save_new_task).grid(row=5, column=1)

# --- Main Window ---
root = tk.Tk()
root.title("Tasketron")
root.geometry("700x400")

tk.Button(root, text="Add Task", command=add_task_window).pack(pady=10)
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Delete Selected Task", command=delete_selected_task).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Mark as Completed", command=complete_selected_task).grid(row=0, column=1, padx=10)


cols = ("Title", "Due Date", "Difficulty", "Completed")
task_table = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    task_table.heading(col, text=col)
task_table.pack(fill='both', expand=True)

refresh_table()
root.mainloop()
