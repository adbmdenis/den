#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour réinitialiser la base de données
"""

import os
import sys
from datetime import datetime

def reset_database():
    """Réinitialise la base de données"""
    
    print("=" * 60)
    print("  RÉINITIALISATION DE LA BASE DE DONNÉES")
    print("=" * 60)
    print()
    
    db_path = "database.db"
    
    # Vérifier si la base existe
    if os.path.exists(db_path):
        print(f"📁 Base de données trouvée : {db_path}")
        
        # Créer une sauvegarde
        backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            import shutil
            shutil.copy2(db_path, backup_path)
            print(f"✅ Sauvegarde créée : {backup_path}")
        except Exception as e:
            print(f"⚠️  Impossible de créer la sauvegarde : {e}")
        
        # Demander confirmation
        print("\n⚠️  ATTENTION : Cette action va supprimer TOUTES les données !")
        print("   - Tous les clients")
        print("   - Tous les abonnements")
        print("   - Toutes les ventes")
        print("   - Tous les vendeurs (sauf super admin)")
        print("   - Tous les logs")
        print()
        
        confirm = input("Êtes-vous SÛR de vouloir continuer ? (tapez 'OUI' en majuscules) : ")
        
        if confirm != "OUI":
            print("\n❌ Annulé - Aucune modification effectuée")
            return False
        
        # Supprimer la base de données
        print("\n🗑️  Suppression de l'ancienne base de données...")
        try:
            os.remove(db_path)
            print("✅ Base de données supprimée")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression : {e}")
            return False
    else:
        print(f"📁 Aucune base de données existante trouvée")
    
    # Réinitialiser avec les valeurs par défaut
    print("\n🔄 Réinitialisation de la base de données...")
    try:
        # Importer et initialiser
        import database as db
        db.init_database()
        
        print("\n✅ Base de données réinitialisée avec succès !")
        print("\n📊 Configuration par défaut :")
        print("   - Super Admin créé")
        print("   - Types d'abonnements créés (1, 3, 6, 12 mois)")
        print("   - Cache Vavoo initialisé")
        print()
        print("🔐 Identifiants Super Admin :")
        
        # Lire depuis config
        from config import SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD, SUPER_ADMIN_EMAIL
        print(f"   Username : {SUPER_ADMIN_USERNAME}")
        print(f"   Password : {SUPER_ADMIN_PASSWORD}")
        print(f"   Email    : {SUPER_ADMIN_EMAIL}")
        print()
        print("🚀 Vous pouvez maintenant démarrer le serveur :")
        print("   python server.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la réinitialisation : {e}")
        return False

if __name__ == "__main__":
    success = reset_database()
    sys.exit(0 if success else 1)
