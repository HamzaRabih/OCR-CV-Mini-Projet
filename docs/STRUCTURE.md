# 🏗️ Structure du projet OCR - Guide détaillé

**Organisation logique du projet en dossiers**

---

## 📋 Vue d'ensemble

```
Mini_projet_CV/                 ← Racine du projet
│
├── README.md                   ← Point d'entrée (vous êtes ici)
├── requirements_gui.txt        ← Dépendances Python
├── STRUCTURE.md                ← Ce fichier
│
├── src/                        ← 🐍 CODE SOURCE
│   ├── core/                   Logique OCR réutilisable
│   │   ├── functions.py        (40 lignes)
│   │   └── main.py             (120 lignes)
│   │
│   └── gui/                    Interface graphique
│       ├── gui_app.py          (450 lignes)
│       ├── launch_gui.py       (10 lignes)
│       └── config.py           (100 lignes)
│
├── docs/                       ← 📚 DOCUMENTATION (7 fichiers)
│   ├── QUICKSTART_GUI.md       Démarrage 5 min
│   ├── README_GUI_UPGRADE.md   Vue d'ensemble
│   ├── ARCHITECTURE.md         Structure technique
│   ├── ADVANCED_GUIDE.md       Cas avancés
│   ├── INDEX.md                Navigation
│   ├── MANIFEST.md             Inventaire
│   └── RECAP_FINAL.md          Résumé final
│
├── utils/                      ← 🛠️ UTILITAIRES
│   ├── create_sample_image.py  Génère images de test
│   └── install_tesseract.ps1   Installation Tesseract
│
└── data/                       ← 📂 DONNÉES
    ├── images/                 Images pour OCR
    │   └── document.png        Image d'exemple
    │
    └── output/                 Résultats OCR
        └── *.txt               Fichiers générés
```

---

## 🐍 Dossier `src/` - Code Source

### `src/core/` - Logique OCR (Réutilisable)

#### `functions.py` (40 lignes)
**Rôle** : Fonctions de traitement image indépendantes

```python
def load_image(path: str):
    """Lit une image avec OpenCV"""
    img = cv2.imread(path)
    return img

def preprocess_image(img):
    """Applique prétraitement (gris + blur + otsu)"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, 
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh
```

**Utilisation** :
```python
from src.core.functions import load_image, preprocess_image
```

**Propriétés** :
- ✅ Aucune dépendance sur GUI
- ✅ Réutilisable dans n'importe quel projet
- ✅ Testable indépendamment
- ✅ Optimisée pour performance

---

#### `main.py` (120 lignes)
**Rôle** : Version CLI de l'application

```python
def extract_text_from_image(image_path: str) -> str:
    """OCR : load → preprocess → pytesseract"""
    img = load_image(image_path)
    processed = preprocess_image(img)
    text = pytesseract.image_to_string(processed)
    return text

def main():
    """Orchestration CLI"""
    image_path = sys.argv[1] if len(sys.argv) > 1 else "images/document.png"
    text = extract_text_from_image(image_path)
    print("--- Texte extrait ---")
    print(text)
    # Sauvegarder dans .txt
```

**Utilisation** :
```bash
python src/core/main.py data/images/document.png
```

**Propriétés** :
- ✅ Indépendant de la GUI
- ✅ Peut s'exécuter seul
- ✅ Gestion d'erreurs robuste

---

### `src/gui/` - Application Graphique

#### `gui_app.py` (450 lignes)
**Rôle** : Interface GUI complète (CustomTkinter)

```python
class OCRApp(ctk.CTk):
    """Application OCR avec interface graphique moderne"""
    
    def __init__(self):
        super().__init__()
        # Initialisation GUI
        self._create_ui()
    
    def _create_ui(self):
        """Crée tous les widgets (2 panneaux)"""
        # Panneau gauche : contrôles + aperçu
        # Panneau droite : zone texte + boutons
    
    def load_image(self):
        """Charger image via dialog"""
        file_path = tk_filedialog.askopenfilename(...)
        img = load_image(file_path)
        self.show_image_preview(file_path)
    
    def run_ocr_threaded(self):
        """Lancer OCR dans thread séparé"""
        thread = threading.Thread(target=self._run_ocr_internal)
        thread.start()
    
    def _run_ocr_internal(self):
        """Logique OCR (dans thread)"""
        processed = preprocess_image(self.current_image)
        text = pytesseract.image_to_string(processed)
        self.text_box.insert("1.0", text)
    
    def save_text(self):
        """Sauvegarder texte en .txt"""
        file_path = tk_filedialog.asksaveasfilename(...)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.extracted_text)
```

**Utilisation** :
```bash
python src/gui/gui_app.py
```

**Propriétés** :
- ✅ Réutilise `functions.py` et `main.py`
- ✅ Threading pour réactivité
- ✅ Gestion d'état intelligente
- ✅ Feedback utilisateur complet

---

#### `launch_gui.py` (10 lignes)
**Rôle** : Point d'entrée simplifié

```python
"""Lanceur de l'application GUI OCR"""
from gui_app import main

if __name__ == "__main__":
    main()
```

**Utilisation** :
```bash
python src/gui/launch_gui.py
```

**Propriétés** :
- ✅ Simple et lisible
- ✅ Permet `python src/gui/launch_gui.py` (plus lisible)

---

#### `config.py` (100 lignes)
**Rôle** : Configuration externalisée

```python
# Tesseract
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# UI
APPEARANCE_MODE = "light"
COLOR_THEME = "blue"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Personnalisation
PREVIEW_MAX_SIZE = (300, 300)
TEXT_FONT_SIZE = 10
```

**Utilisation** :
```python
from config import TESSERACT_PATH, APPEARANCE_MODE
ctk.set_appearance_mode(APPEARANCE_MODE)
```

**Propriétés** :
- ✅ Toute config en un fichier
- ✅ Facilite personnalisation
- ✅ Pas de valeurs hardcodées

---

## 📚 Dossier `docs/` - Documentation

| Fichier | Type | Audience | Longueur |
|---------|------|----------|:--:|
| **QUICKSTART_GUI.md** | Guide | 👤 Débutants | ⏱️ 5 min |
| **README_GUI_UPGRADE.md** | Vue d'ensemble | 👨‍💼 Managers | ⏱️ 10 min |
| **ARCHITECTURE.md** | Technique | 👨‍💻 Devs | ⏱️ 20 min |
| **ADVANCED_GUIDE.md** | Avancé | 🔧 Experts | ⏱️ 30 min |
| **INDEX.md** | Navigation | 📚 Tous | ⏱️ 5 min |
| **MANIFEST.md** | Inventaire | 📋 Tous | ⏱️ 10 min |
| **RECAP_FINAL.md** | Résumé | 🎉 Tous | ⏱️ 5 min |

**Lecture recommandée** :
1. `QUICKSTART_GUI.md` (pour démarrer)
2. `README_GUI_UPGRADE.md` (vue d'ensemble)
3. `ARCHITECTURE.md` (technique)
4. `ADVANCED_GUIDE.md` (avancé)

---

## 🛠️ Dossier `utils/` - Utilitaires

### `create_sample_image.py`
**Rôle** : Génère image d'exemple avec texte

```python
# Crée images/document.png avec du texte
# Usage: python utils/create_sample_image.py
```

**Output** :
- Crée `data/images/document.png`
- Image blanche 1200x400 avec texte noir

---

### `install_tesseract.ps1`
**Rôle** : Installation automatique Tesseract (Windows)

```powershell
# Télécharge et installe Tesseract OCR
# Usage: powershell -ExecutionPolicy Bypass -File utils/install_tesseract.ps1
```

**Options** :
1. Téléchargement automatique (recommandé)
2. Ouvrir page de téléchargement
3. Quitter

---

## 📂 Dossier `data/` - Données

### `data/images/`
**Contient** : Images pour OCR

```
data/images/
├── document.png          Image d'exemple (générée)
├── votre_image.jpg       Vos images (à ajouter)
└── autre_document.png    Autres images
```

**Comment ajouter** :
```bash
cp votre_image.png data/images/
python src/gui/launch_gui.py
```

### `data/output/`
**Contient** : Résultats OCR générés

```
data/output/
├── document_ocr.txt      Texte extrait
├── votre_image_ocr.txt   Autres résultats
└── autre_ocr.txt         ...
```

**Généré automatiquement** lors des extractions

---

## 🔄 Flux d'importation

### Depuis GUI
```python
# gui_app.py
from src.core.functions import load_image, preprocess_image
from src.gui.config import TESSERACT_PATH
import pytesseract
```

### Depuis CLI
```python
# main.py
from src.core.functions import load_image, preprocess_image
import pytesseract
```

### Depuis projet externe
```python
# your_project.py
from src.core.functions import load_image, preprocess_image

# Ou CLI
import subprocess
subprocess.run(["python", "src/core/main.py", "image.png"])
```

---

## 📊 Dépendances par module

```
src/core/functions.py
├─ opencv-python
├─ numpy
└─ pillow

src/core/main.py
├─ src/core/functions.py
├─ pytesseract
├─ opencv-python
└─ sys, os, io

src/gui/gui_app.py
├─ customtkinter
├─ pillow
├─ src/core/functions.py
├─ pytesseract
├─ threading
└─ tkinter

src/gui/config.py
└─ (aucune dépendance externe)
```

---

## 🎯 Conventions de nommage

### Fichiers Python
```
module_name.py           (snake_case, clair)
ClassName.py             (PascalCase si 1 classe principale)
_private_function()      (_ prefix si privé)
PUBLIC_CONSTANT          (UPPER_CASE si constant)
```

### Dossiers
```
src/                     (source code)
docs/                    (documentation)
utils/                   (utilitaires)
data/                    (données)
tests/                   (tests - futur)
```

### Fichiers de config
```
config.py                (configuration)
requirements_gui.txt     (dépendances)
.gitignore              (fichiers à ignorer)
```

---

## 📈 Scalabilité

### Pour ajouter une nouvelle fonctionnalité

1. **Si c'est du traitement image** :
   - Ajouter dans `src/core/functions.py`
   - Exporter la fonction
   - Réutilisable partout

2. **Si c'est une UI** :
   - Ajouter dans `src/gui/gui_app.py`
   - Intégrer avec les autres méthodes
   - Tester en lanceur

3. **Si c'est de la configuration** :
   - Ajouter dans `src/gui/config.py`
   - Utiliser dans `gui_app.py`
   - Documenter dans `docs/`

### Pour ajouter un nouveau module
```
src/
├── core/
├── gui/
├── ml/                   ← Nouveau module ML
│   ├── models.py
│   └── training.py
└── api/                  ← Nouveau module API
    └── server.py
```

---

## 🔐 Sécurité et maintenabilité

### ✅ Bonnes pratiques respectées

- ✅ Séparation concerns (core vs GUI)
- ✅ Code modulaire (réutilisable)
- ✅ Configuration externalisée
- ✅ Gestion d'erreurs robuste
- ✅ Documentation complète
- ✅ Pas de hardcoding
- ✅ UTF-8 partout

### 🚀 Performance

- ✅ Threading pour opérations longues
- ✅ Imports optimisés
- ✅ Cache d'images evité GC
- ✅ Binarisation efficace (Otsu)

---

## 📝 Résumé structure

| Dossier | Rôle | Contient | Modificateur |
|---------|------|----------|:--:|
| `src/core/` | OCR core | functions.py, main.py | Utilisateur avancé |
| `src/gui/` | Interface | gui_app.py, config.py | Designer UI |
| `docs/` | Documentation | 7 fichiers .md | Technical writer |
| `utils/` | Utilitaires | Scripts helpers | DevOps |
| `data/images/` | Images | PNG/JPG | User |
| `data/output/` | Résultats | TXT | Generé |

---

## 🎉 Conclusion

Structure **logique**, **scalable** et **maintenable** :
- ✅ Code séparé (core/gui)
- ✅ Configuration centralisée
- ✅ Documentation complète
- ✅ Prêt pour extensions
- ✅ Réutilisable

**Prêt pour production ! 🚀**
