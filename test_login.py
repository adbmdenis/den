#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de connexion superadmin
"""

import sys
import json
import requests
from datetime import datetime

def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }
    color = colors.get(level, colors["INFO"])
    reset = colors["RESET"]
    print(f"{color}[{timestamp}] [{level}] {msg}{reset}")

log("=" * 80)
log("TEST DE CONNEXION SUPERADMIN")
log("=" * 80)

# 1. Vérifier la configuration
log("\n1. Vérification de la configuration...")
try:
    from config import SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD, SECRET_KEY
    log(f"✅ Configuration chargée", "SUCCESS")
    log(f"   Username: {SUPER_ADMIN_USERNAME}", "INFO")
    log(f"   Password: {'*' * len(SUPER_ADMIN_PASSWORD)}", "INFO")
    log(f"   SECRET_KEY: {SECRET_KEY[:20]}...", "INFO")
except Exception as e:
    log(f"❌ Erreur config: {e}", "ERROR")
    sys.exit(1)

# 2. Vérifier la base de données
log("\n2. Vérification de la base de données...")
try:
    import database as db
    
    # Initialiser la DB
    db.init_database()
    log(f"✅ Base de données initialisée", "SUCCESS")
    
    # Chercher le superadmin
    admin = db.get_admin_by_username(SUPER_ADMIN_USERNAME)
    if admin:
        log(f"✅ Superadmin trouvé dans la DB", "SUCCESS")
        log(f"   ID: {admin['id']}", "INFO")
        log(f"   Username: {admin['username']}", "INFO")
        log(f"   Email: {admin.get('email', 'N/A')}", "INFO")
        log(f"   Is Super Admin: {admin['is_super_admin']}", "INFO")
        log(f"   Is Active: {admin['is_active']}", "INFO")
        log(f"   Password Hash: {admin['password'][:30]}...", "INFO")
    else:
        log(f"❌ Superadmin NON TROUVÉ dans la DB!", "ERROR")
        log(f"   Création du superadmin...", "WARNING")
        
        # Créer le superadmin
        from config import SUPER_ADMIN_EMAIL
        admin_id = db.create_super_admin(
            SUPER_ADMIN_USERNAME,
            SUPER_ADMIN_PASSWORD,
            SUPER_ADMIN_EMAIL
        )
        
        if admin_id:
            log(f"✅ Superadmin créé avec ID: {admin_id}", "SUCCESS")
            admin = db.get_admin_by_username(SUPER_ADMIN_USERNAME)
        else:
            log(f"❌ Échec création superadmin", "ERROR")
            sys.exit(1)
    
except Exception as e:
    log(f"❌ Erreur DB: {e}", "ERROR")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 3. Test de vérification du mot de passe
log("\n3. Test de vérification du mot de passe...")
try:
    # Test avec le bon mot de passe
    result = db.verify_admin(SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD)
    if result:
        log(f"✅ Vérification mot de passe: SUCCÈS", "SUCCESS")
        log(f"   Admin retourné: {result['username']}", "INFO")
    else:
        log(f"❌ Vérification mot de passe: ÉCHEC", "ERROR")
        log(f"   Le mot de passe dans config.py ne correspond pas au hash dans la DB!", "ERROR")
        
        # Afficher le hash actuel
        import sqlite3
        conn = sqlite3.connect(db.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM admins WHERE username = ?", (SUPER_ADMIN_USERNAME,))
        row = cursor.fetchone()
        if row:
            log(f"   Hash dans DB: {row[0][:50]}...", "INFO")
        conn.close()
        
        # Proposer de réinitialiser
        log(f"\n💡 Solution: Réinitialiser le mot de passe", "WARNING")
        log(f"   Exécutez: python reset_admin_password.py", "WARNING")
    
    # Test avec un mauvais mot de passe
    result_bad = db.verify_admin(SUPER_ADMIN_USERNAME, "mauvais_password")
    if result_bad:
        log(f"⚠️  ATTENTION: Mauvais mot de passe accepté!", "WARNING")
    else:
        log(f"✅ Mauvais mot de passe rejeté correctement", "SUCCESS")
        
except Exception as e:
    log(f"❌ Erreur vérification: {e}", "ERROR")
    import traceback
    traceback.print_exc()

# 4. Test de l'API de login
log("\n4. Test de l'API de login...")
SERVER_URL = "http://192.168.1.19:8888"

try:
    # Préparer les données
    login_data = {
        "username": SUPER_ADMIN_USERNAME,
        "password": SUPER_ADMIN_PASSWORD
    }
    
    log(f"   Envoi de la requête POST à {SERVER_URL}/api/login", "INFO")
    log(f"   Données: {json.dumps(login_data, indent=2)}", "INFO")
    
    # Envoyer la requête
    response = requests.post(
        f"{SERVER_URL}/api/login",
        json=login_data,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    log(f"\n   Status Code: {response.status_code}", "INFO")
    log(f"   Headers: {dict(response.headers)}", "INFO")
    
    try:
        response_data = response.json()
        log(f"   Réponse: {json.dumps(response_data, indent=2)}", "INFO")
    except:
        log(f"   Réponse (texte): {response.text[:200]}", "INFO")
    
    if response.status_code == 200:
        log(f"\n✅ LOGIN RÉUSSI!", "SUCCESS")
        if 'token' in response_data:
            log(f"   Token: {response_data['token'][:50]}...", "SUCCESS")
        if 'admin' in response_data:
            log(f"   Admin: {response_data['admin']}", "SUCCESS")
    else:
        log(f"\n❌ LOGIN ÉCHOUÉ!", "ERROR")
        log(f"   Code: {response.status_code}", "ERROR")
        if 'error' in response_data:
            log(f"   Erreur: {response_data['error']}", "ERROR")
        
except requests.exceptions.ConnectionError:
    log(f"❌ Impossible de se connecter au serveur", "ERROR")
    log(f"   Le serveur est-il démarré sur {SERVER_URL}?", "ERROR")
except Exception as e:
    log(f"❌ Erreur API: {e}", "ERROR")
    import traceback
    traceback.print_exc()

# 5. Vérifier le code de server.py
log("\n5. Vérification du code de login dans server.py...")
try:
    with open('server.py', 'r', encoding='utf-8') as f:
        server_code = f.read()
    
    # Chercher la route /api/login
    if 'def do_POST' in server_code:
        log(f"✅ Méthode do_POST trouvée", "SUCCESS")
    else:
        log(f"❌ Méthode do_POST non trouvée", "ERROR")
    
    if '/api/login' in server_code:
        log(f"✅ Route /api/login trouvée", "SUCCESS")
    else:
        log(f"❌ Route /api/login non trouvée", "ERROR")
    
    if 'db.verify_admin' in server_code:
        log(f"✅ Appel à db.verify_admin trouvé", "SUCCESS")
    else:
        log(f"❌ Appel à db.verify_admin non trouvé", "ERROR")
        
except Exception as e:
    log(f"⚠️  Impossible de lire server.py: {e}", "WARNING")

# Résumé
log("\n" + "=" * 80)
log("RÉSUMÉ DU DIAGNOSTIC")
log("=" * 80)

issues = []
if not admin:
    issues.append("❌ Superadmin non trouvé dans la DB")
elif not admin['is_active']:
    issues.append("❌ Superadmin désactivé")
elif not result:
    issues.append("❌ Mot de passe incorrect dans la DB")

if issues:
    log("\n⚠️  PROBLÈMES DÉTECTÉS:", "WARNING")
    for issue in issues:
        log(f"   {issue}", "ERROR")
    
    log("\n💡 SOLUTIONS:", "WARNING")
    log("   1. Réinitialiser le mot de passe:", "INFO")
    log("      python serveur_iptv/reset_admin_password.py", "INFO")
    log("\n   2. Ou recréer la base de données:", "INFO")
    log("      python serveur_iptv/reset_database.py", "INFO")
else:
    log("\n✅ Aucun problème détecté dans la configuration", "SUCCESS")
    log("\n💡 Si le login échoue toujours:", "INFO")
    log("   - Vérifiez que le serveur est bien redémarré", "INFO")
    log("   - Videz le cache du navigateur", "INFO")
    log("   - Vérifiez la console du navigateur (F12)", "INFO")

log("\n" + "=" * 80)
