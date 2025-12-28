#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test de l'API après déploiement
"""

import sys
import requests
import json

def test_api(base_url):
    """Teste les endpoints principaux de l'API"""
    
    print("=" * 60)
    print(f"  TEST DE L'API : {base_url}")
    print("=" * 60)
    print()
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1 : Page d'accueil
    print("1️⃣  Test de la page d'accueil...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Page d'accueil accessible")
            tests_passed += 1
        else:
            print(f"   ❌ Erreur {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests_failed += 1
    
    # Test 2 : API Status
    print("\n2️⃣  Test de l'API status...")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API status : {data.get('status')}")
            print(f"   📺 Chaînes : {data.get('channels', 0)}")
            print(f"   🖥️  Serveur : {data.get('server')}")
            print(f"   🔌 Port : {data.get('port')}")
            tests_passed += 1
        else:
            print(f"   ❌ Erreur {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests_failed += 1
    
    # Test 3 : Types d'abonnements
    print("\n3️⃣  Test des types d'abonnements...")
    try:
        response = requests.get(f"{base_url}/api/subscription-types", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {len(data)} types d'abonnements disponibles")
            for sub_type in data[:3]:  # Afficher les 3 premiers
                print(f"      - {sub_type.get('name')} : {sub_type.get('duration_days')} jours")
            tests_passed += 1
        else:
            print(f"   ❌ Erreur {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests_failed += 1
    
    # Test 4 : Page de login
    print("\n4️⃣  Test de la page de login...")
    try:
        response = requests.get(f"{base_url}/login", timeout=10)
        if response.status_code == 200:
            print("   ✅ Page de login accessible")
            tests_passed += 1
        else:
            print(f"   ❌ Erreur {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests_failed += 1
    
    # Test 5 : Panel admin
    print("\n5️⃣  Test du panel admin...")
    try:
        response = requests.get(f"{base_url}/admin", timeout=10)
        if response.status_code == 200:
            print("   ✅ Panel admin accessible")
            tests_passed += 1
        else:
            print(f"   ❌ Erreur {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests_failed += 1
    
    # Test 6 : Espace client
    print("\n6️⃣  Test de l'espace client...")
    try:
        response = requests.get(f"{base_url}/client", timeout=10)
        if response.status_code == 200:
            print("   ✅ Espace client accessible")
            tests_passed += 1
        else:
            print(f"   ❌ Erreur {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests_failed += 1
    
    # Test 7 : API Xtream Codes (sans authentification)
    print("\n7️⃣  Test de l'API Xtream Codes...")
    try:
        response = requests.get(f"{base_url}/player_api.php", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'user_info' in data:
                print("   ✅ API Xtream Codes répond")
                print(f"      Auth : {data['user_info'].get('auth', 0)}")
                tests_passed += 1
            else:
                print("   ⚠️  API répond mais format inattendu")
                tests_failed += 1
        else:
            print(f"   ❌ Erreur {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests_failed += 1
    
    # Résumé
    print("\n" + "=" * 60)
    print("  RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"\n✅ Tests réussis : {tests_passed}")
    print(f"❌ Tests échoués : {tests_failed}")
    
    total = tests_passed + tests_failed
    success_rate = (tests_passed / total * 100) if total > 0 else 0
    
    print(f"\n📊 Taux de réussite : {success_rate:.1f}%")
    
    if tests_failed == 0:
        print("\n🎉 Tous les tests sont passés ! Votre serveur est opérationnel.")
        return 0
    elif success_rate >= 70:
        print("\n⚠️  La plupart des tests sont passés, mais il y a quelques problèmes.")
        return 1
    else:
        print("\n❌ Plusieurs tests ont échoué. Vérifiez la configuration.")
        return 2

def test_login(base_url, username, password):
    """Teste la connexion admin"""
    print("\n" + "=" * 60)
    print("  TEST DE CONNEXION ADMIN")
    print("=" * 60)
    print()
    
    try:
        response = requests.post(
            f"{base_url}/api/login",
            json={"username": username, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Connexion admin réussie !")
                print(f"   Token : {data.get('token')[:20]}...")
                print(f"   Admin : {data.get('admin', {}).get('username')}")
                print(f"   Super Admin : {data.get('admin', {}).get('is_super_admin')}")
                return 0
            else:
                print("❌ Connexion échouée")
                return 1
        else:
            print(f"❌ Erreur {response.status_code}")
            if response.status_code == 401:
                print("   Identifiants invalides")
            return 1
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return 1

def main():
    """Fonction principale"""
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} <URL>")
        print(f"  {sys.argv[0]} <URL> <username> <password>")
        print()
        print("Exemples:")
        print(f"  {sys.argv[0]} https://serveur-iptv.onrender.com")
        print(f"  {sys.argv[0]} https://serveur-iptv.onrender.com superadmin Super@2024!")
        return 1
    
    base_url = sys.argv[1].rstrip('/')
    
    # Tests de base
    result = test_api(base_url)
    
    # Test de connexion si identifiants fournis
    if len(sys.argv) >= 4:
        username = sys.argv[2]
        password = sys.argv[3]
        login_result = test_login(base_url, username, password)
        result = max(result, login_result)
    
    print("\n" + "=" * 60)
    return result

if __name__ == "__main__":
    sys.exit(main())
