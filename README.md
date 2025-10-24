# 🖼️ Suppresseur d'Arrière-Plan - Application Python

Application de bureau simple pour supprimer automatiquement les arrière-plans d'images en utilisant l'intelligence artificielle.

## 🎯 Fonctionnalités

- ✅ Interface graphique intuitive avec Tkinter
- ✅ Suppression automatique d'arrière-plan par IA (modèle U2-Net)
- ✅ Prévisualisation côte à côte (avant/après)
- ✅ Support de multiples formats d'images (PNG, JPG, JPEG, BMP, GIF, WEBP)
- ✅ Sauvegarde en PNG avec transparence
- ✅ 100% gratuit et open-source

## 🔧 La Technologie

Cette application utilise **rembg**, une bibliothèque Python open-source basée sur le modèle **U2-Net**. C'est la même technologie sous-jacente utilisée par :

- 🍎 Apple (mode Portrait sur iPhone)
- 🎨 Canva (suppression d'arrière-plan)
- 🖥️ Adobe Photoshop (sélection automatique)
- 🌐 remove.bg et autres services en ligne

**U2-Net** est un réseau de neurones profonds conçu spécifiquement pour la détection d'objets saillants et la segmentation d'images.

## 📋 Prérequis

- Python 3.10 ou supérieur (jusqu'à 3.13)
- pip (gestionnaire de paquets Python)

## 🚀 Installation

### 1. Installer les dépendances

**Pour CPU uniquement (ordinateurs sans GPU NVIDIA) :**

```bash
pip install rembg[cpu]
pip install pillow
```

**Pour GPU (si vous avez une carte NVIDIA avec CUDA) :**

```bash
pip install rembg[gpu]
pip install pillow
```

> **Note :** Tkinter est généralement inclus avec Python. Si ce n'est pas le cas :
> - **Ubuntu/Debian :** `sudo apt-get install python3-tk`
> - **Fedora :** `sudo dnf install python3-tkinter`
> - **macOS/Windows :** Tkinter est inclus par défaut

### 2. Télécharger l'application

Copiez le fichier `bg_remover_app.py` sur votre ordinateur.

### 3. Lancer l'application

```bash
python bg_remover_app.py
```

Ou sous Windows :

```bash
python.exe bg_remover_app.py
```

## 📖 Mode d'emploi

1. **Charger une image** : Cliquez sur "📂 Charger une image" et sélectionnez votre photo
2. **Supprimer l'arrière-plan** : Cliquez sur "✂️ Supprimer l'arrière-plan" (cela prend 5-10 secondes)
3. **Enregistrer le résultat** : Cliquez sur "💾 Enregistrer le résultat" pour sauvegarder votre image en PNG avec fond transparent
4. **Réinitialiser** : Cliquez sur "🔄 Réinitialiser" pour recommencer avec une nouvelle image

## 🎨 Modèles disponibles dans rembg

L'application utilise par défaut le modèle U2-Net, mais rembg supporte plusieurs modèles :

- **u2net** (défaut) : Excellent pour personnes, animaux, objets
- **u2netp** : Version plus rapide et légère
- **isnet-general-use** : Nouveau modèle pour usages généraux
- **isnet-anime** : Spécialisé pour personnages d'anime
- **u2net_cloth_seg** : Pour la segmentation de vêtements
- **silueta** : Version compacte (43 MB)
- **sam** : Segment Anything Model de Meta

Pour changer de modèle, modifiez la ligne dans le code :

```python
# Au lieu de :
self.output_image = remove(self.input_image)

# Utilisez :
from rembg import remove, new_session
session = new_session("isnet-general-use")  # ou autre modèle
self.output_image = remove(self.input_image, session=session)
```

## ⚡ Optimisation des performances

### Pour un traitement plus rapide :

1. **Utilisez un GPU** : Installez `rembg[gpu]` si vous avez une carte NVIDIA
2. **Réduisez la taille des images** : Les images plus petites se traitent plus rapidement
3. **Utilisez le modèle u2netp** : Plus léger mais légèrement moins précis

### Temps de traitement typiques :

- **CPU** : 5-15 secondes par image
- **GPU** : 1-3 secondes par image

## 🛠️ Personnalisation

Vous pouvez facilement personnaliser l'application :

### Ajouter un fond coloré au lieu de la transparence :

```python
from rembg import remove
from PIL import Image

# Après avoir enlevé le fond
output_with_bg = remove(input_image)

# Créer un fond coloré
background = Image.new('RGB', output_with_bg.size, (255, 255, 255))  # Blanc
background.paste(output_with_bg, (0, 0), output_with_bg)
```

### Traiter plusieurs images en batch :

```python
import os
from pathlib import Path

input_folder = "images_a_traiter"
output_folder = "images_traitees"

for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"{Path(filename).stem}_no_bg.png")
        
        with open(input_path, 'rb') as i:
            input_data = i.read()
            output_data = remove(input_data)
            
            with open(output_path, 'wb') as o:
                o.write(output_data)
```

## 🐛 Résolution de problèmes

### Erreur : "No module named 'rembg'"
```bash
pip install rembg[cpu]
```

### Erreur : "No module named 'PIL'"
```bash
pip install pillow
```

### L'application est lente
- Utilisez la version GPU si possible
- Réduisez la taille de vos images avant traitement
- Fermez les autres applications gourmandes en ressources

### Erreur de mémoire (MemoryError)
- Votre image est probablement trop grande
- Réduisez la résolution de l'image avant traitement

## 📦 Structure du projet

```
bg_remover_app.py      # Application principale avec interface Tkinter
README.md              # Ce fichier
```

## 🌟 Améliorations possibles

- [ ] Traitement par lots (multiple images)
- [ ] Choix du modèle dans l'interface
- [ ] Ajout de fonds personnalisés
- [ ] Prévisualisation en temps réel
- [ ] Support du drag & drop
- [ ] Export dans différents formats
- [ ] Historique des traitements
- [ ] Raccourcis clavier

## 📚 Ressources

- [Documentation rembg](https://github.com/danielgatis/rembg)
- [U2-Net Paper](https://arxiv.org/abs/2005.09007)
- [ONNX Runtime](https://onnxruntime.ai/)
- [Documentation Tkinter](https://docs.python.org/3/library/tkinter.html)

## 🤝 Contribution

N'hésitez pas à améliorer cette application et à partager vos modifications !

## 📄 Licence

Ce projet utilise :
- **rembg** : MIT License
- **Tkinter** : Python Software Foundation License
- Code de cette application : Libre d'utilisation

## 🙏 Remerciements

- Daniel Gatis pour la bibliothèque **rembg**
- Les créateurs du modèle **U2-Net**
- La communauté open-source

---

**Bon traitement d'images ! 🎉**