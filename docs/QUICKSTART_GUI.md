# 🚀 Guide de démarrage rapide - OCR GUI

## 5 minutes pour commencer

### Étape 1 : Installer les dépendances

```bash
pip install -r requirements_gui.txt
```

### Étape 2 : Installer Tesseract OCR

**Windows :**
1. Téléchargez l'installeur depuis https://github.com/tesseract-ocr/tesseract/wiki/Downloads
2. Exécutez le `.exe` et acceptez l'installation par défaut
3. Redémarrez votre terminal

**Linux (Debian/Ubuntu) :**
```bash
sudo apt install tesseract-ocr
```

### Étape 3 : Lancer l'application

```bash
python launch_gui.py
```

**La fenêtre s'ouvre automatiquement !** 🎉

---

## 📱 Utilisation

1. **Charger une image**
   - Cliquez sur `📂 Charger une image`
   - Sélectionnez une image (PNG, JPG, etc.)
   - Un aperçu apparaît automatiquement

2. **Extraire le texte**
   - Cliquez sur `⚙️ Extraire le texte`
   - Attendez que le traitement se termine
   - Le texte s'affiche dans la zone de droite

3. **Sauvegarder**
   - Cliquez sur `💾 Sauvegarder le texte`
   - Choisissez où sauvegarder
   - Fichier `.txt` créé ! ✓

4. **Copier**
   - Cliquez sur `📋 Copier le texte`
   - Le texte est copié dans le presse-papiers
   - Collez-le où vous voulez (Ctrl+V)

5. **Effacer**
   - Cliquez sur `🗑️ Effacer` pour réinitialiser

---

## ⌨️ Raccourcis utiles

- `Ctrl+O` → Ouvrir une image
- `Ctrl+E` → Extraire le texte
- `Ctrl+S` → Sauvegarder le texte

---

## 🎨 Interface en un coup d'œil

```
┌─────────────────────────────────────────────────────┐
│  📄 Extraction de Texte par OCR                     │
│  Chargez une image et extrayez le texte auto.       │
├─────────────────────┬─────────────────────────────┤
│   GAUCHE            │     DROITE                   │
│   ──────────────    │     ──────                   │
│ 📂 Charger          │  ┌─────────────────────┐   │
│ ⚙️ Extraire         │  │ Texte extrait      │   │
│                     │  │ (scrollable)       │   │
│ Aperçu image        │  │                   │   │
│ ┌─────────────┐     │  │                   │   │
│ │             │     │  │                   │   │
│ │   [IMG]     │     │  │                   │   │
│ │             │     │  │                   │   │
│ └─────────────┘     │  └─────────────────────┘   │
│                     │  💾 🗑️  (boutons)      │
│ État: ✓ Prêt        │                         │
└─────────────────────┴─────────────────────────────┘
```

---

## 🆘 Problèmes courants ?

**Q: "Tesseract not found"**
A: Installez Tesseract OCR depuis le lien ci-dessus

**Q: "ModuleNotFoundError: customtkinter"**
A: `pip install customtkinter`

**Q: L'image ne s'affiche pas**
A: Vérifiez que Pillow est installé : `pip install pillow`

**Q: Rien ne se passe quand je clique sur "Extraire"**
A: Vérifiez que vous avez d'abord chargé une image

---

## 📚 Documentation complète

Consultez `README_GUI_UPGRADE.md` pour :
- Architecture détaillée
- Configuration personnalisée
- Évolutions futures
- Dépannage avancé

---

## ✅ Version CLI encore disponible

Si vous préférez la ligne de commande :
```bash
python main.py images/document.png
```

Voir `README.md` pour plus de détails.

---

Bon OCR ! 🎉
