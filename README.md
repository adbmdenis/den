# 🎬 Serveur IPTV - Système de Gestion

Système complet de gestion IPTV avec panel d'administration, gestion des clients, ventes et génération de playlists M3U.

## 🚀 Fonctionnalités

- ✅ **Panel d'administration** - Interface web complète
- ✅ **Gestion des clients** - CRUD complet (Créer, Lire, Modifier, Supprimer)
- ✅ **Gestion des ventes** - Suivi des abonnements
- ✅ **Génération M3U** - Playlists personnalisées par client
- ✅ **Multi-services** - Support de plusieurs sources IPTV
- ✅ **Authentification** - Système de tokens sécurisé
- ✅ **Base de données** - SQLite intégrée
- ✅ **API REST** - Endpoints complets

## 📋 Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)

## 🔧 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/adbmdenis/den.git
cd den
```

### 2. Installer les dépendances

```bash
pip install flask requests
```

### 3. Configuration

Éditer `config.py` pour configurer:
- Identifiants superadmin
- Port du serveur
- Paramètres de la base de données

```python
# Exemple de configuration
SUPER_ADMIN_USERNAME = "superadmin"
SUPER_ADMIN_PASSWORD = "Super@2024!"
SERVER_PORT = 8888
```

### 4. Démarrer le serveur

```bash
python server.py
```

Le serveur démarre sur `http://localhost:8888`

## 🌐 Accès au Panel Admin

**URL:** http://localhost:8888/login

**Identifiants par défaut:**
- Username: `superadmin`
- Password: `Super@2024!`

⚠️ **Important:** Changez le mot de passe après la première connexion!

## 📁 Structure du Projet

```
serveur_iptv/
├── server.py              # Serveur principal
├── admin_panel.py         # Panel d'administration
├── database.py            # Gestion base de données
├── multi_service.py       # Gestion multi-services IPTV
├── config.py              # Configuration
├── database.db            # Base de données SQLite
├── README.md              # Ce fichier
└── docs/
    ├── GUIDE_HEBERGEMENT.md      # Guide d'hébergement
    ├── COMPARAISON_HEBERGEURS.txt # Comparaison hébergeurs
    ├── ACCES_RAPIDE.txt          # Accès rapide
    └── STATUS_FINAL.md           # Statut du projet
```

## 🔌 API Endpoints

### Authentification
- `POST /api/login` - Connexion admin

### Clients
- `GET /api/clients` - Liste des clients
- `POST /api/clients/create` - Créer un client
- `PUT /api/clients/update` - Modifier un client
- `DELETE /api/clients/delete` - Supprimer un client

### Ventes
- `GET /api/sales` - Liste des ventes
- `POST /api/sales/create` - Créer une vente

### Administrateurs
- `GET /api/admins` - Liste des admins
- `POST /api/admins/create` - Créer un admin

### Statistiques
- `GET /api/stats` - Statistiques globales

### Playlists
- `GET /playlist/<client_id>` - Playlist M3U du client

## 🛠️ Scripts Utiles

### Test de connexion
```bash
python test_login_simple.py
```

### Réinitialiser le mot de passe superadmin
```bash
python fix_superadmin_password.py
```

### Test d'intégration
```bash
python test_admin_integration.py
```

### Redémarrer le serveur (Windows)
```bash
REDEMARRER_MAINTENANT.bat
```

## 🚀 Déploiement en Production

Consultez le guide complet: [GUIDE_HEBERGEMENT.md](GUIDE_HEBERGEMENT.md)

### Hébergeurs Recommandés

1. **Contabo VPS S** - 5€/mois (Meilleur rapport qualité/prix)
2. **Hetzner CX31** - 9.50€/mois (Plus fiable)
3. **OVH VPS Value** - 7€/mois (Support français)

### Déploiement Rapide

```bash
# Sur le serveur
git clone https://github.com/adbmdenis/den.git
cd den
pip install flask requests
python server.py
```

Pour un déploiement complet avec Nginx, SSL, et systemd, consultez le guide d'hébergement.

## 🔒 Sécurité

### Recommandations

- ✅ Changez les identifiants par défaut
- ✅ Utilisez HTTPS en production
- ✅ Configurez un firewall (UFW)
- ✅ Installez Fail2Ban
- ✅ Faites des sauvegardes régulières
- ✅ Mettez à jour régulièrement

### Configuration Firewall

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

## 📊 Monitoring

### Voir les logs
```bash
# Logs du serveur
tail -f logs/server.log

# Logs système (si service systemd)
sudo journalctl -u iptv -f
```

### Monitoring des ressources
```bash
# CPU et RAM
htop

# Connexions réseau
netstat -tulpn | grep 8888
```

## 🐛 Dépannage

### Problème: Boutons ne fonctionnent pas
**Solution:** Redémarrer le serveur
```bash
# Windows
REDEMARRER_MAINTENANT.bat

# Linux
sudo systemctl restart iptv
```

### Problème: Login échoue (401)
**Solution:** Synchroniser le mot de passe
```bash
python fix_superadmin_password.py
```

### Problème: Base de données corrompue
**Solution:** Réinitialiser la base
```bash
# Sauvegarder l'ancienne
cp database.db database.db.backup

# Supprimer et redémarrer (créera une nouvelle DB)
rm database.db
python server.py
```

## 📚 Documentation

- [Guide d'hébergement complet](GUIDE_HEBERGEMENT.md)
- [Comparaison des hébergeurs](COMPARAISON_HEBERGEURS.txt)
- [Accès rapide](ACCES_RAPIDE.txt)
- [Statut du projet](STATUS_FINAL.md)

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📝 Changelog

### Version 1.0.0 (Décembre 2025)
- ✅ Panel d'administration complet
- ✅ Gestion des clients et ventes
- ✅ Génération de playlists M3U
- ✅ Authentification sécurisée
- ✅ API REST complète
- ✅ Documentation complète

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 👤 Auteur

**Denis ADBM**
- GitHub: [@adbmdenis](https://github.com/adbmdenis)

## 🙏 Remerciements

Merci à tous ceux qui ont contribué à ce projet!

## 📞 Support

Pour toute question ou problème:
1. Consultez la documentation
2. Vérifiez les issues GitHub
3. Créez une nouvelle issue si nécessaire

---

**⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile sur GitHub!**
# den
