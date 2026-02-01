"""
Génère un exemple d'image `images/document.png` contenant du texte.
Utile si vous n'avez pas d'image de test prête.
"""

import os
import cv2

OUT_DIR = 'images'
OUT_FILE = os.path.join(OUT_DIR, 'document.png')

os.makedirs(OUT_DIR, exist_ok=True)

# Création d'une image blanche
w, h = 1200, 400
img = 255 * (1 * np.ones((h, w, 3), dtype='uint8')) if 'np' in globals() else None

if img is None:
    import numpy as np
    img = 255 * np.ones((h, w, 3), dtype='uint8')

# Texte d'exemple (plusieurs lignes)
lines = [
    "Ceci est un exemple de texte pour OCR.",
    "Lignes multiples, Tesseract devrait les détecter.",
    "Numéro: 12345 | Date: 2026-02-01"
]

y0, dy = 60, 70
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.2
color = (0, 0, 0)  # noir
thickness = 2

for i, line in enumerate(lines):
    y = y0 + i * dy
    cv2.putText(img, line, (40, y), font, font_scale, color, thickness, cv2.LINE_AA)

cv2.imwrite(OUT_FILE, img)
print(f"Image d'exemple générée: {OUT_FILE}")
