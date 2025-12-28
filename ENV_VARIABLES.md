# Variables d'Environnement

Ce document liste toutes les variables d'environnement utilisées par le serveur IPTV.

## 📋 Variables Requises

### PORT
- **Description** : Port sur lequel le serveur écoute
- **Valeur par défaut** : `8888`
- **Render** : Automatiquement défini par Render
- **Exemple** : `8888`

### SECRET_KEY
- **Description** : Clé secrète pour l'authentification et la sécurité
- **Valeur par défaut** : Générée automatiquement si non définie
- **Render** : Utilisez "Generate Value" dans Render
- **Exemple** : `a1b2c3d4e5f6...` (64 caractères hexadécimaux)
- **Génération** : `python generate_secret_key.py`

### SUPER_ADMIN_USERNAME
- **Description** : Nom d'utilisateur du super administrateur
- **Valeur par défaut** : `superadmin`
- **Render** : Définissez votre propre valeur
- **Exemple** : `admin`, `superadmin`, `root`

### SUPER_ADMIN_PASSWORD
- **Description** : Mot de passe du super administrateur
- **Valeur par défaut** : `Super@2024!`
- **Render** : ⚠️ **CHANGEZ CETTE VALEUR !**
- **Exemple** : `MonMotDePasseSecurise123!`
- **Recommandations** :
  - Minimum 12 caractères
  - Majuscules et minuscules
  - Chiffres et caractères spéciaux
  - Ne pas utiliser de mots du dictionnaire

### SUPER_ADMIN_EMAIL
- **Description** : Email du super administrateur
- **Valeur par défaut** : `admin@iptv.local`
- **Render** : Définissez votre email
- **Exemple** : `admin@votredomaine.com`

## 📋 Variables Optionnelles

### DATABASE_PATH
- **Description** : Chemin vers le fichier de base de données SQLite
- **Valeur par défaut** : `database.db` (dans le répertoire du projet)
- **Render** : Laissez la valeur par défaut (le disque persistant gère cela)
- **Exemple** : `/opt/render/project/src/database.db`

### TOKEN_REFRESH_INTERVAL
- **Description** : Intervalle de rafraîchissement du token VAVOO (en secondes)
- **Valeur par défaut** : `900` (15 minutes)
- **Render** : Laissez la valeur par défaut
- **Exemple** : `900`, `600`, `1800`

### HOST
- **Description** : Adresse IP sur laquelle le serveur écoute
- **Valeur par défaut** : `0.0.0.0` (toutes les interfaces)
- **Render** : Laissez la valeur par défaut
- **Exemple** : `0.0.0.0`, `127.0.0.1`

## 🔧 Configuration sur Render

### Méthode 1 : Via render.yaml (Automatique)

Le fichier `render.yaml` définit automatiquement les variables :

```yaml
envVars:
  - key: PORT
    value: 8888
  - key: SECRET_KEY
    generateValue: true  # Render génère automatiquement
  - key: SUPER_ADMIN_USERNAME
    value: superadmin
  - key: SUPER_ADMIN_PASSWORD
    value: Super@2024!  # ⚠️ À CHANGER après déploiement
  - key: SUPER_ADMIN_EMAIL
    value: admin@iptv.local
```

### Méthode 2 : Via le Dashboard Render (Manuel)

1. Allez dans votre service sur Render
2. Cliquez sur "Environment"
3. Ajoutez chaque variable :
   - Cliquez sur "Add Environment Variable"
   - Entrez le nom (ex: `SECRET_KEY`)
   - Entrez la valeur
   - Cliquez sur "Save Changes"

### Méthode 3 : Via .env (Local uniquement)

Pour le développement local, créez un fichier `.env` :

```bash
# Copiez .env.example vers .env
cp .env.example .env

# Éditez .env avec vos valeurs
nano .env
```

**⚠️ Important** : Le fichier `.env` est dans `.gitignore` et ne sera JAMAIS commité.

## 🔒 Sécurité

### Variables Sensibles

Ces variables contiennent des informations sensibles :
- `SECRET_KEY` : Ne JAMAIS partager
- `SUPER_ADMIN_PASSWORD` : Ne JAMAIS commiter dans Git
- `DATABASE_PATH` : Peut contenir des chemins sensibles

### Bonnes Pratiques

1. **Ne commitez JAMAIS** les variables sensibles dans Git
2. **Utilisez des mots de passe forts** pour `SUPER_ADMIN_PASSWORD`
3. **Changez les valeurs par défaut** immédiatement après le déploiement
4. **Utilisez "Generate Value"** dans Render pour `SECRET_KEY`
5. **Sauvegardez** vos variables d'environnement dans un gestionnaire de mots de passe

### Rotation des Secrets

Pour changer `SECRET_KEY` :

1. Générez une nouvelle clé : `python generate_secret_key.py`
2. Mettez à jour la variable dans Render
3. Le service redémarrera automatiquement
4. ⚠️ Tous les utilisateurs devront se reconnecter

## 📝 Exemples de Configuration

### Configuration Minimale (Développement)

```bash
PORT=8888
SECRET_KEY=dev_secret_key_not_for_production
SUPER_ADMIN_USERNAME=admin
SUPER_ADMIN_PASSWORD=admin123
SUPER_ADMIN_EMAIL=admin@localhost
```

### Configuration Production (Render)

```bash
PORT=8888
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
SUPER_ADMIN_USERNAME=superadmin
SUPER_ADMIN_PASSWORD=MonMotDePasseTresSecurise2024!@#
SUPER_ADMIN_EMAIL=admin@mondomaine.com
DATABASE_PATH=/opt/render/project/src/database.db
TOKEN_REFRESH_INTERVAL=900
```

## 🆘 Dépannage

### Variable non reconnue

**Symptôme** : Le serveur utilise la valeur par défaut au lieu de votre variable

**Solution** :
1. Vérifiez l'orthographe de la variable
2. Redémarrez le service après modification
3. Vérifiez les logs pour voir quelle valeur est utilisée

### SECRET_KEY change à chaque redémarrage

**Symptôme** : Les utilisateurs doivent se reconnecter après chaque redémarrage

**Solution** :
1. Définissez explicitement `SECRET_KEY` dans les variables d'environnement
2. Ne laissez pas la génération automatique se faire à chaque démarrage

### Mot de passe admin ne fonctionne pas

**Symptôme** : Impossible de se connecter avec le mot de passe défini

**Solution** :
1. Vérifiez que `SUPER_ADMIN_PASSWORD` est bien défini
2. Vérifiez qu'il n'y a pas d'espaces avant/après
3. Redémarrez le service après modification
4. Vérifiez les logs pour voir si la variable est bien lue

## 📚 Ressources

- [Documentation Render - Variables d'environnement](https://render.com/docs/environment-variables)
- [Bonnes pratiques de sécurité](https://render.com/docs/security)
- [Guide de déploiement complet](DEPLOY.md)

---

✅ **Configurez correctement vos variables d'environnement pour un déploiement sécurisé !**
