#!/bin/bash

echo "============================================================"
echo "COPIE DES FICHIERS ESSENTIELS POUR NOUVEAU PROJET IPTV"
echo "============================================================"
echo ""

# Demander le chemin de destination
read -p "Entrez le chemin du nouveau projet (ex: /home/user/mon_nouveau_iptv): " DEST

# Vérifier si le dossier existe, sinon le créer
if [ ! -d "$DEST" ]; then
    echo ""
    echo "📁 Création du dossier: $DEST"
    mkdir -p "$DEST"
fi

echo ""
echo "📦 Copie des fichiers essentiels..."
echo ""

# Copier les fichiers Python principaux
echo "✅ Copie de server.py"
cp -f "server.py" "$DEST/"

echo "✅ Copie de config.py"
cp -f "config.py" "$DEST/"

echo "✅ Copie de database.py"
cp -f "database.py" "$DEST/"

echo "✅ Copie de admin_panel.py"
cp -f "admin_panel.py" "$DEST/"

echo "✅ Copie de vavoo_service.py"
cp -f "vavoo_service.py" "$DEST/"

echo "✅ Copie de multi_service.py"
cp -f "multi_service.py" "$DEST/"

# Copier les fichiers de configuration
echo "✅ Copie de .env.example"
cp -f ".env.example" "$DEST/"

echo "✅ Copie de requirements.txt"
cp -f "requirements.txt" "$DEST/"

echo "✅ Copie de .gitignore"
cp -f ".gitignore" "$DEST/"

# Copier les scripts de démarrage
echo "✅ Copie de start.bat"
cp -f "start.bat" "$DEST/"

echo "✅ Copie de start.sh"
cp -f "start.sh" "$DEST/"

# Rendre start.sh exécutable
chmod +x "$DEST/start.sh"

# Copier les scripts utilitaires (optionnel)
echo "✅ Copie de reset_database.py"
cp -f "reset_database.py" "$DEST/"

echo "✅ Copie de test_server.py"
cp -f "test_server.py" "$DEST/"

# Copier la documentation
echo "✅ Copie de README.md"
cp -f "README.md" "$DEST/"

echo ""
echo "============================================================"
echo "✅ COPIE TERMINÉE!"
echo "============================================================"
echo ""
echo "📁 Fichiers copiés dans: $DEST"
echo ""
echo "📋 PROCHAINES ÉTAPES:"
echo ""
echo "1. Aller dans le nouveau dossier:"
echo "   cd \"$DEST\""
echo ""
echo "2. Créer le fichier .env:"
echo "   cp .env.example .env"
echo ""
echo "3. Éditer .env avec vos paramètres:"
echo "   nano .env"
echo ""
echo "4. Installer les dépendances:"
echo "   pip install -r requirements.txt"
echo ""
echo "5. Démarrer le serveur:"
echo "   ./start.sh"
echo ""
echo "============================================================"
