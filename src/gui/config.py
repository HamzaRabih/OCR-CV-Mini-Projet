"""
Configuration de l'application OCR GUI
Modifiez ce fichier pour personnaliser l'apparence et le comportement
"""

# ============================================================================
# CONFIGURATION TESSERACT
# ============================================================================

# Chemin vers l'exécutable tesseract.exe
# Changez si vous l'avez installé ailleurs
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Langue OCR (ajouter d'autres codes comme 'fra+eng')
OCR_LANGUAGE = None  # None = automatique (multi-langue); 'eng' = anglais; 'fra' = français

# ============================================================================
# CONFIGURATION INTERFACE UTILISATEUR
# ============================================================================

# Mode d'apparence : "light" ou "dark"
APPEARANCE_MODE = "light"

# Thème de couleur : "blue", "green", "dark-blue"
COLOR_THEME = "blue"

# ============================================================================
# GÉOMÉTRIE FENÊTRE
# ============================================================================

# Dimensions initiales (WxH)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Maximiser la fenêtre au démarrage ?
START_MAXIMIZED = False

# Rendre la fenêtre redimensionnable ?
RESIZABLE = True

# ============================================================================
# COULEURS PERSONNALISÉES (optionnel)
# ============================================================================

# Si vous voulez des couleurs différentes, décommentez et modifiez
COLORS = {
    "primary": "#0084FF",      # Bleu (Charger, primaire)
    "success": "#34C759",      # Vert (Succès, OCR terminé)
    "warning": "#FF9500",      # Orange (En cours, sauvegarde)
    "danger": "#FF3B30",       # Rouge (Erreurs, suppression)
    "info": "#5AC8FA",         # Cyan (Actions secondaires)
    "background": "#F5F5F5",   # Gris clair (Zones texte)
    "border": "#CCCCCC",       # Gris (Cadres)
}

# ============================================================================
# APERÇU IMAGE
# ============================================================================

# Taille maximale de l'aperçu en pixels (largeur, hauteur)
PREVIEW_MAX_SIZE = (300, 300)

# ============================================================================
# ZONE DE TEXTE
# ============================================================================

# Police pour l'affichage du texte OCR
TEXT_FONT_FAMILY = "Courier New"
TEXT_FONT_SIZE = 10

# ============================================================================
# FICHIERS
# ============================================================================

# Nom par défaut pour la sauvegarde
DEFAULT_SAVE_FILENAME = "texte_ocr.txt"

# Répertoire par défaut pour sauvegarder (si vide, utilise le dernier)
DEFAULT_SAVE_DIR = ""

# ============================================================================
# COMPORTEMENT APPLICATION
# ============================================================================

# Afficher les messages de succès ?
SHOW_SUCCESS_MESSAGES = True

# Afficher les messages d'erreur en boîte de dialogue ?
SHOW_ERROR_DIALOGS = True

# Centrer la fenêtre au démarrage ?
CENTER_WINDOW = True

# ============================================================================
# THREADING
# ============================================================================

# Délai en secondes avant de montrer un message "OCR en cours..." (0 = immédiat)
OCR_PROGRESS_DELAY = 0

# ============================================================================
# RACCOURCIS CLAVIER
# ============================================================================

# Activez/Désactivez les raccourcis clavier
KEYBOARD_SHORTCUTS_ENABLED = True

# Personnalisez les raccourcis (format tkinter)
SHORTCUTS = {
    "open": "<Control-o>",
    "extract": "<Control-e>",
    "save": "<Control-s>",
    "clear": "<Control-Shift-Delete>",
}

# ============================================================================
# LOGGING (optionnel)
# ============================================================================

# Activer le logging ?
LOGGING_ENABLED = False

# Niveau de log : "DEBUG", "INFO", "WARNING", "ERROR"
LOG_LEVEL = "INFO"

# Fichier log
LOG_FILE = "ocr_gui.log"
