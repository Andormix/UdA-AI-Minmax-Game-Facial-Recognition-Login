# import Reconeixement_Facial
import ReconeixementFacial

def login(mycursor, mydb):

    Continuar = True

    while(Continuar):

        print("######################################################################################")
        print("#                                                                                    #")
        print(" #                             SPLATOON LOGIN                                        #")
        print("#                                                                                    #")
        print("######################################################################################")
        print("#                                                                                    #")
        print("#     1. Login                                                                       #")
        print("#     2. Registre                                                                    #")
        print("#     3. Mode desconegut                                                             #")
        print("#     4. Sortir                                                                      #")
        print("#                                                                                    #")
        print("######################################################################################")
        print()

        opcio = int(input("     - Selecciona una opció: "))

        if opcio == 1:

            print()
            Nick = input("     - Nick: ")
            print()

            mycursor.execute("select NICK from Usuaris WHERE NICK = %s", (Nick,) )
            res = mycursor.fetchone()

            mycursor.execute("select NICK from Administrador WHERE NICK = %s", (Nick,) )
            admin = mycursor.fetchone()
            

            if res is None:
                
                print("     - L'usuari no existeix, comprovi que el Nick és correcte! ")
                print()

            else:

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

                    return True, Nick, True

                if Verificacio:
                    return True, Nick, False


        elif opcio == 2:

            print()
            NomComplet = input("      - Nom Real: ")      # Nom Real
            NomCompletDividit = NomComplet.split()

            if len(NomCompletDividit) == 1:
                print("      - Falten els cognoms! ")
                print("      - Registre completat sense èxit!")
                return False, 'None', False
                
            elif len(NomCompletDividit) == 2:
                print("      - Falta el segon cognom! ")
                print("      - Registre completat sense èxit!")
                return False, 'None', False

            Nick = input("     - Nickname: ")     # Nickname ( Unique )
            print()

            mycursor.execute("select NICK from Usuaris WHERE NICK = %s", (Nick,) )
            res = mycursor.fetchone()
            
            if res is None:  # Evitem BUG:06 Duplicats

                
                mycursor.execute("insert into Usuaris(NICK, Nom_Usuari, Cognom1, Cognom2)  values(%s, %s, %s, %s)", (Nick, NomCompletDividit[0], NomCompletDividit[1], NomCompletDividit[2]))
                mydb.commit() 

                mycursor.execute("insert into Players(NICK, Info)  values(%s, %s)", (Nick, 'Player Info'))
                mydb.commit() 

                print("     + A continuació prendrem 50 fotografies perquè puguis autenticar el teu ")
                print("       usuari amb reconeixement facial")
                print()
                input("     - Pressioni ENTER quan estigui preparat! ")
                print()

                ReconeixementFacial.Crear_perfil(mycursor, mydb, Nick)

                print(" - Registre completat mab èxit!")
                print()

            else:

                print("     - L'usuari ja existeix! Si us plau, triï un nick diferent ")
                print()


        elif opcio == 3:

            return True, 'Desconegut', False
            print()

        elif opcio == 4:

            return False, 'Desconegut', False
            print()
