#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script pour corriger complètement admin_panel.py"""

import shutil

# Copier le fichier original
shutil.copy('../admin_panel.py', 'admin_panel.py')

# Lire le fichier
with open('admin_panel.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Trouver la position où insérer les fonctions utilitaires
# Elles doivent être AVANT la fermeture du premier </script>
# et AVANT l'appel à get_admin_js2()

# Chercher la ligne "function loadLogs()" et ajouter les fonctions après
search_text = '''function loadLogs(){{
fetch("/api/admin/logs?limit=100",{{headers:H()}}).then(r=>r.json()).then(logs=>{{
var h=logs.map(l=>'<tr><td>'+new Date(l.created_at).toLocaleString()+'</td><td>'+l.action+'</td><td>'+(l.details||"-")+'</td><td>'+(l.ip_address||"-")+'</td></tr>').join("");
document.getElementById("logs-table").innerHTML=h||'<tr><td colspan="4">Aucun</td></tr>';
}});
}}
</script>
""" + get_admin_js2(local_ip, port)'''

replacement_text = '''function loadLogs(){{
fetch("/api/admin/logs?limit=100",{{headers:H()}}).then(r=>r.json()).then(logs=>{{
var h=logs.map(l=>'<tr><td>'+new Date(l.created_at).toLocaleString()+'</td><td>'+l.action+'</td><td>'+(l.details||"-")+'</td><td>'+(l.ip_address||"-")+'</td></tr>').join("");
document.getElementById("logs-table").innerHTML=h||'<tr><td colspan="4">Aucun</td></tr>';
}});
}}

// ===== FONCTIONS UTILITAIRES =====
function showModal(id){{document.getElementById(id).classList.add("active");}}
function hideModal(id){{document.getElementById(id).classList.remove("active");}}
function logout(){{localStorage.removeItem("admin_token");localStorage.removeItem("admin_info");window.location.href="/login";}}
function copyText(t){{navigator.clipboard.writeText(t).then(()=>alert("Copie!"));}}
function refreshChannels(){{
if(!confirm("Rafraîchir toutes les chaînes depuis Vavoo?\\nCela peut prendre 1-2 minutes."))return;
var btn=event.target;
btn.disabled=true;
btn.textContent="⏳ Rafraîchissement...";
fetch("/api/admin/channels/refresh",{{method:"POST",headers:H()}}).then(r=>r.json()).then(res=>{{
btn.disabled=false;
btn.textContent="🔄 Rafraîchir chaînes";
if(res.success){{
alert("✅ Chaînes mises à jour!\\n\\nChaînes: "+res.stats.total_channels+"\\nFilms: "+res.stats.total_movies+"\\nSéries: "+res.stats.total_series);
loadStats();
}}else alert("❌ Erreur: "+res.error);
}}).catch(e=>{{
btn.disabled=false;
btn.textContent="🔄 Rafraîchir chaînes";
alert("❌ Erreur: "+e);
}});
}}
</script>
""" + get_admin_js2(local_ip, port)'''

# Remplacer
if search_text in content:
    content = content.replace(search_text, replacement_text)
    print("✅ Fonctions utilitaires ajoutées dans le script principal")
else:
    print("❌ Pattern de recherche non trouvé")
    print("Tentative de correction alternative...")
    
    # Alternative: chercher juste avant </script>
    search_alt = '''}}
</script>
""" + get_admin_js2(local_ip, port)'''
    
    replacement_alt = '''}}

// ===== FONCTIONS UTILITAIRES =====
function showModal(id){{document.getElementById(id).classList.add("active");}}
function hideModal(id){{document.getElementById(id).classList.remove("active");}}
function logout(){{localStorage.removeItem("admin_token");localStorage.removeItem("admin_info");window.location.href="/login";}}
function copyText(t){{navigator.clipboard.writeText(t).then(()=>alert("Copie!"));}}
function refreshChannels(){{
if(!confirm("Rafraîchir toutes les chaînes depuis Vavoo?\\nCela peut prendre 1-2 minutes."))return;
var btn=event.target;
btn.disabled=true;
btn.textContent="⏳ Rafraîchissement...";
fetch("/api/admin/channels/refresh",{{method:"POST",headers:H()}}).then(r=>r.json()).then(res=>{{
btn.disabled=false;
btn.textContent="🔄 Rafraîchir chaînes";
if(res.success){{
alert("✅ Chaînes mises à jour!\\n\\nChaînes: "+res.stats.total_channels+"\\nFilms: "+res.stats.total_movies+"\\nSéries: "+res.stats.total_series);
loadStats();
}}else alert("❌ Erreur: "+res.error);
}}).catch(e=>{{
btn.disabled=false;
btn.textContent="🔄 Rafraîchir chaînes";
alert("❌ Erreur: "+e);
}});
}}
</script>
""" + get_admin_js2(local_ip, port)'''
    
    if search_alt in content:
        content = content.replace(search_alt, replacement_alt)
        print("✅ Fonctions utilitaires ajoutées (méthode alternative)")

# Maintenant supprimer les doublons dans get_admin_js2
# Chercher et supprimer les 4 lignes à la fin de get_admin_js2
old_end = '''function copyText(t){{navigator.clipboard.writeText(t).then(()=>alert("Copie!"));}}
function showModal(id){{document.getElementById(id).classList.add("active");}}
function hideModal(id){{document.getElementById(id).classList.remove("active");}}
function logout(){{localStorage.removeItem("admin_token");localStorage.removeItem("admin_info");window.location.href="/login";}}
</script></body></html>"""'''

new_end = '''</script></body></html>"""'''

if old_end in content:
    content = content.replace(old_end, new_end)
    print("✅ Doublons supprimés de get_admin_js2()")

# Écrire le fichier corrigé
with open('admin_panel.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*60)
print("✅ FICHIER admin_panel.py CORRIGÉ!")
print("="*60)
print("\nFonctions ajoutées dans le script principal:")
print("  - showModal()")
print("  - hideModal()")
print("  - logout()")
print("  - copyText()")
print("  - refreshChannels()")
print("\nRedémarrez le serveur pour tester les changements.")
