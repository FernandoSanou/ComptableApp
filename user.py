def user(): 
    name = f'Identifiant : {username}'
    fonction = f'Fonction : {role}'
    work = f'Lieu de travail : {ets}'
    label_show_title = tkinter.Label(frame2,text="Utilisateur : ",bg="#fff",fg="#2963d6",font=('calibri',16))
    label_show_title.grid(row=0 ,column=0,columnspan=2,sticky='nw')
    
    label_show_username = tkinter.Label(frame2,text=name,bg="#fff",fg="#555",font=('calibri',13))
    label_show_username.grid(row=1 ,column=0,columnspan=2,sticky='ne')
    
    label_show_role = tkinter.Label(frame2,text=fonction,bg="#fff",fg="#555",font=('calibri',13))
    label_show_role.grid(row=2 ,column=0,columnspan=2,sticky='ne')
    
    label_show_ets = tkinter.Label(frame2,text=work,bg="#fff",fg="#555",font=('calibri',13))
    label_show_ets.grid(row=3 ,column=0,columnspan=2,sticky='ne')