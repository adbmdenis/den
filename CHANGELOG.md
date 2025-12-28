# Changelog

## [1.1.0] - Préparation pour Render

### Ajouté
- ✅ Configuration des variables d'environnement
- ✅ Fichier `render.yaml` pour déploiement automatique
- ✅ Fichier `.gitignore` pour sécurité
- ✅ Fichier `Procfile` pour Render
- ✅ Fichier `runtime.txt` pour spécifier Python 3.11
- ✅ Fichier `.env.example` comme template
- ✅ Guide de déploiement complet `DEPLOY.md`
- ✅ Support du disque persistant pour la base de données

### Modifié
- ✅ `config.py` : Utilise maintenant les variables d'environnement
  - `PORT` : Port du serveur (auto-détecté par Render)
  - `SECRET_KEY` : Clé secrète (générée par Render)
  - `SUPER_ADMIN_USERNAME` : Nom d'utilisateur admin
  - `SUPER_ADMIN_PASSWORD` : Mot de passe admin
  - `SUPER_ADMIN_EMAIL` : Email admin
  - `DATABASE_PATH` : Chemin de la base de données
  - `TOKEN_REFRESH_INTERVAL` : Intervalle de rafraîchissement
- ✅ `requirements.txt` : Ajout de gunicorn

### Sécurité
- 🔒 Les mots de passe ne sont plus en dur dans le code
- 🔒 La base de données est exclue du dépôt Git
- 🔒 Les variables sensibles sont dans les variables d'environnement

## [1.0.0] - Version initiale

### Fonctionnalités
- ✅ Serveur IPTV multi-thread haute performance
- ✅ Support Vavoo (Live TV + VOD)
- ✅ API Xtream Codes pour IPTV Smarters Pro
- ✅ Panel d'administration complet
- ✅ Gestion des vendeurs et quotas
- ✅ Gestion des clients et abonnements
- ✅ Système de paiement multi-méthodes
- ✅ Logs et statistiques détaillés
- ✅ Contrôle des connexions simultanées
