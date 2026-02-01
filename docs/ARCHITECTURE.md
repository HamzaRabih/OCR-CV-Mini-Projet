# 🏗️ Architecture du projet OCR - Complète

## Vue d'ensemble globale

```
Utilisateur
    │
    ├─── CLI (main.py) ────────┐
    │                          │
    └─── GUI (gui_app.py) ◄───┤
                               │
                    ┌──────────┘
                    │
            Logique OCR (functions.py)
                    │
         ┌──────────┴──────────┐
         │                     │
    load_image()        preprocess_image()
         │                     │
         └──────────┬──────────┘
                    │
            pytesseract (wrapper)
                    │
            Tesseract OCR (exécutable)
```

---

## 📁 Structure des fichiers (complète)

```
Mini_projet_CV/
│
├── 📄 CONFIGURATION & DOCUMENTATION
│   ├── README.md                    # Documentation originale (CLI)
│   ├── README_GUI_UPGRADE.md        # ★ Documentation complète de la GUI
│   ├── QUICKSTART_GUI.md            # ★ Guide rapide de démarrage
│   ├── ARCHITECTURE.md              # ★ Ce fichier
│   ├── config.py                    # ★ Fichier de configuration personnalisable
│   └── requirements_gui.txt         # ★ Dépendances pour la GUI
│
├── 🐍 CODE PYTHON
│   ├── functions.py                 # ✓ Réutilisée : Fonctions OCR de base
│   │   ├── load_image()             # Lit image avec OpenCV
│   │   └── preprocess_image()       # Gris + binarisation
│   │
│   ├── main.py                      # ✓ Conservée : Version CLI
│   │   └── Utilise functions.py + pytesseract
│   │
│   ├── gui_app.py                   # ★ NOUVEAU : Application GUI
│   │   ├── Classe OCRApp            # Interface principale
│   │   ├── Réutilise functions.py   # Code OCR inchangé
│   │   └── Threading + UI moderne
│   │
│   ├── launch_gui.py                # ★ Lanceur simple GUI
│   │
│   ├── create_sample_image.py       # Générateur d'images de test
│   │
│   └── install_tesseract.ps1        # Script d'installation Tesseract
│
├── 📂 DONNÉES
│   └── images/
│       └── document.png             # Image d'exemple
│
└── 📋 FICHIERS DE SORTIE (générés à l'exécution)
    ├── document_ocr.txt             # Texte extrait (CLI)
    ├── texte_ocr.txt                # Texte extrait (GUI - défaut)
    └── [autre nom].txt              # Personnalisé (GUI)
```

---

## 🔄 Flux d'exécution

### Version CLI (main.py)

```
Démarrage
    │
    ▼
Charger image (argv ou défaut)
    │
    ▼
Vérifier fichier existe
    │
    ▼
load_image()
    │
    ▼
preprocess_image()
    ├─► Conversion gris (cv2.cvtColor)
    ├─► Blur Gaussien (cv2.GaussianBlur)
    └─► Binarisation Otsu (cv2.threshold)
    │
    ▼
pytesseract.image_to_string()
    │
    ▼
Tesseract OCR (exécutable)
    │
    ▼
Résultat OCR
    │
    ├─► Affichage console
    │
    └─► Sauvegarde .txt (UTF-8)
    │
    ▼
Fin
```

### Version GUI (gui_app.py)

```
Démarrage
    │
    ▼
Initialiser fenêtre CustomTkinter
    │
    ▼
Charger config.py (optionnel)
    │
    ▼
Créer UI (_create_ui)
    ├─► Barre titre
    ├─► Panneau gauche (contrôles + aperçu)
    └─► Panneau droite (texte + boutons)
    │
    ▼
Attendre interaction utilisateur
    │
    ├─► Bouton "Charger" → load_image()
    │   ├─ Dialog fichier
    │   ├─ load_image() (functions.py)
    │   ├─ show_image_preview()
    │   └─ update_status()
    │
    ├─► Bouton "Extraire" → run_ocr_threaded()
    │   ├─ Lancer thread séparé (_run_ocr_internal)
    │   ├─ preprocess_image() (functions.py)
    │   ├─ pytesseract.image_to_string()
    │   ├─ Afficher dans text_box
    │   └─ Activer "Sauvegarder" + "Copier"
    │
    ├─► Bouton "Sauvegarder" → save_text()
    │   ├─ Dialog fichier (asksaveasfilename)
    │   ├─ Écrire fichier UTF-8
    │   └─ Messagebox succès
    │
    ├─► Bouton "Copier" → copy_text()
    │   └─ clipboard.append()
    │
    └─► Bouton "Effacer" → clear_all()
        └─ Réinitialiser tout
    │
    ▼
Boucle d'événements Tkinter
```

---

## 🔌 Points d'intégration

### 1. Importation du code OCR

**Dans gui_app.py :**
```python
from functions import load_image, preprocess_image
import pytesseract

# ... plus tard dans _run_ocr_internal() ...
processed = preprocess_image(self.current_image)
text = pytesseract.image_to_string(processed)
```

✅ **Aucune modification** de `functions.py`

### 2. Configuration centralisée

**Dans config.py :**
```python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
APPEARANCE_MODE = "light"
WINDOW_WIDTH = 1200
```

**Dans gui_app.py :**
```python
from config import *  # Import de tous les paramètres

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
```

### 3. Threading pour l'OCR

```python
def run_ocr_threaded(self):
    """Lance OCR sans bloquer l'UI"""
    thread = threading.Thread(
        target=self._run_ocr_internal,
        daemon=True
    )
    thread.start()
```

---

## 🎯 Dépendances et versions

### Core OCR (inchangé)
```
opencv-python      4.12.0.88  # Traitement images
pytesseract         0.3.13    # Wrapper Tesseract
numpy              >=2.0      # Matrices/calculs
```

### GUI (nouveau)
```
customtkinter       5.2.0     # Interface moderne
pillow             >=8.0.0    # Images (aperçu)
```

### Système (externe)
```
Tesseract OCR       5.x+      # Exécutable reconnaissance texte
```

---

## 🎨 Classe OCRApp - Structure détaillée

```python
class OCRApp(ctk.CTk):
    """Fenêtre principale de l'application"""
    
    # === Initialisation ===
    __init__()                        # Setup fenêtre + config
    
    # === Construction UI ===
    _create_ui()                      # Crée tous les widgets
    
    # === Chargement image ===
    load_image()                      # Dialog + charge image
    show_image_preview()              # Affiche aperçu redimensionné
    
    # === OCR (threading) ===
    run_ocr_threaded()                # Lance OCR en thread
    _run_ocr_internal()               # Logique OCR (dans thread)
    
    # === Sauvegarde/Export ===
    save_text()                       # Enregistre .txt
    copy_text()                       # Presse-papiers
    
    # === Gestion state ===
    clear_all()                       # Réinitialise tout
    update_status()                   # Met à jour indicateur
    
    # === UI Feedback ===
    show_error()                      # Boîte d'erreur
    show_success()                    # Boîte succès
    
    # === Utilitaires ===
    _center_window()                  # Centre fenêtre
    _bind_shortcuts()                 # Raccourcis clavier
```

---

## 📊 Diagramme d'état

```
┌─────────────────────────────────────────────────────────┐
│ ÉTAT "PRÊT"                                             │
│ - Aucune image chargée                                  │
│ - Bouton "Extraire" : DÉSACTIVÉ                        │
│ - Boutons "Sauvegarder/Copier" : DÉSACTIVÉS           │
│ - Statut : 🔲 Prêt (gris)                             │
└─────────────────────────────────────────────────────────┘
                    ▲              │
                    │              │ Utilisateur clique
                    │              │ "Charger image"
                    │              ▼
┌─────────────────────────────────────────────────────────┐
│ ÉTAT "IMAGE CHARGÉE"                                    │
│ - Image affichée en aperçu                             │
│ - Bouton "Extraire" : ACTIVÉ                           │
│ - Boutons "Sauvegarder/Copier" : DÉSACTIVÉS           │
│ - Statut : 🟢 Image chargée                           │
└─────────────────────────────────────────────────────────┘
                    ▲              │
                    │              │ Utilisateur clique
                    │              │ "Extraire texte"
                    │              ▼
┌─────────────────────────────────────────────────────────┐
│ ÉTAT "OCR EN COURS"                                     │
│ - Image affichée                                        │
│ - Bouton "Extraire" : DÉSACTIVÉ + "⏳ OCR en cours"   │
│ - Thread OCR en arrière-plan                           │
│ - Statut : 🟠 OCR en cours                            │
└─────────────────────────────────────────────────────────┘
                    ▲              │
                    │              │ Thread termine
                    │              │ (succès ou erreur)
                    │              ▼
┌─────────────────────────────────────────────────────────┐
│ ÉTAT "RÉSULTAT DISPONIBLE"                             │
│ - Texte affiché dans zone texte                        │
│ - Bouton "Extraire" : ACTIVÉ (pour nouvelle extract)   │
│ - Boutons "Sauvegarder/Copier" : ACTIVÉS              │
│ - Statut : 🟢 OCR terminé ✓                           │
└─────────────────────────────────────────────────────────┘
            │                           │
            │                           │ Utilisateur sauvegarde
            │ Utilisateur                │ ou réinitialise
            │ clique "Effacer"           ▼
            │                    Fichier .txt créé
            └──────────────────────────────┘
                        ▼
                    RETOUR "PRÊT"
```

---

## 🚀 Optimisations et bonnes pratiques

### 1. **Threading pour réactivité**
```python
threading.Thread(target=self._run_ocr_internal, daemon=True).start()
```
→ L'UI reste réactive même pendant l'OCR volumineux

### 2. **Gestion de la mémoire (images)**
```python
self.image_label.image = photo  # Important : évite garbage collection
```
→ Références image conservées

### 3. **Encodage UTF-8 partout**
```python
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(self.extracted_text)
```
→ Support complet des caractères accentués

### 4. **Détection auto de Tesseract**
```python
path = shutil.which('tesseract')  # Cherche dans PATH
if not path:
    # Chemins classiques Windows
    common = [r"C:\Program Files\Tesseract-OCR\tesseract.exe", ...]
```
→ Installation flexible

### 5. **Configuration externalisée**
```python
try:
    from config import *
except ImportError:
    # Fallback aux valeurs par défaut
```
→ Personnalisation sans toucher au code

---

## 🔐 Gestion des erreurs

```
Erreur Tesseract non trouvé
    └─► Recherche auto du chemin
        ├─ Dans PATH (shutil.which)
        └─ Chemins courants Windows
            └─ Si trouvé : configure + réessaye
            └─ Si non : message explicite + lien install

Erreur fichier image invalide
    └─► try/except + messagebox.showerror()

Erreur d'encodage UTF-8
    └─► encoding='utf-8', errors='replace'

Erreur lors de la sauvegarde
    └─► Dialog d'erreur + log
```

---

## 📈 Performance et scalabilité

| Opération | Temps | Notes |
|-----------|-------|-------|
| Chargement image | <100ms | OpenCV natif |
| Prétraitement | <200ms | Gris + Blur + Otsu |
| OCR (petite image) | 1-2s | Tesseract |
| OCR (grande image) | 5-10s | Tesseract |
| Affichage UI | <50ms | CustomTkinter |
| Sauvegarde .txt | <100ms | I/O fichier |

✅ Threading garantit UI réactive même si OCR lent

---

## 🔗 Relations entre modules

```
┌─────────────────────────────────────────────────────┐
│                   gui_app.py                        │
│  ┌─────────────────────────────────────────────┐  │
│  │ Classe OCRApp (Interface)                   │  │
│  └─────────────────────────────────────────────┘  │
│         │              │               │           │
│         ▼              ▼               ▼           │
│    functions.py  pytesseract    config.py         │
│    ├─ load_image()      │          │              │
│    └─ preprocess_img()  │          ├─ Tesseract   │
│         │               │          │   path       │
│         └───┬───────────┘          ├─ Thème       │
│             │                       └─ Géométrie  │
│             ▼                                     │
│      Tesseract OCR (exécutable)                   │
│             │                                     │
│             ▼                                     │
│      Texte extrait                               │
│             │                                     │
│         ┌───┴───┐                                 │
│         ▼       ▼                                 │
│      Console  Fichier .txt                       │
└─────────────────────────────────────────────────┘
```

---

## 🎓 Points d'apprentissage

1. **CustomTkinter** : Framework GUI moderne Python
2. **Threading** : Opérations longues sans bloquer UI
3. **File dialogs** : Interaction utilisateur
4. **Configuration externalisée** : Flexibilité de l'app
5. **Intégration de code existant** : Réutilisation sans modification
6. **Gestion d'erreurs robuste** : UX amélieurée
7. **UTF-8 et encodage** : Texte multilangue

---

## 📝 Logs et débogage

Pour tracer l'exécution, décommentez les `print()` dans :
- `_run_ocr_internal()` : Voir les étapes OCR
- `load_image()` : Voir les chemins fichiers
- Callbacks d'erreur : Voir les exceptions

Futurs améliorations : logging module pour fichier `.log`

---

## 🎉 Conclusion

L'architecture sépare :
- **Logique métier** (functions.py) : Réutilisable indépendamment
- **Interface CLI** (main.py) : Simple et efficace
- **Interface GUI** (gui_app.py) : Moderne et conviviale
- **Configuration** (config.py) : Flexible et personnalisable

Tout reste modulaire et maintenable !
