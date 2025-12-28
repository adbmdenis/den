#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier et corriger les erreurs dans admin_panel.py
"""

import re

def check_admin_panel():
    """Vérifie le fichier admin_panel.py pour les erreurs communes"""
    
    print("=" * 60)
    print("  VÉRIFICATION DU PANEL ADMIN")
    print("=" * 60)
    print()
    
    try:
        with open("admin_panel.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        errors = []
        warnings = []
        
        # Vérifier les doubles accolades
        if "{{" in content and not "{{{{" in content:
            # C'est normal dans les f-strings Python
            pass
        
        # Vérifier les fonctions JavaScript essentielles
        required_functions = [
            "showModal",
            "hideModal",
            "logout",
            "loadStats",
            "loadClients",
            "createClient",
            "showSection"
        ]
        
        print("📋 Vérification des fonctions JavaScript...")
        for func in required_functions:
            pattern = f"function {func}"
            if pattern in content:
                print(f"  ✅ {func}")
            else:
                print(f"  ❌ {func} MANQUANTE")
                errors.append(f"Fonction {func} manquante")
        
        # Vérifier les modals
        print("\n📋 Vérification des modals...")
        required_modals = [
            "newClientModal",
            "sellModal",
            "editClientModal",
            "extendModal"
        ]
        
        for modal in required_modals:
            if modal in content:
                print(f"  ✅ {modal}")
            else:
                print(f"  ❌ {modal} MANQUANT")
                warnings.append(f"Modal {modal} manquant")
        
        # Vérifier les boutons
        print("\n📋 Vérification des boutons...")
        button_patterns = [
            (r'onclick="showModal\(', "Boutons showModal"),
            (r'onclick="logout\(\)', "Bouton logout"),
            (r'onclick="showSection\(', "Boutons showSection"),
        ]
        
        for pattern, desc in button_patterns:
            if re.search(pattern, content):
                print(f"  ✅ {desc}")
            else:
                print(f"  ⚠️  {desc} non trouvés")
                warnings.append(f"{desc} non trouvés")
        
        # Résumé
        print("\n" + "=" * 60)
        print("  RÉSUMÉ")
        print("=" * 60)
        
        if errors:
            print(f"\n❌ {len(errors)} erreur(s) critique(s) :")
            for err in errors:
                print(f"  - {err}")
        
        if warnings:
            print(f"\n⚠️  {len(warnings)} avertissement(s) :")
            for warn in warnings:
                print(f"  - {warn}")
        
        if not errors and not warnings:
            print("\n✅ Aucune erreur détectée !")
            print("\nLe problème vient probablement des identifiants admin.")
            print("Consultez START_HERE.md pour la solution.")
        
        return len(errors) == 0
        
    except FileNotFoundError:
        print("❌ Fichier admin_panel.py non trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

if __name__ == "__main__":
    check_admin_panel()
