# 🚀 GUIDE DE RÉUTILISATION - Créer un nouveau projet IPTV

## 📦 3 MÉTHODES POUR RÉCUPÉRER LES FICHIERS

### Méthode 1: Utiliser le package ZIP (RECOMMANDÉ) ✅

Le fichier **`iptv_package_20251228.zip`** contient tous les fichiers essentiels.

```bash
# 1. Extraire le ZIP dans un nouveau dossier
# 2. Suivre les instructions ci-dessous
```

**Avantages:**
- ✅ Tous les fichiers essentiels inclus
- ✅ Aucun fichier inutile
- ✅ Facile à partager
- ✅ Prêt à l'emploi

---

### Méthode 2: Script automatique

#### Windows:
```cmd
copier_fichiers_essentiels.bat
```

#### Linux/Mac:
```bash
chmod +x copier_fichiers_essentiels.sh
./copier_fichiers_essentiels.sh
```

Le script vous demandera le chemin de destination et copiera automatiquement tous les fichiers essentiels.

---

### Méthode 3: Copie manuelle

Copier uniquement ces fichiers:

#### Fichiers Python (6 fichiers)
```
✅ server.py
✅ config.py
✅ database.py
✅ admin_panel.py
✅ vavoo_service.py
✅ multi_service.py
```

#### Configuration (3 fichiers)
```
✅ .env.example
✅ requirements.txt
✅ .gitignore
```

#### Scripts (2 fichiers)
```
✅ start.bat
✅ start.sh
```

#### Utilitaires optionnels (2 fichiers)
```
⚠️ reset_database.py
⚠️ test_server.py
```

---

## 🛠️ INSTALLATION DU NOUVEAU PROJET

### Étape 1: Préparer le dossier

```bash
# Créer un nouveau dossier
mkdir mon_nouveau_iptv
cd mon_nouveau_iptv

# Extraire le ZIP ou copier les fichiers ici
```

### Étape 2: Créer le fichier .env

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### Étape 3: Configurer les paramètres

Éditer le fichier `.env`:

```bash
# Windows
notepad .env

# Linux/Mac
nano .env
```

Modifier ces valeurs:

```env
# Port du serveur
SERVER_PORT=8888

# Identifiants Super Admin
SUPER_ADMIN_USERNAME=votre_admin
SUPER_ADMIN_PASSWORD=VotreMotDePasse123!

# Clé secrète (générer une nouvelle!)
SECRET_KEY=votre_cle_secrete_unique_123456789

# Base de données
DATABASE_PATH=database.db
```

### Étape 4: Installer les dépendances

```bash
pip install -r requirements.txt
```

**Dépendances installées:**
- Flask (serveur web)
- requests (requêtes HTTP)
- python-dotenv (variables d'environnement)

### Étape 5: Démarrer le serveur

#### Windows:
```cmd
start.bat
```

#### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

#### Ou manuellement:
```bash
python server.py
```

---

## 🎯 PERSONNALISATION

### 1. Changer le port

Dans `.env`:
```env
SERVER_PORT=9000
```

### 2. Changer les identifiants admin

Dans `.env`:
```env
SUPER_ADMIN_USERNAME=mon_admin
SUPER_ADMIN_PASSWORD=MonMotDePasse2024!
```

### 3. Personnaliser l'interface

Dans `admin_panel.py`, modifier le CSS:

```python
CSS = """<style>
/* Changer la couleur principale */
.btn-primary{background:#e94560;color:white}  /* Rouge actuel */
.btn-primary{background:#3498db;color:white}  /* Bleu */
.btn-primary{background:#2ecc71;color:white}  /* Vert */

/* Changer le logo */
.logo{font-size:1.5em;color:#e94560;...}
</style>"""
```

### 4. Ajouter d'autres sources IPTV

Dans `multi_service.py`, ajouter de nouvelles sources:

```python
def get_channels_from_autre_source():
    """Récupérer les chaînes d'une autre source"""
    # Votre code ici
    pass
```

---

## 🔐 SÉCURITÉ

### Avant de déployer:

1. **Changer TOUS les mots de passe**
   ```env
   SUPER_ADMIN_PASSWORD=MotDePasseTresFort123!@#
   ```

2. **Générer une nouvelle SECRET_KEY**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

3. **Ne JAMAIS commiter .env dans Git**
   ```bash
   # Vérifier que .env est dans .gitignore
   cat .gitignore | grep .env
   ```

4. **Utiliser HTTPS en production**
   - Configurer un reverse proxy (nginx, Apache)
   - Obtenir un certificat SSL (Let's Encrypt)

5. **Limiter l'accès**
   - Configurer un firewall
   - Utiliser des IP whitelists
   - Activer l'authentification forte

---

## 📊 STRUCTURE DU PROJET

```
mon_nouveau_iptv/
│
├── 🐍 FICHIERS PYTHON
│   ├── server.py              ← Serveur HTTP principal
│   ├── config.py              ← Configuration
│   ├── database.py            ← Base de données SQLite
│   ├── admin_panel.py         ← Interface web admin
│   ├── vavoo_service.py       ← Service Vavoo
│   └── multi_service.py       ← Multi-sources IPTV
│
├── ⚙️ CONFIGURATION
│   ├── .env                   ← Variables d'environnement (à créer)
│   ├── .env.example           ← Template
│   ├── requirements.txt       ← Dépendances Python
│   └── .gitignore            ← Fichiers à ignorer
│
├── 🚀 SCRIPTS
│   ├── start.bat             ← Démarrage Windows
│   ├── start.sh              ← Démarrage Linux/Mac
│   ├── reset_database.py     ← Réinitialiser la DB
│   └── test_server.py        ← Tester le serveur
│
└── 💾 DONNÉES (générées automatiquement)
    └── database.db           ← Base de données SQLite
```

---

## 🧪 TESTER LE NOUVEAU PROJET

### 1. Vérifier que le serveur démarre

```bash
python server.py
```

Vous devriez voir:
```
Serveur demarre sur: http://192.168.x.x:8888
```

### 2. Tester l'accès web

Ouvrir dans le navigateur:
```
http://localhost:8888
```

### 3. Tester le panel admin

```
http://localhost:8888/admin
```

Se connecter avec les identifiants du `.env`

### 4. Tester l'API

```bash
python test_server.py
```

---

## 🐛 DÉPANNAGE

### Erreur: "Port already in use"

Le port 8888 est déjà utilisé. Solutions:

1. Changer le port dans `.env`:
   ```env
   SERVER_PORT=9000
   ```

2. Ou arrêter le processus qui utilise le port:
   ```bash
   # Windows
   netstat -ano | findstr :8888
   taskkill /PID <PID> /F
   
   # Linux/Mac
   lsof -i :8888
   kill -9 <PID>
   ```

### Erreur: "Module not found"

Les dépendances ne sont pas installées:

```bash
pip install -r requirements.txt
```

### Erreur: "Permission denied"

Sur Linux/Mac, rendre les scripts exécutables:

```bash
chmod +x start.sh
chmod +x copier_fichiers_essentiels.sh
```

### Base de données corrompue

Réinitialiser la base de données:

```bash
python reset_database.py
```

---

## 📚 DOCUMENTATION

### Fichiers de documentation disponibles:

- **README.md** - Documentation principale
- **QUICKSTART.md** - Guide de démarrage rapide
- **FICHIERS_A_RECUPERER.md** - Liste des fichiers essentiels
- **GUIDE_REUTILISATION.md** - Ce guide

### URLs importantes:

- Page d'accueil: `http://localhost:8888/`
- Panel Admin: `http://localhost:8888/admin`
- Portail Client: `http://localhost:8888/client`
- API Login: `http://localhost:8888/api/login`

---

## 🎓 EXEMPLES D'UTILISATION

### Exemple 1: Projet local de développement

```bash
# 1. Extraire le ZIP
unzip iptv_package_20251228.zip -d dev_iptv

# 2. Configurer
cd dev_iptv
cp .env.example .env
nano .env  # Modifier les paramètres

# 3. Installer et démarrer
pip install -r requirements.txt
python server.py
```

### Exemple 2: Déploiement sur serveur VPS

```bash
# 1. Uploader les fichiers sur le serveur
scp iptv_package_20251228.zip user@server:/home/user/

# 2. Se connecter au serveur
ssh user@server

# 3. Extraire et configurer
cd /home/user
unzip iptv_package_20251228.zip -d iptv_prod
cd iptv_prod
cp .env.example .env
nano .env  # Configurer pour production

# 4. Installer les dépendances
pip3 install -r requirements.txt

# 5. Démarrer avec systemd ou screen
screen -S iptv
python3 server.py
# Ctrl+A puis D pour détacher
```

### Exemple 3: Projet avec Git

```bash
# 1. Créer un nouveau repo Git
git init mon_iptv
cd mon_iptv

# 2. Extraire les fichiers
unzip ../iptv_package_20251228.zip

# 3. Premier commit
git add .
git commit -m "Initial commit - IPTV server"

# 4. Configurer (ne pas commiter .env!)
cp .env.example .env
nano .env

# 5. Démarrer
pip install -r requirements.txt
python server.py
```

---

## ✅ CHECKLIST FINALE

Avant de considérer le projet prêt:

- [ ] Tous les fichiers essentiels copiés
- [ ] Fichier `.env` créé et configuré
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Mots de passe changés
- [ ] SECRET_KEY générée
- [ ] Port configuré et disponible
- [ ] Serveur démarre sans erreur
- [ ] Page d'accueil accessible
- [ ] Panel admin accessible
- [ ] Connexion admin fonctionne
- [ ] Chaînes IPTV chargées
- [ ] Tests passés (`test_server.py`)

---

## 🎉 FÉLICITATIONS!

Votre nouveau projet IPTV est prêt à être utilisé!

**Fonctionnalités disponibles:**
- ✅ 8873+ chaînes IPTV (Vavoo)
- ✅ Panel d'administration complet
- ✅ Gestion des clients
- ✅ Gestion des abonnements
- ✅ Gestion des vendeurs
- ✅ Système de paiement
- ✅ API Xtream Codes
- ✅ Support IPTV Smarters Pro
- ✅ Multi-connexions
- ✅ Logs et statistiques

---

**Date**: 28 décembre 2025  
**Version**: 1.0  
**Package**: iptv_package_20251228.zip  
**Taille**: 0.04 MB
