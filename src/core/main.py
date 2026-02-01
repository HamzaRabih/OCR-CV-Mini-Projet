"""
Mini-projet OCR simple avec Tesseract
Fichiers:
- main.py         : point d'entrée
- functions.py    : fonctions de lecture et prétraitement d'images
- create_sample_image.py : script pour générer images/document.png (exemple)
- images/         : dossier contenant l'image `document.png`

Instructions rapides (voir README.md pour plus de détails):
1) Installer Tesseract (Windows: installez depuis https://github.com/tesseract-ocr/tesseract; Linux: `sudo apt install tesseract-ocr`)
2) Installer dépendances Python: `pip install opencv-python pytesseract`
3) (Windows) Si besoin, décommenter et définir `pytesseract.pytesseract.tesseract_cmd` vers le chemin de l'exécutable tesseract
4) Générer l'image d'exemple: `python create_sample_image.py` (créera `images/document.png`)
5) Lancer: `python main.py` (ou `python main.py images/document.png`)

"""

import os
import sys
import cv2
import pytesseract
import shutil
import platform
import io
from src.core.functions import load_image, preprocess_image

# Configure UTF-8 pour l'affichage des caractères accentués sur Windows PowerShell
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# --- Si vous êtes sous Windows et tesseract n'est pas dans le PATH,
#     décommentez et modifiez la ligne ci-dessous en remplaçant le chemin

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_image(image_path: str) -> str:
    """Lit l'image, applique le prétraitement, puis extrait le texte via pytesseract."""
    img = load_image(image_path)
    processed = preprocess_image(img)

    # pytesseract attend une image en niveaux de gris ou couleur; ici on lui passe l'image seuillée
    # Config basique: --psm 3 (segmentation par défaut) ; on peut ajouter `lang='fra'` si Tesseract a le pack français installé
    try:
        text = pytesseract.image_to_string(processed)
    except pytesseract.pytesseract.TesseractNotFoundError:
        # Tesseract non trouvé : essayons de localiser automatiquement l'exécutable
        def find_tesseract_executable():
            # 1) vérifier si 'tesseract' est dans le PATH
            path = shutil.which('tesseract')
            if path:
                return path

            # 2) chemins courants sous Windows
            if platform.system().lower().startswith('win'):
                common = [
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                ]
                for p in common:
                    if os.path.exists(p):
                        return p

            return None

        found = find_tesseract_executable()
        if found:
            pytesseract.pytesseract.tesseract_cmd = found
            print(f"Tesseract trouvé automatiquement : {found} (réessayage)")
            try:
                text = pytesseract.image_to_string(processed)
            except Exception as e:
                raise RuntimeError(f"Erreur lors de l'appel à pytesseract après configuration automatique : {e}")
        else:
            msg = (
                "Tesseract n'est pas installé ou n'est pas dans le PATH.\n"
                "Sous Windows : installez depuis https://github.com/tesseract-ocr/tesseract et ajoutez le dossier \"Tesseract-OCR\" au PATH, ou définissez\n"
                "pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' dans le script.\n"
                "Sous Linux (Debian/Ubuntu) : `sudo apt install tesseract-ocr`.\n"
                "Après installation, relancez le script."
            )
            raise RuntimeError(msg)
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'appel à pytesseract: {e}")

    return text


def main():
    # chemin par défaut
    default_image = os.path.join('images', 'document.png')
    image_path = sys.argv[1] if len(sys.argv) > 1 else default_image

    if not os.path.exists(image_path):
        print(f"Image non trouvée: {image_path}\nGénérez l'exemple avec: python create_sample_image.py")
        return

    print(f"Lecture de l'image: {image_path}")
    text = extract_text_from_image(image_path)

    # Affichage dans la console
    print("--- Texte extrait ---")
    print(text)
    print("---------------------")

    # Sauvegarde dans un fichier .txt
    out_name = os.path.splitext(os.path.basename(image_path))[0] + '_ocr.txt'
    with open(out_name, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Texte sauvegardé dans: {out_name}")


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as e:
        # Affiche un message propre sans traceback long
        print("Erreur :", e)
        print("Pour résoudre : installez Tesseract ou définissez pytesseract.pytesseract.tesseract_cmd vers l'exécutable.")
        sys.exit(1)
    except Exception as e:
        print("Erreur inattendue :", e)
        sys.exit(1)
