#coding:utf-8

import tkinter 
import sqlite3
from tkinter import messagebox
import subprocess



window = tkinter.Tk()
window.title("Mon Compable - Connexion")
win_x = 580
win_y = 460
screen_x = window.winfo_screenwidth()
screen_y = window.winfo_screenheight()
posX = (screen_x // 2) - (win_x // 2)
posY = (screen_y // 2) - (win_y // 2)
window.minsize(580,460)
window.geometry(f"{win_x}x{win_y}+{posX}+{posY}")
window.configure(bg="#f0f0f1")

# fonctions
def login(*args):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    username= entry_username.get()
    password = entry_password.get()
    if username =='' or password == '':    
        messagebox.showwarning('Erreur','champs de saisi invalid')
    else:
        try:
            print(f'nom {username} password {password}')
            user = (username,)
            req = cursor.execute('SELECT * FROM users WHERE name_user=?',user) 
            user_info = req.fetchone()
            name = user_info[1]
            role = user_info[2]
            ets = user_info[3]
            mdp = user_info[4]
            action = 'login'
            if password ==  mdp:
                messagebox.showinfo('Sucsess',f'Utilisateur : {username} ({role})')
                window.destroy()
                subprocess.run(['python','index.py',action,name,role,ets,mdp])
            else:
                messagebox.showerror('Erreur','Mot de passe incorrect')
        except:
            messagebox.showwarning('Erreurs','Identifiant incorrect')
        finally:
            connection.close()
           
            
# redirection vers signup
def redirect_signUp(*args):
    window.destroy()
    subprocess.run(['python','signUp.py'])
        







# creation des widget
frame= tkinter.Frame(window,bg="#f0f0f1")
label_login = tkinter.Label(frame,text='Connexion',bg="#f0f0f1",fg="#2963d6",font=('Arial',30))
label_username = tkinter.Label(frame,text="Identifiant : ",bg="#f0f0f1",fg="black",font=('Arial',15))
entry_username= tkinter.Entry(frame,font=('Arial',15))
label_password = tkinter.Label(frame,text="Mot de passe : ",bg="#f0f0f1",fg="black",font=('Arial',15))
entry_password = tkinter.Entry(frame,show="*",font=('Arial',15))
button_login = tkinter.Button(frame,text="Connexion",bg="#2963d6",fg="white",font=('Arial',15),border=0,command=login,)
button_away = tkinter.Button(frame,text='j\'ai déja un compte me connecter',bg="#f0f0f1",fg="black",font=('Arial',10),border=0,command=redirect_signUp)


# positionnement des widget
frame.pack(pady=45)
label_login.grid(row = 0,column=0 ,columnspan=2,pady=15)
label_username.grid(row=1,column=0,sticky='w')
entry_username.grid(row=1,column=1)
label_password.grid(row=2,column=0,pady=10,sticky='w')
entry_password.grid(row=2,column=1,pady=10)
button_login.grid(row=3,column=0,columnspan=2,pady=15,ipady=2,ipadx=5)
button_away.grid(row=4,column=0,columnspan=2,pady=5)



window.mainloop()