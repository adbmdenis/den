#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger le fichier admin_panel.py
Ajoute les fonctions JavaScript manquantes au bon endroit
"""

import re

def fix_admin_panel():
    """Corrige le fichier admin_panel.py"""
    
    print("=" * 60)
    print("  CORRECTION DU FICHIER ADMIN_PANEL.PY")
    print("=" * 60)
    print()
    
    try:
        # Lire le fichier
        with open("admin_panel.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        print("✅ Fichier lu")
        
        # Vérifier si les fonctions sont présentes
        if "function showModal" in content and "function hideModal" in content:
            print("✅ Les fonctions showModal et hideModal sont présentes")
            
            # Vérifier si elles sont au bon endroit
            # Elles doivent être AVANT la fermeture du script principal
            
            # Trouver la position de la fonction get_admin_js2
            if "def get_admin_js2" in content:
                print("⚠️  Les fonctions sont dans get_admin_js2 (séparées)")
                print("   Elles doivent être dans le script principal")
                
                # Solution : Ajouter les fonctions dans le script principal
                # Chercher la ligne avant </script></body></html> dans render_admin_panel
                
                # Pattern à chercher
                pattern = r'(document\.getElementById\("pwdForm"\)\.onsubmit=changePwd;)\s*\}\}\);'
                
                # Remplacement avec les fonctions ajoutées
                replacement = r'\1\n\n// Fonctions utilitaires\nfunction showModal(id){document.getElementById(id).classList.add("active");}\nfunction hideModal(id){document.getElementById(id).classList.remove("active");}\nfunction logout(){localStorage.removeItem("admin_token");localStorage.removeItem("admin_info");window.location.href="/login";}\nfunction copyText(t){navigator.clipboard.writeText(t).then(()=>alert("Copie!"));}\n});'
                
                new_content = re.sub(pattern, replacement, content)
                
                if new_content != content:
                    # Sauvegarder
                    with open("admin_panel.py", "w", encoding="utf-8") as f:
                        f.write(new_content)
                    
                    print("✅ Fichier corrigé et sauvegardé")
                    print("\n📝 Les fonctions ont été ajoutées au script principal")
                    return True
                else:
                    print("⚠️  Pattern non trouvé, correction manuelle nécessaire")
                    return False
            else:
                print("✅ Structure correcte")
                return True
        else:
            print("❌ Fonctions showModal/hideModal manquantes")
            return False
            
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

if __name__ == "__main__":
    success = fix_admin_panel()
    
    if success:
        print("\n✅ Correction terminée !")
        print("\n🚀 Redémarrez le serveur :")
        print("   python server.py")
    else:
        print("\n❌ Correction échouée")
        print("\n💡 Solution manuelle :")
        print("   Ajoutez ces lignes dans le script principal de render_admin_panel :")
        print("""
function showModal(id){document.getElementById(id).classList.add("active");}
function hideModal(id){document.getElementById(id).classList.remove("active");}
function logout(){localStorage.removeItem("admin_token");localStorage.removeItem("admin_info");window.location.href="/login";}
function copyText(t){navigator.clipboard.writeText(t).then(()=>alert("Copie!"));}
""")
