#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de clé secrète pour SECRET_KEY
"""

import secrets

def generate_secret_key(length=32):
    """Génère une clé secrète aléatoire"""
    return secrets.token_hex(length)

if __name__ == "__main__":
    print("=" * 60)
    print("  GÉNÉRATEUR DE CLÉ SECRÈTE")
    print("=" * 60)
    print()
    print("Voici votre nouvelle clé secrète :")
    print()
    print(f"  {generate_secret_key()}")
    print()
    print("Copiez cette valeur et utilisez-la pour SECRET_KEY")
    print("dans les variables d'environnement de Render.")
    print()
    print("⚠️  Ne partagez JAMAIS cette clé !")
    print("=" * 60)
