#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug: Vérifie le HTML généré par admin_panel.py
"""

import sys
sys.path.insert(0, 'serveur_iptv')

from admin_panel import render_admin_panel

# Générer le HTML
html = render_admin_panel("192.168.1.1", "8080")

print("=" * 80)
print("ANALYSE DU HTML GÉNÉRÉ")
print("=" * 80)

# Statistiques
print(f"\n📊 Statistiques:")
print(f"   - Taille totale: {len(html)} caractères")
print(f"   - Nombre de lignes: {html.count(chr(10))}")
print(f"   - Blocs <script>: {html.count('<script>')}")
print(f"   - Blocs </script>: {html.count('</script>')}")

# Vérifier les fonctions
functions = [
    'function showModal',
    'function hideModal', 
    'function logout',
    'function loadClients',
    'function refreshChannels',
    'function showSection'
]

print(f"\n🔍 Fonctions JavaScript:")
for func in functions:
    found = func in html
    status = "✅" if found else "❌"
    print(f"   {status} {func}: {'TROUVÉE' if found else 'MANQUANTE'}")

# Trouver la position du script
script_pos = html.find('<script>')
if script_pos > 0:
    print(f"\n📍 Position du bloc <script>:")
    print(f"   - Commence à: caractère {script_pos}")
    print(f"   - Pourcentage du fichier: {(script_pos/len(html)*100):.1f}%")
    
    # Afficher les 500 premiers caractères du script
    script_start = html[script_pos:script_pos+500]
    print(f"\n📝 Début du bloc <script>:")
    print("   " + "-" * 76)
    for line in script_start.split('\n')[:15]:
        print(f"   {line}")
    print("   " + "-" * 76)
else:
    print(f"\n❌ ERREUR: Aucun bloc <script> trouvé!")

# Vérifier la fin du fichier
print(f"\n📝 Fin du fichier (derniers 200 caractères):")
print("   " + "-" * 76)
end_content = html[-200:]
for line in end_content.split('\n'):
    print(f"   {line}")
print("   " + "-" * 76)

# Vérifier les onclick
onclick_count = html.count('onclick=')
print(f"\n🖱️  Attributs onclick trouvés: {onclick_count}")

# Trouver les premiers onclick
import re
onclick_matches = re.findall(r'onclick="([^"]+)"', html)
if onclick_matches:
    print(f"\n📋 Premiers appels onclick:")
    for i, match in enumerate(onclick_matches[:10], 1):
        print(f"   {i}. {match}")

# Sauvegarder dans un fichier pour inspection
output_file = "serveur_iptv/debug_admin_output.html"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n💾 HTML sauvegardé dans: {output_file}")
print(f"   Ouvrez ce fichier dans un navigateur pour tester directement")

print("\n" + "=" * 80)
print("DIAGNOSTIC")
print("=" * 80)

issues = []
if html.count('<script>') == 0:
    issues.append("❌ CRITIQUE: Aucun bloc <script> trouvé!")
if html.count('<script>') != html.count('</script>'):
    issues.append("❌ CRITIQUE: Nombre de <script> et </script> différent!")
if 'function showModal' not in html:
    issues.append("❌ CRITIQUE: Fonction showModal manquante!")
if onclick_count > 0 and 'function showModal' not in html:
    issues.append("❌ CRITIQUE: Des onclick appellent showModal mais la fonction n'existe pas!")

if issues:
    print("\n⚠️  PROBLÈMES DÉTECTÉS:")
    for issue in issues:
        print(f"   {issue}")
else:
    print("\n✅ Aucun problème détecté dans la structure HTML")

print("\n" + "=" * 80)
