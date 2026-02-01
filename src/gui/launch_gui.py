"""
Script de lancement de l'application OCR GUI
Simplement exécutez : python launch_gui.py
"""

import sys
from pathlib import Path

# Assurer que la racine du projet est dans sys.path afin que
# les imports de type `from src.core.functions import ...` fonctionnent
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.gui.gui_app import main
except Exception:
    # Fallback: tenter un import local pour compatibilité
    from gui_app import main


if __name__ == "__main__":
    main()
