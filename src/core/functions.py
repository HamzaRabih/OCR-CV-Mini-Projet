"""
Fonctions utilitaires pour le mini-projet OCR
- `load_image(path)` : lit une image avec OpenCV
- `preprocess_image(img)` : conversion en niveaux de gris + seuillage

Les commentaires expliquent brièvement chaque étape.
"""

import cv2


def load_image(path: str):
    """Lit une image depuis `path` et vérifie qu'elle existe.

    Retourne l'image au format BGR (OpenCV).
    """
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Impossible de lire l'image: {path}")
    return img


def preprocess_image(img):
    """Applique un prétraitement simple pour améliorer l'OCR:

    1. Conversion en niveaux de gris
    2. (Optionnel) Flou gaussien pour réduire le bruit
    3. Binarisation (seuillage) avec Otsu pour obtenir une image binaire

    Retourne l'image seuillée (noir/blanc) adaptée à `pytesseract`.
    """
    # Conversion en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Réduction du bruit (aide parfois pour l'OCR)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Binarisation avec Otsu (détermine automatiquement le meilleur seuil)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh
