#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démarrage du serveur IPTV avec logs détaillés
"""

import sys
import os
from datetime import datetime

def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    colors = {
        "INFO": "\033[94m",      # Bleu
        "SUCCESS": "\033[92m",   # Vert
        "WARNING": "\033[93m",   # Jaune
        "ERROR": "\033[91m",     # Rouge
        "RESET": "\033[0m"       # Reset
    }
    color = colors.get(level, colors["INFO"])
    reset = colors["RESET"]
    print(f"{color}[{timestamp}] [{level}] {msg}{reset}")

log("=" * 80)
log("DÉMARRAGE DU SERVEUR IPTV AVEC LOGS DÉTAILLÉS")
log("=" * 80)

# 1. Vérification des imports
log("\n📦 Vérification des modules...")
try:
    log("   Chargement de config.py...", "INFO")
    from config import SERVER_HOST, SERVER_PORT, SECRET_KEY
    log(f"   ✅ config.py chargé - Port: {SERVER_PORT}", "SUCCESS")
except Exception as e:
    log(f"   ❌ Erreur config.py: {e}", "ERROR")
    sys.exit(1)

try:
    log("   Chargement de database.py...", "INFO")
    import database as db
    log("   ✅ database.py chargé", "SUCCESS")
except Exception as e:
    log(f"   ❌ Erreur database.py: {e}", "ERROR")
    sys.exit(1)

try:
    log("   Chargement de multi_service.py...", "INFO")
    from multi_service import multi_service, set_server_ip
    log("   ✅ multi_service.py chargé", "SUCCESS")
except Exception as e:
    log(f"   ❌ Erreur multi_service.py: {e}", "ERROR")
    sys.exit(1)

try:
    log("   Chargement de admin_panel.py...", "INFO")
    from admin_panel import render_home_page, render_login_page, render_admin_panel, render_client_portal
    log("   ✅ admin_panel.py chargé", "SUCCESS")
except Exception as e:
    log(f"   ❌ Erreur admin_panel.py: {e}", "ERROR")
    sys.exit(1)

# 2. Initialisation de la base de données
log("\n💾 Initialisation de la base de données...")
try:
    db.init_database()
    log("   ✅ Base de données initialisée", "SUCCESS")
    
    # Vérifier le super admin
    admin = db.get_admin_by_username("superadmin")
    if admin:
        log(f"   ✅ Super admin trouvé: {admin['username']}", "SUCCESS")
    else:
        log("   ⚠️  Super admin non trouvé - sera créé au premier démarrage", "WARNING")
    
    # Stats de la DB
    stats = db.get_global_stats()
    log(f"   📊 Stats DB:", "INFO")
    log(f"      - Admins: {stats.get('total_admins', 0)}", "INFO")
    log(f"      - Clients: {stats.get('total_clients', 0)}", "INFO")
    log(f"      - Ventes: {stats.get('total_sales', 0)}", "INFO")
    
except Exception as e:
    log(f"   ❌ Erreur initialisation DB: {e}", "ERROR")
    sys.exit(1)

# 3. Initialisation du service IPTV
log("\n📺 Initialisation du service IPTV...")
try:
    multi_service.initialize()
    log("   ✅ Service IPTV initialisé", "SUCCESS")
    log("   ⏳ Chargement des chaînes Vavoo...", "INFO")
    multi_service.load_all_sources()
    
    stats = multi_service.get_stats()
    log(f"   📊 Stats IPTV:", "SUCCESS")
    log(f"      - Chaînes: {stats.get('total_channels', 0)}", "INFO")
    log(f"      - Films: {stats.get('total_movies', 0)}", "INFO")
    log(f"      - Séries: {stats.get('total_series', 0)}", "INFO")
    log(f"      - Token Vavoo: {'✅ Valide' if stats.get('token_valid') else '❌ Invalide'}", "INFO")
    
except Exception as e:
    log(f"   ❌ Erreur initialisation IPTV: {e}", "ERROR")
    log("   ⚠️  Le serveur démarrera sans chaînes", "WARNING")

# 4. Test de génération des pages
log("\n🌐 Test de génération des pages HTML...")
try:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    log(f"   📍 IP locale détectée: {local_ip}", "INFO")
    
    # Test page d'accueil
    html = render_home_page(local_ip, SERVER_PORT)
    log(f"   ✅ Page d'accueil: {len(html)} caractères", "SUCCESS")
    
    # Test page de login
    html = render_login_page()
    log(f"   ✅ Page de login: {len(html)} caractères", "SUCCESS")
    
    # Test panel admin
    html = render_admin_panel(local_ip, SERVER_PORT)
    log(f"   ✅ Panel admin: {len(html)} caractères", "SUCCESS")
    log(f"      - Blocs <script>: {html.count('<script>')}", "INFO")
    log(f"      - Fonction showModal: {'✅' if 'function showModal' in html else '❌'}", "INFO")
    log(f"      - Fonction loadClients: {'✅' if 'function loadClients' in html else '❌'}", "INFO")
    
    # Test portail client
    html = render_client_portal(local_ip, SERVER_PORT)
    log(f"   ✅ Portail client: {len(html)} caractères", "SUCCESS")
    
except Exception as e:
    log(f"   ❌ Erreur génération pages: {e}", "ERROR")

# 5. Démarrage du serveur
log("\n🚀 Démarrage du serveur HTTP...")
log(f"   📍 Adresse: http://{SERVER_HOST}:{SERVER_PORT}")
log(f"   📍 IP locale: http://{local_ip}:{SERVER_PORT}")
log("=" * 80)
log("✅ SERVEUR PRÊT - Appuyez sur Ctrl+C pour arrêter")
log("=" * 80)
log("\n📋 ROUTES DISPONIBLES:")
log(f"   🏠 Page d'accueil:    http://{local_ip}:{SERVER_PORT}/")
log(f"   🔐 Login admin:       http://{local_ip}:{SERVER_PORT}/login")
log(f"   👨‍💼 Panel admin:       http://{local_ip}:{SERVER_PORT}/admin")
log(f"   👤 Portail client:    http://{local_ip}:{SERVER_PORT}/client")
log(f"   📺 API Xtream:        http://{local_ip}:{SERVER_PORT}/player_api.php")
log(f"   📋 Playlist M3U:      http://{local_ip}:{SERVER_PORT}/get.php?username=USER&password=PASS")
log("=" * 80)

# Démarrer le serveur
try:
    import server
    # Le serveur démarre automatiquement quand on importe server.py
except KeyboardInterrupt:
    log("\n\n⏹️  Arrêt du serveur...", "WARNING")
    log("👋 Au revoir!", "INFO")
except Exception as e:
    log(f"\n\n❌ Erreur serveur: {e}", "ERROR")
    import traceback
    traceback.print_exc()
