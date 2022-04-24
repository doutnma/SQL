from tkinter import ttk
import tkinter as tk
import sqlite3
"""
#con = sqlite3.connect(":memory:")
con = sqlite3.connect("example.db")
cur = con.cursor()
cur.executescript('''''')
data = cur.execute("")
for row in data:
    print(row)
con.close()
"""
#registrační formulář
window1 = tk.Tk()
window1.geometry("100x100")
window1.title("Registrační formulář")

jmeno= tk.StringVar()
prijmeni= tk.StringVar()
num = tk.StringVar()
adress= tk.StringVar()
telnum= tk.StringVar()

#připojení k databázi a registrace uživatele
def Connect():
    con = sqlite3.connect("example.db")
    cur = con.cursor()

    #pokud chybí jakékoliv pole je registrace zamítnuta
    if jmeno.get() == "" or prijmeni.get() == "" or num.get() == "" or adress.get() == "" or telnum.get() == "":
        label_zprava.config(text="Vyplňte prosím všechna pole", fg="red")
    elif jmeno.get().isnumeric() or prijmeni.get().isnumeric() or num.get().isalpha() or telnum.get().isalpha():
        label_zprava.config(text="Nesprávně vyplněná pole", fg="red")

    #Naopak, pokud je vše v pořádku, proběhla registrace úspěšně a je tedy spuštěno druhé okno s tabulkou
    else:
        cur.execute("insert into uzivatele_form(jmeno, prijmeni, rodne_cislo, emailova_adresa, telefonni_cislo) VALUES(?, ?, ?, ?, ?)", (jmeno.get(), prijmeni.get(), num.get(), adress.get(), telnum.get()))
        con.commit()
        jmeno.set("")
        prijmeni.set("")
        num.set("")
        adress.set("")
        telnum.set("")
        label_zprava.config(text="Úspěšná registrace!", fg="green")

        # funkce zobrazení dat z databáze
        def View():
            con1 = sqlite3.connect("example.db")
            cur1 = con1.cursor()
            cur1.execute("SELECT * FROM uzivatele_form")
            rows = cur1.fetchall()
            for row in rows:
                print(row)
                tree.insert("", tk.END, values=row)
            con1.close()

        #parametry tabulky
        window2 = tk.Tk()
        window2.geometry("100x100")
        window2.title("Tabulka")
        tree = ttk.Treeview(window2, column=("c1", "c2", "c3", "c4", "c5"), show='headings', height=50)

        tree.column("#1", anchor=tk.CENTER)

        tree.heading("#1", text="Jméno")

        tree.column("#2", anchor=tk.CENTER)

        tree.heading("#2", text="Příjmení")

        tree.column("#3", anchor=tk.CENTER)

        tree.heading("#3", text="Rodné číslo")

        tree.column("#4", anchor=tk.CENTER)

        tree.heading("#4", text="E-mail")

        tree.column("#5", anchor=tk.CENTER)

        tree.heading("#5", text="Telefonní číslo")

        tree.pack()

        #volání funkce pro zobrazená dat z databáze
        View()

        #uzavření okna registračního formuláře a naopak otevření okna s tabulkou
        window1.destroy()
        window2.mainloop()

    cur.close()
    con.close()

#Pole formuláře
label_form = tk.Label(window1, text="Registrační formulář",width=20,font=("bold", 15))
label_form.place(x=70,y=20)

label_jmeno = tk.Label(window1, text="Jméno", width=20, font=("bold", 10))
label_jmeno.place(x=33,y=80)

entry_jmeno = tk.Entry(window1, textvariable=jmeno)
entry_jmeno.place(x=148,y=80)

label_prijmeni = tk.Label(window1, text="Příjmení", width=20, font=("bold", 10))
label_prijmeni.place(x=33,y=120)

entry_prijmeni = tk.Entry(window1, textvariable=prijmeni)
entry_prijmeni.place(x=148,y=120)

label_rodne_cislo = tk.Label(window1, text="Rod. č.", width=20, font=("bold", 10))
label_rodne_cislo.place(x=33,y=160)

entry_rodne_cislo = tk.Entry(window1,textvariable=num)
entry_rodne_cislo.place(x=148,y=160)

label_emailova_adresa = tk.Label(window1, text="E-mail", width=20, font=("bold", 10))
label_emailova_adresa.place(x=33,y=200)

entry_emailova_adresa = tk.Entry(window1, textvariable=adress)
entry_emailova_adresa.place(x=148,y=200)

label_telefonni_cislo = tk.Label(window1, text="Tel. č.", width=20, font=("bold", 10))
label_telefonni_cislo.place(x=33,y=240)

entry_telefonni_cislo = tk.Entry(window1, textvariable=telnum)
entry_telefonni_cislo.place(x=148,y=240)

label_zprava = tk.Label(window1, text="", font=("bold", 10))
label_zprava.place(x=98,y=270)

tk.Button(window1, text='Odeslat', width=10, bg='brown', fg='white', command=Connect).place(x=170,y=310)

#úvodní volání funkce registračního formuláře
window1.mainloop()