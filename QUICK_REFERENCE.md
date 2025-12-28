# ⚡ Référence Rapide - Serveur IPTV

## 🔗 URLs Importantes

| Page | URL |
|------|-----|
| **Accueil** | https://iptv-0e41.onrender.com/ |
| **Panel Admin** | https://iptv-0e41.onrender.com/admin |
| **Espace Client** | https://iptv-0e41.onrender.com/client |
| **API Status** | https://iptv-0e41.onrender.com/api/status |

## 🔐 Identifiants par Défaut

```
Username: superadmin
Password: Super@2024!
```

⚠️ **CHANGEZ CE MOT DE PASSE !**

## 🎯 Actions Rapides

### Créer un Client
1. Dashboard → **"+ Nouveau client"**
2. Remplir : Username, Password
3. **Créer**
4. Copier les infos affichées

### Vendre un Abonnement
1. Clients → Cliquer **"Vendre"** sur un client
2. Choisir : Type, Connexions, Montant
3. **Vendre**

### Prolonger un Abonnement
1. Clients → Cliquer **"Prolonger"** sur un client
2. Entrer : Nombre de jours
3. **Prolonger**

### Rafraîchir les Chaînes (Super Admin)
1. Dashboard → **"🔄 Rafraîchir chaînes"**
2. Confirmer
3. Attendre 1-2 minutes

## 📺 Configuration Client IPTV

### IPTV Smarters Pro
```
Type: Xtream Codes API
URL: https://iptv-0e41.onrender.com
Username: [client_username]
Password: [client_password]
```

### URL M3U
```
https://iptv-0e41.onrender.com/get.php?username=USER&password=PASS
```

## 📊 Statistiques Actuelles

- 📺 **Chaînes** : 8900
- 🎬 **Films** : ~450
- 📺 **Séries** : ~120
- ✅ **Status** : En ligne

## 🔧 Dépannage Express

| Problème | Solution |
|----------|----------|
| Dashboard vide | F5 + Attendre 30 secondes |
| Token invalide | Déconnexion → Reconnexion |
| Stats à 0 | Attendre 2 min + F5 |
| Client ne se connecte pas | Vérifier abonnement actif |

## 📱 Menu Navigation

```
📊 Dashboard       → Vue d'ensemble
👥 Clients         → Liste des clients
💰 Ventes          → Historique des ventes
👨‍💼 Vendeurs       → Gestion vendeurs (Super Admin)
📦 Abonnements     → Types d'abonnements (Super Admin)
📋 Logs            → Historique actions (Super Admin)
⚙️ Paramètres      → Changer mot de passe
```

## 💰 Types d'Abonnements

| Type | Durée | Prix |
|------|-------|------|
| 1_mois | 30j | 5€ |
| 3_mois | 90j | 12€ |
| 6_mois | 180j | 20€ |
| 12_mois | 365j | 35€ |

## 🔄 Workflow Complet

### Nouveau Client + Vente

```
1. + Nouveau client
   ↓
2. Remplir formulaire
   ↓
3. Créer
   ↓
4. Copier infos
   ↓
5. Cliquer "Vendre"
   ↓
6. Choisir type
   ↓
7. Vendre
   ↓
8. Envoyer infos au client
```

## 🧪 Test Rapide

```bash
python test_deployed_site.py https://iptv-0e41.onrender.com
```

## 📖 Documentation Complète

- `GUIDE_UTILISATION.md` - Guide complet
- `DEPLOY.md` - Déploiement
- `FEATURE_REFRESH_CHANNELS.md` - Rafraîchissement

---

✅ **Votre serveur est opérationnel !**
