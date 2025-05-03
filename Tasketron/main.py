import tkinter as tk
from logic.task_manager import TaskManager
from ui.layout import TasketronUI

def main():
    root = tk.Tk()
    root.title("🗂 Tasketron")
    root.geometry("900x500")
    root.configure(bg="#f9f9f9")

    manager = TaskManager()
    app = TasketronUI(root, manager)

    root.mainloop()

if __name__ == "__main__":
    main()
