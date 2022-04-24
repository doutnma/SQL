from tkinter import ttk
import tkinter as tk
import sqlite3

#základ z hodinky

#con = sqlite3.connect(":memory:")
con = sqlite3.connect("example.db")
cur = con.cursor()
cur.executescript("""""")

data = cur.execute("")

for row in data:
    print(row)
con.close()

#SQL tabulka

#pripojeni
def connect():

    con = sqlite3.connect("example.db")
    cur = con.cursor()

#zobrazeni
def View():

    con1 = sqlite3.connect("example.db")
    cur1 = con1.cursor()

    cur1.execute("SELECT * FROM legendy")
    rows = cur1.fetchall()

    for row in rows:
        print(row)
        tree.insert("", tk.END, values=row)

    con1.close()

connect()

window = tk.Tk()
window.geometry("100x100")
window.title("SQL tabulka")

tree = ttk.Treeview(window, column=("c1", "c2", "c3"), show='headings')

tree.column("#1", anchor=tk.CENTER)

tree.heading("#1", text="Jméno")

tree.column("#2", anchor=tk.CENTER)

tree.heading("#2", text="Příjmení")

tree.column("#3", anchor=tk.CENTER)

tree.heading("#3", text="Věk")

tree.pack()

button1 = tk.Button(text="Zobrazit data", command=View)
button1.pack(pady=10)
window.mainloop()