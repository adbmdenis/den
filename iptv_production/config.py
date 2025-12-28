#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration du serveur IPTV Production
"""

import os
import secrets

# ============== SERVEUR ==============
SERVER_HOST = os.getenv("HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("PORT", 8888))
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))

# ============== BASE DE DONNÉES ==============
DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "database.db"))

# ============== VAVOO ==============
TOKEN_REFRESH_INTERVAL = int(os.getenv("TOKEN_REFRESH_INTERVAL", 900))  # 15 minutes
CHANNELS_REFRESH_INTERVAL = int(os.getenv("CHANNELS_REFRESH_INTERVAL", 1800))  # 30 minutes

# ============== SUPER ADMIN ==============
SUPER_ADMIN_USERNAME = os.getenv("SUPER_ADMIN_USERNAME", "superadmin")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD", "Super@2024!")
SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL", "admin@iptv.local")

# ============== TYPES D'ABONNEMENTS PAR DÉFAUT ==============
DEFAULT_SUBSCRIPTION_TYPES = [
    {"name": "1_mois", "duration_days": 30, "price": 5.00, "stock": 1000, "description": "Abonnement 1 mois"},
    {"name": "3_mois", "duration_days": 90, "price": 12.00, "stock": 500, "description": "Abonnement 3 mois"},
    {"name": "6_mois", "duration_days": 180, "price": 20.00, "stock": 300, "description": "Abonnement 6 mois"},
    {"name": "12_mois", "duration_days": 365, "price": 35.00, "stock": 200, "description": "Abonnement 12 mois"},
]

# ============== PAIEMENT ==============
PAYMENT_STATUS = {
    "pending": "En attente",
    "paid": "Payé",
    "cancelled": "Annulé",
    "refunded": "Remboursé"
}

PAYMENT_METHODS = {
    "cash": "Espèces",
    "mobile_money": "Mobile Money",
    "card": "Carte bancaire",
    "bank_transfer": "Virement bancaire",
    "paypal": "PayPal",
    "manual": "Manuel"
}

# ============== SÉCURITÉ ==============
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_MINUTES = 15
SESSION_DURATION_HOURS = 24

# ============== STREAMING ==============
MAX_CONCURRENT_STREAMS = 1000  # Nombre max de streams simultanés
STREAM_TIMEOUT = 300  # Timeout en secondes
STREAM_BUFFER_SIZE = 65536  # 64KB

# ============== LOGS ==============
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "iptv_server.log")

# ============== PERFORMANCE ==============
THREAD_POOL_SIZE = int(os.getenv("THREAD_POOL_SIZE", 1000))
REQUEST_QUEUE_SIZE = int(os.getenv("REQUEST_QUEUE_SIZE", 500))

# ============== CACHE ==============
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # 1 heure

print(f"[CONFIG] Serveur configuré sur {SERVER_HOST}:{SERVER_PORT}")
print(f"[CONFIG] Base de données: {DATABASE_PATH}")
print(f"[CONFIG] Super Admin: {SUPER_ADMIN_USERNAME}")
