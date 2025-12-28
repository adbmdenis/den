#!/bin/bash
# Script pour pousser tous les fichiers sur GitHub

echo "=========================================="
echo "  PUSH FINAL SUR GITHUB"
echo "=========================================="
echo ""

# Ajouter tous les fichiers
echo "📦 Ajout de tous les fichiers..."
git add .

# Créer le commit
echo ""
echo "💾 Création du commit..."
git commit -m "Fix: Correction complète - Identifiants + Reset DB + Documentation"

# Pousser sur GitHub
echo ""
echo "🚀 Push sur GitHub..."
git push origin main

echo ""
echo "=========================================="
echo "  ✅ PUSH TERMINÉ !"
echo "=========================================="
echo ""
echo "Render va redéployer automatiquement."
echo "Attendez 5-10 minutes puis suivez LISEZ_MOI_DABORD.md"
echo ""
