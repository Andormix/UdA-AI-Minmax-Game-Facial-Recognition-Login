import cv2
import time
import os
import pickle
import numpy as np
from PIL import Image

def Crear_perfil(mycursor, mydb, Usuari):


    Contador_imatges = 1
    Cuenta_regresiva = 3
    marcapasos = 100

    dirname = os.path.dirname(__file__)              
    photo_location = os.path.join(dirname, 'img\\Registro.png')

    cap = cv2.VideoCapture(700)
    window_title  = 'Cuenta regresiva: ' + str(Cuenta_regresiva)

    while(True):

        # Capturo frame per frame
        ret, frame = cap.read()

        cv2.imshow("unique_window_identifier", frame)
        cv2.setWindowTitle("unique_window_identifier", window_title)

        key = cv2.waitKey(10)
        if key == 27:                     # ESCAPE (27) SI PRESIONEM ESCAPE TANQUEM EL VIDEO
            cv2.destroyAllWindows()
            break

        if Cuenta_regresiva >= 0 and marcapasos >= 0:

            if marcapasos == 100 or marcapasos == 66 or marcapasos == 33 or marcapasos == 0:
                window_title = 'Cuenta regresiva: ' + str(Cuenta_regresiva)
                Cuenta_regresiva -=1

            marcapasos -= 1

        else:

            # Mostrem el video
            window_title = 'Reconeixement facial. Fotografies restants: ' + str(51 -Contador_imatges)

            # Transformem la imatge a gis ja que el algoritme està bassat en escala de gissos
            imatge_gris = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)
            cv2.imwrite(photo_location, imatge_gris) # IMATGES A FOLDER  ( és un buffer )

            with open(photo_location,'rb') as file:

                data = file.read()

                mycursor.execute("Insert into Dataset(NICK, Num, Foto) Values(%s, %s, %s)", (Usuari, Contador_imatges, data))
                mydb.commit()

            time.sleep(0.2)

            Contador_imatges += 1
            if Contador_imatges == 51:
                break
            
    cap.release()
    cv2.destroyAllWindows()

def Load_MYSQL_Dataset(mycursor):
    
    dirname = os.path.dirname(__file__)              
    photo_location = os.path.join(dirname, 'Dataset\\')

    mycursor.execute("SELECT * from Dataset")

    Dataset = mycursor.fetchall()

    for Data in Dataset:

        Nick = Data[1]
        Num = Data[2]
        Foto = Data[3]

        if os.path.exists((photo_location + str(Nick) + "\\")) == False: # Comprovem si el directori existeix

            os.mkdir((photo_location + str(Nick) + "\\"))

        Nom_imatge = photo_location + str(Nick) + "\\" + str(Num) + ".png"
        #print(Nom_imatge)

        with open(Nom_imatge, 'wb') as f:
            f.write(Foto)

def reconeixement_facial(Nick):

    # Si detecta la cara de l'usuari X vegades passa el test
    num_vegades_detectat = 0

    # Si detecta altra cara X vegades no passa el test
    num_vegades_no_detectat = 1

    # Mètode reconeixement cares
    face_cascade = cv2.CascadeClassifier('Cascadas/haarcascade_frontalface_alt2.xml')

    # En aquest trebal utilitzarem LBPH
    recon = cv2.face.LBPHFaceRecognizer_create()
    recon.read('trainner.yml') # BUG 05: error: (-2:Unspecified error) File can't be opened for reading! Sol: Typo en entrenament_cares.py

    Etiquetes = { "Nom": 1}
    # Agafem el nostre diccionari d'etiquetes
    with open("Etiquetes.pickle", 'rb') as file:
        Etiquetes_inv = pickle.load(file)
        Etiquetes = {v:k for k, v in Etiquetes_inv.items()}   # Invertim

    Contador_imatges = 1

    cap = cv2.VideoCapture(700)
    while(True):

        # Capturo frame per frame
        ret, frame = cap.read()

        # Transformem la imatge a gis ja que el algoritme està bassat en escala de gissos
        gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)

        # Detecta la cara realitza un quadrat (x, y, w, h)
        faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)

        # On és la meva cara 
        for (x, y, w, h) in faces:  

            # "Region of interest" del frame gris, el quadrat
            roi_gray = gray[y:y+h, x:x+w] # (Coordenada_Y_Inici, Coordenada_Y_Fi)

            # "Region of interest" del frame en color, el quadrat
            roi_color = frame [y:y+h, x:x+w]

            # RECONEIXEMENT

            Id, probabilitat = recon.predict(roi_gray)  # % De la region de interés
            if probabilitat >= 60 and probabilitat <= 100:                                        # HEM DE JUGAR AMB EL %
                # print(Id)
                print ("     + Cara detectada: ")
                print("        - Nick: " + Etiquetes[Id])
                fuente = cv2.FONT_HERSHEY_COMPLEX_SMALL
                nom = Etiquetes[Id]
                color = (255, 255, 255) # Saturación de color
                tamaño = 2
                cv2.putText(frame, nom, (x + 35, y- 20), fuente, 1, color, tamaño, cv2.LINE_AA)
                # print(probabilitat)

                if Etiquetes[Id] == Nick:

                    num_vegades_detectat += 1

                else:
                    num_vegades_no_detectat += 1

                if num_vegades_detectat == 5:

                    print()
                    print("     + Verificació completada amb èxit!")
                    print()

                    cap.release()
                    cv2.destroyAllWindows()
                    return True 

                elif num_vegades_no_detectat == 5:

                    print()
                    print("     -  " + Etiquetes[Id] + " ets un Impostor!")
                    print()

                    cap.release()
                    cv2.destroyAllWindows()

                    return False
                    

            img_item = "Cara_en_gris.png"
            cv2.imwrite(img_item, roi_gray)

            # Dibuixem el rectangle
            color = (255, 255, 255)
            tamaño = 1
            anchura = x + w # coordenada final x
            altura = y + h # coordenada final y
            cv2.rectangle(frame, (x, y), (anchura, altura), color, tamaño)

            #img_item = "Cara_en_gris.png"
            #cv2.imwrite(img_item, roi_gray)

        # Mostrem el video
        cv2.imshow('INICI DE SESSIO. PRESSIONI ESC PER SORTIR', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()





def Crear_YML():
    face_cascade = cv2.CascadeClassifier('Cascadas/haarcascade_frontalface_alt2.xml')

    # Obrim el nostre directori on hem carregat les fotos desde MYSQL
    dirname = os.path.dirname(__file__)              
    imatge_dir = os.path.join(dirname, 'Dataset\\')

    # En aquest trebal utilitzarem LBPH
    recon = cv2.face.LBPHFaceRecognizer_create()

    Id = 0
    persones_ids = {}
    y_persones = []    # Etiquetes
    x_entrenament = [] # Pixels 

    # Iterem les imatges del nostre directori / SQL
    for root, dirs, files in os.walk(imatge_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root, file)

                # Agafem el nom del directori, el label
                persona = os.path.basename(os.path.dirname(path))  # Control de cassos límit ? " " "-"
                # y_persones(persona)
                # x_entrenament(path)
                #print(path)

                if persona in persones_ids:   # Si ja existeix
                    pass
                else: 
                    persones_ids[persona] = Id  #Si no existeix
                    Id += 1

                Id_actual = persones_ids[persona]
                #print(persones_ids)
                

                pil_image = Image.open(path).convert("L") # L -> escala de grisos
                imatge_array = np.array(pil_image, "uint8")
                #print(imatge_array)

                faces = face_cascade.detectMultiScale(imatge_array, scaleFactor = 1.5, minNeighbors = 5)

                for (x, y, w, h) in faces:  
                    
                    roi = imatge_array[y:y+h, x:x+w]
                    x_entrenament.append(roi)
                    y_persones.append(Id_actual)

    # print(x_entrenament)
    # print(y_persones)

    with open("Etiquetes.pickle", 'wb') as f:
        pickle.dump(persones_ids, f)

    recon.train(x_entrenament, np.array(y_persones))
    recon.save("trainner.yml")

