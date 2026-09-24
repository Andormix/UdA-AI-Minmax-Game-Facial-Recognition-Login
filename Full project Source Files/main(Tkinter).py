###########################################################################################################
#                                                                                                         #
#                                           LLIBRERIES                                                    #
#                                                                                                         #
###########################################################################################################

import mysql.connector
from tkinter import *
from tkinter import messagebox as msg 

## Llibreries pròpies ##
import MenusJoc
import ReconeixementFacial

###########################################################################################################
#                                                                                                         #
#                                           FUNCIONS                                                      #
#                                                                                                         #
###########################################################################################################

# Crea un espai en Tkinter windows
def espacio(screen):
    Label(screen, text="", bg=Background).pack()

# Elimina una window Tkinder
def eliminarWindow(window):
    window.destroy()

# Inicia el Menu del joc amb usuari "Desconegut"
def iniciDesconegut(window, mydb, mycursor):

    eliminarWindow(window)
    MenusJoc.menuPrincipal("Desconegut", mycursor, mydb, False)
    primeraWindow(mydb, mycursor)
    
# Obre la window per fer el reconeixement facial
def windowLoginConReconFacial(mydb, mycursor, window):

    window2 = Toplevel(window)

    window2.title("INICI DE SESSIÓ")
    window2.geometry("500x300")
    window2.configure(bg=Background)

    Label(window2, text= "INICI DE SESSIÓ", fg=Blanc, bg=Negre, font=(Fuente, 18), width="500", height="2").pack()
    espacio(window2)
    Label(window2, text="Usuario:", fg=Blanc, bg=Background, font=(Fuente, 12)).pack()

    entry = Entry(window2, justify=CENTER, font=(Fuente, 12))
    entry.focus_force()
    entry.pack(side=TOP, ipadx=30, ipady=6)

    button = Button(window2, text="Iniciar sessió", fg=Blanc, bg=Gris, activebackground=Background, borderwidth=0, font=(Fuente, 14), height="2", width="22",
    command = lambda: iniciaJocSiLogin(entry.get(), window2, mydb, mycursor, window))
    button.place(x = 125, y = 175)

# Efectua el reconeixement facial
def iniciaJocSiLogin(Nick, window2, mydb, mycursor, window):

    mycursor.execute("select NICK from Usuaris WHERE NICK = %s", (Nick,) )

    res = mycursor.fetchone()

    mycursor.execute("select NICK from Administrador WHERE NICK = %s", (Nick,) )
    admin = mycursor.fetchone()
    

    if res is None:
        
        textoEnWindow(window2, "L'usuari no existeix!", 1)
        print("     - L'usuari no existeix, comprovi que el Nick és correcte! ")
        print()

    else:

        textoEnWindow(window2, "Loading Data Credentials...", 1)
        print("     - Loading Data Credentials... Please Wait.")
        ReconeixementFacial.Load_MYSQL_Dataset(mycursor)
        print("     - Loading Done.")
        print()
        print("     - Creating YML... Please Wait.")
        ReconeixementFacial.Crear_YML()
        print("     - YML Created.")
        print()
        print("     - Starting facial recognition. Please wait.")
        print()
        Verificacio = ReconeixementFacial.reconeixement_facial(Nick)

        if Verificacio and admin is not None:

            eliminarWindow(window2)
            eliminarWindow(window)

            MenusJoc.menuPrincipal(Nick, mycursor, mydb, True)

            primeraWindow(mycursor, mydb)

        elif Verificacio:

            eliminarWindow(window2)
            eliminarWindow(window)

            MenusJoc.menuPrincipal(Nick, mycursor, mydb, False)

            primeraWindow(mycursor, mydb)      

# Obre la primera window del programa on estan les opcions de registre i el login
def primeraWindow(mydb, mycursor):
    
    window = Tk()
    window.geometry("600x450")
    window.title("SPLATOON")
    window.configure(bg= Background)

    # BOTONS I ETIQUETES #
    Label(text="SPLATOON V2", fg=Blanc, bg=Negre, font=(Fuente, 18), width="500", height="2").pack()
    espacio(window)
    espacio(window)
    Button(text="Iniciar sessió", fg=Blanc, bg=Gris, activebackground=Background, borderwidth=0, font=(Fuente, 14), height="2", width="40", command = lambda: windowLoginConReconFacial(mydb, mycursor, window)).pack()
    espacio(window)
    Button(text="Registrarse", fg=Blanc, bg=Gris, activebackground=Background, borderwidth=0, font=(Fuente, 14), height="2", width="40", command = lambda: windowRegistreUsuari(mydb, mycursor, window)).pack()
    espacio(window)
    Button(text="Mode desconegut", fg=Blanc, bg=Gris, activebackground=Background, borderwidth=0, font=(Fuente, 14), height="2", width="40", command  = lambda: iniciDesconegut(window, mydb, mycursor)).pack()
    espacio(window)
    Button(text="Sortir", fg=Blanc, bg=Gris, activebackground=Background, borderwidth=0, font=(Fuente, 14), height="2", width="40", command =lambda: eliminarWindow(window)).pack()
    window.mainloop()

# Obre la windo pel registre d'un nou usuari
def windowRegistreUsuari(mydb, mycursor, window):
    
    window2 = Toplevel(window)

    window2.title("REGISTRE D'USUARI")
    window2.geometry("500x400")
    window2.configure(bg=Background)

    Label(window2, text= "REGISTRE D'USUARI", fg=Blanc, bg=Negre, font=(Fuente, 18), width="500", height="2").pack()
    espacio(window2)

    Label(window2, text="Usuari: ", fg=Blanc, bg=Background, font=(Fuente, 12)).pack()
    entry = Entry(window2, justify=CENTER, font=(Fuente, 12))
    entry.focus_force()
    entry.pack(side=TOP, ipadx=30, ipady=6)

    Label(window2, text="Nick:", fg=Blanc, bg=Background, font=(Fuente, 12)).pack()
    entry2 = Entry(window2, justify=CENTER, font=(Fuente, 12))
    entry2.focus_force()
    entry2.pack(side=TOP, ipadx=30, ipady=6)

    button = Button(window2, text="COMENÇAR REGISTRE FACIAL", fg=Blanc, bg=Gris, activebackground=Background, borderwidth=0, font=(Fuente, 14), height="2", width="30",
    command = lambda: registraUsuariSiCorrecte(entry.get(), entry2.get(), window2, mydb, mycursor, window))
    button.place(x = 75, y = 250)
    print()

# Escriu texte en la part baixa de les windows
def textoEnWindow(window, text, flag):

    if flag:

        Lower_left = Label(window, text=text, fg=Blanc, bg=Background, font=(Fuente, 12))
        Lower_left.place(relx=.5, rely=.95, anchor ='center')
    else:

        Lower_left = Label(window, text=text, fg=Blanc, bg=Background, font=(Fuente, 12))
        Lower_left.place(relx=.5, rely=.95, anchor ='sw')

def registraUsuariSiCorrecte(NomComplet, Nick, window2, mydb, mycursor, window):

    NomCompletDividit = NomComplet.split()

    if len(NomCompletDividit) == 0:

        textoEnWindow(window2, "Falta el nom complet", 1)

    elif len(NomCompletDividit) == 1:

        textoEnWindow(window2, "Falten els cognoms!", 1)

    elif len(NomCompletDividit) == 2:

        textoEnWindow(window2, "Falta el segon cognom!", 1)

    elif Nick == "":

        textoEnWindow(window2, "Falta el Nick", 1)

    else:

        mycursor.execute("select NICK from Usuaris WHERE NICK = %s", (Nick,) )
        res = mycursor.fetchone()
        
        if res is None:  # Evitem BUG:06 Duplicats

            
            mycursor.execute("insert into Usuaris(NICK, Nom_Usuari, Cognom1, Cognom2)  values(%s, %s, %s, %s)", (Nick, NomCompletDividit[0], NomCompletDividit[1], NomCompletDividit[2]))
            mydb.commit() 

            mycursor.execute("insert into Players(NICK, Info)  values(%s, %s)", (Nick, 'Player Info'))
            mydb.commit() 

            ReconeixementFacial.Crear_perfil(mycursor, mydb, Nick)

            print(" - Registre completat mab èxit!")
            print()
            eliminarWindow(window2)

        else:

            textoEnWindow(window2, "L'usuari ja existeix!", 1)
        


###########################################################################################################
#                                                                                                         #
#                                     INICI DEL PROGRAMA                                                  #
#                                                                                                         #
###########################################################################################################

## DEFINICIÓ DELS COLORS TKINTER ##

Blanc = "#f4f5f4"
Negre = "#101010"
Gris = "#202020"
Background = "#151515"
Fuente = "Century Gothic"

## CONEXIÓ A LA NOSTRA BD EN EL SERVIDOR ANDROMEDA ##

mydb = mysql.connector.connect(
host="192.168.3.10",
user="terict",          
# password='terict',    #SENSE PASSWORD
database='tericttest' 
)

mycursor = mydb.cursor()
primeraWindow(mydb, mycursor)
