# 📦 Fichiers à récupérer pour créer un nouveau projet IPTV

## 🔴 FICHIERS ESSENTIELS (OBLIGATOIRES)

Ces fichiers sont **indispensables** pour que le serveur IPTV fonctionne:

### 1. Fichiers Python principaux
```
✅ server.py              - Serveur HTTP principal (routes, API)
✅ config.py              - Configuration (port, admin, paiements)
✅ database.py            - Gestion base de données SQLite
✅ admin_panel.py         - Interface web admin (HTML/CSS/JS)
✅ vavoo_service.py       - Service pour récupérer les chaînes Vavoo
✅ multi_service.py       - Gestion multi-sources IPTV (optionnel mais recommandé)
```

### 2. Fichiers de configuration
```
✅ .env.example           - Template des variables d'environnement
✅ requirements.txt       - Dépendances Python à installer
✅ .gitignore            - Fichiers à ignorer dans Git
```

### 3. Scripts de démarrage
```
✅ start.bat             - Démarrage automatique Windows
✅ start.sh              - Démarrage automatique Linux/Mac
```

---

## 🟡 FICHIERS UTILES (RECOMMANDÉS)

Ces fichiers facilitent l'utilisation mais ne sont pas obligatoires:

### Scripts utilitaires
```
⚠️ reset_database.py     - Réinitialiser la base de données
⚠️ test_server.py        - Tester le serveur après installation
```

### Documentation
```
📄 README.md             - Documentation principale
📄 QUICKSTART.md         - Guide de démarrage rapide
📄 INSTRUCTIONS.md       - Instructions détaillées
```

---

## 🔵 FICHIERS À NE PAS RÉCUPÉRER

Ces fichiers sont spécifiques à ce projet ou temporaires:

### Fichiers temporaires/debug
```
❌ fix_admin_panel_complete.py  - Script de correction (déjà appliqué)
❌ fix_admin_panel.py           - Script de correction (déjà appliqué)
❌ test_admin_buttons.py        - Tests spécifiques
❌ database.db                  - Base de données (sera recréée)
❌ __pycache__/                 - Cache Python (sera recréé)
```

### Documentation spécifique
```
❌ DIFFERENCES.md               - Différences avec l'ancien projet
❌ FIX_JAVASCRIPT_ERROR.md      - Documentation de correction
❌ PROBLEME_RESOLU.md           - Documentation de résolution
❌ START_HERE.txt               - Guide spécifique
❌ LISEZMOI.txt                 - Guide spécifique
```

---

## 📋 CHECKLIST POUR NOUVEAU PROJET

### Étape 1: Créer le dossier du nouveau projet
```bash
mkdir mon_nouveau_iptv
cd mon_nouveau_iptv
```

### Étape 2: Copier les fichiers essentiels
```bash
# Copier les fichiers Python principaux
copy server.py mon_nouveau_iptv/
copy config.py mon_nouveau_iptv/
copy database.py mon_nouveau_iptv/
copy admin_panel.py mon_nouveau_iptv/
copy vavoo_service.py mon_nouveau_iptv/
copy multi_service.py mon_nouveau_iptv/

# Copier les fichiers de configuration
copy .env.example mon_nouveau_iptv/
copy requirements.txt mon_nouveau_iptv/
copy .gitignore mon_nouveau_iptv/

# Copier les scripts de démarrage
copy start.bat mon_nouveau_iptv/
copy start.sh mon_nouveau_iptv/

# (Optionnel) Copier les scripts utilitaires
copy reset_database.py mon_nouveau_iptv/
copy test_server.py mon_nouveau_iptv/
```

### Étape 3: Configurer le nouveau projet
```bash
cd mon_nouveau_iptv

# Créer le fichier .env à partir du template
copy .env.example .env

# Éditer .env avec vos paramètres
notepad .env
```

### Étape 4: Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 5: Démarrer le serveur
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

---

## 🎯 STRUCTURE MINIMALE DU NOUVEAU PROJET

Voici la structure minimale pour un projet IPTV fonctionnel:

```
mon_nouveau_iptv/
├── server.py              ← Serveur principal
├── config.py              ← Configuration
├── database.py            ← Base de données
├── admin_panel.py         ← Interface admin
├── vavoo_service.py       ← Service Vavoo
├── multi_service.py       ← Multi-sources (optionnel)
├── .env                   ← Variables d'environnement (à créer)
├── .env.example           ← Template
├── requirements.txt       ← Dépendances
├── .gitignore            ← Git ignore
├── start.bat             ← Démarrage Windows
└── start.sh              ← Démarrage Linux/Mac
```

---

## ⚙️ PERSONNALISATION DU NOUVEAU PROJET

### 1. Modifier config.py
```python
# Changer le port si nécessaire
SERVER_PORT = 8888  # ou autre port

# Changer les identifiants admin
SUPER_ADMIN_USERNAME = "votre_admin"
SUPER_ADMIN_PASSWORD = "votre_password"
```

### 2. Créer le fichier .env
```bash
# Copier le template
copy .env.example .env

# Éditer avec vos valeurs
SERVER_PORT=8888
SUPER_ADMIN_USERNAME=admin
SUPER_ADMIN_PASSWORD=VotreMotDePasse123!
SECRET_KEY=votre_cle_secrete_unique
```

### 3. Personnaliser l'interface (optionnel)
Dans `admin_panel.py`, vous pouvez modifier:
- Les couleurs du CSS
- Le logo
- Les textes
- Les fonctionnalités

---

## 🚀 COMMANDES RAPIDES

### Copier tous les fichiers essentiels en une commande (Windows)
```cmd
xcopy /Y server.py config.py database.py admin_panel.py vavoo_service.py multi_service.py .env.example requirements.txt .gitignore start.bat start.sh C:\chemin\vers\nouveau_projet\
```

### Copier tous les fichiers essentiels en une commande (Linux/Mac)
```bash
cp server.py config.py database.py admin_panel.py vavoo_service.py multi_service.py .env.example requirements.txt .gitignore start.bat start.sh /chemin/vers/nouveau_projet/
```

---

## 📦 CRÉER UN PACKAGE RÉUTILISABLE

Pour créer un package zip avec tous les fichiers essentiels:

### Windows (PowerShell)
```powershell
$files = @(
    "server.py",
    "config.py", 
    "database.py",
    "admin_panel.py",
    "vavoo_service.py",
    "multi_service.py",
    ".env.example",
    "requirements.txt",
    ".gitignore",
    "start.bat",
    "start.sh"
)
Compress-Archive -Path $files -DestinationPath iptv_package.zip
```

### Linux/Mac
```bash
zip iptv_package.zip \
    server.py \
    config.py \
    database.py \
    admin_panel.py \
    vavoo_service.py \
    multi_service.py \
    .env.example \
    requirements.txt \
    .gitignore \
    start.bat \
    start.sh
```

---

## 🔐 SÉCURITÉ

Avant de déployer ailleurs:

1. ✅ **Changer les identifiants admin** dans `.env`
2. ✅ **Générer une nouvelle SECRET_KEY** unique
3. ✅ **Ne jamais commiter le fichier `.env`** dans Git
4. ✅ **Utiliser des mots de passe forts**
5. ✅ **Configurer un firewall** si déployé sur internet

---

## 📞 SUPPORT

Si vous avez des questions sur la réutilisation de ces fichiers:
1. Lisez d'abord `README.md` et `QUICKSTART.md`
2. Vérifiez que toutes les dépendances sont installées
3. Assurez-vous que le port n'est pas déjà utilisé
4. Consultez les logs du serveur pour les erreurs

---

**Date de création**: 28 décembre 2025  
**Version**: 1.0  
**Compatibilité**: Windows, Linux, Mac
