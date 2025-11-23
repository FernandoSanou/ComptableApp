#coding:utf-8

import tkinter 
import sys
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import time
window = tkinter.Tk()
window.title("Mon Compable")
win_x = 1080
win_y = 620
screen_x = window.winfo_screenwidth()
screen_y = window.winfo_screenheight()
posX = (screen_x // 2) - (win_x // 2)
posY = (screen_y // 2) - (win_y // 2)
window.minsize(1080,620)
window.geometry(f"{win_x}x{win_y}+{posX}+{posY-35}")
window.configure(bg="#fff")
window.columnconfigure(0,weight=1)
window.columnconfigure(1,weight=0)
window.columnconfigure(2,weight=500)
window.rowconfigure(0,weight=1)



# recuperaion des donnees
# def get_user_info(*args):
# action = sys.argv[1]
# username = sys.argv[2]
# role = sys.argv[3]
# ets = sys.argv[4]
# mdp = sys.argv[5] 
action = "login"
username = "Fernnado"
role = "codeur"
ets = "ETS VISA"
mdp = "0000" 

print(f'idenifiant : {username} role : {role} ets : {ets} password : {mdp} action : {action}')

stop_user_fonction = False
stop_vente_fonction = False

def user_show():

    # stop_vente_fonction = True
    name = f'Identifiant : {username}'
    fonction = f'Fonction : {role}'
    work = f'Lieu de travail : {ets}'
    label_show_title = tkinter.Label(frame2,text="Utilisateur : ",bg="#fff",fg="#2963d6",font=('calibri',16))
    label_show_title.grid(row=0 ,column=0,columnspan=2,sticky='nw')
    
    label_show_username = tkinter.Label(frame2,text=name,bg="#fff",fg="black",font=('calibri',13))
    label_show_username.grid(row=1 ,column=0,columnspan=2,sticky='ne')
    
    label_show_role = tkinter.Label(frame2,text=fonction,bg="#fff",fg="black",font=('calibri',13))
    label_show_role.grid(row=2 ,column=0,columnspan=2,sticky='ne')
    
    label_show_ets = tkinter.Label(frame2,text=work,bg="#fff",fg="black",font=('calibri',13))
    label_show_ets.grid(row=3 ,column=0,columnspan=2,sticky='ne')
# vente partie
def vente_show(*args):
    # verifier si ily a des produits dansla base de donnees
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    name = (username,)
    cursor.execute('SELECT * FROM produits WHERE username=?',name)
    rows = cursor.fetchall()
    timevar = time.strftime('%d/%m/%Y')
    date = f'Ventes :{timevar}'
    label_show_title = tkinter.Label(frame2,text=date,bg="#fff",fg="#2963d6",font=('calibri',16))
    label_show_title.grid(row=0 ,column=0,sticky='nw')
    day = time.strftime("%A")
    print(day)
    month = time.strftime("%B")
    print(month)
    years = time.strftime("%y")
    print(years)
    getMoney = (username,day,month,years)
    cursor.execute("SELECT * FROM money WHERE  day=? AND month = ? AND years=? AND username=? ",getMoney)
    result = cursor.fetchone()
    if result is None:
        caisseMoney = 0
    else:
        caisseMoney = result
    # caisseMoney = 160000
    sold = f'Vendu en ce jour : {caisseMoney} f '
    label_add_vente = tkinter.Label(frame2,text=sold,bg="#fff",fg="black",font=('calibri',16))
    label_add_vente.grid(row=2 ,column=1,sticky='nw')
    button_add_vente  = tkinter.Button(frame2,text='Vendre + ',border=0,bg='#2963d6',fg='#fff',font=('Arial',15),command=addVente)
    button_add_vente.grid(row=4,column=1,sticky='nw',ipadx=0 ,ipady=0)

    connection.close()

def addVente(**args):
    def add_vente_fonction(**args):
        print('je veux la somme')
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        quantite = entry_quantite.get()
        print(quantite)
        if quantite=="":
            messagebox.showwarning('Erreur','champs de saisi invalid')
        else:
            quantite = int(entry_quantite.get())
            name_vente = list_name.get(list_name.curselection())
            print(name_vente)
                
        # try:           
            produit = (name_vente,)
            cursor.execute('SELECT * FROM produits WHERE name_produits=?',produit)
            rows = cursor.fetchone()
            name_product = rows[1]
            prix_achat = rows[2]
            prix_vente = rows[3]
            quantite_stock = rows[5]
            date = time.strftime('%d/%m/%Y')
            print(rows[1])
            montant = int(quantite) * int(prix_vente)
            benefice = (int(prix_vente)-int(prix_achat))*int(quantite)
            print(montant)
            ventes = (cursor.lastrowid,name_product,quantite,prix_vente,username,date,)
            print(ventes)
            if quantite <= quantite_stock: 
                stock = int(quantite_stock)- int(quantite)
                new_stock = (stock,name_product,username,)
                print(new_stock)
                cursor.execute("INSERT INTO vente (name_product,quantite,prix_vente,montant,restant,username,date) VALUES (?,?,?,?,?,?,?)",(name_product,quantite,prix_vente,montant,stock,username,date))
                connection.commit()
                
                messagebox.showinfo('Sucsess',f'Vente éffectuée ! \nnom du produit : {name_product}\nprix de vente : {prix_vente}\nQuantité : {quantite}\nMontant : {montant}\nBénéfice : {benefice} \nRestant dans le stock : {stock}')
                cursor.execute("UPDATE produits SET stock=? WHERE name_produits=? AND username=?",new_stock)
                connection.commit()

                # verification du solde
                user = (username,)
                cursor.execute("SELECT SUM(montant) FROM vente WHERE username=?",user)
                resultats = cursor.fetchone()[0]
                print(resultats)
                day = time.strftime("%A")
                print(day)
                month = time.strftime("%B")
                print(month)
                years = time.strftime("%y")
                print(years)
                getMoney = (day,month,years,username)
                cursor.execute("SELECT * FROM money WHERE day=? AND month = ? AND years=? AND username=? ",getMoney)
                result = cursor.fetchone()
                if result is None :
                    getMoney = (resultats,day,month,years,username,)
                    print(getMoney)
                    cursor.execute("INSERT INTO money (money,day,month,years,username)VALUES(?,?,?,?,?)",getMoney)
                    cursor.commit()
                else :
                    messagebox.showwarning('Erreur',f'votre vente de {name_product} est supérieur est supétieur au nombre restant dans le stock\nRestant : {quantite_stock}\nNombre demandé {quantite}')
                    second_window.destroy()

        # except:
            # messagebox.showerror('Erreurs','Erreurs survenu dans l\'enrégistrement de la vente')
            # second_window.destroy()
            
        # finally:
            connection.close()
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    second_window = tkinter.Toplevel(window)
    second_window.title='Ajout de ventes'
    win_x = 720
    win_y = 540
    screen_x = window.winfo_screenwidth()
    screen_y = window.winfo_screenheight()
    posX = (screen_x // 2) - (win_x // 2)
    posY = (screen_y // 2) - (win_y // 2)
    second_window.minsize(720,540)
    second_window.geometry(f"{win_x}x{win_y}+{posX}+{posY-35}")
    second_window.configure(bg="#f5f6f6")
    frame_second_window= tkinter.Frame(second_window,bg="#f5f6f6")



    
    label_add_vente = tkinter.Label(frame_second_window,text='Ajout vente : ',bg="#f5f6f6",fg="#2963d6",font=('Calibri',30))
    label_name = tkinter.Label(frame_second_window,text="Nom produit: ",bg="#f5f6f6",fg="black",font=('Calibri',15))
    entry_name = tkinter.Entry(frame_second_window,font=('Calibri',15))
    label_stock = tkinter.Label(frame_second_window,text="Stock",bg="#f5f6f6",fg="black",font=('Calibri',10))
    label_quantite = tkinter.Label(frame_second_window,text="QUANTITE : ",bg="#f5f6f6",fg="black",font=('Calibri',15))
    entry_quantite = tkinter.Entry(frame_second_window,font=('Calibri',15))
    label_benef = tkinter.Label(frame_second_window,text="Benefice",bg="#f5f6f6",fg="black",font=('Calibri',15))
    button_add_vente= tkinter.Button(frame_second_window,text="Vendre",bg="#2963d6",fg="white",font=('Calibri',15),border=0,command=add_vente_fonction)
    list_name = tkinter.Listbox(frame_second_window,font=('Calibri',15))


    user = (username,)
    cursor.execute('SELECT * FROM produits WHERE username=?',user)
    rows = cursor.fetchall()
    i = 0
    # print(rows)
    for name_product in rows:
        name_vente = name_product[1]
        list_name.insert(tkinter.END,name_product[1])
    
    # list_name.bind('<<ListboxSelect>>',on_select)

    
    
    
    connection.close()
    
    # button_away = tkinter.Button(frame_second_window,text='j\'ai déja un compte me connecter',bg="#f5f6f6",fg="black",font=('Calibri',10),border=0,command=redirect_login)
    
    # positionnement des widgets
    frame_second_window.pack(pady=45)
    label_add_vente.grid(row = 0,column=0 ,columnspan=2,pady=15)
    label_name.grid(row=1,column=0,sticky='w')
    list_name.grid(row=1,column=1)
    # entry_name.grid(row=1,column=1)
    #     button_sold_vente.grid(row=2,column=1,sticky='w')
    label_quantite.grid(row=3,column=0,sticky='w',pady=3)
    entry_quantite.grid(row=3,column=1)
    # label_benef.grid(row=4,column=1,sticky='w',pady=3)
    button_add_vente.grid(row=5,column=0,columnspan=2,pady=15,ipady=2,ipadx=5)
    # button_away.grid(row=6,column=0,columnspan=5,pady=3)
# stock


def stock_show(*args):
    def data_user(*args):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()  
        name = (username,)
        cursor.execute('SELECT * FROM produits WHERE username=?',name)
        rows = cursor.fetchall()
        connection.close()
        return rows
    
    label_show_title = tkinter.Label(frame2,text="Stock : ",bg="#fff",fg="#2963d6",font=('calibri',16))
    label_show_title.grid(row=0 ,column=0,sticky='nw')
    
    label_show_description = tkinter.Label(frame2,text="Ajoutez et gerez vos produits dans le stock",bg="#fff",fg="black",font=('calibri',16))
    label_show_description.grid(row=0 ,column=1,columnspan=3,sticky='nw')
    
    button_add_produit  = tkinter.Button(frame2,text='Ajoutez',border=0,bg='#2963d6',fg='#fff',font=('Arial',15),command=addProduct)
    button_add_produit.grid(row=3,column=1,sticky='nw',ipadx=5 ,ipady=3,pady=10)

    button_modife_produit  = tkinter.Button(frame2,text='Modifier',border=0,bg='#2963d6',fg='#fff',font=('Arial',15),command=modife_product)
    button_modife_produit.grid(row=3,column=2,sticky='nw',ipadx=5 ,ipady=3,pady=10)

    button_delete_produit  = tkinter.Button(frame2,text='Supprimer',border=0,bg='#2963d6',fg='#fff',font=('Arial',15))
    button_delete_produit.grid(row=3,column=3,sticky='nw',ipadx=5 ,ipady=3,pady=10)
   
    label_show_text = tkinter.Label(frame2,text="Vos produits:",bg="#fff",fg="black",font=('calibri',16))
    label_show_text.grid(row=5 ,column=2,columnspan=2,sticky='nw')
    # creation du treeview
    tree = ttk.Treeview(frame2,columns=("ID","Nom produit","prix ahat","prix vente","Bénéfice","Quantité"),show='headings')
    tree.heading('ID',text="ID")
    tree.heading('Nom produit',text="Nom produit")
    tree.heading('prix ahat',text="prix ahat")
    tree.heading('prix vente',text="prix vente")
    tree.heading('Bénéfice',text='Bénéfice')
    tree.heading('Quantité',text='Quantité')
    
    # ajout de donnees
    data =data_user()
    for item in data:
        tree.insert('',tkinter.END,values=item)
        
    tree.grid(row=6 ,column=0,columnspan=4,sticky='nsew')
    
    
# sous fonctions
def addProduct(**args):
    def add_product_fonction(*args):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        name_product = entry_name.get()
        prix_achat = entry_prix_achat.get()
        prix_vente = entry_prix_vente.get()
        quantite = entry_quantite.get()
        print(f'nom produit :{name_product}\n prix d\'achat : {prix_achat}\nprix vente : {prix_vente}\nquantite{quantite}')
        if name_product=='' and prix_achat=='' and prix_vente=="" and quantite=='':
            messagebox.showwarning('Erreur','champs de saisi invalid')
        else:
            benef = int(prix_vente) - int(prix_achat)
            stock = quantite
            try:           
                product = (cursor.lastrowid,name_product,prix_achat,prix_vente,benef,quantite,stock,username,)
                cursor.execute("INSERT INTO produits VALUES(?,?,?,?,?,?,?,?)",product)
                connection.commit()
                messagebox.showinfo('Sucsess',f'Nom produit : {name_product}\nprix d\'achat : {prix_achat}\n prix vente : {prix_vente}\nBénéfice par produit : {benef}\nquantite : {quantite}')
                
            except:
                messagebox.showerror('Erreurs','Erreurs survenu dans l\'enrégistrement de l\'utilisateur')
            finally:
                connection.close()
        
    second_window = tkinter.Toplevel(window)
    second_window.title='Ajout produits'
    win_x = 720
    win_y = 540
    screen_x = window.winfo_screenwidth()
    screen_y = window.winfo_screenheight()
    posX = (screen_x // 2) - (win_x // 2)
    posY = (screen_y // 2) - (win_y // 2)
    second_window.minsize(720,540)
    second_window.geometry(f"{win_x}x{win_y}+{posX}+{posY-35}")
    second_window.configure(bg="#f5f6f6")
    frame_second_window= tkinter.Frame(second_window,bg="#f5f6f6")
    label_add_product = tkinter.Label(frame_second_window,text='Ajout produit : ',bg="#f5f6f6",fg="#2963d6",font=('Calibri',30))
    label_name = tkinter.Label(frame_second_window,text="Nom produit: ",bg="#f5f6f6",fg="black",font=('Calibri',15))
    entry_name = tkinter.Entry(frame_second_window,font=('Calibri',15))
    label_prix_achat = tkinter.Label(frame_second_window,text="Prix unitaire d'achat : ",bg="#f5f6f6",fg="black",font=('Calibri',15))
    entry_prix_achat= tkinter.Entry(frame_second_window,font=('Calibri',15))
    label_prix_vente = tkinter.Label(frame_second_window,text="Prix unitaire de vente : ",bg="#f5f6f6",fg="black",font=('Calibri',15))
    entry_prix_vente= tkinter.Entry(frame_second_window,font=('Calibri',15))
    label_quantite = tkinter.Label(frame_second_window,text="QUANTITE : ",bg="#f5f6f6",fg="black",font=('Calibri',15))
    entry_quantite = tkinter.Entry(frame_second_window,font=('Calibri',15))
    button_add_product= tkinter.Button(frame_second_window,text="Inserer",bg="#2963d6",fg="white",font=('Calibri',15),border=0,command=add_product_fonction)
    # button_away = tkinter.Button(frame_second_window,text='j\'ai déja un compte me connecter',bg="#f5f6f6",fg="black",font=('Calibri',10),border=0,command=redirect_login)
    
    # positionnement des widgets
    frame_second_window.pack(pady=45)
    label_add_product.grid(row = 0,column=0 ,columnspan=2,pady=15)
    label_name.grid(row=1,column=0,sticky='w')
    entry_name.grid(row=1,column=1)
    label_prix_achat.grid(row=2,column=0,pady=10,sticky='w')
    entry_prix_achat.grid(row=2,column=1,pady=10)
    label_prix_vente.grid(row=3,column=0,pady=10,sticky='w')
    entry_prix_vente.grid(row=3,column=1,pady=10)
    label_quantite.grid(row=4,column=0,sticky='w')
    entry_quantite.grid(row=4,column=1)
    button_add_product.grid(row=5,column=0,columnspan=2,pady=15,ipady=2,ipadx=5)
    # button_away.grid(row=6,column=0,columnspan=5,pady=3)
# sous action modifier 
def modife_product(*args):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    second_window = tkinter.Toplevel(window)
    second_window.title='Modification produits'
    win_x = 720
    win_y = 540
    screen_x = window.winfo_screenwidth()
    screen_y = window.winfo_screenheight()
    posX = (screen_x // 2) - (win_x // 2)
    posY = (screen_y // 2) - (win_y // 2)
    second_window.minsize(720,540)
    second_window.geometry(f"{win_x}x{win_y}+{posX}+{posY-35}")
    second_window.configure(bg="#f5f6f6")
    frame_second_window= tkinter.Frame(second_window,bg="#f5f6f6")
    label_modife_product = tkinter.Label(frame_second_window,text='Ajout produit : ',bg="#f5f6f6",fg="#2963d6",font=('Calibri',30))
    label_name = tkinter.Label(frame_second_window,text="Nom produit: ",bg="#f5f6f6",fg="black",font=('Calibri',15))
    list_name = tkinter.Listbox(frame_second_window,font=('Calibri',15))
    user = (username,)
    cursor.execute('SELECT * FROM produits WHERE username=?',user)
    rows = cursor.fetchall()
    i = 0
    print(rows)
    for name_product in rows:
        i +=1
        list_name.insert(i,name_product[1])
    label_prix_achat = tkinter.Label(frame_second_window,text="Prix unitaire d'achat : ",bg="#f5f6f6",fg="black",font=('Calibri',15))
    entry_prix_achat= tkinter.Entry(frame_second_window,font=('Calibri',15))
    label_prix_vente = tkinter.Label(frame_second_window,text="Prix unitaire de vente : ",bg="#f5f6f6",fg="black",font=('Calibri',15))
    entry_prix_vente= tkinter.Entry(frame_second_window,font=('Calibri',15))
    label_quantite = tkinter.Label(frame_second_window,text="QUANTITE : ",bg="#f5f6f6",fg="black",font=('Calibri',15))
    entry_quantite = tkinter.Entry(frame_second_window,font=('Calibri',15))
    button_add_product= tkinter.Button(frame_second_window,text="Inserer",bg="#2963d6",fg="white",font=('Calibri',15),border=0)
        
    # positionnement des widgets
    frame_second_window.pack(pady=45)
    label_modife_product.grid(row = 0,column=0 ,columnspan=2,pady=15)
    label_name.grid(row=1,column=0,sticky='w')
    list_name.grid(row=1,column=1)
    label_prix_achat.grid(row=2,column=0,pady=10,sticky='w')
    entry_prix_achat.grid(row=2,column=1,pady=10)
    label_prix_vente.grid(row=3,column=0,pady=10,sticky='w')
    entry_prix_vente.grid(row=3,column=1,pady=10)
    label_quantite.grid(row=4,column=0,sticky='w')
    entry_quantite.grid(row=4,column=1)
    button_add_product.grid(row=5,column=0,columnspan=2,pady=15,ipady=2,ipadx=5)
    # button_away.grid(row=6,column=0,columnspan=5,pady=3)
     

    
# partie lien de navigation
frame = tkinter.Frame(window,bg='#2963d6')
label_ets = tkinter.Label(frame,text=ets,bg="#2963d6",fg="white",font=('arial',10))
label_title = tkinter.Label(frame,text="Mon Compable",bg="white",fg="#2963d6",font=('Calibri',16),width=15)
label_user = tkinter.Label(frame,text='Utilisateur',bg="#2963d6",fg="white",font=('Calibri',16))
label_vente = tkinter.Label(frame,text='Vente',bg="#2963d6",fg="white",font=('Calibri',16))
label_stock = tkinter.Label(frame,text='Stock',bg="#2963d6",fg="white",font=('Calibri',16))
label_caisse = tkinter.Label(frame,text='Caisse',bg="#2963d6",fg="white",font=('Calibri',16))
label_rapport = tkinter.Label(frame,text='Rapport',bg="#2963d6",fg="white",font=('Calibri',16))
label_out = tkinter.Label(frame,text='Quitter',bg="#2963d6",fg="white",font=('Calibri',16))


frame2 = tkinter.Frame(window,bg='#fff')

frame2.columnconfigure(0,weight=50)
frame2.columnconfigure(1,weight=50)
frame2.columnconfigure(2,weight=50)
frame2.columnconfigure(3,weight=50)
# frame2.columnconfigure(4,weight=50)

# frame2.rowconfigure(0,weight=5)
# frame2.rowconfigure(1,weight=5)
# frame2.rowconfigure(2,weight=5)
# frame2.rowconfigure(3,weight=5)
# frame2.rowconfigure(4,weight=5)
# frame2.rowconfigure(5,weight=5)
# frame2.rowconfigure(6,weight=5)
# frame2.rowconfigure(7,weight=5)
# frame2.rowconfigure(8,weight=5)


# fonctions pour ouvrir les les options
def open_user_option(*args):
    for lbl in labels:
        lbl.config(font=('calibri',16))
    label_user.config(font=('Calibri',16,'underline'))
    
def open_vente_option(*args):
    vente_show()
    for lbl in labels:
        lbl.config(font=('calibri',16))
    label_vente.config(font=('Calibri',16,'underline'))
    
def open_stock_option(*args):
    stock_show()
    for lbl in labels:
        lbl.config(font=('calibri',16))
    label_stock.config(font=('Calibri',16,'underline'))
def open_caisse_option(*args):
    for lbl in labels:
        lbl.config(font=('calibri',16))
    label_caisse.config(font=('Calibri',16,'underline'))
def open_rapport_option(*args):
    for lbl in labels:
        lbl.config(font=('calibri',16))
    label_rapport.config(font=('Calibri',16,'underline'))
def open_out_option(*args):
    for lbl in labels:
        lbl.config(font=('calibri',16))
    label_out.config(font=('Calibri',16,'underline'))
    
labels = [] 
labels = [label_user,label_vente,label_stock,label_caisse,label_rapport,label_out]

label_user.bind('<Button-1>',open_user_option)
# label_user.bind('<Button-1>',user_show)
label_vente.bind('<Button-1>',open_vente_option)
label_stock.bind('<Button-1>',open_stock_option)
label_caisse.bind('<Button-1>',open_caisse_option)
label_rapport.bind('<Button-1>',open_rapport_option)
label_out.bind('<Button-1>',open_out_option)


# foncion 
# affichage des widgets
frame2.grid(row=0,column=2,columnspan=2,sticky="nsew")
frame.grid(row=0,column=0,sticky="nsew")
label_ets.grid(row=0,column= 0,sticky='w',pady=10,ipadx=15)
label_title.grid(row=1,column= 0,sticky='w',ipady=10,ipadx=15)
label_user.grid(row=2,column= 0,sticky='w',ipady=10,ipadx=15)
label_vente.grid(row=3,column= 0,sticky='w',ipady=10,ipadx=15)
label_stock.grid(row=4,column= 0,sticky='w',ipady=10,ipadx=15)
label_caisse.grid(row=5,column= 0,sticky='w',ipady=10,ipadx=15)
label_rapport.grid(row=6,column= 0,sticky='w',ipady=10,ipadx=15)
label_out.grid(row=7,column= 0,sticky='w',ipady=10,ipadx=15)

# window.configure(menu=main_menu)

window.mainloop()