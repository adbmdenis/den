#!/bin/bash

echo "============================================"
echo "   IPTV SERVER PRODUCTION - Démarrage"
echo "============================================"
echo ""

# Aller dans le répertoire du script
cd "$(dirname "$0")"

echo "[1/3] Installation des dépendances..."
pip install -r requirements.txt

echo ""
echo "[2/3] Vérification de la configuration..."
if [ ! -f .env ]; then
    echo "ATTENTION: Fichier .env non trouvé!"
    echo "Copie de .env.example vers .env..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Éditez .env et configurez vos paramètres!"
    read -p "Appuyez sur Entrée pour continuer..."
fi

echo ""
echo "[3/3] Démarrage du serveur..."
echo ""
echo "============================================"
echo "   Serveur démarré sur http://localhost:8888"
echo "============================================"
echo ""
echo "Panel Admin: http://localhost:8888/admin"
echo "Espace Client: http://localhost:8888/client"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo "============================================"
echo ""

python3 server.py
