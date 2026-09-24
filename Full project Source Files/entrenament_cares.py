import os
import numpy as np
from PIL import Image
import cv2
import pickle

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