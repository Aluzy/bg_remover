#!/usr/bin/env python3
"""
Application de suppression d'arrière-plan avec interface Tkinter
Utilise la bibliothèque rembg (basée sur U2-Net)
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from rembg import remove
import os
from pathlib import Path


class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Suppresseur d'Arrière-Plan")
        self.root.geometry("900x700")
        
        # Variables
        self.input_image = None
        self.output_image = None
        self.input_path = None
        
        # Configuration de l'interface
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Titre
        title_label = ttk.Label(
            main_frame, 
            text="🖼️ Suppresseur d'Arrière-Plan", 
            font=('Arial', 18, 'bold')
        )
        title_label.grid(row=0, column=0, pady=10)
        
        # Frame des boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10)
        
        # Boutons
        self.load_btn = ttk.Button(
            button_frame, 
            text="📂 Charger une image", 
            command=self.load_image
        )
        self.load_btn.grid(row=0, column=0, padx=5)
        
        self.process_btn = ttk.Button(
            button_frame, 
            text="✂️ Supprimer l'arrière-plan", 
            command=self.remove_background,
            state=tk.DISABLED
        )
        self.process_btn.grid(row=0, column=1, padx=5)
        
        self.save_btn = ttk.Button(
            button_frame, 
            text="💾 Enregistrer le résultat", 
            command=self.save_image,
            state=tk.DISABLED
        )
        self.save_btn.grid(row=0, column=2, padx=5)
        
        self.reset_btn = ttk.Button(
            button_frame, 
            text="🔄 Réinitialiser", 
            command=self.reset
        )
        self.reset_btn.grid(row=0, column=3, padx=5)
        
        # Frame pour les images
        images_frame = ttk.Frame(main_frame)
        images_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        images_frame.columnconfigure(0, weight=1)
        images_frame.columnconfigure(1, weight=1)
        images_frame.rowconfigure(0, weight=1)
        
        # Frame image originale
        input_frame = ttk.LabelFrame(images_frame, text="Image Originale", padding="10")
        input_frame.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.input_canvas = tk.Canvas(input_frame, bg='gray85', width=400, height=400)
        self.input_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Frame image traitée
        output_frame = ttk.LabelFrame(images_frame, text="Image Traitée", padding="10")
        output_frame.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.output_canvas = tk.Canvas(output_frame, bg='gray85', width=400, height=400)
        self.output_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Barre de statut
        self.status_label = ttk.Label(
            main_frame, 
            text="Prêt - Chargez une image pour commencer", 
            relief=tk.SUNKEN
        )
        self.status_label.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Barre de progression
        self.progress = ttk.Progressbar(
            main_frame, 
            mode='indeterminate', 
            length=300
        )
        self.progress.grid(row=4, column=0, pady=5)
        
    def load_image(self):
        """Charge une image depuis le disque"""
        file_path = filedialog.askopenfilename(
            title="Sélectionner une image",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"),
                ("Tous les fichiers", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.input_path = file_path
                self.input_image = Image.open(file_path)
                
                # Afficher l'image originale
                self.display_image(self.input_image, self.input_canvas)
                
                # Activer le bouton de traitement
                self.process_btn.config(state=tk.NORMAL)
                
                # Réinitialiser l'image de sortie
                self.output_image = None
                self.output_canvas.delete("all")
                self.save_btn.config(state=tk.DISABLED)
                
                self.status_label.config(
                    text=f"Image chargée : {Path(file_path).name}"
                )
                
            except Exception as e:
                messagebox.showerror(
                    "Erreur", 
                    f"Impossible de charger l'image :\n{str(e)}"
                )
    
    def remove_background(self):
        """Supprime l'arrière-plan de l'image"""
        if not self.input_image:
            return
        
        try:
            # Démarrer la barre de progression
            self.progress.start()
            self.status_label.config(text="Traitement en cours...")
            self.process_btn.config(state=tk.DISABLED)
            self.root.update()
            
            # Appliquer la suppression d'arrière-plan
            self.output_image = remove(self.input_image)
            
            # Afficher le résultat
            self.display_image(self.output_image, self.output_canvas)
            
            # Activer le bouton de sauvegarde
            self.save_btn.config(state=tk.NORMAL)
            self.process_btn.config(state=tk.NORMAL)
            
            self.status_label.config(
                text="Arrière-plan supprimé avec succès !"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Erreur", 
                f"Erreur lors du traitement :\n{str(e)}"
            )
            self.status_label.config(text="Erreur lors du traitement")
            self.process_btn.config(state=tk.NORMAL)
            
        finally:
            # Arrêter la barre de progression
            self.progress.stop()
    
    def save_image(self):
        """Enregistre l'image traitée"""
        if not self.output_image:
            return
        
        # Proposer un nom de fichier par défaut
        if self.input_path:
            input_name = Path(self.input_path).stem
            default_name = f"{input_name}_sans_fond.png"
        else:
            default_name = "image_sans_fond.png"
        
        file_path = filedialog.asksaveasfilename(
            title="Enregistrer l'image",
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[
                ("PNG (transparence)", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Tous les fichiers", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.output_image.save(file_path)
                self.status_label.config(
                    text=f"Image enregistrée : {Path(file_path).name}"
                )
                messagebox.showinfo(
                    "Succès", 
                    "Image enregistrée avec succès !"
                )
            except Exception as e:
                messagebox.showerror(
                    "Erreur", 
                    f"Impossible d'enregistrer l'image :\n{str(e)}"
                )
    
    def display_image(self, image, canvas):
        """Affiche une image dans un canvas"""
        # Obtenir la taille du canvas
        canvas.update()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        # Redimensionner l'image pour qu'elle tienne dans le canvas
        img_copy = image.copy()
        img_copy.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
        
        # Convertir pour Tkinter
        photo = ImageTk.PhotoImage(img_copy)
        
        # Centrer l'image dans le canvas
        x = (canvas_width - photo.width()) // 2
        y = (canvas_height - photo.height()) // 2
        
        # Afficher l'image
        canvas.delete("all")
        canvas.create_image(x, y, anchor=tk.NW, image=photo)
        canvas.image = photo  # Garder une référence
    
    def reset(self):
        """Réinitialise l'application"""
        self.input_image = None
        self.output_image = None
        self.input_path = None
        
        self.input_canvas.delete("all")
        self.output_canvas.delete("all")
        
        self.process_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        
        self.status_label.config(
            text="Prêt - Chargez une image pour commencer"
        )


def main():
    """Point d'entrée de l'application"""
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()