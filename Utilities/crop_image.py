import cv2
import numpy as np
import os


def detourer_visages(image_path, output_dir, face_cascade_path="haarcascade_frontalface_default.xml"):
    # Charger le classificateur en cascade Haar pour la détection des visages
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + face_cascade_path)

    # Charger l'image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Erreur : Impossible de charger l'image {image_path}")
        return

    # Convertir l'image en niveaux de gris (nécessaire pour la détection)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Détecter les visages
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Vérifier s'il y a des visages détectés
    if len(faces) == 0:
        print(f"Aucun visage détecté dans l'image {image_path}.")
        return

    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Extraire et enregistrer chaque visage
    base_name = os.path.splitext(os.path.basename(image_path))[0]  # Nom de base de l'image
    for i, (x, y, w, h) in enumerate(faces):
        # Extraire le visage
        face = image[y:y + h, x:x + w]

        # Chemin pour enregistrer l'image détourée
        output_path = os.path.join(output_dir, f"{base_name}_face_{i + 1}.jpg")

        # Sauvegarder le visage
        cv2.imwrite(output_path, face)
        print(f"Visage sauvegardé : {output_path}")


def process_folder(input_dir, output_dir, face_cascade_path="haarcascade_frontalface_default.xml"):
    # Vérifier si le dossier d'entrée existe
    if not os.path.exists(input_dir):
        print(f"Erreur : Le dossier d'entrée {input_dir} n'existe pas.")
        return

    # Parcourir tous les fichiers du dossier
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)

        # Vérifier si c'est un fichier image
        if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Traitement de l'image : {file_path}")
            detourer_visages(file_path, output_dir, face_cascade_path)


# Exemple d'utilisation
input_dir = r"C:\Users\33658\Downloads\DataSet\test\Sandra Bullock"
output_dir = r"C:\Users\33658\Documents\Sandra Bullock Crop"
process_folder(input_dir, output_dir)
