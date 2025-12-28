#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test du serveur IPTV Production
"""

import requests
import sys
import time

BASE_URL = "http://localhost:8888"

def test_server():
    """Teste le serveur local"""
    
    print("=" * 60)
    print("  TEST DU SERVEUR IPTV PRODUCTION")
    print("=" * 60)
    print(f"\nURL: {BASE_URL}")
    print()
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Page d'accueil
    print("1️⃣  Test de la page d'accueil...")
    try:
        r = requests.get(f"{BASE_URL}/", timeout=5)
        if r.status_code == 200:
            print("   ✅ Page d'accueil accessible")
            tests_passed += 1
        else:
            print(f"   ❌ Erreur {r.status_code}")
            tests_failed += 1
    except requests.exceptions.ConnectionError:
        print("   ❌ Serveur non accessible - Est-il démarré ?")
        print("\n💡 Démarrez le serveur avec : python server.py")
        return False
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests_failed += 1
    
    # Test 2: API Status
    print("\n2️⃣  Test de l'API status...")
    try:
        r = requests.get(f"{BASE_URL}/api/status", timeout=5)
        if r.status_code == 200:
            data = r.json()
            print(f"   ✅ API status : {data.get('status')}")
            print(f"   📺 Chaînes : {data.get('channels', 0)}")
            tests_passed += 1
        else:
            print(f"   ❌ Erreur {r.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests_failed += 1
    
    # Test 3: Page de login
    print("\n3️⃣  Test de la page de login...")
    try:
        r = requests.get(f"{BASE_URL}/login", timeout=5)
        if r.status_code == 200:
            print("   ✅ Page de login accessible")
            tests_passed += 1
        else:
            print(f"   ❌ Erreur {r.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests_failed += 1
    
    # Test 4: Panel admin
    print("\n4️⃣  Test du panel admin...")
    try:
        r = requests.get(f"{BASE_URL}/admin", timeout=5)
        if r.status_code == 200:
            print("   ✅ Panel admin accessible")
            tests_passed += 1
        else:
            print(f"   ❌ Erreur {r.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests_failed += 1
    
    # Test 5: Connexion admin
    print("\n5️⃣  Test de connexion admin...")
    try:
        r = requests.post(
            f"{BASE_URL}/api/login",
            json={"username": "superadmin", "password": "Super@2024!"},
            timeout=5
        )
        if r.status_code == 200:
            result = r.json()
            if result.get('success'):
                print("   ✅ Connexion admin réussie")
                tests_passed += 1
            else:
                print(f"   ❌ Échec : {result.get('error')}")
                tests_failed += 1
        else:
            print(f"   ❌ Erreur {r.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests_failed += 1
    
    # Résumé
    print("\n" + "=" * 60)
    print("  RÉSUMÉ")
    print("=" * 60)
    
    total = tests_passed + tests_failed
    print(f"\n✅ Tests réussis : {tests_passed}/{total}")
    print(f"❌ Tests échoués : {tests_failed}/{total}")
    
    if tests_failed == 0:
        print("\n🎉 Tous les tests sont passés !")
        print("\n📝 Prochaines étapes :")
        print("  1. Ouvrez http://localhost:8888/admin")
        print("  2. Connectez-vous avec : superadmin / Super@2024!")
        print("  3. Créez un client de test")
        print("  4. Vendez un abonnement")
        return True
    else:
        print("\n⚠️  Certains tests ont échoué")
        print("\n💡 Vérifiez :")
        print("  - Le serveur est démarré")
        print("  - Le port 8888 est disponible")
        print("  - Les dépendances sont installées")
        return False

if __name__ == "__main__":
    print("\n⏳ Attente du démarrage du serveur...")
    time.sleep(2)
    
    success = test_server()
    sys.exit(0 if success else 1)
