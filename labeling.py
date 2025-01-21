import os
import csv

# Chemin vers votre dataset
dataset_path = "/Users/tom/Documents/Datasets/Celebrity Faces Dataset"
output_csv = "Celebrity_Faces_Labeled.csv"

# Ouvrir le fichier CSV en écriture
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Écrire les en-têtes
    writer.writerow(["image_path", "label"])

    # Parcourir chaque dossier dans le dataset
    for folder_name in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, folder_name)
        if os.path.isdir(folder_path):  # Vérifier que c'est un dossier
            # Parcourir chaque image dans le dossier
            for image_name in os.listdir(folder_path):
                image_path = os.path.join(folder_path, image_name)
                # Ajouter une ligne dans le CSV avec le chemin de l'image et la classe
                writer.writerow([image_path, folder_name])

print(f"Annotations enregistrées dans {output_csv}")
