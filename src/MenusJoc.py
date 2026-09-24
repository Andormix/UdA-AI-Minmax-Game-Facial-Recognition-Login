###########################################################################################################
#                                                                                                         #
#                                           LLIBRERIES                                                    #
#                                                                                                         #
###########################################################################################################

import numpy as np
import pygame
from pygame import mixer 
import os

## Llibreries pròpies ##
import TADS
import Constants
import LògicaJoc


#######################################
#                                     #
#           MENU   + PART SQL         #
#                                     #
#######################################

def menuPrincipal(Nick_Usuari, mycursor, mydb, Admin):

    pygame.init()
    dirname = os.path.dirname(__file__)  # Les imatges les he ficat a una subcarpeta per temes d'organització
    mixer.music.load(os.path.join(dirname,'audio\\Loop.wav'))
    mixer.music.play(-1)                    # (-1) indica play on loop

    Part = TADS.Partida() # Declaració de partida
    Continuar = True

    while (Continuar):
        
        print()
        print("######################################################################################")
        print("#                                                                                    #")
        print(" #                                  SPLATOON                                        #")
        print("#                                                                                    #")
        print("######################################################################################")
        print("#                                                                                    #")
        print("      Benvingut: " + Nick_Usuari)
        print("#                                                                                    #")
        print("#     1.  Mode Fàcil                                                                 #")
        print("#     2.  Mode Normal                                                                #")
        print("#     3.  Mode Dificil                                                               #")
        print("#     4.  Mode Programador                                                           #")
        print("#     5.  Modo Dios            (Triga varis minuts)                                  #")
        print("#     6.  Visualitzar Historic de moviments de la partida anterior (Punters)         #")
        print("#     7.  Visualitzar TOP 10 JUGADES   (Query SQL)                                   #")
        print("#     8.  Visualitzar TOP 5 JUGADORS   (Query SQL)                                   #")
        print("#     9.  Visualitzar una partia amb ID   (MariDB - Andromeda)                       #")
        print("#     10. Sortir                                                                     #")
        print("#                                                                                    #")

        if Admin: 
            print("######################################################################################")
            print("#                                                                                    #")
            print("#     11.  Menú administrador                                                        #")

        print("#                                                                                    #")
        print("######################################################################################")
        print()

        opcio = int(input("     - Selecciona una opció: "))
        print()

        if opcio == 7:

            print("######################################################################################")
            print("#                                                                                    #")
            print(" #                                  SCOREBOARD                                      #")
            print("#                                                                                    #")
            print("######################################################################################")
            print()

            mycursor.execute("""SELECT NICK, PUNTUACIO, ID_NIVELL, ID_PARTIDA FROM Partides WHERE PUNTUACIO > 0 ORDER BY 3 DESC, 2 DESC, 1, 4 DESC LIMIT 10 """)
            myresult = mycursor.fetchall()

            for partida in myresult:
                print("         ID: " + str(partida[3]) + "      Puntuació: " + str(partida[1]) + "      Nivell: " + str(partida[2]) +"     + jugador: " + partida[0], )
            
            print()
            input("     - Pesione ENTER para continuar ")
            print()

        elif opcio == 8:

            print("######################################################################################")
            print("#                                                                                    #")
            print(" #                              TOP 5 JUGADORS                                      #")
            print("#                                                                                    #")
            print("######################################################################################")
            print()

            mycursor.execute("""SELECT NICK, ID_NIVELL, MAX(PUNTUACIO) FROM Partides WHERE ID_PARTIDA IN

                                (SELECT ID_PARTIDA FROM Partides WHERE (NICK, ID_NIVELL) IN 
                                (SELECT NICK, MAX(ID_NIVELL) FROM Partides 	WHERE PUNTUACIO > 0 GROUP BY NICK) 
                                AND PUNTUACIO > 0) 

                                GROUP BY NICK ORDER BY 2 DESC, 3 DESC""")

            myresult = mycursor.fetchall()

            for partida in myresult:
                print("      Puntuació: " + str(partida[2]) + "      Nivell: " + str(partida[1]) +"     + jugador: " + partida[0], )
            
            print()
            input("     - Pesione ENTER para continuar ")
            print()

        elif opcio == 10:

            Continuar = False
            break

        elif opcio == 11 and Admin:

            menuAdministrador(mycursor, mydb)

        elif opcio < 1 or opcio > 10:

            print(" - Opcio incorrecta, provi de nou")

        else:
            
            # Generem la partida (+ Moviments) que hem d'emmagatzemar en la BD
            Part = executarOpcio(opcio, mycursor, Nick_Usuari, Part)

            if 0 < opcio < 6:
            
                mycursor.execute("insert into Partides(NICK, ID_NIVELL, PUNTUACIO) values(%s, %s, %s)", (Nick_Usuari, int(Part.ID_Nivell), int(Part.Puntuacio),))
                mydb.commit() 

                mycursor.execute('select MAX(ID_PARTIDA) from Partides')
                myresult = mycursor.fetchone()
                ID_Partida = myresult[0]

                print("----------------------------------")
                print("+ Partida inserida en MariaDB")
                print("- ID_PARTIDA: " + str(ID_Partida))
                print("- NICK: " + Nick_Usuari)
                print("- ID_NIVELL: " + str(int(Part.ID_Nivell)))
                print("- PUNTUACIÓ: " + str(int(Part.Puntuacio)))
                print("----------------------------------")

                x = TADS.Inici(Part.LlistaMoviments)

                # Itera tots els moviments de la partida fins arribar al resultat final.
                while x != TADS.Fi(Part.LlistaMoviments):

                    mapa = str((Part.LlistaMoviments.MEMO[x].Estat).tolist())

                    mycursor.execute( # Insireix totes les dades del Moviment
                        """insert into Moviments(Num, Turn, PuntsIA, PuntsPlayer, CasellesIA, CasellesPlayer, 
                        GuanyaIA, GuanyaPLAYER, Taules, OfegamentIA, OfegamentPLAYER, ID_PARTIDA, Estat) 
                        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(

                        Part.LlistaMoviments.MEMO[x].ID,      
                        Part.LlistaMoviments.MEMO[x].Turn, 

                        int(Part.LlistaMoviments.MEMO[x].PuntsIA), 
                        int(Part.LlistaMoviments.MEMO[x].PuntsPlayer), 

                        Part.LlistaMoviments.MEMO[x].CasellesIA, 
                        Part.LlistaMoviments.MEMO[x].CasellesPlayer,

                        Part.LlistaMoviments.MEMO[x].GuanyaIA, 
                        Part.LlistaMoviments.MEMO[x].GuanyaPLAYER, 

                        Part.LlistaMoviments.MEMO[x].Taules, 
                        Part.LlistaMoviments.MEMO[x].OfegamentIA, 
                        Part.LlistaMoviments.MEMO[x].OfegamentPLAYER,
                        
                        ID_Partida,
                        mapa))
                    mydb.commit() 
                        
                    x = TADS.Seguent(Part.LlistaMoviments, x)

                    pygame.init()
                    mixer.music.load(os.path.join(dirname,'audio\\Loop.wav'))
                    mixer.music.play(-1)                    # (-1) indica play on loop
    pygame.quit()

def executarOpcio(Opcio, mycursor, Nick_Usuari, Part):


    if 0 < Opcio < 6:   # Genera una partida nova

        Part = TADS.Partida()
        Part = TADS.CrearPartida(Part, Constants.MAX_JUGADES)

    if Opcio == 1:

        Part = LògicaJoc.joc(1, Part)
        Part.ID_Nivell = 1
        print()

    elif Opcio == 2:

        Part = LògicaJoc.joc(2, Part)
        Part.ID_Nivell = 2
        print()

    elif Opcio == 3:

        Part = LògicaJoc.joc(3, Part)
        Part.ID_Nivell = 3
        print()

    elif Opcio == 4:

        Part = LògicaJoc.joc(4, Part)
        Part.ID_Nivell = 4
        print()
    
    elif Opcio == 5:

        Part = LògicaJoc.joc(4, Part)
        Part.ID_Nivell = 4
        print()
        

    elif Opcio == 6:


        print("######################################################################################")
        print("#                                                                                    #")
        print(" #                  HISTORIAL MOVIMENTS (VISUALITZA TAD MOVIMENT)                    #")
        print("#                                                                                    #")
        print("######################################################################################")

        if TADS.LlistaBuida(Part.LlistaMoviments):

            print()
            print(" - Has de jugar primer! ")
            print()

        else:
            x = TADS.Inici(Part.LlistaMoviments)   # Itera tots els moviments de la partida generada

            while x != TADS.Fi(Part.LlistaMoviments):

                print()
                print("# PUNTER A TAD MOVIMENT (ELEMENT), POS " + str(x) + " EN LOE DINTRE DEL TAD PARTIDA #")
                print()

                TADS.ImprimeixMoviment(Part.LlistaMoviments, x)
                x = TADS.Seguent(Part.LlistaMoviments, x)

                print("######################################################################################")

            print()

    elif Opcio == 9:

        ID_Partida = input("     - ID de la partida a visualitzar: ")
        ID_Partida = int(ID_Partida) # Casting 

        mycursor.execute("SELECT Estat FROM Moviments WHERE ID_PARTIDA = %s", (ID_Partida, ))
        myresult = mycursor.fetchall()
                
        flag_init = 1

        for x in myresult:

            Map = eval(x[0])
            Map  = np.stack(Map, axis = 0)    # Passem el text a array.
            # Map= np.flip(Map, axis = 0)    # Com està copiat al revés l'hem de girar

            # Calculem el tamany que tenia la partida que volem carregar
            if flag_init == 1:

                col_count = len(Map[0])
                row_count = len(Map)
                width = len(Map[0]) * Constants.SQUARESIZE
                height = len(Map) * Constants.SQUARESIZE
                size = (width, height)
                screen2 = pygame.display.set_mode(size)
                flag_init = 0

            LògicaJoc.dibuixa_tauler(Map, screen2, height, col_count, row_count, True)
            pygame.time.wait(1000) 

            for event in pygame.event.get():     # Bucle d'events, requisit pel bon funcionament de Pygame window
                if event.type == pygame.QUIT:
                    run = False
                    
        pygame.time.wait(5000)      # Finalització de la partida
        pygame.display.quit()
        print()

    else:
        print()

    # Guardem en partida les dades generades.
    if 0 < Opcio < 6:

        Part.Nick = Nick_Usuari

        if Part.LlistaMoviments.MEMO[Part.LlistaMoviments.ultim].GuanyaPLAYER:

            Part.Puntuacio = Part.LlistaMoviments.MEMO[Part.LlistaMoviments.ultim].PuntsPlayer

        elif Part.LlistaMoviments.MEMO[Part.LlistaMoviments.ultim].GuanyaIA:

            Part.Puntuacio = - (Part.LlistaMoviments.MEMO[Part.LlistaMoviments.ultim].PuntsIA)
        else:

            Part.Puntuacio = 0

    return Part 

def menuAdministrador(mycursor, mydb):
    Continuar = True

    while (Continuar):

        print("######################################################################################")
        print("#                                                                                    #")
        print(" #                                ADMIN MENU  - CRUD                                #")
        print("#                                                                                    #")
        print("######################################################################################")
        print("#                                                                                    #")
        print("#                                                                                    #")
        print("#     1. Realitzar consulta SQL                  (No funcional)                      #")
        print("#     2. Consultar els usuaris registrats        (READ)                              #")
        print("#     3. Actualitzar el Nick d'un Usuari         (UPDATE CASCADE)                    #")
        print("#     4. Donar de baixa un Usuari                (DELETE CASCADE)                    #")
        print("#     5. Fer Administrador a un Usuari           (CREATE)                            #")
        print("#     6. Consultar els administradors            (READ)                              #")
        print("#     7. Sortir                                                                      #")
        print("#                                                                                    #")
        print("######################################################################################")
        print()
        opcio = int(input(" - Selecciona una opció: "))
        print()

        if opcio == 1:
            
            try:
                Query = input("QUERY: ")
            except:
                print(" - Error de sintaxis SQL")
            print()

        elif opcio == 2:

            mycursor.execute("select NICK, Nom_Usuari, Cognom1, Cognom2 from Usuaris where NICK NOT LIKE 'Desconegut'")
            resultat = mycursor.fetchall()

            for element in resultat:
                print(element)
            print()

        elif opcio == 3:

            Nick_current = input("      - Nick que vols actualitzar: ")

            # Comprovem que existeix
            mycursor.execute("select NICK from Usuaris WHERE NICK = %s", (Nick_current,) )
            res = mycursor.fetchone()
            

            if res is None or res[0] == 'Desconegut':
                
                print("      - L'usuari no existeix, comprovi que el Nick és correcte! ")
                print()

            else:

                # Si existeix continuem
                Nick_actualitzat = input("      - Nou Nickname: ")
                mycursor.execute("UPDATE Usuaris SET NICK = %s WHERE NICK = %s", (Nick_actualitzat, Nick_current,))
                mydb.commit()
                print("      - Nick actualitzat amb èxit!")
                print()

        elif opcio == 4:

            Nick_current = input("      - Nick del Usuari que vols eliminar: ")

            # Comprovem que existeix
            mycursor.execute("select NICK from Usuaris WHERE NICK = %s", (Nick_current,) )
            res = mycursor.fetchone()
            

            if res is None or res[0] == 'Desconegut' or res[0] == 'Admin':
                
                print("      - L'usuari no existeix, comprovi que el Nick és correcte! ")
                print()

            else:

                mycursor.execute("DELETE FROM Usuaris WHERE NICK = %s", (Nick_current,) )
                mydb.commit()
                print("      - Nick eliminat amb èxit!")
                print()
            
        elif opcio == 5:

            Nick_current = input("      - Nick del Usuari que vols afegir com admin: ")

            # Comprovem que existeix
            mycursor.execute("select NICK from Usuaris WHERE NICK = %s", (Nick_current,) )
            res = mycursor.fetchone()
            

            if res is None or res[0] == 'Desconegut':
                
                print("      - L'usuari no existeix, comprovi que el Nick és correcte! ")
                print()

            else:
                
                Info = " "
                Info = input("      - Info del admin: ")

                mycursor.execute("insert into Administrador(NICK, Mes_Info)  values(%s, %s)", (Nick_current, Info) )
                mydb.commit()
                print("      - Admin creat amb èxit!")
                print()

        elif opcio == 6:

            mycursor.execute("Select * from Administrador")
            resultat = mycursor.fetchall()

            for element in resultat:
                print(element)
            print()

        elif opcio == 7:
            Continuar = False
            break
