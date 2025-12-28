#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour trouver les identifiants admin corrects
"""

import requests

BASE_URL = "https://iptv-0e41.onrender.com"

# Liste des combinaisons possibles
CREDENTIALS = [
    ("superadmin", "Super@2024!"),
    ("superadmin", "superadmin"),
    ("admin", "admin"),
    ("admin", "Admin@2024!"),
    ("superadmin", "admin123"),
    ("admin", "admin123"),
]

def test_login(username, password):
    """Teste une combinaison username/password"""
    try:
        r = requests.post(
            f"{BASE_URL}/api/login",
            json={"username": username, "password": password},
            timeout=10
        )
        
        if r.status_code == 200:
            result = r.json()
            if result.get('success'):
                return True, result.get('token')
        
        return False, None
    except:
        return False, None

def main():
    print("=" * 60)
    print("  RECHERCHE DES IDENTIFIANTS ADMIN")
    print("=" * 60)
    print(f"\nURL: {BASE_URL}")
    print(f"\nTest de {len(CREDENTIALS)} combinaisons...\n")
    
    for i, (username, password) in enumerate(CREDENTIALS, 1):
        print(f"{i}. Test: {username} / {password[:3]}{'*' * (len(password)-3)}", end=" ... ")
        
        success, token = test_login(username, password)
        
        if success:
            print("✅ TROUVÉ !")
            print("\n" + "=" * 60)
            print("  IDENTIFIANTS CORRECTS")
            print("=" * 60)
            print(f"\nUsername: {username}")
            print(f"Password: {password}")
            print(f"\nToken: {token[:30]}...")
            print("\n✅ Utilisez ces identifiants pour vous connecter !")
            print("=" * 60)
            return
        else:
            print("❌")
    
    print("\n" + "=" * 60)
    print("  AUCUNE COMBINAISON TROUVÉE")
    print("=" * 60)
    print("\n⚠️  Les identifiants ne sont pas dans la liste testée.")
    print("\nSolutions:")
    print("1. Vérifiez les variables d'environnement sur Render")
    print("2. Consultez FIX_LOGIN_PROBLEM.md")
    print("3. Redéployez avec de nouveaux identifiants")

if __name__ == "__main__":
    main()
