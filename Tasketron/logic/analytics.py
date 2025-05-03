from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import Toplevel

def show_completion_pie(tasks, parent):
    if not tasks:
        return

    completed = sum(t["completed"] for t in tasks)
    pending = len(tasks) - completed

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        [completed, pending],
        labels=["Completed", "Pending"],
        colors=["green", "red"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.set_title("Task Completion")
    ax.axis('equal')

    # Create a new popup window inside the GUI
    win = Toplevel(parent)
    win.title("📊 Completion Chart")
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack()
