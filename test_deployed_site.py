#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnostic pour le site déployé sur Render
"""

import requests
import sys

def test_site(base_url):
    """Teste le site déployé"""
    print("=" * 60)
    print(f"  DIAGNOSTIC DU SITE : {base_url}")
    print("=" * 60)
    print()
    
    tests = []
    
    # Test 1 : Page d'accueil
    print("1️⃣  Test de la page d'accueil...")
    try:
        r = requests.get(f"{base_url}/", timeout=10)
        if r.status_code == 200:
            print(f"   ✅ OK ({len(r.text)} caractères)")
            tests.append(True)
        else:
            print(f"   ❌ Erreur {r.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests.append(False)
    
    # Test 2 : Page de login
    print("\n2️⃣  Test de la page de login...")
    try:
        r = requests.get(f"{base_url}/login", timeout=10)
        if r.status_code == 200:
            print(f"   ✅ OK ({len(r.text)} caractères)")
            if "loginForm" in r.text:
                print("   ✅ Formulaire de login présent")
            else:
                print("   ⚠️  Formulaire de login manquant")
            tests.append(True)
        else:
            print(f"   ❌ Erreur {r.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests.append(False)
    
    # Test 3 : Panel admin (sans auth)
    print("\n3️⃣  Test du panel admin...")
    try:
        r = requests.get(f"{base_url}/admin", timeout=10)
        if r.status_code == 200:
            print(f"   ✅ OK ({len(r.text)} caractères)")
            
            # Vérifier les éléments clés
            checks = {
                "stats-box": "Boîte de statistiques",
                "loadStats": "Fonction loadStats",
                "loadClients": "Fonction loadClients",
                "showSection": "Fonction showSection",
                "dashboard": "Section dashboard"
            }
            
            for key, desc in checks.items():
                if key in r.text:
                    print(f"   ✅ {desc} présent")
                else:
                    print(f"   ❌ {desc} MANQUANT")
            
            tests.append(True)
        else:
            print(f"   ❌ Erreur {r.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests.append(False)
    
    # Test 4 : API Status
    print("\n4️⃣  Test de l'API status...")
    try:
        r = requests.get(f"{base_url}/api/status", timeout=10)
        if r.status_code == 200:
            data = r.json()
            print(f"   ✅ API répond")
            print(f"   📊 Status : {data.get('status')}")
            print(f"   📺 Chaînes : {data.get('channels', 0)}")
            tests.append(True)
        else:
            print(f"   ❌ Erreur {r.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests.append(False)
    
    # Test 5 : Erreurs JavaScript
    print("\n5️⃣  Recherche d'erreurs JavaScript potentielles...")
    try:
        r = requests.get(f"{base_url}/admin", timeout=10)
        if r.status_code == 200:
            # Chercher des patterns d'erreurs communes
            errors = []
            
            if "{{" in r.text and not "{{{{" in r.text:
                errors.append("Doubles accolades non échappées détectées")
            
            if "function (" in r.text:
                errors.append("Syntaxe de fonction incorrecte détectée")
            
            if "undefined" in r.text.lower():
                errors.append("Références 'undefined' détectées")
            
            if errors:
                print("   ⚠️  Erreurs potentielles détectées :")
                for err in errors:
                    print(f"      - {err}")
            else:
                print("   ✅ Aucune erreur évidente détectée")
            
            tests.append(len(errors) == 0)
        else:
            tests.append(False)
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        tests.append(False)
    
    # Résumé
    print("\n" + "=" * 60)
    print("  RÉSUMÉ")
    print("=" * 60)
    
    passed = sum(tests)
    total = len(tests)
    
    print(f"\n✅ Tests réussis : {passed}/{total}")
    print(f"❌ Tests échoués : {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 Tous les tests sont passés !")
        return 0
    elif passed >= total * 0.7:
        print("\n⚠️  La plupart des tests passent, mais il y a des problèmes.")
        return 1
    else:
        print("\n❌ Plusieurs tests ont échoué.")
        return 2

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_deployed_site.py <URL>")
        print("Exemple: python test_deployed_site.py https://iptv-0e41.onrender.com")
        sys.exit(1)
    
    url = sys.argv[1].rstrip('/')
    sys.exit(test_site(url))
