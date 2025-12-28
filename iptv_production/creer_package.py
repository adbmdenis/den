#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Créer un package ZIP avec tous les fichiers essentiels"""

import zipfile
import os
from datetime import datetime

# Liste des fichiers essentiels à inclure
FICHIERS_ESSENTIELS = [
    # Fichiers Python principaux
    "server.py",
    "config.py",
    "database.py",
    "admin_panel.py",
    "vavoo_service.py",
    "multi_service.py",
    
    # Fichiers de configuration
    ".env.example",
    "requirements.txt",
    ".gitignore",
    
    # Scripts de démarrage
    "start.bat",
    "start.sh",
    
    # Scripts utilitaires
    "reset_database.py",
    "test_server.py",
    
    # Documentation
    "README.md",
    "QUICKSTART.md",
    "FICHIERS_A_RECUPERER.md",
]

def creer_package():
    """Créer le package ZIP"""
    
    # Nom du fichier ZIP avec date
    date_str = datetime.now().strftime("%Y%m%d")
    nom_zip = f"iptv_package_{date_str}.zip"
    
    print("=" * 60)
    print("CRÉATION DU PACKAGE IPTV")
    print("=" * 60)
    print()
    
    # Créer le fichier ZIP
    with zipfile.ZipFile(nom_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        fichiers_ajoutes = 0
        fichiers_manquants = []
        
        for fichier in FICHIERS_ESSENTIELS:
            if os.path.exists(fichier):
                print(f"✅ Ajout de {fichier}")
                zipf.write(fichier)
                fichiers_ajoutes += 1
            else:
                print(f"⚠️  Fichier manquant: {fichier}")
                fichiers_manquants.append(fichier)
    
    print()
    print("=" * 60)
    print("✅ PACKAGE CRÉÉ!")
    print("=" * 60)
    print()
    print(f"📦 Fichier: {nom_zip}")
    print(f"📊 Fichiers ajoutés: {fichiers_ajoutes}/{len(FICHIERS_ESSENTIELS)}")
    
    if fichiers_manquants:
        print()
        print("⚠️  Fichiers manquants:")
        for f in fichiers_manquants:
            print(f"   - {f}")
    
    # Taille du fichier
    taille = os.path.getsize(nom_zip)
    taille_mb = taille / (1024 * 1024)
    print()
    print(f"💾 Taille: {taille_mb:.2f} MB")
    print()
    print("📋 UTILISATION:")
    print()
    print("1. Extraire le ZIP dans un nouveau dossier")
    print("2. Créer le fichier .env:")
    print("   copy .env.example .env")
    print("3. Éditer .env avec vos paramètres")
    print("4. Installer les dépendances:")
    print("   pip install -r requirements.txt")
    print("5. Démarrer le serveur:")
    print("   python server.py")
    print()
    print("=" * 60)

if __name__ == "__main__":
    creer_package()
