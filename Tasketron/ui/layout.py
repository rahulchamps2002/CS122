import tkinter as tk
from tkinter import ttk, messagebox
from logic.analytics import show_completion_pie

class TasketronUI:
    def __init__(self, root, task_manager):
        self.root = root
        self.manager = task_manager
        self.setup_ui()

    def setup_ui(self):
        self.root.title("🗂 Tasketron")
        self.root.geometry("900x500")
        self.root.configure(bg="#f9f9f9")

        tk.Label(self.root, text="📋 Task List", font=("Helvetica", 16), bg="#f9f9f9").pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#f9f9f9")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Add Task", width=20, command=self.open_add_task_window).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Mark Completed", width=20, command=self.mark_done).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Delete Task", width=20, command=self.delete_task).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="📊 View Stats", width=20, command=lambda: show_completion_pie(self.manager.tasks, self.root)).grid(row=0, column=3, padx=10)

        self.columns = ("Title", "Due Date", "Category", "Priority", "Completed")
        self.table = ttk.Treeview(self.root, columns=self.columns, show="headings")
        for col in self.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=150)
        self.table.pack(expand=True, fill="both", padx=20, pady=10)

        self.refresh_table()

    def refresh_table(self):
        self.table.delete(*self.table.get_children())
        for task in self.manager.tasks:
            self.table.insert('', 'end', iid=task["id"], values=(
                task["title"],
                task["due_date"],
                task["category"],
                task["priority"],
                "✔" if task["completed"] else "✘"
            ))

    def open_add_task_window(self):
        def save():
            self.manager.add_task(
                title_entry.get(),
                desc_entry.get(),
                category_entry.get(),
                due_entry.get(),
                priority_entry.get()
            )
            self.refresh_table()
            win.destroy()

        win = tk.Toplevel(self.root)
        win.title("Add New Task")

        tk.Label(win, text="Title").grid(row=0, column=0)
        title_entry = tk.Entry(win); title_entry.grid(row=0, column=1)

        tk.Label(win, text="Description").grid(row=1, column=0)
        desc_entry = tk.Entry(win); desc_entry.grid(row=1, column=1)

        tk.Label(win, text="Category").grid(row=2, column=0)
        category_entry = tk.Entry(win); category_entry.grid(row=2, column=1)

        tk.Label(win, text="Due Date (YYYY-MM-DD)").grid(row=3, column=0)
        due_entry = tk.Entry(win); due_entry.grid(row=3, column=1)

        tk.Label(win, text="Priority").grid(row=4, column=0)
        priority_entry = tk.Entry(win); priority_entry.grid(row=4, column=1)

        tk.Button(win, text="Save Task", command=save).grid(row=5, column=1, pady=10)

    def mark_done(self):
        try:
            task_id = self.table.selection()[0]
            self.manager.toggle_complete(task_id)
            self.refresh_table()
        except IndexError:
            messagebox.showwarning("No Selection", "Select a task first.")

    def delete_task(self):
        try:
            task_id = self.table.selection()[0]
            self.manager.delete_task(task_id)
            self.refresh_table()
        except IndexError:
            messagebox.showwarning("No Selection", "Select a task first.")
