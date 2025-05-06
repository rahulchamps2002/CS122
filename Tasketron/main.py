import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from logic.task_manager import TaskManager
from logic.analytics import show_completion_pie

class TasketronApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🗂 Tasketron")
        self.root.geometry("800x600")
        self.manager = TaskManager()
        self.setup_styles()
        self.setup_ui()
        self.refresh_task_list()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")  # A cleaner theme for customization

        # General font and background colors
        style.configure("TLabel", font=("Segoe UI", 10), background="#f0f8ff", foreground="black")
        style.configure("TButton", font=("Segoe UI", 10), background="#4CAF50", foreground="white")
        style.configure("TEntry", font=("Segoe UI", 10), relief="solid", padding=5, background="#f9f9f9", foreground="black")
        style.configure("TCombobox", font=("Segoe UI", 10), background="#f9f9f9", foreground="black")

        # Treeview styles
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25, background="#ffffff", fieldbackground="#ffffff", foreground="black")  # White background with black text
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#4CAF50", foreground="white")
        style.map("Treeview", background=[("selected", "#cce5ff")])  # blue highlight for selected item

        # Button hover effects
        style.map("TButton", background=[("active", "#45a049")])

    def create_entry_with_placeholder(self, parent, text_var, placeholder, **kwargs):
        entry = ttk.Entry(parent, textvariable=text_var, **kwargs)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END) if entry.get() == placeholder else None)
        entry.bind("<FocusOut>", lambda e: entry.insert(0, placeholder) if not entry.get() else None)
        return entry

    def setup_ui(self):
        self.title_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.cat_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.priority_var = tk.StringVar()

        # Form
        form_frame = ttk.LabelFrame(self.root, text="Add New Task", padding=10)
        form_frame.pack(padx=15, pady=10, fill="x")

        self.create_entry_with_placeholder(form_frame, self.title_var, "Title", width=20).grid(row=0, column=0, padx=5, pady=5)
        self.create_entry_with_placeholder(form_frame, self.desc_var, "Description", width=25).grid(row=0, column=1, padx=5, pady=5)
        self.create_entry_with_placeholder(form_frame, self.cat_var, "Category", width=15).grid(row=0, column=2, padx=5, pady=5)
        self.create_entry_with_placeholder(form_frame, self.date_var, "YYYY-MM-DD", width=15).grid(row=0, column=3, padx=5, pady=5)

        priority_cb = ttk.Combobox(form_frame, textvariable=self.priority_var, values=["Low", "Medium", "High"], width=10)
        priority_cb.set("Priority")
        priority_cb.grid(row=0, column=4, padx=5, pady=5)

        ttk.Button(form_frame, text="➕ Add Task", command=self.add_task).grid(row=0, column=5, padx=5, pady=5)

        # Task List Treeview
        columns = ("desc", "due", "cat", "priority", "status")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120)

        # Add color to rows
        self.tree.tag_configure("odd", background="#ffffff", foreground="black")  # White background with black text for odd rows
        self.tree.tag_configure("even", background="#ffffff", foreground="black")  # White background with black text for even rows

        self.tree.pack(padx=15, pady=10, fill="both", expand=True)

        # Control Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="✔ Toggle Complete", command=self.toggle_selected).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="🗑 Delete Task", command=self.delete_selected).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="📊 Completion Chart", command=self.show_chart).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="📅 View Calendar", command=self.open_calendar).pack(side="left", padx=10)

    def refresh_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, task in enumerate(self.manager.tasks):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", iid=task["id"], values=(
                task["description"],
                task["due_date"],
                task["category"],
                task["priority"],
                "✔" if task["completed"] else "✘"
            ), tags=(tag,))

    def add_task(self):
        self.manager.add_task(
            self.title_var.get(),
            self.desc_var.get(),
            self.cat_var.get(),
            self.date_var.get(),
            self.priority_var.get()
        )
        self.refresh_task_list()

    def get_selected_task_id(self):
        selected = self.tree.selection()
        return selected[0] if selected else None

    def toggle_selected(self):
        tid = self.get_selected_task_id()
        if tid:
            self.manager.toggle_complete(tid)
            self.refresh_task_list()

    def delete_selected(self):
        tid = self.get_selected_task_id()
        if tid and messagebox.askyesno("Confirm", "Delete this task?"):
            self.manager.delete_task(tid)
            self.refresh_task_list()

    def show_chart(self):
        show_completion_pie(self.manager.tasks, self.root)

    def open_calendar(self):
        top = tk.Toplevel(self.root)
        top.title("📅 Task Calendar")
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(padx=10, pady=10)

        def show_tasks_for_day():
            date = cal.get_date()
            tasks_today = [t for t in self.manager.tasks if t["due_date"] == date]
            msg = "\n".join(f'{t["title"]} - {"✔" if t["completed"] else "✘"}' for t in tasks_today) or "No tasks."
            messagebox.showinfo(f"Tasks on {date}", msg)

        ttk.Button(top, text="Show Tasks", command=show_tasks_for_day).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = TasketronApp(root)
    root.mainloop()
