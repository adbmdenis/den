#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour synchroniser le mot de passe du superadmin avec config.py
"""

import sys
import sqlite3
import hashlib
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

def hash_password(password):
    """Hash le mot de passe avec SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

log("=" * 80)
log("SYNCHRONISATION DU MOT DE PASSE SUPERADMIN")
log("=" * 80)

# 1. Charger la configuration
log("\n1. Chargement de la configuration...")
try:
    from config import SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD, SUPER_ADMIN_EMAIL
    log(f"✅ Configuration chargée", "SUCCESS")
    log(f"   Username: {SUPER_ADMIN_USERNAME}", "INFO")
    log(f"   Password: {SUPER_ADMIN_PASSWORD}", "INFO")
    log(f"   Email: {SUPER_ADMIN_EMAIL}", "INFO")
except Exception as e:
    log(f"❌ Erreur: {e}", "ERROR")
    sys.exit(1)

# 2. Connexion à la base de données
log("\n2. Connexion à la base de données...")
try:
    import database as db
    conn = sqlite3.connect(db.DATABASE_PATH)
    cursor = conn.cursor()
    log(f"✅ Connecté à: {db.DATABASE_PATH}", "SUCCESS")
except Exception as e:
    log(f"❌ Erreur: {e}", "ERROR")
    sys.exit(1)

# 3. Vérifier si le superadmin existe
log("\n3. Recherche du superadmin...")
try:
    cursor.execute("SELECT id, username, password, is_active FROM admins WHERE username = ?", 
                   (SUPER_ADMIN_USERNAME,))
    admin = cursor.fetchone()
    
    if admin:
        admin_id, username, old_hash, is_active = admin
        log(f"✅ Superadmin trouvé", "SUCCESS")
        log(f"   ID: {admin_id}", "INFO")
        log(f"   Username: {username}", "INFO")
        log(f"   Is Active: {is_active}", "INFO")
        log(f"   Hash actuel: {old_hash[:50]}...", "INFO")
    else:
        log(f"⚠️  Superadmin non trouvé, création...", "WARNING")
        
        # Créer le superadmin
        new_hash = hash_password(SUPER_ADMIN_PASSWORD)
        cursor.execute("""
            INSERT INTO admins (username, password, email, is_super_admin, is_active, created_at)
            VALUES (?, ?, ?, 1, 1, datetime('now'))
        """, (SUPER_ADMIN_USERNAME, new_hash, SUPER_ADMIN_EMAIL))
        conn.commit()
        admin_id = cursor.lastrowid
        
        log(f"✅ Superadmin créé avec ID: {admin_id}", "SUCCESS")
        admin = (admin_id, SUPER_ADMIN_USERNAME, new_hash, 1)
        
except Exception as e:
    log(f"❌ Erreur: {e}", "ERROR")
    conn.close()
    sys.exit(1)

# 4. Mettre à jour le mot de passe
log("\n4. Mise à jour du mot de passe...")
try:
    new_hash = hash_password(SUPER_ADMIN_PASSWORD)
    
    log(f"   Ancien hash: {admin[2][:50]}...", "INFO")
    log(f"   Nouveau hash: {new_hash[:50]}...", "INFO")
    
    if admin[2] == new_hash:
        log(f"✅ Le mot de passe est déjà correct!", "SUCCESS")
    else:
        log(f"⚠️  Mise à jour nécessaire", "WARNING")
        
        cursor.execute("""
            UPDATE admins 
            SET password = ?, 
                login_attempts = 0, 
                locked_until = NULL,
                is_active = 1
            WHERE id = ?
        """, (new_hash, admin[0]))
        
        conn.commit()
        log(f"✅ Mot de passe mis à jour!", "SUCCESS")
    
except Exception as e:
    log(f"❌ Erreur: {e}", "ERROR")
    conn.close()
    sys.exit(1)

# 5. Vérification finale
log("\n5. Vérification finale...")
try:
    # Recharger l'admin
    cursor.execute("SELECT id, username, password, is_active FROM admins WHERE id = ?", (admin[0],))
    admin_check = cursor.fetchone()
    
    log(f"   ID: {admin_check[0]}", "INFO")
    log(f"   Username: {admin_check[1]}", "INFO")
    log(f"   Hash: {admin_check[2][:50]}...", "INFO")
    log(f"   Is Active: {admin_check[3]}", "INFO")
    
    # Vérifier avec db.verify_admin
    conn.close()
    
    result = db.verify_admin(SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD)
    if result:
        log(f"\n✅ VÉRIFICATION RÉUSSIE!", "SUCCESS")
        log(f"   Le mot de passe fonctionne correctement", "SUCCESS")
    else:
        log(f"\n❌ VÉRIFICATION ÉCHOUÉE!", "ERROR")
        log(f"   Le mot de passe ne fonctionne toujours pas", "ERROR")
        sys.exit(1)
    
except Exception as e:
    log(f"❌ Erreur: {e}", "ERROR")
    if conn:
        conn.close()
    sys.exit(1)

# Résumé
log("\n" + "=" * 80)
log("RÉSUMÉ")
log("=" * 80)
log(f"\n✅ Mot de passe synchronisé avec succès!", "SUCCESS")
log(f"\nIdentifiants de connexion:", "INFO")
log(f"   Username: {SUPER_ADMIN_USERNAME}", "INFO")
log(f"   Password: {SUPER_ADMIN_PASSWORD}", "INFO")
log(f"\n💡 Vous pouvez maintenant vous connecter sur:", "INFO")
log(f"   http://192.168.1.19:8888/login", "INFO")
log("\n" + "=" * 80)
