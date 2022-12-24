import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import pickle as pk
from random import randrange
import time


#Définition des Utilitaires 
def ecrire(doc, titre_doc):
    lien = "{}".format(titre_doc)
    with open(lien, 'wb') as recap:
        donnees = pk.Pickler(recap)
        donnees.dump(doc)
        donnees.dump("\n")
    return doc

def lire(doc, titre_cible):
    lien = "{}".format(titre_cible)
    with open(lien, 'rb') as sta:
        donnees = pk.Unpickler(sta)
        doc = donnees.load()
    return doc

#Définitions des images utilisées
lien_absolu = os.path.abspath(__file__)
direction_vers_le_dossier = os.path.dirname(lien_absolu)
os.chdir(direction_vers_le_dossier)
lien_font_page = "font.png"
lien_ico = ""

#Définition des variable utilisées
temps_select = 0
liste_img = []
list_lien = []
dico_temps = {"15 Secondes":15,"30 Secondes": 30,"45 Secondes":45,"1 Minute":60,"1 Minute et 15 secondes":75,"1 Minute et 30 secondes":90}
liste_temps = ["15 Secondes","30 Secondes","45 Secondes","1 Minute","1 Minute et 15 secondes","1 Minute et 30 secondes"]

#Creer la fenetre d'init
fenetre_acceuil = Tk()

#Personnaliser la fenêtre
fenetre_acceuil.title("Configuration du Diaporama Infini")
w, h = fenetre_acceuil.winfo_screenwidth(), fenetre_acceuil.winfo_screenheight()
fenetre_acceuil.iconbitmap("logo.ico")
fenetre_acceuil.geometry("%dx%d+0+0" % (w, h))
fenetre_acceuil.minsize(width=w,height=h)
fenetre_acceuil.maxsize(width=w,height=h)
fenetre_acceuil.configure(background='#224466')

#Reparamètrage à partir des dimensions de l'image (Fond d'écran)
img = PhotoImage(file=lien_font_page)
w = img.width()
h = img.height()

#Création du Canvas
can_configuration = Canvas(fenetre_acceuil, width=w, height=h, bg='black')
can_configuration.create_image(0,0, anchor=NW, image=img)
can_configuration.place(x=0, y=0, relwidth=1, relheight=1)

#Récupération de la liste de lien des images
try: 
    liste_img = lire(liste_img,'liste_img')
except FileNotFoundError or OSError:
    liste_img = []

#Suppression des temps précédents
try:
    os.remove('temps_select')
except FileNotFoundError:
    pass

#Label d'information 1
titre1 = Label(can_configuration,text="Bienvenue sur le programme de Diaporama Infini V1", font=("Courrier",50), width=40, bg='black', fg='blue2',relief=SUNKEN)
titre1.pack(pady=10, fill=X, side=TOP)
can_configuration.create_window(w/2,100, window=titre1)

#Label d'information 2
titre2 = Label(can_configuration, text="Initialisez la liste de lien d'image à traiter :", font=("Courrier", 30), bg='black', fg='blue2',relief=SUNKEN)
titre2.pack(pady=10)
can_configuration.create_window(w/2,200, window=titre2)

#Label d'information ListBox
titre_list = Label(can_configuration, text="Combien de temps voulez-vous que dure l'affichage des images: ", font=("Courrier", 20), bg='black', fg='blue2',relief=SUNKEN)
titre_list.pack(pady=10)
can_configuration.create_window(w/2,275, window=titre_list)

#Création de la Listbox
list_principal = Listbox(can_configuration, font=("Courrier",30),  bg='black', fg='blue2',height=2, activestyle='dotbox',selectbackground='deepskyblue2', selectforeground='#224466',relief=SUNKEN)
list_principal.pack(pady=10)
can_configuration.create_window(w/2,350, window=list_principal)

#Ajout de la Scollbar vertical
scrollbarV = Scrollbar(can_configuration,orient='vertical')
scrollbarV.pack(side=RIGHT, fill=BOTH)
can_configuration.create_window(w-730,350, window=scrollbarV,height=90)

#Ajout des variables
pas = 0
for pas in range(len(liste_temps)):
    list_principal.insert(pas,liste_temps[pas])
    pas += 1 
list_principal.config(yscrollcommand = scrollbarV.set)
scrollbarV.config(command = list_principal.yview)

#Label d'information 3
titre2 = Label(can_configuration, text="Choisir les images à utilisées:", font=("Courrier", 20), bg='black', fg='deepskyblue2',relief=SUNKEN)
titre2.pack(pady=10)
can_configuration.create_window(w/2-750,475, window=titre2)

#Fonction du bouton de recherche d'image à traité
def img_tracker():
    liste_img = []
    img_attente = ""
    try: 
        liste_img = lire(liste_img,'liste_img')
    except FileNotFoundError or OSError:
        liste_img = []
    if liste_img == []:
        showinfo(title="Information",message="Vous n'avez pas encore mis de lien d'image")  
        img_attente = askopenfilename(title="Recherche d'Image à ajouter",filetypes=[("Fichier en .PNG",".png")])
        testlien = os.path.exists(img_attente)
        if testlien == True: #Lorsque le lien est bon
            showinfo(title="Information",message="Votre lien est bon")
            liste_img.append(img_attente)
            ecrire(liste_img,'liste_img')
            showinfo(title="Information",message="Votre lien est enregistré")
            list_lien.delete(0,END)
            pas = 0
            for pas in range(len(liste_img)):
                list_lien.insert(pas,liste_img[pas])
                pas += 1 
            list_lien.config(yscrollcommand = scrollbarV_lien.set)
            scrollbarV_lien.config(command = list_lien.yview)
            list_lien.configure(height=4)
        else:
            showinfo(title="Information",message="Votre lien n'est pas bon")
            return
    else:
        verif_ouverture = askyesno(title="Message",message="Voulez-vous enregistré un nouveau lien?")
        if verif_ouverture == True:
            img_attente = askopenfilename(title="Recherche d'Image à ajouter",filetypes=[("Fichier en .PNG",".png")])
            testlien = os.path.exists(img_attente)
            if testlien == True: #Lorsque le lien est bon
                showinfo(title="Information",message="Votre lien est bon")
                #Verif que le lien img en attente ne soit pas deja dans la liste
                liste_img.append(img_attente)
                ecrire(liste_img,'liste_img')
                showinfo(title="Information",message="Votre lien est enregistré")
                list_lien.delete(0,END)
                pas = 0
                for pas in range(len(liste_img)):
                    list_lien.insert(pas,liste_img[pas])
                    pas += 1 
                list_lien.config(yscrollcommand = scrollbarV_lien.set)
                scrollbarV_lien.config(command = list_lien.yview)
                list_lien.configure(height=4)
            else:
                showinfo(title="Information",message="Votre lien n'est pas bon")
                return

#Bouton de paramétrage de fichier à traiter
but_lien = Button(can_configuration, text="Ajoutez un lien dans la liste", font=("Courrier", 15),
bg='gray', fg='deepskyblue2', command=img_tracker)
but_lien.pack(pady=10)
can_configuration.create_window(w/2-750,550, window=but_lien)

#Label d'information ListBox des lien enregistrés
titre_list_lien = Label(can_configuration, text="Les liens déjà enregistrés: ", font=("Courrier", 20), bg='black', fg='gray',relief=SUNKEN)
titre_list_lien.pack(pady=10)
can_configuration.create_window(w/2,455, window=titre_list_lien)

#Création de la Listbox des liens enregistrés
list_lien = Listbox(can_configuration, font=("Courrier",30),  bg='black', fg='gray',height=2, activestyle='dotbox',selectbackground='gray', selectforeground='deepskyblue2',relief=SUNKEN)
list_lien.pack(pady=10)
can_configuration.create_window(w/2+20,600,width=1220, window=list_lien)

#Ajout de la Scollbar vertical pour la liste des liens
scrollbarV_lien = Scrollbar(can_configuration,orient='vertical')
scrollbarV_lien.pack(side=RIGHT, fill=BOTH)
can_configuration.create_window(w-340,600, window=scrollbarV_lien,height=190)

#Ajout de la Scollbar horizontal pour la liste des liens
scrollbarH_lien = Scrollbar(can_configuration,orient='horizontal')
scrollbarH_lien.pack(side=RIGHT, fill=BOTH)
can_configuration.create_window(w-340,600, window=scrollbarH_lien,height=190)

#Ajout des variables de la liste des liens
if liste_img == []:
    can_configuration.create_window(w-340,550, window=scrollbarV_lien,height=7)
    list_lien.insert(0,"(vide)")
    list_lien.configure(height=1)
else:
    can_configuration.create_window(w-340,602, window=scrollbarV_lien,height=190)
    list_lien.delete(0,END)
    pas = 0
    for pas in range(len(liste_img)):
        list_lien.insert(pas,liste_img[pas])
        pas += 1 
    list_lien.config(yscrollcommand = scrollbarV_lien.set)
    scrollbarV_lien.config(command = list_lien.yview)
    list_lien.configure(height=4)

#Ajout des variables de la liste des liens
if liste_img == []:
    can_configuration.create_window(w/2+10,700, window=scrollbarH_lien,height=10,width=110)
    list_lien.configure(height=1)
else:
    can_configuration.create_window(w/2+10,700, window=scrollbarH_lien,height=10,width=1200)
    list_lien.config(xscrollcommand = scrollbarH_lien.set)
    scrollbarH_lien.config(command = list_lien.xview)
    list_lien.configure(height=4)

#Fonction du bouton pour supprimer un lien
def sup_tracker():
    selection = ""
    liste_img = []
    try: 
        liste_img = lire(liste_img,'liste_img')
    except FileNotFoundError or OSError:
        liste_img = []
    if liste_img == []:
        showinfo(title="Information",message="Vous n'avez pas de lien enregistrés,\nSuppression impossible")
        return
    else:
        for i in list_lien.curselection():
            selection = list_lien.get(i)      
        if selection == "":
            showinfo(title="Information",message="Vous n'avez pas de séléctionné de lien,\nSuppression impossible")
            return
        else:
            verif_suppression = askyesno(title="Message",message="Vous avez séléctionné: '{}',\nSouhaitez-vous le supprimer définitivement de la liste de lien".format(selection))
            if verif_suppression == True:
                if selection in liste_img:
                    element_sup = liste_img.index(selection)
                    del liste_img[element_sup]
                else:
                    showinfo(title="Information",message="L'élément séléctionné est intraitable,\nSuppression impossible")
                    return
                ecrire(liste_img,'liste_img')
                showinfo(title="Information",message="Votre lien est supprimé")
                list_lien.delete(0,END)
                pas = 0
                for pas in range(len(liste_img)):
                    list_lien.insert(pas,liste_img[pas])
                    pas += 1 
                list_lien.config(yscrollcommand = scrollbarV_lien.set)
                scrollbarV_lien.config(command = list_lien.yview)
                list_lien.configure(height=4)
            else:
                showinfo(title="Information",message="Suppression annulé")
                return

#Bouton de suppression
but_sup = Button(can_configuration, text="Supprimez un lien dans la liste", font=("Courrier", 15),
bg='gray', fg='deepskyblue2', command=sup_tracker)
but_sup.pack(pady=10)
can_configuration.create_window(w/2-750,650, window=but_sup)      

def diapo_infinity():
    selection_temps = ""
    liste_img = []
    try: 
        liste_img = lire(liste_img,'liste_img')
    except FileNotFoundError or OSError:
        liste_img = []
    if liste_img == []:
        showinfo(title="Information",message="Vous n'avez pas de lien enregistrés,\nLancement impossible")
        try:
            os.remove('temps_select')
        except FileNotFoundError:
            pass
        return
    else:#On as les images de chargées
        for time in list_principal.curselection():
            selection_temps = list_principal.get(time)      
        if selection_temps == "":
            showinfo(title="Information",message="Vous n'avez pas de séléctionné de temps,\nLancement impossible")
            return
        else:#On as séléctionner un temps de durée des images
            verif_lancement = askyesno(title="Lancement",message="Vous avez séléctionné le temps de durée: '{}',\nEtes-vous sûr de vouloir lancé le programme avec ces paramètres?".format(selection_temps))    
            if verif_lancement== True:
                temps_select = dico_temps.get(selection_temps)
                ecrire(temps_select,'temps_select')
                showinfo(title="Information",message="Vous avez séléctionné de temps de '{}',\nLancement de l'application".format(selection_temps))
                fenetre_acceuil.destroy()
            else:
                showinfo(title="Information",message="L'élément séléctionné est intraitable,\nLancement impossible")
                try:
                    os.remove('temps_select')
                except FileNotFoundError:
                    pass
                return

#Bouton de lancement
but_sup = Button(can_configuration, text="Lancer le Diaporama avec ces Paramètres", font=("Time new roman", 35),
bg='RoyalBlue3', fg='deepskyblue2', command=diapo_infinity)
but_sup.pack(pady=10)
can_configuration.create_window(w/2,800, window=but_sup)  

#Fonction pour l'horloge
def display_t():
    heure = time.strftime('%H:%M:%S %p')
    horloge.config(text=heure)
    horloge.after(100,display_t)

#Horloge
horloge = Label(can_configuration, font=("Time new roman",35,'bold'),bg='gray', fg='#224466')
horloge.pack(pady=10)
can_configuration.create_window(w/2,900, window=horloge)
display_t()

fenetre_acceuil.mainloop()

try:#On verifie que la liste de temps ne soit pas vide
    temps_select = lire(temps_select,'temps_select')     
except FileNotFoundError or OSError:
    temps_select = 0
if temps_select == 0:
    pass
else:
    try: 
        liste_img = lire(liste_img,'liste_img')
    except FileNotFoundError or OSError:
        liste_img = []
    if liste_img == []:
        pass
    else:
        fenetre_diapo_inf = Tk()
        #Personnaliser la fenêtre
        fenetre_diapo_inf.title("Diaporama Infini")
        w, h = fenetre_diapo_inf.winfo_screenwidth(), fenetre_diapo_inf.winfo_screenheight()
        fenetre_diapo_inf.iconbitmap("logo.ico")
        fenetre_diapo_inf.geometry("%dx%d+0+0" % (w, h))
        fenetre_diapo_inf.minsize(width=w,height=h)
        fenetre_diapo_inf.configure(background="black")

        condition = True
        def change_img():
            if condition:
                liste_max = len(liste_img)
                try:
                    liste_random = randrange(liste_max)
                except ValueError:
                    liste_random = 0
                choix = liste_img[liste_random]
                img_random = PhotoImage(file=choix)
                w_imgt = img_random.width()
                h_imgt = img_random.height()
                if w_imgt == w and h_imgt == h:
                    can_infinity.config(image=img_random)
                    can_infinity.image = img_random
                    can_infinity.after(temps_select*1000, change_img)
                elif w_imgt > w and h_imgt > h:
                    img_resized = img_random.resize(w_imgt,h_imgt)
                    can_infinity.config(image=img_resized)
                    can_infinity.image = img_resized
                    can_infinity.after(temps_select*1000, change_img)
                elif w_imgt < w and h_imgt < h:
                    can_infinity.config(image=img_random, anchor=CENTER)
                    can_infinity.image = img_random
                    can_infinity.after(temps_select*1000, change_img)

        #Il manque à centré les images trop petite et redimentionné les images trop grandes
        can_infinity = Label(fenetre_diapo_inf, width=w, height=h, bg="black")
        can_infinity.pack()
        change_img()
        fenetre_diapo_inf.mainloop()
    




