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
window1.geometry("500x500")
window1.title("Registrační formulář")

jmeno = tk.StringVar()
prijmeni = tk.StringVar()
num = tk.StringVar()
adress = tk.StringVar()
telnum = tk.StringVar()

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
            tree.bind('<ButtonRelease-1>', focus)

        #parametry tabulky
        window2 = tk.Tk()
        window2.geometry("100x100")
        window2.title("Tabulka")

        tree = ttk.Treeview(window2, column=("c1", "c2", "c3", "c4", "c5"), show='headings', height=15)

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

        #funckce, která vybere vybraného uživatele do proměnné
        def focus(event):
            global user_focus
            row_id = tree.identify_row(event.y)
            item = tree.item(tree.focus())
            user_focus = item['values']

        #funkce editování dat
        def Edit():
            window3 = tk.Tk()
            window3.geometry("100x100")
            window3.title("Úprava uživatele")

            label_form1 = tk.Label(window3, text="Úprava dat", width=20, font=("bold", 18))
            label_form1.place(x=130, y=20)

            label_jmeno1 = tk.Label(window3, text="Jméno", width=20, font=("bold", 15))
            label_jmeno1.place(x=17, y=80)

            entry_jmeno1 = tk.Entry(window3, textvariable=jmeno)
            entry_jmeno1.place(x=160, y=80)

            label_prijmeni1 = tk.Label(window3, text="Příjmení", width=20, font=("bold", 15))
            label_prijmeni1.place(x=17, y=120)

            entry_prijmeni1 = tk.Entry(window3, textvariable=prijmeni)
            entry_prijmeni1.place(x=160, y=120)

            label_rodne_cislo1 = tk.Label(window3, text="Rod. č.", width=20, font=("bold", 15))
            label_rodne_cislo1.place(x=17, y=160)

            entry_rodne_cislo1 = tk.Entry(window3, textvariable=num)
            entry_rodne_cislo1.place(x=160, y=160)

            label_emailova_adresa1 = tk.Label(window3, text="E-mail", width=20, font=("bold", 15))
            label_emailova_adresa1.place(x=17, y=200)

            entry_emailova_adresa1 = tk.Entry(window3, textvariable=adress)
            entry_emailova_adresa1.place(x=160, y=200)

            label_telefonni_cislo1 = tk.Label(window3, text="Tel. č.", width=20, font=("bold", 15))
            label_telefonni_cislo1.place(x=17, y=240)

            entry_telefonni_cislo1 = tk.Entry(window3, textvariable=telnum)
            entry_telefonni_cislo1.place(x=160, y=240)

            label_zprava1 = tk.Label(window3, text="", font=("bold", 15))
            label_zprava1.place(x=140, y=280)

            entry_jmeno1.insert(tk.END, user_focus[0])
            entry_prijmeni1.insert(tk.END, user_focus[1])
            entry_rodne_cislo1.insert(tk.END, user_focus[2])
            entry_emailova_adresa1.insert(tk.END, user_focus[3])
            entry_telefonni_cislo1.insert(tk.END, user_focus[4])

            tk.Button(window3, text='Odeslat', fg="blue", width=10).place(x=200, y=320)

        #funkce smazání dat
        def Delete():
            selected_item = tree.selection()
            if selected_item:
                x = selected_item[0]
                tree.delete(x)
                cur.execute("DELETE FROM uzivatele_form WHERE (jmeno, prijmeni, rodne_cislo, emailova_adresa, telefonni_cislo) = (?, ?, ?, ?, ?)", (str(user_focus[0]), str(user_focus[1]), str(user_focus[2]), str(user_focus[3]), str(user_focus[4])))
                con.commit()
                print("mazani vybraneho data")

        #tlačítka pro smazání a editování dat
        button_edit = tk.Button(window2, text="Úprava dat", command=Edit)
        button_edit.place(x=148,y=240)
        button_edit.pack()

        button_delete = tk.Button(window2, text="Smazání dat", command=Delete)
        button_delete.place(x=170, y=240)
        button_delete.pack()

        #volání funkce pro zobrazená dat z databáze
        View()

        #uzavření okna registračního formuláře a naopak otevření okna s tabulkou
        window1.destroy()
        window2.mainloop()

    cur.close()
    con.close()

#Pole formuláře
label_form = tk.Label(window1, text="Registrační formulář",width=20,font=("bold", 18))
label_form.place(x=130,y=20)

label_jmeno = tk.Label(window1, text="Jméno", width=20, font=("bold", 15))
label_jmeno.place(x=17,y=80)

entry_jmeno = tk.Entry(window1, textvariable=jmeno)
entry_jmeno.place(x=160,y=80)

label_prijmeni = tk.Label(window1, text="Příjmení", width=20, font=("bold", 15))
label_prijmeni.place(x=17,y=120)

entry_prijmeni = tk.Entry(window1, textvariable=prijmeni)
entry_prijmeni.place(x=160,y=120)

label_rodne_cislo = tk.Label(window1, text="Rod. č.", width=20, font=("bold", 15))
label_rodne_cislo.place(x=17,y=160)

entry_rodne_cislo = tk.Entry(window1,textvariable=num)
entry_rodne_cislo.place(x=160,y=160)

label_emailova_adresa = tk.Label(window1, text="E-mail", width=20, font=("bold", 15))
label_emailova_adresa.place(x=17,y=200)

entry_emailova_adresa = tk.Entry(window1, textvariable=adress)
entry_emailova_adresa.place(x=160,y=200)

label_telefonni_cislo = tk.Label(window1, text="Tel. č.", width=20, font=("bold", 15))
label_telefonni_cislo.place(x=17,y=240)

entry_telefonni_cislo = tk.Entry(window1, textvariable=telnum)
entry_telefonni_cislo.place(x=160,y=240)

label_zprava = tk.Label(window1, text="", font=("bold", 15))
label_zprava.place(x=140,y=280)

tk.Button(window1, text='Odeslat', fg="blue", width=10, command=Connect).place(x=200,y=320)

#úvodní volání funkce registračního formuláře
window1.mainloop()