import os
import pandas as pd


def update_csv(csv_path, images_folder, output_csv):
    # Charger le CSV original avec un encodage compatible
    df = pd.read_csv(csv_path, delimiter=';', encoding='latin1')

    # Obtenir la liste des images restantes dans le dossier
    remaining_images = set(os.listdir(images_folder))

    # Ajouter le suffixe "_face.jpg" pour vérifier la correspondance avec les fichiers
    df['Image_with_ext'] = df['Image'].astype(str) + "_face.jpg"

    # Filtrer les entrées du CSV pour ne conserver que celles dont l'image existe
    filtered_df = df[df['Image_with_ext'].isin(remaining_images)]

    # Supprimer la colonne intermédiaire avant la sauvegarde
    filtered_df = filtered_df.drop(columns=['Image_with_ext'])

    # Sauvegarder le CSV mis à jour
    filtered_df.to_csv(output_csv, index=False, sep=';')
    print(f"CSV mis à jour sauvegardé sous : {output_csv}")


# Utilisation
csv_path = r"C:\Users\33658\PycharmProjects\Act-O-Matic\Datasets\FaceCropAge\Will Smith Crop\index.csv"
images_folder = r"C:\Users\33658\PycharmProjects\Act-O-Matic\Datasets\FaceCropAge\Will Smith Crop"
output_csv = r"C:\Users\33658\PycharmProjects\Act-O-Matic\Datasets\FaceCropAge\Will Smith Crop\index_cleaned.csv"

update_csv(csv_path, images_folder, output_csv)
