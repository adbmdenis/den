#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de login simple"""

import requests
import json

SERVER_URL = "http://192.168.1.19:8888"

print("\n" + "=" * 60)
print("TEST DE LOGIN SUPERADMIN")
print("=" * 60)

# Charger les identifiants
from config import SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD

print(f"\nUsername: {SUPER_ADMIN_USERNAME}")
print(f"Password: {SUPER_ADMIN_PASSWORD}")

# Test de login
print(f"\nEnvoi de la requete POST a {SERVER_URL}/api/login...")

try:
    response = requests.post(
        f"{SERVER_URL}/api/login",
        json={
            "username": SUPER_ADMIN_USERNAME,
            "password": SUPER_ADMIN_PASSWORD
        },
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Reponse: {json.dumps(data, indent=2)}")
    except:
        print(f"Reponse (texte): {response.text}")
    
    if response.status_code == 200:
        print("\n" + "=" * 60)
        print("LOGIN REUSSI!")
        print("=" * 60)
        if 'token' in data:
            print(f"\nToken: {data['token'][:50]}...")
        if 'admin' in data:
            print(f"Admin: {data['admin']}")
    else:
        print("\n" + "=" * 60)
        print("LOGIN ECHOUE!")
        print("=" * 60)
        if 'error' in data:
            print(f"\nErreur: {data['error']}")
            
except Exception as e:
    print(f"\nERREUR: {e}")

print("\n" + "=" * 60)
