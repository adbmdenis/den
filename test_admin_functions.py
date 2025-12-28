#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test détaillé des fonctionnalités admin
"""

import requests
import json

BASE_URL = "https://iptv-0e41.onrender.com"

def test_login():
    """Test de connexion admin"""
    print("=" * 60)
    print("TEST 1 : CONNEXION ADMIN")
    print("=" * 60)
    
    data = {
        "username": "superadmin",
        "password": "Super@2024!"
    }
    
    try:
        r = requests.post(f"{BASE_URL}/api/login", json=data, timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Réponse: {r.text[:500]}")
        
        if r.status_code == 200:
            result = r.json()
            if result.get('success'):
                print("✅ Connexion réussie !")
                print(f"Token: {result.get('token')[:30]}...")
                return result.get('token')
            else:
                print(f"❌ Échec: {result.get('error')}")
                return None
        else:
            print(f"❌ Erreur HTTP {r.status_code}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_stats(token):
    """Test des statistiques"""
    print("\n" + "=" * 60)
    print("TEST 2 : STATISTIQUES")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        r = requests.get(f"{BASE_URL}/api/admin/stats", headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            stats = r.json()
            print("✅ Statistiques récupérées !")
            print(json.dumps(stats, indent=2))
            return True
        else:
            print(f"❌ Erreur: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_create_client(token):
    """Test de création de client"""
    print("\n" + "=" * 60)
    print("TEST 3 : CRÉATION DE CLIENT")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "username": f"testclient_{int(__import__('time').time())}",
        "password": "Test123!",
        "full_name": "Client Test",
        "email": "test@example.com",
        "phone": "0123456789"
    }
    
    print(f"Données: {json.dumps(data, indent=2)}")
    
    try:
        r = requests.post(f"{BASE_URL}/api/admin/clients/create", 
                         headers=headers, json=data, timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Réponse: {r.text[:500]}")
        
        if r.status_code == 200:
            result = r.json()
            if result.get('success'):
                print("✅ Client créé avec succès !")
                print(f"Client ID: {result.get('client', {}).get('id')}")
                print(f"Username: {result.get('client', {}).get('username')}")
                print(f"Token: {result.get('client', {}).get('token')[:30]}...")
                return result.get('client')
            else:
                print(f"❌ Échec: {result.get('error')}")
                return None
        else:
            print(f"❌ Erreur HTTP {r.status_code}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_subscription_types(token):
    """Test des types d'abonnements"""
    print("\n" + "=" * 60)
    print("TEST 4 : TYPES D'ABONNEMENTS")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        r = requests.get(f"{BASE_URL}/api/admin/subscription-types", 
                        headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            types = r.json()
            print(f"✅ {len(types)} types d'abonnements trouvés !")
            for t in types:
                print(f"  - {t.get('name')}: {t.get('duration_days')}j - {t.get('price')}€")
            return types
        else:
            print(f"❌ Erreur: {r.text[:200]}")
            return []
    except Exception as e:
        print(f"❌ Exception: {e}")
        return []

def test_channels_stats(token):
    """Test des stats des chaînes"""
    print("\n" + "=" * 60)
    print("TEST 5 : STATISTIQUES CHAÎNES")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        r = requests.get(f"{BASE_URL}/api/admin/channels/stats", 
                        headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            stats = r.json()
            print("✅ Statistiques chaînes récupérées !")
            print(json.dumps(stats, indent=2))
            return True
        else:
            print(f"❌ Erreur: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_admin_page():
    """Test de la page admin HTML"""
    print("\n" + "=" * 60)
    print("TEST 6 : PAGE ADMIN HTML")
    print("=" * 60)
    
    try:
        r = requests.get(f"{BASE_URL}/admin", timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Taille: {len(r.text)} caractères")
        
        # Vérifier les éléments clés
        checks = {
            "newClientModal": "Modal nouveau client",
            "sellModal": "Modal vente",
            "loadStats": "Fonction loadStats",
            "createClient": "Fonction createClient",
            "showModal": "Fonction showModal",
            "stats-box": "Boîte de stats"
        }
        
        missing = []
        for key, desc in checks.items():
            if key in r.text:
                print(f"  ✅ {desc}")
            else:
                print(f"  ❌ {desc} MANQUANT")
                missing.append(desc)
        
        if missing:
            print(f"\n⚠️  {len(missing)} éléments manquants")
            return False
        else:
            print("\n✅ Tous les éléments présents")
            return True
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    print("🔍 TEST COMPLET DES FONCTIONNALITÉS ADMIN")
    print("URL:", BASE_URL)
    print()
    
    # Test 1: Login
    token = test_login()
    if not token:
        print("\n❌ ARRÊT: Impossible de se connecter")
        return
    
    # Test 2: Stats
    test_stats(token)
    
    # Test 3: Créer un client
    client = test_create_client(token)
    
    # Test 4: Types d'abonnements
    types = test_subscription_types(token)
    
    # Test 5: Stats chaînes
    test_channels_stats(token)
    
    # Test 6: Page HTML
    test_admin_page()
    
    print("\n" + "=" * 60)
    print("FIN DES TESTS")
    print("=" * 60)

if __name__ == "__main__":
    main()
