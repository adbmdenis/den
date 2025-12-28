# 📖 Guide d'Utilisation Complet - Serveur IPTV

## 🌐 Votre Serveur

**URL** : https://iptv-0e41.onrender.com

**Status** : ✅ En ligne et fonctionnel
- 📺 **8900 chaînes** disponibles
- 🎬 Films et séries VOD
- ✅ API Xtream Codes opérationnelle

---

## 🔐 Connexion au Panel Admin

### 1. Accéder au Panel

Allez sur : https://iptv-0e41.onrender.com/admin

### 2. Identifiants par Défaut

```
Username : superadmin
Password : Super@2024!
```

⚠️ **IMPORTANT** : Changez ce mot de passe immédiatement après la première connexion !

### 3. Première Connexion

1. Entrez votre username et password
2. Cliquez sur "Connexion"
3. Vous serez redirigé vers le Dashboard

---

## 📊 Le Dashboard (Tableau de Bord)

### Vue d'Ensemble

Le Dashboard affiche :

#### Pour les Super Admins :
- 👥 **Vendeurs** : Nombre total de vendeurs
- 👤 **Clients** : Nombre total de clients
- ✅ **Abonnements actifs** : Abonnements en cours
- 💰 **Ventes** : Nombre total de ventes
- 💵 **CA** : Chiffre d'affaires total

#### Statistiques IPTV (Super Admin uniquement) :
- 📺 **Chaînes Live** : Nombre de chaînes TV
- 🎬 **Films VOD** : Nombre de films
- 📺 **Séries** : Nombre de séries
- 🔑 **Token Vavoo** : Status du token (Valide/Invalide)

### Actions Rapides

- **+ Nouveau client** : Créer un nouveau client
- **Voir les clients** : Liste de tous les clients
- **Historique ventes** : Voir toutes les ventes
- **🔄 Rafraîchir chaînes** : Mettre à jour les chaînes (Super Admin)

---

## 👥 Gestion des Clients

### Créer un Nouveau Client

1. Cliquez sur **"+ Nouveau client"**
2. Remplissez le formulaire :
   - **Username** : Identifiant unique (requis)
   - **Password** : Mot de passe (requis)
   - **Nom complet** : Nom du client
   - **Email** : Email du client
   - **Téléphone** : Numéro de téléphone
   - **Notes** : Notes personnelles
3. Cliquez sur **"Créer"**

### Après Création

Une fenêtre s'affiche avec :
- ✅ Confirmation de création
- 🔑 Identifiants du client
- 📺 URL de la playlist M3U
- 🔗 URL avec token

**Copiez ces informations** et envoyez-les au client !

### Vendre un Abonnement

1. Dans la liste des clients, cliquez sur **"Vendre"**
2. Choisissez :
   - **Type d'abonnement** : 1 mois, 3 mois, 6 mois, 12 mois
   - **Connexions max** : Nombre d'appareils simultanés (1-5)
   - **Montant** : Prix (pré-rempli)
   - **Méthode de paiement** : Espèces, Mobile Money, Carte, Manuel
   - **Status paiement** : Payé, En attente, Annulé
3. Cliquez sur **"Vendre"**

### Actions sur un Client

Pour chaque client, vous pouvez :

- **👁️ Voir** : Afficher les détails complets
  - Informations personnelles
  - Abonnement actif
  - Date d'expiration
  - URL de playlist
  
- **✏️ Modifier** : Changer les informations
  - Nom, email, téléphone
  - Activer/désactiver le compte
  - Changer le mot de passe
  
- **💰 Vendre** : Vendre un nouvel abonnement

- **⏱️ Prolonger** : Ajouter des jours à l'abonnement
  - Choisir le nombre de jours
  - Prolonge l'abonnement existant
  
- **🔌 Connexions** : Modifier le nombre de connexions simultanées
  - Augmenter ou diminuer
  - Prend effet immédiatement

---

## 💰 Gestion des Ventes

### Voir l'Historique

1. Cliquez sur **"Ventes"** dans le menu
2. Vous verrez toutes les ventes avec :
   - Date et heure
   - Client
   - Type d'abonnement
   - Montant
   - Méthode de paiement
   - Status

### Filtrer les Ventes

Utilisez les filtres en haut :
- **Recherche** : Par nom de client
- **Type** : Filtrer par type d'abonnement
- **Status** : Filtrer par status de paiement

---

## 👨‍💼 Gestion des Vendeurs (Super Admin uniquement)

### Créer un Vendeur

1. Allez dans **"Vendeurs"**
2. Cliquez sur **"+ Nouveau vendeur"**
3. Remplissez :
   - Username
   - Password
   - Email
4. Cliquez sur **"Créer"**

### Définir les Quotas

Les quotas définissent ce qu'un vendeur peut vendre :

1. Cliquez sur **"Quotas"** pour un vendeur
2. Remplissez :
   - **Type d'abonnement** : Quel type il peut vendre
   - **Quantité max** : Combien il peut en vendre
   - **Prix autorisé** : À quel prix
   - **Validité** : Nombre de jours de validité du quota
3. Cliquez sur **"Définir quota"**

**Exemple** :
- Type : 1_mois
- Quantité : 100
- Prix : 5.00 EUR
- Validité : 365 jours

→ Le vendeur peut vendre 100 abonnements de 1 mois à 5€ pendant 1 an.

---

## 📦 Types d'Abonnements

### Types par Défaut

| Type | Durée | Prix |
|------|-------|------|
| 1_mois | 30 jours | 5.00 € |
| 3_mois | 90 jours | 12.00 € |
| 6_mois | 180 jours | 20.00 € |
| 12_mois | 365 jours | 35.00 € |

### Créer un Nouveau Type (Super Admin)

1. Allez dans **"Abonnements"**
2. Cliquez sur **"+ Nouveau type"**
3. Remplissez :
   - **Nom** : Nom unique (ex: "2_mois")
   - **Durée** : Nombre de jours
   - **Prix** : Prix en EUR
   - **Stock** : Quantité disponible
   - **Description** : Description optionnelle
4. Cliquez sur **"Créer"**

---

## 🔄 Rafraîchir les Chaînes (Super Admin)

### Quand Rafraîchir ?

- Nouvelles chaînes ajoutées sur Vavoo
- Chaînes manquantes ou non fonctionnelles
- Mise à jour du contenu VOD
- Token Vavoo invalide

### Comment Rafraîchir ?

1. Sur le **Dashboard**
2. Cliquez sur **"🔄 Rafraîchir chaînes"**
3. Confirmez l'action
4. Attendez 1-2 minutes
5. Un message affiche les nouvelles statistiques

**Résultat** :
```
✅ Chaînes mises à jour!

Chaînes: 8900
Films: 450
Séries: 120
```

---

## 📺 Configuration IPTV pour les Clients

### IPTV Smarters Pro

Donnez ces informations à vos clients :

```
Type : Xtream Codes API
Server URL : https://iptv-0e41.onrender.com
Username : [username du client]
Password : [password du client]
```

### URL M3U Directe

```
https://iptv-0e41.onrender.com/get.php?username=USER&password=PASS
```

OU avec token :

```
https://iptv-0e41.onrender.com/get.php?token=TOKEN_DU_CLIENT
```

---

## ⚙️ Paramètres

### Changer Votre Mot de Passe

1. Allez dans **"Paramètres"**
2. Entrez votre **mot de passe actuel**
3. Entrez votre **nouveau mot de passe**
4. Confirmez le **nouveau mot de passe**
5. Cliquez sur **"Modifier"**

---

## 📊 Logs (Super Admin)

### Voir les Logs

1. Allez dans **"Logs"**
2. Vous verrez toutes les actions :
   - Date et heure
   - Action effectuée
   - Détails
   - Adresse IP

### Types d'Actions Loguées

- `login` : Connexion admin/client
- `client_created` : Création de client
- `sale` : Vente d'abonnement
- `subscription_extended` : Prolongation
- `channels_refreshed` : Rafraîchissement des chaînes
- `admin_created` : Création de vendeur
- `quota_set` : Définition de quota

---

## 🆘 Problèmes Courants

### Le Dashboard ne charge pas

**Solution** :
1. Rafraîchissez la page (F5)
2. Videz le cache du navigateur (Ctrl+Shift+Delete)
3. Déconnectez-vous et reconnectez-vous
4. Essayez un autre navigateur

### Les statistiques sont à 0

**Cause** : Le serveur vient de démarrer ou les chaînes ne sont pas chargées

**Solution** :
1. Attendez 2-3 minutes
2. Rafraîchissez la page
3. Si Super Admin, cliquez sur "🔄 Rafraîchir chaînes"

### Erreur "Token invalide"

**Cause** : Votre session a expiré

**Solution** :
1. Déconnectez-vous
2. Reconnectez-vous avec vos identifiants

### Les clients ne peuvent pas se connecter

**Vérifications** :
1. L'abonnement est-il actif ?
2. La date d'expiration est-elle dépassée ?
3. Le compte est-il activé ?
4. Les identifiants sont-ils corrects ?

### Erreur "Quota atteint"

**Cause** : Le vendeur a atteint son quota de ventes

**Solution** (Super Admin) :
1. Allez dans "Vendeurs"
2. Cliquez sur "Quotas" pour le vendeur
3. Augmentez la quantité max
4. Ou créez un nouveau quota

---

## 📱 Espace Client

### URL

https://iptv-0e41.onrender.com/client

### Fonctionnalités

Les clients peuvent :
- Se connecter avec leurs identifiants
- Voir leur abonnement actif
- Voir la date d'expiration
- Obtenir leur URL de playlist
- Voir l'historique de leurs abonnements

---

## 🔒 Sécurité

### Bonnes Pratiques

1. **Changez le mot de passe par défaut** immédiatement
2. **Utilisez des mots de passe forts** (12+ caractères)
3. **Ne partagez jamais** vos identifiants admin
4. **Vérifiez régulièrement** les logs
5. **Désactivez** les comptes inactifs

### Déconnexion

Cliquez toujours sur **"Déconnexion"** en haut à droite quand vous avez terminé.

---

## 📞 Support

### En Cas de Problème

1. Consultez ce guide
2. Vérifiez les logs
3. Testez avec : `python test_deployed_site.py https://iptv-0e41.onrender.com`
4. Consultez la documentation dans les fichiers .md

### Fichiers Utiles

- `DEPLOY.md` - Déploiement
- `FEATURE_REFRESH_CHANNELS.md` - Rafraîchissement
- `FIX_RENDER_ERROR.md` - Erreurs Render
- `ENV_VARIABLES.md` - Variables d'environnement

---

## ✅ Checklist Quotidienne

- [ ] Vérifier que le serveur est en ligne
- [ ] Vérifier les nouvelles ventes
- [ ] Vérifier les abonnements qui expirent bientôt
- [ ] Répondre aux clients
- [ ] Vérifier les logs pour les erreurs

---

## 🎉 Félicitations !

Votre serveur IPTV est maintenant opérationnel avec :
- ✅ 8900 chaînes disponibles
- ✅ Panel d'administration complet
- ✅ Gestion des clients et abonnements
- ✅ API Xtream Codes fonctionnelle
- ✅ Rafraîchissement des chaînes

**Bon business ! 💰**
