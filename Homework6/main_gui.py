
import tkinter as tk
from tkinter import ttk, messagebox
from DataBase_ORM import add_book, get_all_books, edit_book, delete_book

root = tk.Tk()
root.title("Book Management")

fields = {}
tk.Label(root, text="📘 BOOK ID", font=("Arial", 10, "bold"), fg="red").grid(row=0, column=0, padx=10, pady=5, sticky='e')
fields['id'] = tk.Entry(root, bg="lightyellow", relief="solid", borderwidth=2)
fields['id'].grid(row=0, column=1, padx=10, pady=5)
for i, label in enumerate(["ID", "Title", "Author", "Year", "Price"]):
    tk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    fields[label.lower()] = entry


# Treeview
tree = ttk.Treeview(root, columns=("ID", "Title", "Author", "Year", "Price"), show='headings')
for col in tree["columns"]:
    tree.heading(col, text=col)
tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

# Functions
def add():
    if not fields['id'].get():
        messagebox.showerror("Error", "Book ID is required.")
        return
    msg = add_book(
        int(fields['id'].get()),
        fields['title'].get(),
        fields['author'].get(),
        int(fields['year'].get()),
        float(fields['price'].get())
    )
    messagebox.showinfo("Add Book", msg)
    show()

def show():
    for i in tree.get_children():
        tree.delete(i)
    for book in get_all_books():
        tree.insert('', 'end', values=(book.id, book.title, book.author, book.year, book.price))

def update():
    if not fields['id'].get():
        messagebox.showerror("Error", "Book ID is required.")
        return
    msg = edit_book(
        int(fields['id'].get()),
        fields['title'].get(),
        fields['author'].get(),
        int(fields['year'].get()),
        float(fields['price'].get())
    )
    messagebox.showinfo("Update Book", msg)
    show()

def delete():
    if not fields['id'].get():
        messagebox.showerror("Error", "Book ID is required.")
        return
    msg = delete_book(int(fields['id'].get()))
    messagebox.showinfo("Delete Book", msg)
    show()

# Buttons
tk.Button(root, text="Add Book", command=add).grid(row=0, column=2, padx=10)
tk.Button(root, text="Update Book", command=update).grid(row=1, column=2, padx=10)
tk.Button(root, text="Delete Book", command=delete).grid(row=2, column=2, padx=10)
tk.Button(root, text="Show All", command=show).grid(row=3, column=2, padx=10)

root.mainloop()
