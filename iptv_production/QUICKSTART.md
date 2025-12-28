# ⚡ Démarrage Rapide - IPTV Production

## 🚀 Installation en 3 Minutes

### Étape 1 : Installer les Dépendances

```bash
pip install -r requirements.txt
```

### Étape 2 : Configurer

```bash
# Copier la configuration
cp .env.example .env

# Éditer .env (optionnel, les valeurs par défaut fonctionnent)
nano .env  # ou notepad .env sur Windows
```

### Étape 3 : Démarrer

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

## 🌐 Accès

Une fois démarré, ouvrez votre navigateur :

- **Page d'accueil** : http://localhost:8888/
- **Panel Admin** : http://localhost:8888/admin
- **Espace Client** : http://localhost:8888/client

## 🔐 Connexion

### Identifiants par Défaut

```
Username: superadmin
Password: Super@2024!
```

⚠️ **Changez ces identifiants dans le panel admin !**

## 📋 Première Utilisation

### 1. Se Connecter

1. Allez sur http://localhost:8888/admin
2. Entrez les identifiants par défaut
3. Vous serez redirigé vers le dashboard

### 2. Créer un Client

1. Cliquez sur **"+ Nouveau client"**
2. Remplissez :
   - Username : `testclient`
   - Password : `Test123!`
   - Nom complet : `Client Test`
3. Cliquez sur **"Créer"**
4. Notez les identifiants affichés

### 3. Vendre un Abonnement

1. Dans la liste des clients, cliquez sur **"Vendre"**
2. Choisissez :
   - Type : `1_mois`
   - Connexions max : `1`
   - Montant : `5.00`
3. Cliquez sur **"Vendre"**

### 4. Tester avec IPTV Smarters Pro

Donnez ces informations au client :

```
Type: Xtream Codes API
URL: http://localhost:8888
Username: testclient
Password: Test123!
```

## 🎯 Fonctionnalités Disponibles

- ✅ **Dashboard** avec statistiques
- ✅ **8900+ chaînes** Live TV
- ✅ **Films** et **Séries** VOD
- ✅ **Gestion des clients**
- ✅ **Vente d'abonnements**
- ✅ **Prolongation**
- ✅ **Gestion des vendeurs** (Super Admin)
- ✅ **Rafraîchissement des chaînes**
- ✅ **Historique** et **Logs**

## 🔧 Configuration Avancée

Éditez `.env` pour personnaliser :

```bash
# Port du serveur
PORT=8888

# Identifiants admin
SUPER_ADMIN_USERNAME=superadmin
SUPER_ADMIN_PASSWORD=VotreMotDePasseSecurise!

# Performance
THREAD_POOL_SIZE=1000
```

## 🧪 Tests

```bash
# Tester le serveur
python test_server.py

# Réinitialiser la base de données
python reset_database.py
```

## 🆘 Problèmes Courants

### Le serveur ne démarre pas

**Vérifiez** :
- Python est installé (version 3.7+)
- Les dépendances sont installées
- Le port 8888 n'est pas déjà utilisé

### Impossible de se connecter

**Solution** :
- Vérifiez les identifiants dans `.env`
- Réinitialisez la base de données : `python reset_database.py`

### Les chaînes ne se chargent pas

**Solution** :
- Attendez 2-3 minutes au premier démarrage
- Cliquez sur "🔄 Rafraîchir chaînes" dans le dashboard

## 📖 Documentation Complète

- **`README.md`** - Vue d'ensemble
- **`GUIDE_UTILISATION.md`** - Guide complet
- **`API.md`** - Documentation API

---

✅ **C'est tout ! Votre serveur IPTV est prêt !**
