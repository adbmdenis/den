#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour réinitialiser complètement la base de données
ATTENTION : Ceci supprimera TOUTES les données !
"""

import os
import sys
import sqlite3
from datetime import datetime

def backup_database(db_path):
    """Crée une sauvegarde de la base de données"""
    if os.path.exists(db_path):
        backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            import shutil
            shutil.copy2(db_path, backup_path)
            print(f"✅ Sauvegarde créée : {backup_path}")
            return backup_path
        except Exception as e:
            print(f"⚠️  Impossible de créer la sauvegarde : {e}")
            return None
    return None

def reset_database(db_path):
    """Supprime et réinitialise la base de données"""
    print("=" * 60)
    print("  RÉINITIALISATION DE LA BASE DE DONNÉES")
    print("=" * 60)
    print()
    
    # Vérifier si la base existe
    if os.path.exists(db_path):
        print(f"📁 Base de données trouvée : {db_path}")
        
        # Créer une sauvegarde
        print("\n📦 Création d'une sauvegarde...")
        backup_path = backup_database(db_path)
        
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
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la réinitialisation : {e}")
        print("\n⚠️  Si vous avez une sauvegarde, vous pouvez la restaurer :")
        if backup_path:
            print(f"   mv {backup_path} {db_path}")
        return False

def show_database_info(db_path):
    """Affiche les informations sur la base de données actuelle"""
    if not os.path.exists(db_path):
        print("❌ Aucune base de données trouvée")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("=" * 60)
        print("  INFORMATIONS BASE DE DONNÉES ACTUELLE")
        print("=" * 60)
        print()
        
        # Admins
        cursor.execute("SELECT COUNT(*) FROM admins")
        admin_count = cursor.fetchone()[0]
        print(f"👥 Admins/Vendeurs : {admin_count}")
        
        # Clients
        cursor.execute("SELECT COUNT(*) FROM clients")
        client_count = cursor.fetchone()[0]
        print(f"👤 Clients : {client_count}")
        
        # Abonnements actifs
        cursor.execute("SELECT COUNT(*) FROM subscriptions WHERE status = 'active' AND end_date > datetime('now')")
        active_subs = cursor.fetchone()[0]
        print(f"✅ Abonnements actifs : {active_subs}")
        
        # Ventes
        cursor.execute("SELECT COUNT(*) FROM sales")
        sales_count = cursor.fetchone()[0]
        print(f"💰 Ventes : {sales_count}")
        
        # Logs
        cursor.execute("SELECT COUNT(*) FROM logs")
        logs_count = cursor.fetchone()[0]
        print(f"📋 Logs : {logs_count}")
        
        conn.close()
        
        print()
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

def main():
    db_path = "database.db"
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "info":
            show_database_info(db_path)
            return
        elif sys.argv[1] == "reset":
            if reset_database(db_path):
                print("\n✅ Réinitialisation terminée !")
                print("\n🚀 Vous pouvez maintenant démarrer le serveur :")
                print("   python server.py")
            else:
                print("\n❌ Échec de la réinitialisation")
                sys.exit(1)
            return
    
    # Mode interactif
    print("=" * 60)
    print("  GESTION DE LA BASE DE DONNÉES")
    print("=" * 60)
    print()
    print("Options :")
    print("  1. Voir les informations")
    print("  2. Réinitialiser la base de données")
    print("  3. Annuler")
    print()
    
    choice = input("Votre choix (1-3) : ")
    
    if choice == "1":
        show_database_info(db_path)
    elif choice == "2":
        reset_database(db_path)
    else:
        print("❌ Annulé")

if __name__ == "__main__":
    main()
