# 🎬 Serveur IPTV Production

Serveur IPTV complet avec gestion des abonnements, multi-vendeurs, et 8900+ chaînes.

## 🚀 Démarrage Rapide

### Installation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Copier la configuration
cp .env.example .env

# Modifier .env avec vos paramètres

# Démarrer le serveur
python server.py
```

### Accès

- **Page d'accueil** : http://localhost:8888/
- **Panel Admin** : http://localhost:8888/admin
- **Espace Client** : http://localhost:8888/client

### Identifiants par Défaut

```
Username: superadmin
Password: Super@2024!
```

⚠️ **Changez ces identifiants immédiatement !**

## 📋 Fonctionnalités

### ✅ Gestion Complète

- **Dashboard** avec statistiques en temps réel
- **Gestion des clients** (création, modification, suppression)
- **Vente d'abonnements** (1, 3, 6, 12 mois)
- **Prolongation** d'abonnements
- **Gestion des vendeurs** et quotas
- **Historique** des ventes et logs
- **Rafraîchissement** des chaînes

### 📺 IPTV

- **8900+ chaînes** Live TV
- **Films** VOD
- **Séries** VOD
- **API Xtream Codes** compatible
- **Playlists M3U**
- **Streaming** haute performance

### 🔒 Sécurité

- Authentification par token
- Hashage des mots de passe (SHA256)
- Contrôle des connexions simultanées
- Logs de toutes les actions
- Protection contre les attaques

## 📖 Documentation

- **`GUIDE_UTILISATION.md`** - Guide complet d'utilisation
- **`API.md`** - Documentation de l'API
- **`DEPLOYMENT.md`** - Guide de déploiement

## 🧪 Tests

```bash
# Tester le serveur
python test_server.py

# Tester l'API
python test_api.py

# Réinitialiser la base de données
python reset_database.py
```

## 📊 Structure

```
iptv_production/
├── server.py           # Serveur HTTP principal
├── config.py           # Configuration
├── database.py         # Gestion base de données
├── multi_service.py    # Service IPTV (Vavoo)
├── admin_panel.py      # Interface web admin
├── requirements.txt    # Dépendances
├── .env.example        # Configuration exemple
└── README.md           # Ce fichier
```

## 🔧 Configuration

Éditez `.env` pour configurer :

- Port du serveur
- Identifiants admin
- Paramètres de performance
- Intervalles de rafraîchissement

## 📞 Support

Pour toute question, consultez la documentation ou créez une issue.

---

✅ **Serveur IPTV Production - Prêt pour la production !**
