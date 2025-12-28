#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test: Vérifie ce que le serveur renvoie réellement
"""

import requests
import sys

SERVER_URL = "http://192.168.1.19:8888"

print("=" * 80)
print("TEST DE LA RÉPONSE DU SERVEUR")
print("=" * 80)

print(f"\n🌐 Connexion à: {SERVER_URL}/admin")

try:
    response = requests.get(f"{SERVER_URL}/admin", timeout=10)
    
    print(f"\n📊 Statistiques de la réponse:")
    print(f"   - Status code: {response.status_code}")
    print(f"   - Content-Type: {response.headers.get('Content-Type')}")
    print(f"   - Content-Length: {response.headers.get('Content-Length', 'Non spécifié')}")
    print(f"   - Taille réelle: {len(response.text)} caractères")
    
    html = response.text
    
    print(f"\n🔍 Analyse du HTML reçu:")
    print(f"   - Blocs <script>: {html.count('<script>')}")
    print(f"   - Blocs </script>: {html.count('</script>')}")
    print(f"   - Attributs onclick: {html.count('onclick=')}")
    
    # Vérifier les fonctions
    functions = [
        'function showModal',
        'function hideModal',
        'function logout',
        'function loadClients',
        'function refreshChannels'
    ]
    
    print(f"\n📋 Fonctions JavaScript:")
    missing = []
    for func in functions:
        found = func in html
        status = "✅" if found else "❌"
        print(f"   {status} {func}")
        if not found:
            missing.append(func)
    
    # Vérifier la fin du fichier
    print(f"\n📝 Fin du fichier (derniers 300 caractères):")
    print("   " + "-" * 76)
    end_content = html[-300:]
    for line in end_content.split('\n'):
        print(f"   {line[:76]}")
    print("   " + "-" * 76)
    
    # Chercher où se termine le script
    last_script_pos = html.rfind('</script>')
    if last_script_pos > 0:
        print(f"\n📍 Dernier </script> trouvé à: caractère {last_script_pos}")
        print(f"   Pourcentage du fichier: {(last_script_pos/len(html)*100):.1f}%")
        
        # Vérifier ce qu'il y a après
        after_script = html[last_script_pos:]
        print(f"\n📝 Contenu après </script>:")
        print("   " + "-" * 76)
        for line in after_script.split('\n'):
            print(f"   {line}")
        print("   " + "-" * 76)
    
    # Diagnostic
    print(f"\n" + "=" * 80)
    print("DIAGNOSTIC")
    print("=" * 80)
    
    if response.status_code != 200:
        print(f"\n❌ ERREUR: Status code {response.status_code}")
    elif html.count('<script>') == 0:
        print(f"\n❌ CRITIQUE: Aucun bloc <script> dans la réponse!")
    elif html.count('<script>') != html.count('</script>'):
        print(f"\n❌ CRITIQUE: Blocs <script> non fermés!")
    elif missing:
        print(f"\n❌ CRITIQUE: Fonctions manquantes: {', '.join(missing)}")
        print(f"\n💡 Le serveur coupe probablement la réponse avant la fin!")
        print(f"   Vérifiez les limites de buffer dans server.py")
    elif not html.endswith('</html>'):
        print(f"\n⚠️  ATTENTION: Le HTML ne se termine pas par </html>")
        print(f"   Derniers caractères: {repr(html[-50:])}")
    else:
        print(f"\n✅ Le serveur renvoie un HTML complet et valide!")
    
    # Sauvegarder pour inspection
    with open('serveur_iptv/server_response.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\n💾 Réponse sauvegardée dans: serveur_iptv/server_response.html")
    
except requests.exceptions.ConnectionError:
    print(f"\n❌ ERREUR: Impossible de se connecter au serveur")
    print(f"   Le serveur est-il démarré sur {SERVER_URL}?")
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
