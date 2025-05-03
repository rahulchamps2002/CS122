import tkinter as tk
from tkinter import messagebox
import random
import time

sentences = [
    "The quick brown fox jumps over the lazy dog in the summer breeze.",
    "Artificial intelligence is revolutionizing how people work and learn today.",
    "Typing speed improves with consistent practice and concentration every day.",
    "Python is a powerful and versatile language used in many modern applications.",
    "The rain in Spain falls mainly on the plain in unpredictable patterns."
]

target_sentence = random.choice(sentences)
start_time = None
typing_started = False

def start_timer(event):
    global start_time, typing_started
    if not typing_started:
        typing_started = True
        start_time = time.time()
        update_timer()

def update_timer():
    if not typing_started:
        return
    elapsed = int(time.time() - start_time)
    remaining = 60 - elapsed
    if remaining >= 0:
        timer_label.config(text=f"Time remaining: {remaining} sec")
        root.after(1000, update_timer)
    else:
        finish_test()

def check_typing(event):
    if not typing_started:
        return
    typed = entry.get()
    if typed.strip() == target_sentence.strip():
        finish_test()

def finish_test():
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    typed = entry.get().strip()
    match = typed == target_sentence.strip()
    messagebox.showinfo("Typing Test Complete", f"Time Taken: {duration} sec\nExact Match: {'Yes' if match else 'No'}")
    root.quit()

root = tk.Tk()
root.title("Typing Speed Practice")
root.geometry("900x300")
root.configure(bg="white")  # background color

sentence_label = tk.Label(
    root,
    text=target_sentence,
    font=("Arial", 14),
    wraplength=850,
    bg="white",
    fg="black"
)
sentence_label.pack(pady=20)

entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=100,
    bg="white",              # ensures visible background
    fg="black",              # text color
    insertbackground="black" # blinking cursor color
)
entry.pack(pady=10)
entry.bind("<KeyPress>", start_timer)
entry.bind("<KeyRelease>", check_typing)

timer_label = tk.Label(
    root,
    text="Time remaining: 60 sec",
    font=("Arial", 12),
    bg="white",
    fg="blue"
)
timer_label.pack(pady=10)

entry.focus()
root.mainloop()
