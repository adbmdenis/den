# ✅ Checklist de Déploiement sur Render

Utilisez cette checklist pour vous assurer que tout est prêt avant et après le déploiement.

## 📋 Avant le Déploiement

### 1. Préparation du Code

- [ ] Tous les fichiers sont présents :
  - [ ] `server.py`
  - [ ] `config.py`
  - [ ] `database.py`
  - [ ] `multi_service.py`
  - [ ] `admin_panel.py`
  - [ ] `vavoo_service.py`
  - [ ] `requirements.txt`
  - [ ] `render.yaml`
  - [ ] `Procfile`
  - [ ] `runtime.txt`
  - [ ] `.gitignore`

- [ ] Vérification de la configuration :
  ```bash
  python check_config.py
  ```

- [ ] Génération d'une clé secrète :
  ```bash
  python generate_secret_key.py
  ```
  - [ ] Clé secrète copiée et sauvegardée en lieu sûr

### 2. Sécurité

- [ ] Le fichier `.gitignore` est présent
- [ ] `database.db` est dans `.gitignore`
- [ ] `.env` est dans `.gitignore`
- [ ] Aucun mot de passe en clair dans le code
- [ ] Mot de passe admin fort choisi (min. 12 caractères)

### 3. Git et GitHub

- [ ] Dépôt Git initialisé :
  ```bash
  git init
  ```

- [ ] Tous les fichiers ajoutés :
  ```bash
  git add .
  ```

- [ ] Premier commit créé :
  ```bash
  git commit -m "Préparation pour Render"
  ```

- [ ] Dépôt GitHub créé
- [ ] Remote ajouté :
  ```bash
  git remote add origin https://github.com/VOTRE-USERNAME/serveur-iptv.git
  ```

- [ ] Code poussé sur GitHub :
  ```bash
  git push -u origin main
  ```

## 🚀 Déploiement sur Render

### 4. Configuration Render

- [ ] Compte Render créé (https://render.com)
- [ ] Nouveau Blueprint créé
- [ ] Dépôt GitHub connecté
- [ ] `render.yaml` détecté automatiquement
- [ ] Service créé avec succès

### 5. Variables d'Environnement

- [ ] `PORT` : Défini (8888)
- [ ] `SECRET_KEY` : Généré ou défini manuellement
- [ ] `SUPER_ADMIN_USERNAME` : Défini
- [ ] `SUPER_ADMIN_PASSWORD` : **CHANGÉ** (ne pas utiliser la valeur par défaut !)
- [ ] `SUPER_ADMIN_EMAIL` : Défini avec votre email

### 6. Disque Persistant

- [ ] Disque créé :
  - [ ] Nom : `iptv-data`
  - [ ] Chemin : `/opt/render/project/src`
  - [ ] Taille : 1 GB

### 7. Déploiement

- [ ] Build réussi (vérifier les logs)
- [ ] Service démarré (statut "Live")
- [ ] URL du service notée : `https://__________.onrender.com`

## ✅ Après le Déploiement

### 8. Tests de Base

- [ ] Page d'accueil accessible :
  ```
  https://votre-service.onrender.com/
  ```

- [ ] API status fonctionne :
  ```
  https://votre-service.onrender.com/api/status
  ```

- [ ] Panel admin accessible :
  ```
  https://votre-service.onrender.com/admin
  ```

- [ ] Connexion admin réussie avec les identifiants définis

### 9. Tests Fonctionnels

- [ ] Création d'un vendeur (admin) réussie
- [ ] Création d'un client réussie
- [ ] Vente d'un abonnement réussie
- [ ] Génération de playlist M3U réussie
- [ ] API Xtream Codes fonctionne

### 10. Tests IPTV

- [ ] Configuration IPTV Smarters Pro :
  - [ ] Type : Xtream Codes API
  - [ ] Server URL : `https://votre-service.onrender.com`
  - [ ] Username : [client créé]
  - [ ] Password : [mot de passe client]

- [ ] Connexion IPTV Smarters Pro réussie
- [ ] Liste des chaînes chargée
- [ ] Lecture d'une chaîne réussie

### 11. Monitoring

- [ ] Logs vérifiés (onglet "Logs" dans Render)
- [ ] Métriques vérifiées (onglet "Metrics")
- [ ] Aucune erreur critique dans les logs

### 12. Sécurité Post-Déploiement

- [ ] Mot de passe admin changé (si valeur par défaut utilisée)
- [ ] Clé secrète sauvegardée dans un gestionnaire de mots de passe
- [ ] Accès admin testé avec le nouveau mot de passe
- [ ] Variables d'environnement sensibles notées en lieu sûr

### 13. Documentation

- [ ] URL du service documentée
- [ ] Identifiants admin sauvegardés en lieu sûr
- [ ] Instructions partagées avec l'équipe (si applicable)

## 📝 Informations à Sauvegarder

Notez ces informations dans un endroit sûr :

```
=== SERVEUR IPTV - INFORMATIONS DE DÉPLOIEMENT ===

URL du service : https://________________.onrender.com

Super Admin :
  - Username : ________________
  - Password : ________________
  - Email : ________________

Variables d'environnement :
  - SECRET_KEY : ________________
  - PORT : 8888

Render :
  - Nom du service : ________________
  - Région : ________________
  - Plan : Free / Starter / Pro

GitHub :
  - Dépôt : https://github.com/________________/serveur-iptv

Date de déploiement : ________________
```

## 🔄 Maintenance

### Mises à Jour

- [ ] Processus de mise à jour documenté :
  ```bash
  git add .
  git commit -m "Description des changements"
  git push
  ```

- [ ] Redéploiement automatique vérifié

### Sauvegardes

- [ ] Stratégie de sauvegarde de la base de données définie
- [ ] Fréquence de sauvegarde décidée
- [ ] Lieu de stockage des sauvegardes défini

### Monitoring

- [ ] Alertes configurées (si plan payant)
- [ ] Fréquence de vérification des logs définie
- [ ] Personne responsable du monitoring identifiée

## 🆘 En Cas de Problème

### Contacts

- [ ] Support Render : https://render.com/support
- [ ] Documentation : https://render.com/docs
- [ ] Community : https://community.render.com

### Rollback

Si quelque chose ne va pas :

1. [ ] Vérifier les logs dans Render
2. [ ] Revenir à la version précédente sur GitHub :
   ```bash
   git revert HEAD
   git push
   ```
3. [ ] Ou redéployer manuellement une version antérieure dans Render

## ✅ Déploiement Terminé !

Une fois toutes les cases cochées, votre serveur IPTV est :
- ✅ Déployé sur Render
- ✅ Sécurisé
- ✅ Fonctionnel
- ✅ Prêt pour la production

---

**Date de complétion** : ________________

**Déployé par** : ________________

**Notes supplémentaires** :
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
