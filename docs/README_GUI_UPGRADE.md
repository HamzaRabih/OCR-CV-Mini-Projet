# OCR GUI - Application Upgrade UX/UI

## 📋 Vue d'ensemble de l'upgrade

L'application OCR a été **complètement réinventée** avec une interface moderne et intuitive, tout en **conservant intégralement** le cœur OCR existant.

### ✨ Améliorations principales

#### 1. **Interface Moderne avec CustomTkinter**
   - Design contemporain et épuré
   - Thème clair avec couleurs harmonieuses
   - Composants modernes et arrondis
   - Adaptation automatique à différentes résolutions

#### 2. **Architecture à 2 panneaux**
   - **Gauche** : Contrôles et aperçu de l'image
   - **Droite** : Zone de texte scrollable pour le résultat OCR
   - Layout responsif et équilibré

#### 3. **Boutons intuitifs avec icônes emoji**
   - 📂 Charger une image
   - ⚙️ Extraire le texte
   - 💾 Sauvegarder le texte
   - 📋 Copier le texte
   - 🗑️ Effacer tout

#### 4. **Aperçu d'image redimensionné**
   - Affichage automatique de l'image chargée
   - Redimensionnement proportionnel (max 300x300)
   - Bordure visuelle avec feedback utilisateur

#### 5. **Indicateur d'état visuel**
   - Badge circulaire avec code couleur
   - États : Prêt, En cours, Terminé, Erreur
   - Texte descriptif et actualisé

#### 6. **Gestion intelligente des boutons**
   - Bouton "Extraire" **désactivé** jusqu'au chargement d'une image
   - Boutons "Sauvegarder" et "Copier" **désactivés** jusqu'à l'OCR
   - États synchronisés avec la logique de l'app

#### 7. **Threading et barre de progression**
   - L'OCR s'exécute dans un thread séparé (ne bloque pas l'UI)
   - Bouton change d'état pendant le traitement : "⏳ OCR en cours..."
   - Réactivité garantie même sur images volumineuses

#### 8. **Boîtes de dialogue natives**
   - **File Dialog** pour charger/sauvegarder
   - **Message Boxes** pour succès/erreurs
   - Intégration Windows native

#### 9. **Raccourcis clavier**
   - `Ctrl+O` → Ouvrir une image
   - `Ctrl+S` → Sauvegarder le texte
   - `Ctrl+E` → Extraire le texte
   - Navigation rapide et efficace

#### 10. **Gestion robuste des erreurs**
   - Messages d'erreur explicites et localisés
   - Détection automatique de Tesseract
   - Fallback intelligent si installation standard manque

---

## 📁 Structure des fichiers

```
Mini_projet_CV/
├── main.py                    # Version CLI originale (conservée)
├── functions.py               # Fonctions OCR (réutilisées ✓)
├── gui_app.py                 # ★ NOUVEAU : Application GUI moderne
├── launch_gui.py              # ★ NOUVEAU : Lanceur simplifié
├── create_sample_image.py     # Générateur d'images de test
├── images/
│   └── document.png           # Image d'exemple
├── README.md                  # Documentation originale
└── README_GUI_UPGRADE.md      # ★ NOUVEAU : Cette documentation
```

---

## 🚀 Installation et utilisation

### Prérequis

1. **Python 3.7+** avec les packages suivants :
   ```bash
   pip install customtkinter pillow opencv-python pytesseract
   ```

2. **Tesseract OCR** (exécutable système)
   - Windows : Télécharger depuis https://github.com/tesseract-ocr/tesseract
   - Linux : `sudo apt install tesseract-ocr`

### Lancement de la GUI

```bash
python launch_gui.py
```

Ou directement :
```bash
python gui_app.py
```

---

## 🎨 Architecture du code

### Classe principale : `OCRApp`

```python
class OCRApp(ctk.CTk):
    """
    Application OCR GUI complète
    
    Structuration :
    ├── __init__()                    # Initialisation et setup
    ├── _create_ui()                  # Construction de l'interface
    ├── load_image()                  # Charger une image
    ├── show_image_preview()          # Afficher l'aperçu
    ├── run_ocr_threaded()            # Lancer OCR (thread-safe)
    ├── _run_ocr_internal()           # Logique OCR (thread)
    ├── save_text()                   # Sauvegarder le texte
    ├── copy_text()                   # Copier dans presse-papiers
    ├── clear_all()                   # Réinitialiser tout
    ├── update_status()               # Mettre à jour l'état
    ├── show_error()                  # Boîte d'erreur
    └── _bind_shortcuts()             # Raccourcis clavier
```

### Intégration du code OCR existant

Les fonctions OCR originales sont **directement réutilisées** :

```python
from functions import load_image, preprocess_image
import pytesseract

# Dans _run_ocr_internal() :
processed = preprocess_image(self.current_image)
text = pytesseract.image_to_string(processed)
```

✅ **Aucune modification** du cœur OCR

---

## 🎯 Fonctionnalités détaillées

### 1. Charger une image
- Ouvre un dialog de fichier
- Formats supportés : PNG, JPG, JPEG, BMP, TIFF
- Affiche un aperçu redimensionné
- Active le bouton "Extraire le texte"
- Met à jour l'indicateur d'état

### 2. Extraire le texte
- Applique automatiquement : conversion gris + binarisation (Otsu)
- Détection auto de Tesseract si non configuré
- Threading : ne bloque pas l'UI
- Affiche le résultat dans la zone de texte
- Active "Sauvegarder" et "Copier"

### 3. Sauvegarder le texte
- Dialog pour choisir le chemin
- Nom par défaut : `texte_ocr.txt`
- Encodage UTF-8 pour caractères accentués
- Message de succès avec nom du fichier

### 4. Copier le texte
- Copie dans le presse-papiers système
- Raccourci clavier possible
- Feedback utilisateur immédiat

### 5. Effacer tout
- Réinitialise image, texte, état
- Désactive les boutons appropriés
- Prépare pour une nouvelle extraction

---

## 🎨 Palette de couleurs et design

| Élément | Couleur | Utilisation |
|---------|---------|-------------|
| Primaire (Charger) | #0084FF (Bleu) | Bouton principal |
| Succès | #34C759 (Vert) | OCR terminé, statut OK |
| Warning | #FF9500 (Orange) | En cours, sauvegarde |
| Danger | #FF3B30 (Rouge) | Erreurs, suppression |
| Info | #5AC8FA (Cyan) | Actions secondaires |
| Background | #F5F5F5 (Gris clair) | Zones de texte |
| Border | #CCCCCC (Gris) | Cadres et bordures |

---

## ⌨️ Raccourcis clavier

| Raccourci | Action |
|-----------|--------|
| `Ctrl+O` | Ouvrir une image |
| `Ctrl+E` | Extraire le texte (OCR) |
| `Ctrl+S` | Sauvegarder le texte |
| `Ctrl+X` | Effacer tout (optionnel) |

---

## 🔧 Configuration et personnalisation

### Chemin Tesseract personnalisé

Si Tesseract est ailleurs que `C:\Program Files\Tesseract-OCR`, modifiez dans `gui_app.py` :

```python
# Ligne 31
pytesseract.pytesseract.tesseract_cmd = r"VOTRE_CHEMIN_ICI\tesseract.exe"
```

### Thème clair/sombre

Changez le mode d'apparence :

```python
# Dans __init__() ligne 57
ctk.set_appearance_mode("dark")  # ou "light"
```

### Couleur thème

```python
# Ligne 58
ctk.set_default_color_theme("green")  # ou "blue", "dark-blue"
```

---

## 📊 Comparaison CLI vs GUI

| Aspect | CLI (main.py) | GUI (gui_app.py) |
|--------|---------------|------------------|
| Utilisation | `python main.py image.png` | Interface graphique |
| Aperçu image | ❌ Non | ✅ Oui, redimensionné |
| État en temps réel | Texte seul | ✅ Badge + texte |
| Feedback utilisateur | Minimal | ✅ Messages modernes |
| Threading | ❌ Bloque | ✅ Asynchrone |
| Accessible | Développeurs | ✅ Tout public |
| Multilingue UI | ❌ Français statique | ✅ Peux être internationalisée |

---

## 🐛 Dépannage

### "Tesseract not found"
→ Installez Tesseract OCR ou configurez le chemin dans `gui_app.py`

### L'aperçu d'image ne s'affiche pas
→ Vérifiez que Pillow est installé : `pip install pillow`

### CustomTkinter n'est pas trouvé
→ `pip install customtkinter`

### Erreur d'encodage UTF-8
→ L'app utilise déjà UTF-8 ; si problème persiste, le système peut nécessiter configuration locale

---

## 📈 Évolutions futures possibles

- [ ] Support des documents PDF
- [ ] OCR multi-page en batch
- [ ] Éditeur de texte intégré
- [ ] Historique des extractions
- [ ] Support multilingue (français, anglais, espagnol...)
- [ ] Exportation en Word/PDF
- [ ] Undo/Redo pour les textes
- [ ] Préférences utilisateur sauvegardées
- [ ] Mode sombre amélioré
- [ ] Intégration avec cloud (Google Drive, etc.)

---

## 📝 Notes de développement

- **Threading** : `threading.Thread(target=self._run_ocr_internal, daemon=True)`
- **Références images** : Nécessaires pour éviter garbage collection : `self.image_label.image = photo`
- **Encodage** : UTF-8 partout (console + fichiers)
- **DPI awareness** : CustomTkinter gère automatiquement la mise à l'échelle

---

## 👨‍💻 Auteur

**Application de base** : Mini-projet OCR (2026)
**Upgrade UX/UI** : Développement GUI moderne avec CustomTkinter

---

## 📄 Licence

Même licence que le projet original.
