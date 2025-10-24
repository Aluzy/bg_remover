#!/usr/bin/env python3
"""
Script simple pour tester la suppression d'arrière-plan avec rembg
Sans interface graphique - juste un test rapide
"""

from rembg import remove
from PIL import Image
import sys

def simple_remove_bg(input_path, output_path):
    """
    Supprime l'arrière-plan d'une image
    
    Args:
        input_path: chemin de l'image source
        output_path: chemin de l'image de sortie (PNG recommandé)
    """
    print(f"📂 Chargement de l'image : {input_path}")
    
    try:
        # Charger l'image
        input_image = Image.open(input_path)
        print(f"✅ Image chargée : {input_image.size[0]}x{input_image.size[1]} pixels")
        
        # Supprimer l'arrière-plan
        print("⏳ Suppression de l'arrière-plan en cours...")
        output_image = remove(input_image)
        
        # Sauvegarder le résultat
        output_image.save(output_path)
        print(f"✅ Image sauvegardée : {output_path}")
        print("🎉 Terminé !")
        
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier '{input_path}' n'existe pas")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Vérifier les arguments
    if len(sys.argv) != 3:
        print("Usage : python simple_test.py <image_entree> <image_sortie>")
        print("Exemple : python simple_test.py photo.jpg photo_sans_fond.png")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Exécuter la suppression d'arrière-plan
    simple_remove_bg(input_file, output_file)