# 📖 Instructions - IPTV Production

## 🎯 Nouveau Projet Créé !

Un nouveau dossier `iptv_production` a été créé avec un serveur IPTV complet et amélioré.

## 📁 Contenu du Dossier

```
iptv_production/
├── server.py              # Serveur HTTP principal
├── config.py              # Configuration (améliorée)
├── database.py            # Gestion base de données
├── multi_service.py       # Service IPTV (Vavoo)
├── admin_panel.py         # Interface web admin
├── vavoo_service.py       # Service Vavoo
├── requirements.txt       # Dépendances
├── .env.example           # Configuration exemple
├── .gitignore             # Fichiers à ignorer
├── start.bat              # Démarrage Windows
├── start.sh               # Démarrage Linux/Mac
├── test_server.py         # Script de test
├── reset_database.py      # Réinitialisation DB
├── README.md              # Documentation principale
├── QUICKSTART.md          # Démarrage rapide
└── INSTRUCTIONS.md        # Ce fichier
```

## 🚀 Démarrage Rapide

### 1. Aller dans le Dossier

```bash
cd iptv_production
```

### 2. Installer les Dépendances

```bash
pip install -r requirements.txt
```

### 3. Démarrer le Serveur

**Windows** :
```bash
start.bat
```

**Linux/Mac** :
```bash
chmod +x start.sh
./start.sh
```

**Ou directement** :
```bash
python server.py
```

### 4. Ouvrir le Navigateur

👉 **http://localhost:8888/admin**

### 5. Se Connecter

```
Username: superadmin
Password: Super@2024!
```

## ✨ Améliorations

Ce nouveau serveur inclut :

### ✅ Configuration Améliorée
- Variables d'environnement via `.env`
- Configuration centralisée dans `config.py`
- Paramètres de performance ajustables

### ✅ Scripts Utilitaires
- `start.bat` / `start.sh` - Démarrage facile
- `test_server.py` - Tests automatiques
- `reset_database.py` - Réinitialisation DB

### ✅ Documentation Complète
- `README.md` - Vue d'ensemble
- `QUICKSTART.md` - Démarrage rapide
- `INSTRUCTIONS.md` - Ce fichier

### ✅ Sécurité
- `.gitignore` configuré
- Variables sensibles dans `.env`
- Mots de passe configurables

### ✅ Développement Local
- Optimisé pour le développement
- Tests faciles
- Réinitialisation rapide

## 🎯 Fonctionnalités

Toutes les fonctionnalités du serveur original :

- ✅ **8900+ chaînes** Live TV
- ✅ **Films** et **Séries** VOD
- ✅ **Dashboard** avec statistiques
- ✅ **Gestion des clients**
- ✅ **Vente d'abonnements**
- ✅ **Prolongation**
- ✅ **Gestion des vendeurs**
- ✅ **Rafraîchissement des chaînes**
- ✅ **Historique** et **Logs**
- ✅ **API Xtream Codes**
- ✅ **Playlists M3U**

## 🔧 Configuration

### Fichier .env

Copiez `.env.example` vers `.env` et modifiez :

```bash
cp .env.example .env
```

Éditez `.env` :

```bash
# Port du serveur
PORT=8888

# Identifiants admin
SUPER_ADMIN_USERNAME=superadmin
SUPER_ADMIN_PASSWORD=VotreMotDePasseSecurise!
SUPER_ADMIN_EMAIL=admin@votredomaine.com

# Performance
THREAD_POOL_SIZE=1000
REQUEST_QUEUE_SIZE=500
```

## 🧪 Tests

### Tester le Serveur

```bash
python test_server.py
```

### Réinitialiser la Base de Données

```bash
python reset_database.py
```

## 📖 Documentation

### Guides Disponibles

- **`README.md`** - Documentation principale
- **`QUICKSTART.md`** - Démarrage rapide (3 minutes)
- **`INSTRUCTIONS.md`** - Ce fichier

### Prochainement

- `GUIDE_UTILISATION.md` - Guide complet d'utilisation
- `API.md` - Documentation de l'API
- `DEPLOYMENT.md` - Guide de déploiement

## 🆘 Problèmes Courants

### Le serveur ne démarre pas

**Vérifiez** :
- Python est installé (version 3.7+)
- Les dépendances sont installées : `pip install -r requirements.txt`
- Le port 8888 n'est pas déjà utilisé

**Solution** :
```bash
# Changer le port dans .env
PORT=8889
```

### Impossible de se connecter

**Solution** :
```bash
# Réinitialiser la base de données
python reset_database.py
```

### Les chaînes ne se chargent pas

**Solution** :
- Attendez 2-3 minutes au premier démarrage
- Cliquez sur "🔄 Rafraîchir chaînes" dans le dashboard

## 🔄 Workflow de Développement

### 1. Développer

```bash
# Démarrer le serveur
python server.py

# Dans un autre terminal, tester
python test_server.py
```

### 2. Tester

```bash
# Ouvrir le navigateur
http://localhost:8888/admin

# Créer un client de test
# Vendre un abonnement
# Tester avec IPTV Smarters Pro
```

### 3. Réinitialiser (si nécessaire)

```bash
# Réinitialiser la base de données
python reset_database.py

# Redémarrer le serveur
python server.py
```

## 🚀 Déploiement

Pour déployer en production :

1. **Configurez** `.env` avec des valeurs de production
2. **Changez** le mot de passe admin
3. **Utilisez** un serveur web (Nginx, Apache)
4. **Activez** HTTPS
5. **Configurez** un nom de domaine

Consultez `DEPLOYMENT.md` (à venir) pour plus de détails.

## ✅ Checklist

- [ ] Aller dans le dossier `iptv_production`
- [ ] Installer les dépendances
- [ ] Copier `.env.example` vers `.env`
- [ ] Démarrer le serveur
- [ ] Ouvrir http://localhost:8888/admin
- [ ] Se connecter
- [ ] Créer un client de test
- [ ] Vendre un abonnement
- [ ] Tester avec IPTV Smarters Pro
- [ ] ✅ Tout fonctionne !

## 🎉 Résultat

Vous avez maintenant un serveur IPTV complet :

```
✅ Serveur fonctionnel
✅ 8900+ chaînes disponibles
✅ Interface admin complète
✅ Configuration facile
✅ Tests automatiques
✅ Documentation complète
✅ Prêt pour le développement !
```

---

## 🚀 Prochaines Étapes

1. **Lisez** `QUICKSTART.md`
2. **Démarrez** le serveur
3. **Testez** les fonctionnalités
4. **Développez** vos propres améliorations !

---

✅ **Serveur IPTV Production - Prêt à l'emploi !**
