#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour réinitialiser le mot de passe du super admin
À exécuter LOCALEMENT avec accès à la base de données
"""

import sqlite3
import hashlib
import sys

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def reset_password(db_path, new_password):
    """Réinitialise le mot de passe du super admin"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Trouver le super admin
        cursor.execute("SELECT id, username FROM admins WHERE is_super_admin = 1")
        admin = cursor.fetchone()
        
        if not admin:
            print("❌ Aucun super admin trouvé dans la base de données")
            return False
        
        admin_id, username = admin
        print(f"✅ Super admin trouvé: {username} (ID: {admin_id})")
        
        # Mettre à jour le mot de passe
        hashed = hash_password(new_password)
        cursor.execute("""
            UPDATE admins 
            SET password = ?, login_attempts = 0, locked_until = NULL 
            WHERE id = ?
        """, (hashed, admin_id))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Mot de passe réinitialisé avec succès !")
        print(f"\nNouvelles identifiants:")
        print(f"  Username: {username}")
        print(f"  Password: {new_password}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  RÉINITIALISATION DU MOT DE PASSE SUPER ADMIN")
    print("=" * 60)
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python reset_admin_password.py <nouveau_mot_de_passe>")
        print()
        print("Exemple:")
        print("  python reset_admin_password.py MonNouveauMotDePasse123!")
        sys.exit(1)
    
    new_password = sys.argv[1]
    db_path = "database.db"
    
    print(f"Base de données: {db_path}")
    print(f"Nouveau mot de passe: {new_password}")
    print()
    
    confirm = input("Confirmer la réinitialisation? (oui/non): ")
    if confirm.lower() not in ['oui', 'yes', 'o', 'y']:
        print("❌ Annulé")
        sys.exit(0)
    
    if reset_password(db_path, new_password):
        print("\n✅ Réinitialisation terminée !")
    else:
        print("\n❌ Échec de la réinitialisation")
        sys.exit(1)
