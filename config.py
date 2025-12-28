#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration du serveur IPTV
"""

import os
import secrets

# Serveur
SERVER_HOST = os.getenv("HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("PORT", 8888))
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))

# Base de donnees
DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "database.db"))

# Token VAVOO
TOKEN_REFRESH_INTERVAL = int(os.getenv("TOKEN_REFRESH_INTERVAL", 900))  # 15 minutes

# Super Admin (a changer!)
SUPER_ADMIN_USERNAME = os.getenv("SUPER_ADMIN_USERNAME", "superadmin")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD", "Super@2024!")
SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL", "admin@iptv.local")

# Types d'abonnements par defaut
DEFAULT_SUBSCRIPTION_TYPES = [
    {"name": "1_mois", "duration_days": 30, "price": 5.00, "stock": 1000},
    {"name": "3_mois", "duration_days": 90, "price": 12.00, "stock": 500},
    {"name": "6_mois", "duration_days": 180, "price": 20.00, "stock": 300},
    {"name": "12_mois", "duration_days": 365, "price": 35.00, "stock": 200},
]

# Statuts de paiement
PAYMENT_STATUS = {
    "pending": "En attente",
    "paid": "Payé",
    "cancelled": "Annulé",
    "refunded": "Remboursé"
}

# Methodes de paiement
PAYMENT_METHODS = {
    "cash": "Espèces",
    "mobile_money": "Mobile Money",
    "card": "Carte bancaire",
    "manual": "Manuel"
}

# Securite
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_MINUTES = 15
SESSION_DURATION_HOURS = 24
