#coding:utf-8

import tkinter 
import sqlite3
from tkinter import messagebox
import subprocess

window = tkinter.Tk()
window.title("Mon Compable - Inscription")
win_x = 580
win_y = 460
screen_x = window.winfo_screenwidth()
screen_y = window.winfo_screenheight()
posX = (screen_x // 2) - (win_x // 2)
posY = (screen_y // 2) - (win_y // 2)
window.minsize(580,460)
window.geometry(f"{win_x}x{win_y}+{posX}+{posY}")
window.configure(bg="#f0f0f1")
# connection avec sqlite3


# fonctino de creation de compte
def signup(*args):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    username = entry_username.get()
    role = entry_role.get()
    password = entry_password.get()
    ets = entry_ets.get()
    action = "signUp"
    if username =='' or role == '' or password=='' or ets=='' :
        messagebox.showwarning('Erreur','champs de saisi invalid')
    else:
        try:
            new_user = (cursor.lastrowid,username,role,ets,password)
            print(new_user)
            cursor.execute('INSERT INTO users VALUES (?,?,?,?,?)',new_user)
            connection.commit()
            messagebox.showinfo('Sucsess',f'Utilisateurs Enregistré \nIdentifiant : {username}\nRole : {role}\nEtablissement : {ets}')
            window.destroy()
            subprocess.run(['python','index.py',action,username,role,ets,password])
            
        except:
            messagebox.showerror('Erreurs','Erreurs survenu dans l\'enrégistrement de l\'utilisateur')
        finally:
            connection.close()
            
# fonction de redirection 
def redirect_login(*args):
    window.destroy()
    subprocess.run(['python','login.py'])





# création des widgets
frame= tkinter.Frame(window,bg="#f0f0f1")
label_signUp = tkinter.Label(frame,text='Inscrption',bg="#f0f0f1",fg="#2963d6",font=('Arial',30))
label_username = tkinter.Label(frame,text="Identifiant : ",bg="#f0f0f1",fg="black",font=('Arial',15))
entry_username= tkinter.Entry(frame,font=('Arial',15))
label_role = tkinter.Label(frame,text="Role : ",bg="#f0f0f1",fg="black",font=('Arial',15))
entry_role= tkinter.Entry(frame,font=('Arial',15))
label_ets = tkinter.Label(frame,text="Etablissement : ",bg="#f0f0f1",fg="black",font=('Arial',15))
entry_ets= tkinter.Entry(frame,font=('Arial',15))
label_password = tkinter.Label(frame,text="Mot de passe : ",bg="#f0f0f1",fg="black",font=('Arial',15))
entry_password = tkinter.Entry(frame,show="*",font=('Arial',15))
button_signUp = tkinter.Button(frame,text="Inscription",bg="#2963d6",fg="white",font=('Arial',15),border=0,command=signup)
button_away = tkinter.Button(frame,text='j\'ai déja un compte me connecter',bg="#f0f0f1",fg="black",font=('Arial',10),border=0,command=redirect_login)



# positionnement des widgets
frame.pack(pady=45)
label_signUp.grid(row = 0,column=0 ,columnspan=2,pady=15)
label_username.grid(row=1,column=0,sticky='w')
entry_username.grid(row=1,column=1)
label_role.grid(row=2,column=0,pady=10,sticky='w')
entry_role.grid(row=2,column=1,pady=10)
label_ets.grid(row=3,column=0,pady=10,sticky='w')
entry_ets.grid(row=3,column=1,pady=10)
label_password.grid(row=4,column=0,sticky='w')
entry_password.grid(row=4,column=1)
button_signUp.grid(row=5,column=0,columnspan=2,pady=15,ipady=2,ipadx=5)
button_away.grid(row=6,column=0,columnspan=5,pady=3)



window.mainloop()