# 🚀 Guide de Démarrage Rapide - Render

## ⚡ Déploiement en 5 minutes

### Étape 1 : Préparer votre code

```bash
# Cloner ou naviguer vers votre projet
cd serveur_iptv

# Vérifier que tout est prêt
python check_config.py
```

### Étape 2 : Pousser sur GitHub

```bash
# Initialiser Git (si pas déjà fait)
git init

# Ajouter tous les fichiers
git add .

# Créer le premier commit
git commit -m "Préparation pour Render"

# Ajouter votre dépôt GitHub
git remote add origin https://github.com/VOTRE-USERNAME/serveur-iptv.git

# Pousser le code
git push -u origin main
```

### Étape 3 : Déployer sur Render

1. **Allez sur** https://dashboard.render.com
2. **Cliquez sur** "New +" → "Blueprint"
3. **Connectez** votre dépôt GitHub
4. **Render détecte** automatiquement `render.yaml`
5. **Cliquez sur** "Apply"

### Étape 4 : Configurer les variables sensibles

Dans le dashboard Render, allez dans "Environment" et modifiez :

```
SUPER_ADMIN_PASSWORD = VotreMotDePasseSecurise123!
```

**Important** : Changez le mot de passe par défaut !

### Étape 5 : Accéder à votre serveur

Votre serveur sera accessible à :
```
https://serveur-iptv.onrender.com
```

**Panel Admin** :
```
https://serveur-iptv.onrender.com/admin
```

**Identifiants par défaut** :
- Username : `superadmin`
- Password : Celui que vous avez défini à l'étape 4

---

## 📺 Configuration IPTV Smarters Pro

Dans IPTV Smarters Pro, utilisez :

| Paramètre | Valeur |
|-----------|--------|
| Type | Xtream Codes API |
| Server URL | `https://serveur-iptv.onrender.com` |
| Username | Votre nom d'utilisateur client |
| Password | Votre mot de passe client |

---

## ⚠️ Important

### Plan Gratuit
- Le service s'endort après 15 min d'inactivité
- Premier accès après inactivité : 30-60 secondes de chargement
- 750 heures/mois incluses

### Plan Payant ($7/mois)
- Service toujours actif
- Pas de temps de chargement
- Performances optimales

---

## 🔧 Commandes Utiles

### Voir les logs en temps réel
Dans le dashboard Render → Onglet "Logs"

### Redéployer manuellement
Dans le dashboard Render → "Manual Deploy" → "Clear build cache & deploy"

### Mettre à jour le code
```bash
git add .
git commit -m "Mise à jour"
git push
```
Render redéploie automatiquement !

---

## 🆘 Problèmes Courants

### Le service ne démarre pas
- Vérifiez les logs dans Render
- Assurez-vous que toutes les variables d'environnement sont définies

### Erreur 502
- Le service est en train de démarrer (attendez 1-2 minutes)
- Sur le plan gratuit, le service se réveille (attendez 30-60 secondes)

### Base de données vide
- Vérifiez que le disque persistant est bien configuré
- Chemin de montage : `/opt/render/project/src`

---

## 📖 Documentation Complète

Pour plus de détails, consultez :
- [DEPLOY.md](DEPLOY.md) - Guide complet de déploiement
- [README.md](README.md) - Documentation du projet
- [CHANGELOG.md](CHANGELOG.md) - Historique des modifications

---

✅ **C'est tout ! Votre serveur IPTV est maintenant en ligne !**
