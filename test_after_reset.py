#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour tester le site après réinitialisation
"""

import requests
import sys

BASE_URL = "https://iptv-0e41.onrender.com"

def test_complete_workflow(username, password):
    """Teste le workflow complet"""
    
    print("=" * 60)
    print("  TEST COMPLET APRÈS RÉINITIALISATION")
    print("=" * 60)
    print(f"\nURL: {BASE_URL}")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)}")
    print()
    
    # Test 1: Connexion
    print("1️⃣  Test de connexion...")
    try:
        r = requests.post(
            f"{BASE_URL}/api/login",
            json={"username": username, "password": password},
            timeout=10
        )
        
        if r.status_code == 200:
            result = r.json()
            if result.get('success'):
                token = result.get('token')
                print("   ✅ Connexion réussie !")
                print(f"   Token: {token[:30]}...")
            else:
                print(f"   ❌ Échec: {result.get('error')}")
                return False
        else:
            print(f"   ❌ Erreur HTTP {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test 2: Statistiques (doivent être à 0)
    print("\n2️⃣  Test des statistiques...")
    try:
        r = requests.get(f"{BASE_URL}/api/admin/stats", headers=headers, timeout=10)
        if r.status_code == 200:
            stats = r.json()
            print("   ✅ Statistiques récupérées !")
            print(f"   Clients: {stats.get('total_clients', 0)}")
            print(f"   Abonnements: {stats.get('active_subscriptions', 0)}")
            print(f"   Ventes: {stats.get('total_sales', 0)}")
            
            if stats.get('total_clients', 0) == 0:
                print("   ✅ Base de données vide (normal après reset)")
        else:
            print(f"   ❌ Erreur: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False
    
    # Test 3: Statistiques chaînes
    print("\n3️⃣  Test des chaînes...")
    try:
        r = requests.get(f"{BASE_URL}/api/admin/channels/stats", headers=headers, timeout=10)
        if r.status_code == 200:
            stats = r.json()
            print("   ✅ Statistiques chaînes récupérées !")
            print(f"   Chaînes: {stats.get('total_channels', 0)}")
            print(f"   Films: {stats.get('total_movies', 0)}")
            print(f"   Séries: {stats.get('total_series', 0)}")
            print(f"   Token Vavoo: {'✅ Valide' if stats.get('token_valid') else '❌ Invalide'}")
        else:
            print(f"   ⚠️  Erreur: {r.status_code}")
    except Exception as e:
        print(f"   ⚠️  Exception: {e}")
    
    # Test 4: Créer un client de test
    print("\n4️⃣  Test de création de client...")
    try:
        import time
        client_data = {
            "username": f"testclient_{int(time.time())}",
            "password": "Test123!",
            "full_name": "Client Test",
            "email": "test@example.com"
        }
        
        r = requests.post(
            f"{BASE_URL}/api/admin/clients/create",
            headers=headers,
            json=client_data,
            timeout=10
        )
        
        if r.status_code == 200:
            result = r.json()
            if result.get('success'):
                print("   ✅ Client créé avec succès !")
                client = result.get('client', {})
                print(f"   Username: {client.get('username')}")
                print(f"   Token: {client.get('token', '')[:30]}...")
                return True
            else:
                print(f"   ❌ Échec: {result.get('error')}")
                return False
        else:
            print(f"   ❌ Erreur HTTP {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python test_after_reset.py <username> <password>")
        print()
        print("Exemple:")
        print("  python test_after_reset.py superadmin VotreMotDePasse2024!")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    success = test_complete_workflow(username, password)
    
    print("\n" + "=" * 60)
    if success:
        print("  ✅ TOUS LES TESTS SONT PASSÉS !")
        print("=" * 60)
        print("\n🎉 Votre serveur est opérationnel !")
        print("\nVous pouvez maintenant :")
        print("  - Créer des clients")
        print("  - Vendre des abonnements")
        print("  - Gérer les vendeurs")
        print("  - Rafraîchir les chaînes")
        print()
        print(f"Panel Admin: {BASE_URL}/admin")
        return 0
    else:
        print("  ❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("=" * 60)
        print("\n⚠️  Vérifiez :")
        print("  1. Les identifiants sont corrects")
        print("  2. Les variables d'environnement sur Render")
        print("  3. Le service a bien redémarré")
        print()
        print("Consultez SOLUTION_COMPLETE.md pour plus d'aide.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
