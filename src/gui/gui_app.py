"""
Application GUI OCR moderne avec CustomTkinter
Réutilise les fonctions OCR existantes de functions.py

Fonctionnalités :
- Interface moderne et intuitive
- Aperçu de l'image
- Extraction OCR avec barre de progression
- Sauvegarde du texte avec dialog
- Gestion d'erreurs et messages visuels
- Raccourcis clavier (Ctrl+O, Ctrl+S, Ctrl+E)

Auteur: OCR GUI Upgrade
Date: 2026-02-01
"""

import customtkinter as ctk
from customtkinter import CTkLabel, CTkButton, CTkTextbox, CTkImage
import tkinter as tk
from tkinter import filedialog as tk_filedialog
from tkinter import messagebox as tk_messagebox
from PIL import Image, ImageTk
import os
import sys
import threading
from pathlib import Path

# Importer les fonctions OCR existantes
from src.core.functions import load_image, preprocess_image
import pytesseract
import shutil
import platform

# Importer la configuration (optionnel, fallback à des valeurs par défaut)
try:
    from config import *
except ImportError:
    # Valeurs par défaut si config.py n'existe pas
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    OCR_LANGUAGE = None
    APPEARANCE_MODE = "light"
    COLOR_THEME = "blue"
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    START_MAXIMIZED = False
    RESIZABLE = True
    PREVIEW_MAX_SIZE = (300, 300)
    TEXT_FONT_FAMILY = "Courier New"
    TEXT_FONT_SIZE = 10
    CENTER_WINDOW = True

# ============================================================================
# Configuration Tesseract (réutilisée du main.py)
# ============================================================================
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# ============================================================================
# Classe principale OCRApp
# ============================================================================
class OCRApp(ctk.CTk):
    """Application OCR GUI moderne avec CustomTkinter"""

    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.title("OCR Application - Reconnaissance de Texte")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(RESIZABLE, RESIZABLE)

        # Variables d'état
        self.current_image_path = None
        self.current_image = None
        self.extracted_text = None
        self.is_processing = False
        self.image_preview_photo = None  # Référence pour aperçu image

        # Thème personnalisé
        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(COLOR_THEME)

        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Créer l'interface
        self._create_ui()

        # Centrer la fenêtre (optionnel)
        if CENTER_WINDOW:
            self._center_window()

        # Lier les raccourcis clavier
        self._bind_shortcuts()

    # ========================================================================
    # Création de l'interface utilisateur
    # ========================================================================

    def _create_ui(self):
        """Crée tous les éléments de l'interface"""

        # ─── Barre de titre et description ───────────────────────────────
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=15)

        title_label = CTkLabel(
            title_frame,
            text="📄 Extraction de Texte par OCR",
            font=("Helvetica", 24, "bold"),
            text_color="#1f1f1f",
        )
        title_label.pack(anchor="w")

        subtitle_label = CTkLabel(
            title_frame,
            text="Chargez une image et extrayez le texte automatiquement",
            font=("Helvetica", 12),
            text_color="#777777",
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))

        # ─── Zone gauche : Contrôles et Aperçu ───────────────────────────
        left_frame = ctk.CTkFrame(self)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        left_frame.grid_rowconfigure(2, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        # --- Boutons de contrôle ---
        controls_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        controls_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        controls_frame.grid_columnconfigure((0, 1), weight=1)

        # Bouton Charger Image
        self.load_btn = CTkButton(
            controls_frame,
            text="📂 Charger une image",
            command=self.load_image,
            font=("Helvetica", 12, "bold"),
            height=40,
            fg_color="#0084FF",
            hover_color="#0066CC",
            text_color="white",
        )
        self.load_btn.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        # Bouton Extraire Texte
        self.extract_btn = CTkButton(
            controls_frame,
            text="⚙️ Extraire le texte",
            command=self.run_ocr_threaded,
            font=("Helvetica", 12, "bold"),
            height=40,
            fg_color="#34C759",
            hover_color="#27A844",
            text_color="white",
            state="disabled",  # Désactivé par défaut
        )
        self.extract_btn.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        # --- Zone d'aperçu image ---
        preview_label = CTkLabel(
            left_frame,
            text="Aperçu de l'image",
            font=("Helvetica", 12, "bold"),
            text_color="#1f1f1f",
        )
        preview_label.grid(row=1, column=0, sticky="w", pady=(10, 8))

        # Frame pour l'aperçu avec bordure
        preview_frame = ctk.CTkFrame(left_frame, fg_color="#E8E8E8", border_width=2, border_color="#CCCCCC")
        preview_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)

        self.image_label = CTkLabel(
            preview_frame,
            text="Aucune image chargée",
            font=("Helvetica", 11),
            text_color="#999999",
            fg_color="#E8E8E8",
        )
        self.image_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # --- Indicateur d'état ---
        status_label = CTkLabel(
            left_frame,
            text="État",
            font=("Helvetica", 11, "bold"),
            text_color="#1f1f1f",
        )
        status_label.grid(row=3, column=0, sticky="w", pady=(0, 8))

        # Frame pour le statut avec badge circulaire
        status_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        status_frame.grid(row=4, column=0, sticky="ew")

        self.status_indicator = ctk.CTkFrame(
            status_frame,
            width=12,
            height=12,
            fg_color="#CCCCCC",
            corner_radius=6,
        )
        self.status_indicator.grid(row=0, column=0, sticky="w")
        self.status_indicator.grid_propagate(False)

        self.status_text = CTkLabel(
            status_frame,
            text="Prêt - En attente d'image",
            font=("Helvetica", 10),
            text_color="#666666",
        )
        self.status_text.grid(row=0, column=1, sticky="w", padx=10)

        # ─── Zone droite : Résultat OCR ──────────────────────────────────
        right_frame = ctk.CTkFrame(self)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=15, pady=15)
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # --- Titre résultat ---
        result_label = CTkLabel(
            right_frame,
            text="Texte extrait",
            font=("Helvetica", 12, "bold"),
            text_color="#1f1f1f",
        )
        result_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # --- Zone de texte scrollable ---
        self.text_box = CTkTextbox(
            right_frame,
            font=("Courier New", 10),
            fg_color="#F5F5F5",
            text_color="#1f1f1f",
            border_width=2,
            border_color="#CCCCCC",
        )
        self.text_box.grid(row=1, column=0, sticky="nsew")

        # --- Boutons d'action pour le texte ---
        text_actions_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        text_actions_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        text_actions_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Bouton Sauvegarder
        self.save_btn = CTkButton(
            text_actions_frame,
            text="💾 Sauvegarder le texte",
            command=self.save_text,
            font=("Helvetica", 11, "bold"),
            height=36,
            fg_color="#FF9500",
            hover_color="#E68A00",
            text_color="white",
            state="disabled",
        )
        self.save_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # Bouton Copier
        self.copy_btn = CTkButton(
            text_actions_frame,
            text="📋 Copier le texte",
            command=self.copy_text,
            font=("Helvetica", 11, "bold"),
            height=36,
            fg_color="#5AC8FA",
            hover_color="#3BA8DA",
            text_color="white",
            state="disabled",
        )
        self.copy_btn.grid(row=0, column=1, sticky="ew", padx=5)

        # Bouton Effacer
        self.clear_btn = CTkButton(
            text_actions_frame,
            text="🗑️ Effacer",
            command=self.clear_all,
            font=("Helvetica", 11, "bold"),
            height=36,
            fg_color="#FF3B30",
            hover_color="#E02420",
            text_color="white",
        )
        self.clear_btn.grid(row=0, column=2, sticky="ew", padx=(5, 0))

    # ========================================================================
    # Méthodes de fonctionnalité
    # ========================================================================

    def load_image(self):
        """Charge une image via dialog de fichier"""
        file_path = tk_filedialog.askopenfilename(
            title="Sélectionner une image",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Tous les fichiers", "*.*"),
            ],
        )

        if not file_path:
            return

        try:
            # Charger l'image avec OpenCV
            img = load_image(file_path)
            self.current_image = img
            self.current_image_path = file_path

            # Afficher l'aperçu
            self.show_image_preview(file_path)

            # Mettre à jour l'état
            self.update_status("Image chargée", "#34C759")
            self.extract_btn.configure(state="normal")

        except Exception as e:
            self.show_error(f"Erreur lors du chargement de l'image:\n{str(e)}")
            self.update_status("Erreur de chargement", "#FF3B30")

    def show_image_preview(self, image_path):
        """Affiche un aperçu redimensionné de l'image"""
        try:
            # Ouvrir l'image avec Pillow
            img = Image.open(image_path)

            # Redimensionner pour l'aperçu (max 300x300)
            max_size = (300, 300)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Convertir en PhotoImage Tkinter
            photo = ImageTk.PhotoImage(img)

            # Afficher dans le label
            self.image_label.configure(image=photo, text="")
            # IMPORTANT : Garder une référence pour éviter garbage collection
            self.image_preview_photo = photo

        except Exception as e:
            print(f"Erreur aperçu image: {e}")
            self.image_label.configure(text="Erreur affichage image")

    def run_ocr_threaded(self):
        """Lance l'OCR dans un thread pour ne pas bloquer l'UI"""
        if not self.current_image_path:
            self.show_error("Aucune image chargée")
            return

        # Désactiver le bouton et afficher un indicateur
        self.extract_btn.configure(state="disabled", text="⏳ OCR en cours...")
        self.is_processing = True
        self.update_status("OCR en cours...", "#FF9500")

        # Lancer l'OCR dans un thread séparé
        thread = threading.Thread(target=self._run_ocr_internal, daemon=True)
        thread.start()

    def _run_ocr_internal(self):
        """Lance l'OCR (appelé dans un thread)"""
        try:
            # Vérifier que Tesseract est configuré
            try:
                import cv2
                processed = preprocess_image(self.current_image)
                text = pytesseract.image_to_string(processed)
            except pytesseract.pytesseract.TesseractNotFoundError:
                # Chercher Tesseract automatiquement
                def find_tesseract_executable():
                    path = shutil.which('tesseract')
                    if path:
                        return path

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
                    processed = preprocess_image(self.current_image)
                    text = pytesseract.image_to_string(processed)
                else:
                    raise RuntimeError("Tesseract OCR non trouvé. Veuillez l'installer.")

            # Stocker et afficher le texte
            self.extracted_text = text
            self.text_box.delete("1.0", "end")
            self.text_box.insert("1.0", text)

            # Activer les boutons de sauvegarde
            self.save_btn.configure(state="normal")
            self.copy_btn.configure(state="normal")

            # Mettre à jour l'état
            self.update_status("OCR terminé ✓", "#34C759")

        except Exception as e:
            error_msg = f"Erreur OCR: {str(e)}"
            print(error_msg)  # Log
            self.show_error(error_msg)
            self.update_status("Erreur OCR", "#FF3B30")

        finally:
            # Réactiver le bouton
            self.extract_btn.configure(state="normal", text="⚙️ Extraire le texte")
            self.is_processing = False

    def save_text(self):
        """Sauvegarde le texte extrait dans un fichier .txt"""
        if not self.extracted_text:
            self.show_error("Aucun texte à sauvegarder")
            return

        # Dialog pour choisir le chemin de sauvegarde
        file_path = tk_filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichier texte", "*.txt"), ("Tous les fichiers", "*.*")],
            initialfile="texte_ocr.txt",
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.extracted_text)

            self.show_success(f"Texte sauvegardé avec succès !\n{os.path.basename(file_path)}")
            self.update_status("Texte sauvegardé ✓", "#34C759")

        except Exception as e:
            self.show_error(f"Erreur lors de la sauvegarde:\n{str(e)}")

    def copy_text(self):
        """Copie le texte extrait dans le presse-papiers"""
        if not self.extracted_text:
            self.show_error("Aucun texte à copier")
            return

        try:
            self.clipboard_clear()
            self.clipboard_append(self.extracted_text)
            self.show_success("Texte copié dans le presse-papiers !")
        except Exception as e:
            self.show_error(f"Erreur lors de la copie:\n{str(e)}")

    def clear_all(self):
        """Efface tout (image, texte, état)"""
        self.current_image_path = None
        self.current_image = None
        self.extracted_text = None
        self.image_preview_photo = None

        # Réinitialiser l'UI
        self.image_label.configure(image="", text="Aucune image chargée")
        self.text_box.delete("1.0", "end")

        # Désactiver les boutons
        self.extract_btn.configure(state="disabled")
        self.save_btn.configure(state="disabled")
        self.copy_btn.configure(state="disabled")

        # Réinitialiser l'état
        self.update_status("Prêt - En attente d'image", "#CCCCCC")

    # ========================================================================
    # Méthodes utilitaires UI
    # ========================================================================

    def update_status(self, status_text, color):
        """Met à jour l'indicateur d'état"""
        self.status_indicator.configure(fg_color=color)
        self.status_text.configure(text=status_text)

    def show_error(self, message):
        """Affiche une boîte d'erreur"""
        tk_messagebox.showerror("Erreur", message)

    def show_success(self, message):
        """Affiche une boîte de succès"""
        tk_messagebox.showinfo("Succès", message)

    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _bind_shortcuts(self):
        """Lie les raccourcis clavier"""
        self.bind("<Control-o>", lambda e: self.load_image())  # Ctrl+O : Ouvrir
        self.bind("<Control-s>", lambda e: self.save_text())   # Ctrl+S : Sauvegarder
        self.bind("<Control-e>", lambda e: self.run_ocr_threaded())  # Ctrl+E : Extraire


# ============================================================================
# Point d'entrée de l'application
# ============================================================================
def main():
    """Lance l'application GUI OCR"""
    app = OCRApp()
    app.mainloop()


if __name__ == "__main__":
    main()
