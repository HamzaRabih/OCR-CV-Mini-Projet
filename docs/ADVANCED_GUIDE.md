# 🔧 Guide Avancé - Cas d'usage et debugging

## Table des matières

1. [Cas d'usage avancés](#cas-dusage-avancés)
2. [Debugging et troubleshooting](#debugging-et-troubleshooting)
3. [Personnalisation avancée](#personnalisation-avancée)
4. [Performance et optimisation](#performance-et-optimisation)
5. [Extension de l'application](#extension-de-lapplication)

---

## Cas d'usage avancés

### 1. Utiliser l'app avec plusieurs images en batch

**Scénario** : Vous avez 10 images à traiter.

**Solution 1 : Manuelle (GUI)**
```
Charger image 1 → Extraire → Sauvegarder
Charger image 2 → Extraire → Sauvegarder
... (répéter)
```

**Solution 2 : Script Python (recommandé)**
```python
import os
from functions import load_image, preprocess_image
import pytesseract

dossier = "images/"
for filename in os.listdir(dossier):
    if filename.endswith(".png"):
        path = os.path.join(dossier, filename)
        img = load_image(path)
        processed = preprocess_image(img)
        text = pytesseract.image_to_string(processed)
        
        # Sauvegarder
        out_file = filename.replace(".png", "_ocr.txt")
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✓ {out_file}")
```

### 2. OCR en plusieurs langues

**Cas** : Document français et anglais mélangé.

**Solution** : Modifier config.py
```python
OCR_LANGUAGE = "fra+eng"  # Français + anglais
```

Puis dans `gui_app.py` (_run_ocr_internal) :
```python
text = pytesseract.image_to_string(
    processed,
    lang=OCR_LANGUAGE if OCR_LANGUAGE else None
)
```

**Langues disponibles** : 'eng', 'fra', 'deu', 'spa', 'ita', 'chi_sim', 'chi_tra', etc.

### 3. Traitement avec pre-processing avancé

**Cas** : Image très bruitée, mal contraste.

**Solution** : Améliorer `preprocess_image()` dans `functions.py`

```python
import cv2

def preprocess_image_advanced(img):
    """Prétraitement avancé pour images difficiles"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Réduction bruit aggressif
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    
    # Amélioration contraste (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)
    
    # Seuillage Otsu
    _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh
```

Puis utiliser dans GUI :
```python
from functions import load_image, preprocess_image_advanced

processed = preprocess_image_advanced(self.current_image)
```

### 4. Ajouter persistance (historique)

**Cas** : L'utilisateur veut voir l'historique de ses extractions.

**Solution** : Ajouter base de données SQLite

```python
import sqlite3
from datetime import datetime

def save_to_history(image_path, text, language="auto"):
    """Sauvegarde extraction dans l'historique"""
    conn = sqlite3.connect("ocr_history.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY,
            image_path TEXT,
            text TEXT,
            language TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute(
        "INSERT INTO history (image_path, text, language) VALUES (?, ?, ?)",
        (image_path, text, language)
    )
    
    conn.commit()
    conn.close()
```

---

## Debugging et troubleshooting

### Problème 1 : "ModuleNotFoundError"

**Symptôme** :
```
ModuleNotFoundError: No module named 'customtkinter'
```

**Solutions** :
```bash
# Solution 1 : Installer les dépendances
pip install -r requirements_gui.txt

# Solution 2 : Installer directement
pip install customtkinter pillow

# Solution 3 : Vérifier l'environnement
pip list | grep customtkinter
```

### Problème 2 : Interface figée pendant OCR

**Symptôme** : La fenêtre ne répond pas pendant l'extraction.

**Cause** : OCR n'est pas dans un thread.

**Solution** : Vérifier dans `gui_app.py`
```python
def run_ocr_threaded(self):
    """IMPORTANT : utiliser threading"""
    thread = threading.Thread(target=self._run_ocr_internal, daemon=True)
    thread.start()  # ← Ne pas oublier !
```

### Problème 3 : Pas d'aperçu image

**Symptôme** : Bouton charge l'image mais pas d'aperçu.

**Cause** : Pillow non installé ou chemin invalide.

**Debug** :
```python
from PIL import Image
import traceback

try:
    img = Image.open("images/document.png")
    print(f"Image chargée : {img.size}")
except Exception as e:
    print(f"Erreur : {e}")
    traceback.print_exc()
```

### Problème 4 : OCR extrait mal le texte

**Symptôme** : Résultat avec beaucoup de caractères mal reconnus.

**Solutions** :

a) Vérifier la qualité de l'image
```python
import cv2
img = cv2.imread("image.png")
print(f"Dimensions : {img.shape}")  # Doit être > 100x100
print(f"Contraste : {img.std()}")   # Doit être > 20
```

b) Améliorer le prétraitement
```python
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Essayer différentes approches
    # 1) Binarisation simple
    _, thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # 2) Otsu (plus robuste)
    _, thresh2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 3) Adaptative (pour images variables)
    thresh3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
    
    return thresh2  # Otsu généralement meilleur
```

c) Ajuster la taille
```python
# Upscale l'image avant OCR (si petite)
import cv2
img = cv2.imread("image.png")
if img.shape[0] < 200:
    img = cv2.resize(img, None, fx=2, fy=2)  # ×2 taille
```

### Problème 5 : Erreur UTF-8 dans sauvegarde

**Symptôme** :
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Solution** : Spécifier UTF-8 explicitement
```python
with open(file_path, 'w', encoding='utf-8', errors='replace') as f:
    f.write(text)
```

### Debug mode : Activer les logs

Créez `debug_mode.py` :
```python
import logging
import sys

# Configuration logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ocr_debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Utiliser dans gui_app.py
logger.debug(f"Image chargée : {self.current_image_path}")
logger.info(f"OCR lancé")
logger.error(f"Erreur : {e}")
```

---

## Personnalisation avancée

### 1. Créer un thème personnalisé

Modifier `config.py` :
```python
# Coleurs personnalisées
COLORS = {
    "primary": "#FF6B35",       # Orange vif
    "success": "#004E89",       # Bleu foncé
    "warning": "#F77F00",       # Orange
    "danger": "#D62828",        # Rouge
    "info": "#06A77D",          # Vert
}
```

Puis dans `gui_app.py`, utiliser `COLORS` au lieu de valeurs hardcodées.

### 2. Ajouter des panneaux

Exemple : Ajouter un onglet "Historique"

```python
# Dans _create_ui() :
from customtkinter import CTkTabview

tabs = CTkTabview(self)
tabs.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=15)

# Onglet 1 : Extraction
tab1 = tabs.add("Extraction")
# ... placer les widgets d'extraction ici

# Onglet 2 : Historique
tab2 = tabs.add("Historique")
# ... placer historique ici
```

### 3. Personnaliser les raccourcis

Modifier `config.py` :
```python
SHORTCUTS = {
    "open": "<Control-o>",
    "extract": "<Control-e>",
    "save": "<Control-s>",
    "clear": "<Control-Shift-Delete>",
    "copy": "<Control-c>",  # Nouveau
}
```

Puis dans `gui_app.py` :
```python
def _bind_shortcuts(self):
    for action, key in SHORTCUTS.items():
        if action == "open":
            self.bind(key, lambda e: self.load_image())
        elif action == "extract":
            self.bind(key, lambda e: self.run_ocr_threaded())
        # ... etc
```

---

## Performance et optimisation

### 1. Précharger Tesseract

```python
# Au démarrage (plus lent une fois, puis rapide)
import pytesseract
pytesseract.image_to_string(np.zeros((1, 1)))  # Dummy call pour précharger
```

### 2. Cache des images

```python
# Garder une copie prétraitée pour réutilisation
class OCRApp(ctk.CTk):
    def __init__(self):
        # ...
        self.processed_image_cache = None
```

### 3. Limiter la taille d'aperçu

```python
def show_image_preview(self, image_path):
    img = Image.open(image_path)
    
    # Réduire taille AVANT aperçu (plus rapide)
    img.thumbnail((300, 300), Image.LANCZOS)
    
    photo = ImageTk.PhotoImage(img)
    self.image_label.configure(image=photo)
    self.image_label.image = photo
```

### 4. Profiler l'app

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# ... exécuter OCR ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 fonctions lentes
```

---

## Extension de l'application

### 1. Ajouter un éditeur de texte intégré

```python
class TextEditorWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Boutons édition
        edit_frame = ctk.CTkFrame(self)
        edit_frame.pack(side="top", fill="x", padx=5, pady=5)
        
        ctk.CTkButton(edit_frame, text="Annuler").pack(side="left", padx=2)
        ctk.CTkButton(edit_frame, text="Rétablir").pack(side="left", padx=2)
        ctk.CTkButton(edit_frame, text="Chercher").pack(side="left", padx=2)
        
        # Zone texte
        self.text = CTkTextbox(self)
        self.text.pack(fill="both", expand=True)
```

### 2. Ajouter support PDF

```python
def load_pdf(self, pdf_path):
    """Charge un PDF et l'extrait page par page"""
    try:
        import pdf2image
        images = pdf2image.convert_from_path(pdf_path)
        
        self.pdf_images = images
        self.pdf_current_page = 0
        
        self.show_image_from_pdf()
    except ImportError:
        print("Installez pdf2image : pip install pdf2image")
```

### 3. Ajouter correction orthographique

```python
def correct_text(self):
    """Corrige le texte avec Enchant"""
    try:
        import enchant
        checker = enchant.Dict("fr_FR")
        
        words = self.extracted_text.split()
        corrected = []
        
        for word in words:
            if not checker.check(word):
                suggestions = checker.get_suggestions(word)
                corrected.append(suggestions[0] if suggestions else word)
            else:
                corrected.append(word)
        
        corrected_text = " ".join(corrected)
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", corrected_text)
        
    except ImportError:
        print("Installez : pip install pyenchant")
```

### 4. Export avancé

```python
def export_as_pdf(self):
    """Exporte le texte en PDF"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        
        path = tk_filedialog.asksaveasfilename(defaultextension=".pdf")
        if path:
            c = canvas.Canvas(path, pagesize=A4)
            c.drawString(50, 750, self.extracted_text)
            c.save()
            self.show_success("PDF créé !")
    except ImportError:
        print("Installez : pip install reportlab")

def export_as_docx(self):
    """Exporte en Word"""
    try:
        from docx import Document
        
        path = tk_filedialog.asksaveasfilename(defaultextension=".docx")
        if path:
            doc = Document()
            doc.add_paragraph(self.extracted_text)
            doc.save(path)
            self.show_success("DOCX créé !")
    except ImportError:
        print("Installez : pip install python-docx")
```

---

## Ressources et références

- [CustomTkinter Docs](https://github.com/TomSchimansky/CustomTkinter/wiki)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [OpenCV Docs](https://docs.opencv.org/)
- [pytesseract](https://github.com/madmaze/pytesseract)
- [PIL/Pillow](https://pillow.readthedocs.io/)

---

**Bon développement ! 🚀**
