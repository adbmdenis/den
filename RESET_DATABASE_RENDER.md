# 🔄 Réinitialiser la Base de Données sur Render

## 📋 Objectif

Remettre la base de données à zéro sur Render pour repartir avec une installation propre.

## ⚠️ ATTENTION

Cette opération va supprimer :
- ❌ Tous les clients
- ❌ Tous les abonnements
- ❌ Toutes les ventes
- ❌ Tous les vendeurs (sauf super admin)
- ❌ Tous les logs

## ✅ Solution : Supprimer le Disque Persistant

### Méthode 1 : Via le Dashboard Render (Recommandé)

#### Étape 1 : Aller sur Render

1. Allez sur https://dashboard.render.com
2. Cliquez sur votre service "iptv-0e41"

#### Étape 2 : Supprimer le Disque

1. Cliquez sur **"Disks"** dans le menu de gauche
2. Vous verrez le disque "iptv-data" (1 GB)
3. Cliquez sur **"Delete"** ou l'icône de suppression
4. Confirmez la suppression

#### Étape 3 : Recréer le Disque

1. Cliquez sur **"Add Disk"**
2. Remplissez :
   ```
   Name: iptv-data
   Mount Path: /opt/render/project/src
   Size: 1 GB
   ```
3. Cliquez sur **"Save"**

#### Étape 4 : Redéployer

1. Allez dans **"Manual Deploy"**
2. Cliquez sur **"Clear build cache & deploy"**
3. Attendez 5-10 minutes

#### Étape 5 : Vérifier

1. Allez sur https://iptv-0e41.onrender.com/login
2. Connectez-vous avec les identifiants configurés dans Environment
3. Vérifiez que tout est vide (0 clients, 0 ventes, etc.)

### Méthode 2 : Via SSH (Plan Payant uniquement)

Si vous avez un plan payant avec accès SSH :

```bash
# Se connecter
render ssh

# Aller dans le répertoire
cd /opt/render/project/src

# Sauvegarder (optionnel)
cp database.db database.db.backup

# Supprimer la base de données
rm database.db

# Redémarrer le service
# (Le service redémarrera automatiquement et recréera la base)
```

### Méthode 3 : Redéployer Complètement

#### Option A : Clear Build Cache

1. Dashboard → Votre service
2. Manual Deploy → **"Clear build cache & deploy"**
3. Cochez **"Clear build cache"**
4. Cliquez sur **"Deploy"**

#### Option B : Supprimer et Recréer le Service

1. **Supprimez** le service actuel
2. **Recréez-le** avec le Blueprint
3. La base de données sera vierge

## 🔐 Configurer les Identifiants

Après la réinitialisation, configurez les identifiants :

### Sur Render Dashboard

1. Allez dans **"Environment"**
2. Ajoutez/Modifiez :
   ```
   SUPER_ADMIN_USERNAME = superadmin
   SUPER_ADMIN_PASSWORD = VotreNouveauMotDePasse2024!
   SUPER_ADMIN_EMAIL = admin@votredomaine.com
   ```
3. **Save Changes**

## 🧪 Tester Après Réinitialisation

### Test 1 : Connexion

```bash
python test_admin_functions.py
```

Devrait afficher :
```
✅ Connexion réussie !
```

### Test 2 : Statistiques

Toutes les stats devraient être à 0 :
- Clients : 0
- Abonnements : 0
- Ventes : 0

### Test 3 : Créer un Client

1. Connectez-vous au panel admin
2. Cliquez sur "+ Nouveau client"
3. Créez un client de test
4. Vérifiez qu'il apparaît dans la liste

## 📊 État Après Réinitialisation

```
✅ Base de données vierge
✅ Super admin créé
✅ Types d'abonnements créés (1, 3, 6, 12 mois)
✅ Cache Vavoo initialisé
✅ 0 clients
✅ 0 abonnements
✅ 0 ventes
✅ 0 logs
```

## 🔄 Workflow Complet

```
1. Supprimer le disque sur Render
   ↓
2. Recréer le disque
   ↓
3. Configurer les variables d'environnement
   ↓
4. Redéployer
   ↓
5. Attendre 5-10 minutes
   ↓
6. Se connecter
   ↓
7. Vérifier que tout est à 0
   ↓
8. Créer un client de test
   ↓
9. ✅ Prêt à utiliser !
```

## 🆘 En Cas de Problème

### Le disque ne se supprime pas

**Solution** : Arrêtez le service d'abord
1. Settings → Suspend Service
2. Supprimez le disque
3. Recréez le disque
4. Resume Service

### La base de données n'est pas réinitialisée

**Solution** : Clear build cache
1. Manual Deploy
2. Clear build cache & deploy

### Les identifiants ne fonctionnent toujours pas

**Solution** : Vérifiez les variables d'environnement
1. Environment
2. Vérifiez SUPER_ADMIN_USERNAME et SUPER_ADMIN_PASSWORD
3. Save Changes
4. Attendez le redémarrage

## 📝 Checklist

- [ ] Sauvegarder les données importantes (si nécessaire)
- [ ] Aller sur Render Dashboard
- [ ] Supprimer le disque "iptv-data"
- [ ] Recréer le disque
- [ ] Configurer les variables d'environnement
- [ ] Redéployer
- [ ] Attendre 5-10 minutes
- [ ] Tester la connexion
- [ ] Vérifier que tout est à 0
- [ ] Créer un client de test
- [ ] ✅ Base de données réinitialisée !

## 🎯 Résultat Final

Après la réinitialisation :

```
✅ Base de données propre
✅ Identifiants admin configurés
✅ Connexion fonctionnelle
✅ Tous les boutons fonctionnent
✅ Création de clients OK
✅ Vente d'abonnements OK
✅ 8900 chaînes disponibles
```

---

## 🚀 Action Immédiate

1. **Allez sur** : https://dashboard.render.com
2. **Cliquez sur** : Votre service → Disks
3. **Supprimez** : Le disque "iptv-data"
4. **Recréez** : Un nouveau disque
5. **Redéployez** : Clear build cache & deploy

---

**Une fois réinitialisé, tout fonctionnera parfaitement ! 🎉**
