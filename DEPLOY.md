# Guide de Déploiement sur Render

## 📋 Prérequis

1. Un compte sur [Render.com](https://render.com) (gratuit)
2. Votre code sur GitHub, GitLab ou Bitbucket

## 🚀 Déploiement Automatique

### Option 1 : Avec render.yaml (Recommandé)

1. **Poussez votre code sur GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/votre-username/serveur-iptv.git
   git push -u origin main
   ```

2. **Connectez-vous à Render**
   - Allez sur https://dashboard.render.com
   - Cliquez sur "New +" → "Blueprint"
   - Connectez votre dépôt GitHub
   - Render détectera automatiquement le fichier `render.yaml`
   - Cliquez sur "Apply"

3. **Configuration automatique**
   - Le service sera créé avec toutes les variables d'environnement
   - Un disque persistant sera créé pour la base de données
   - Le déploiement démarre automatiquement

### Option 2 : Déploiement Manuel

1. **Créer un nouveau Web Service**
   - Allez sur https://dashboard.render.com
   - Cliquez sur "New +" → "Web Service"
   - Connectez votre dépôt

2. **Configuration du service**
   - **Name**: `serveur-iptv`
   - **Region**: Frankfurt (ou autre)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
   - **Plan**: Free (ou payant pour plus de performances)

3. **Variables d'environnement**
   Ajoutez ces variables dans l'onglet "Environment" :
   
   | Variable | Valeur | Description |
   |----------|--------|-------------|
   | `PORT` | 8888 | Port du serveur (auto-détecté par Render) |
   | `SECRET_KEY` | [généré] | Clé secrète (cliquez sur "Generate") |
   | `SUPER_ADMIN_USERNAME` | superadmin | Nom d'utilisateur admin |
   | `SUPER_ADMIN_PASSWORD` | VotreMotDePasse123! | Mot de passe admin (CHANGEZ-LE!) |
   | `SUPER_ADMIN_EMAIL` | admin@votredomaine.com | Email admin |
   | `PYTHON_VERSION` | 3.11.0 | Version Python |

4. **Ajouter un disque persistant**
   - Allez dans l'onglet "Disks"
   - Cliquez sur "Add Disk"
   - **Name**: `iptv-data`
   - **Mount Path**: `/opt/render/project/src`
   - **Size**: 1 GB (gratuit)
   - Cliquez sur "Save"

5. **Déployer**
   - Cliquez sur "Create Web Service"
   - Attendez que le déploiement se termine (5-10 minutes)

## 🔗 Accès à votre serveur

Une fois déployé, votre serveur sera accessible à :
```
https://serveur-iptv.onrender.com
```

### URLs importantes :
- **Accueil**: `https://serveur-iptv.onrender.com/`
- **Panel Admin**: `https://serveur-iptv.onrender.com/admin`
- **Espace Client**: `https://serveur-iptv.onrender.com/client`
- **API Status**: `https://serveur-iptv.onrender.com/api/status`

## 📺 Configuration IPTV Smarters Pro

Utilisez ces paramètres dans IPTV Smarters Pro :

| Paramètre | Valeur |
|-----------|--------|
| **Type** | Xtream Codes API |
| **Server URL** | `https://serveur-iptv.onrender.com` |
| **Username** | Votre nom d'utilisateur |
| **Password** | Votre mot de passe |

## ⚙️ Configuration Avancée

### Mise à jour des variables d'environnement

1. Allez dans votre service sur Render
2. Cliquez sur "Environment"
3. Modifiez les variables
4. Cliquez sur "Save Changes"
5. Le service redémarrera automatiquement

### Logs et Monitoring

- **Logs en temps réel**: Onglet "Logs" dans Render
- **Métriques**: Onglet "Metrics" (CPU, RAM, requêtes)
- **Alertes**: Configurez des alertes email

### Redéploiement

Pour redéployer après des modifications :
```bash
git add .
git commit -m "Mise à jour"
git push
```

Render redéploiera automatiquement.

### Redémarrage manuel

Dans le dashboard Render :
1. Cliquez sur "Manual Deploy"
2. Sélectionnez "Clear build cache & deploy"

## 🔒 Sécurité

### Recommandations importantes :

1. **Changez le mot de passe admin** immédiatement après le premier déploiement
2. **Utilisez une SECRET_KEY forte** (générée automatiquement par Render)
3. **Activez HTTPS** (automatique sur Render)
4. **Limitez l'accès** en utilisant les fonctionnalités de sécurité de Render

### Variables sensibles

Ne commitez JAMAIS ces fichiers :
- `.env` (déjà dans .gitignore)
- `database.db` (déjà dans .gitignore)
- Fichiers contenant des mots de passe

## 📊 Plan Gratuit vs Payant

### Plan Gratuit (Free)
- ✅ 750 heures/mois
- ✅ HTTPS automatique
- ✅ Déploiement automatique
- ✅ 1 GB disque persistant
- ⚠️ Le service s'endort après 15 min d'inactivité
- ⚠️ Redémarrage lent (30-60 secondes)

### Plan Payant (Starter - $7/mois)
- ✅ Toujours actif (pas de mise en veille)
- ✅ Plus de RAM et CPU
- ✅ Démarrage instantané
- ✅ Support prioritaire

## 🐛 Dépannage

### Le service ne démarre pas
1. Vérifiez les logs dans l'onglet "Logs"
2. Vérifiez que toutes les variables d'environnement sont définies
3. Vérifiez que le disque persistant est bien monté

### Base de données vide après redémarrage
- Assurez-vous que le disque persistant est configuré
- Le chemin de montage doit être `/opt/render/project/src`

### Erreur 502 Bad Gateway
- Le service est en train de démarrer (attendez 1-2 minutes)
- Sur le plan gratuit, le service se réveille (attendez 30-60 secondes)

### Token VAVOO invalide
- Le service rafraîchit automatiquement le token toutes les 15 minutes
- Vérifiez les logs pour voir si le token est obtenu correctement

## 📞 Support

- **Documentation Render**: https://render.com/docs
- **Community Forum**: https://community.render.com
- **Status Page**: https://status.render.com

## 🔄 Mises à jour

Pour mettre à jour votre serveur :

1. Modifiez votre code localement
2. Testez localement avec `python server.py`
3. Commitez et poussez :
   ```bash
   git add .
   git commit -m "Description des changements"
   git push
   ```
4. Render redéploie automatiquement

## 📝 Notes importantes

- **Premier démarrage** : Peut prendre 5-10 minutes
- **Base de données** : Sauvegardée sur le disque persistant
- **Logs** : Conservés pendant 7 jours sur le plan gratuit
- **Domaine personnalisé** : Possible sur tous les plans (même gratuit)

---

✅ **Votre serveur IPTV est maintenant prêt pour la production !**
