#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test des boutons du panel admin"""

import requests
import json

BASE_URL = "http://localhost:8888"

def test_login():
    """Test de connexion admin"""
    print("🔐 Test de connexion admin...")
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={"username": "superadmin", "password": "Super@2024!"}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print("✅ Connexion réussie!")
            print(f"   Token: {data['token'][:20]}...")
            return data['token']
        else:
            print(f"❌ Erreur: {data.get('error')}")
            return None
    else:
        print(f"❌ Erreur HTTP {response.status_code}")
        return None

def test_admin_page():
    """Test de la page admin pour vérifier les fonctions JavaScript"""
    print("\n📄 Test de la page admin...")
    response = requests.get(f"{BASE_URL}/admin")
    
    if response.status_code == 200:
        html = response.text
        
        # Vérifier que les fonctions JavaScript sont présentes
        functions = ["showModal", "hideModal", "logout", "copyText"]
        missing = []
        
        for func in functions:
            if f"function {func}" not in html:
                missing.append(func)
        
        if missing:
            print(f"❌ Fonctions manquantes: {', '.join(missing)}")
            return False
        else:
            print("✅ Toutes les fonctions JavaScript sont présentes!")
            
        # Vérifier que les boutons onclick sont présents
        buttons = [
            'onclick="showModal',
            'onclick="hideModal',
            'onclick="logout()"',
            'onclick="copyText'
        ]
        
        for btn in buttons:
            if btn in html:
                print(f"   ✓ Bouton trouvé: {btn}")
            else:
                print(f"   ⚠ Bouton non trouvé: {btn}")
        
        return True
    else:
        print(f"❌ Erreur HTTP {response.status_code}")
        return False

def main():
    print("=" * 60)
    print("TEST DES BOUTONS DU PANEL ADMIN")
    print("=" * 60)
    
    # Test de connexion
    token = test_login()
    
    # Test de la page admin
    test_admin_page()
    
    print("\n" + "=" * 60)
    print("✅ TESTS TERMINÉS!")
    print("=" * 60)
    print("\nPour tester manuellement:")
    print(f"1. Ouvrez: {BASE_URL}/admin")
    print("2. Connectez-vous avec: superadmin / Super@2024!")
    print("3. Testez les boutons:")
    print("   - Déconnexion (en haut à droite)")
    print("   - + Nouveau client")
    print("   - Voir les clients")
    print("   - etc.")
    print("\nVérifiez la console du navigateur (F12) pour les erreurs JavaScript")

if __name__ == "__main__":
    main()
