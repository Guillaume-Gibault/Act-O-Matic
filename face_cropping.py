import os
import cv2

# Chemins des dossiers
base_dir = "datasets/train"
images_dir = os.path.join(base_dir, "images")
labels_dir = os.path.join(base_dir, "labels")
output_dir = "cropped_faces"
os.makedirs(output_dir, exist_ok=True)


# Fonction pour recadrer les visages à partir des annotations YOLO
def crop_faces_from_yolo(image_path, label_path, output_folder):
    # Charger l'image
    img = cv2.imread(image_path)
    if img is None:
        return
    height, width, _ = img.shape

    # Lire les annotations YOLO
    with open(label_path, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        # YOLO format: class_id x_center y_center width height
        parts = line.strip().split()
        _, x_center, y_center, box_width, box_height = map(float, parts)

        # Convertir les coordonnées YOLO en pixels
        x_center, y_center = int(x_center * width), int(y_center * height)
        box_width, box_height = int(box_width * width), int(box_height * height)

        # Calculer les coins de la boîte englobante
        x1 = max(0, x_center - box_width // 2)
        y1 = max(0, y_center - box_height // 2)
        x2 = min(width, x_center + box_width // 2)
        y2 = min(height, y_center + box_height // 2)

        # Recadrer le visage
        face = img[y1:y2, x1:x2]

        # Enregistrer l'image recadrée
        face_filename = os.path.join(output_folder, f"{os.path.basename(image_path).split('.')[0]}_face{i}.jpg")
        cv2.imwrite(face_filename, face)


# Parcourir toutes les images et labels pour recadrer
for filename in os.listdir(images_dir):
    image_path = os.path.join(images_dir, filename)
    label_path = os.path.join(labels_dir, os.path.splitext(filename)[0] + ".txt")
    if os.path.exists(label_path):
        crop_faces_from_yolo(image_path, label_path, output_dir)

print(f"Recadrage terminé ! Les visages sont sauvegardés dans {output_dir}")
