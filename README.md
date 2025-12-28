# Plateforme IPTV - Gestion des Abonnements

## 🚀 Démarrage rapide

### En local
```bash
cd serveur_iptv
python server.py
```

### Sur Render (Production)
Voir le guide complet dans [DEPLOY.md](DEPLOY.md)

**Déploiement en 1 clic :**
1. Poussez votre code sur GitHub
2. Connectez votre dépôt à Render
3. Render détecte automatiquement `render.yaml`
4. Votre serveur est en ligne ! 🎉

## 📍 URLs

| Page | URL |
|------|-----|
| Accueil | http://192.168.1.19:8888/ |
| Panel Admin | http://192.168.1.19:8888/admin |
| Espace Client | http://192.168.1.19:8888/client |

## 🔐 Identifiants Super Admin

- **Username:** `superadmin`
- **Password:** `Super@2024!`

## 👥 Rôles et Permissions

### Super Admin
- Accès total à la plateforme
- Créer/modifier/supprimer des vendeurs
- Définir les quotas par vendeur (types d'abonnements autorisés, quantités, prix)
- Gérer les types d'abonnements (1 mois, 3 mois, 6 mois, 12 mois)
- Importer des lignes IPTV
- Voir toutes les ventes et statistiques
- Annuler/suspendre des abonnements

### Vendeur (Admin)
- Créer des clients
- Vendre des abonnements (selon ses quotas)
- Voir son historique de ventes
- Gérer ses clients

### Client
- Se connecter à l'espace client
- Voir son abonnement actif
- Obtenir ses identifiants IPTV
- Voir la date d'expiration

## 📺 Configuration IPTV Smarters Pro

**Type:** Xtream Codes API

| Paramètre | Valeur |
|-----------|--------|
| Server URL | `http://192.168.1.19:8888` |
| Username | Votre nom d'utilisateur |
| Password | Votre mot de passe |

**URL M3U directe:**
```
http://192.168.1.19:8888/get.php?username=USER&password=PASS
```

Ou avec token:
```
http://192.168.1.19:8888/playlist.m3u?token=VOTRE_TOKEN
```

## 💰 Types d'abonnements par défaut

| Type | Durée | Prix |
|------|-------|------|
| 1_mois | 30 jours | 5.00 € |
| 3_mois | 90 jours | 12.00 € |
| 6_mois | 180 jours | 20.00 € |
| 12_mois | 365 jours | 35.00 € |

## 💳 Méthodes de paiement

- Espèces
- Mobile Money
- Carte bancaire
- Manuel

## 🔒 Sécurité

- Authentification par token JWT-like
- Hashage des mots de passe (SHA256)
- Blocage après 5 tentatives de connexion (15 min)
- Logs de toutes les actions
- Contrôle des connexions simultanées par client

## 📁 Structure des fichiers

```
serveur_iptv/
├── server.py          # Serveur HTTP principal
├── database.py        # Gestion SQLite
├── admin_panel.py     # Interface web
├── vavoo_service.py   # Service VAVOO (tokens/chaînes)
├── config.py          # Configuration
├── database.db        # Base de données SQLite
└── README.md          # Documentation
```

## ⚙️ Configuration (config.py)

```python
SERVER_PORT = 8888
SUPER_ADMIN_USERNAME = "superadmin"
SUPER_ADMIN_PASSWORD = "Super@2024!"
TOKEN_REFRESH_INTERVAL = 900  # 15 minutes
```

## 📊 API Endpoints

### Authentification
- `POST /api/login` - Login admin
- `POST /api/client/login` - Login client

### Admin API
- `GET /api/admin/stats` - Statistiques
- `GET /api/admin/clients` - Liste clients
- `GET /api/admin/admins` - Liste vendeurs (super admin)
- `GET /api/admin/sales` - Historique ventes
- `POST /api/admin/clients/create` - Créer client
- `POST /api/admin/sell` - Vendre abonnement
- `POST /api/admin/admins/create` - Créer vendeur
- `POST /api/admin/quotas/set` - Définir quotas

### Client API
- `GET /api/client/me` - Infos client
- `GET /api/client/subscriptions` - Abonnements

### Playlist
- `GET /get.php?username=X&password=Y` - Playlist M3U
- `GET /playlist.m3u?token=X` - Playlist avec token
# iptv
# iptv
