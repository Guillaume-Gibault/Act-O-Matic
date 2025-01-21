import cv2
import numpy as np

def detect_and_crop_face(image_path, output_path="cropped_face.jpg"):
    # Charger le modèle de détection de visage Haarcascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Charger l'image
    image = cv2.imread(image_path)
    if image is None:
        print("Erreur : Impossible de charger l'image.")
        return

    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Détecter les visages
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        print("Aucun visage détecté.")
        return

    # Récupérer les coordonnées du premier visage détecté
    x, y, w, h = faces[0]

    # Détourer le visage
    cropped_face = image[y:y+h, x:x+w]

    # Sauvegarder l'image détourée
    cv2.imwrite(output_path, cropped_face)
    print(f"Visage détouré et sauvegardé dans {output_path}")

    # Afficher le visage détouré
    cv2.imshow("Cropped Face", cropped_face)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Exemple d'utilisation
detect_and_crop_face(r"C:\Users\33658\Downloads\braff1.jpg", r"C:\Users\33658\Downloads\braff1crop.jpg")
