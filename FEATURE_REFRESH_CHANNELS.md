# 🔄 Fonctionnalité : Rafraîchissement des Chaînes

## 📋 Description

Cette fonctionnalité permet au **Super Admin** de rafraîchir manuellement toutes les chaînes IPTV depuis Vavoo, incluant :
- Chaînes Live TV
- Films VOD
- Séries

## 🎯 Accès

**Réservé aux Super Admins uniquement**

## 🖥️ Interface Utilisateur

### Bouton dans le Panel Admin

Un nouveau bouton **"🔄 Rafraîchir chaînes"** est disponible dans la section "Actions rapides" du dashboard.

**Emplacement** : Dashboard → Actions rapides → 🔄 Rafraîchir chaînes

**Couleur** : Orange (#ff6b35) pour le distinguer des autres actions

### Processus de Rafraîchissement

1. **Clic sur le bouton** → Confirmation demandée
2. **Confirmation** → Le bouton affiche "⏳ Rafraîchissement..."
3. **Traitement** → Rechargement de toutes les sources (1-2 minutes)
4. **Résultat** → Message de succès avec les nouvelles statistiques

### Message de Confirmation

```
Rafraîchir toutes les chaînes depuis Vavoo?
Cela peut prendre 1-2 minutes.
```

### Message de Succès

```
✅ Chaînes mises à jour!

Chaînes: 1234
Films: 567
Séries: 89
```

## 🔌 API Endpoint

### POST /api/admin/channels/refresh

**Authentification** : Token Super Admin requis

**Méthode** : POST

**Headers** :
```
Authorization: Bearer {admin_id}:{secret_key}
```

**Réponse Succès** (200) :
```json
{
  "success": true,
  "message": "Chaînes mises à jour avec succès",
  "stats": {
    "total_channels": 1234,
    "total_movies": 567,
    "total_series": 89,
    "token_valid": true,
    "sources": {
      "vavoo": 1234
    }
  }
}
```

**Réponse Erreur** (403) :
```json
{
  "error": "Acces refuse - Super admin uniquement"
}
```

**Réponse Erreur** (500) :
```json
{
  "error": "Erreur: [message d'erreur]"
}
```

## 📊 Statistiques des Chaînes

### GET /api/admin/channels/stats

**Authentification** : Token Admin requis

**Méthode** : GET

**Réponse** :
```json
{
  "total_channels": 1234,
  "total_movies": 567,
  "total_series": 89,
  "token_valid": true,
  "sources": {
    "vavoo": 1234
  }
}
```

### Affichage dans le Dashboard

Les statistiques IPTV sont automatiquement affichées dans le dashboard pour les Super Admins :

```
📺 Statistiques IPTV
┌─────────────────┬──────────┐
│ Chaînes Live    │ 1234     │
│ Films VOD       │ 567      │
│ Séries          │ 89       │
│ Token Vavoo     │ ✅ Valide │
└─────────────────┴──────────┘
```

## 🔄 Rafraîchissement Automatique

En plus du rafraîchissement manuel, le système effectue automatiquement :

- **Token Vavoo** : Toutes les 10 minutes
- **Chaînes** : Au démarrage du serveur

## 📝 Logs

Chaque rafraîchissement manuel est enregistré dans les logs :

```
Action: channels_refreshed
Details: Chaînes: 1234, Films: 567, Séries: 89
User: Super Admin
IP: xxx.xxx.xxx.xxx
Date: 2024-12-28 15:30:00
```

## 🧪 Test de la Fonctionnalité

### Test Manuel

1. Connectez-vous en tant que Super Admin
2. Allez sur le Dashboard
3. Cliquez sur "🔄 Rafraîchir chaînes"
4. Confirmez l'action
5. Attendez 1-2 minutes
6. Vérifiez le message de succès
7. Vérifiez que les statistiques sont mises à jour

### Test API

```bash
# Avec curl
curl -X POST https://votre-service.onrender.com/api/admin/channels/refresh \
  -H "Authorization: Bearer {admin_id}:{secret_key}"

# Avec Python
import requests

response = requests.post(
    "https://votre-service.onrender.com/api/admin/channels/refresh",
    headers={"Authorization": f"Bearer {admin_id}:{secret_key}"}
)

print(response.json())
```

## ⚠️ Limitations

- **Durée** : Le rafraîchissement peut prendre 1-2 minutes
- **Accès** : Réservé aux Super Admins uniquement
- **Fréquence** : Pas de limite, mais évitez de rafraîchir trop souvent
- **Connexion** : Nécessite une connexion internet stable

## 🔧 Dépannage

### Le bouton ne s'affiche pas

**Cause** : Vous n'êtes pas connecté en tant que Super Admin

**Solution** : Connectez-vous avec un compte Super Admin

### Erreur "Acces refuse"

**Cause** : Votre compte n'a pas les droits Super Admin

**Solution** : Contactez un Super Admin pour obtenir les droits

### Le rafraîchissement échoue

**Cause** : Problème de connexion à Vavoo ou timeout

**Solution** :
1. Vérifiez votre connexion internet
2. Réessayez dans quelques minutes
3. Vérifiez les logs du serveur

### Les statistiques ne se mettent pas à jour

**Cause** : Erreur JavaScript ou cache navigateur

**Solution** :
1. Rafraîchissez la page (F5)
2. Videz le cache du navigateur
3. Reconnectez-vous

## 📚 Code Source

### Fichiers Modifiés

- `server.py` : Ajout de l'endpoint `/api/admin/channels/refresh` et `/api/admin/channels/stats`
- `admin_panel.py` : Ajout du bouton et de la fonction JavaScript `refreshChannels()`

### Fonction Backend (server.py)

```python
if path == "/api/admin/channels/refresh":
    if not admin['is_super_admin']:
        self.send_json({"error": "Acces refuse - Super admin uniquement"}, 403)
        return
    
    try:
        log("Rafraichissement manuel des chaînes demandé...")
        multi_service.load_all_sources(force=True)
        stats = multi_service.get_stats()
        
        db.add_log("channels_refreshed", 
                   f"Chaînes: {stats['total_channels']}, Films: {stats['total_movies']}, Séries: {stats['total_series']}", 
                   "admin", admin['id'], self.get_client_ip())
        
        self.send_json({
            "success": True,
            "message": "Chaînes mises à jour avec succès",
            "stats": stats
        })
    except Exception as e:
        log(f"Erreur lors du rafraîchissement: {e}")
        self.send_json({"error": f"Erreur: {str(e)}"}, 500)
    return
```

### Fonction Frontend (admin_panel.py)

```javascript
function refreshChannels() {
    if(!confirm("Rafraîchir toutes les chaînes depuis Vavoo?\\nCela peut prendre 1-2 minutes."))
        return;
    
    var btn = event.target;
    btn.disabled = true;
    btn.textContent = "⏳ Rafraîchissement...";
    
    fetch("/api/admin/channels/refresh", {method:"POST", headers:H()})
        .then(r => r.json())
        .then(res => {
            btn.disabled = false;
            btn.textContent = "🔄 Rafraîchir chaînes";
            
            if(res.success) {
                alert("✅ Chaînes mises à jour!\\n\\nChaînes: " + res.stats.total_channels + 
                      "\\nFilms: " + res.stats.total_movies + 
                      "\\nSéries: " + res.stats.total_series);
                loadStats();
            } else {
                alert("❌ Erreur: " + res.error);
            }
        })
        .catch(e => {
            btn.disabled = false;
            btn.textContent = "🔄 Rafraîchir chaînes";
            alert("❌ Erreur: " + e);
        });
}
```

## ✅ Checklist de Déploiement

- [x] Endpoint API créé
- [x] Vérification des droits Super Admin
- [x] Bouton ajouté dans le panel admin
- [x] Fonction JavaScript implémentée
- [x] Affichage des statistiques
- [x] Logs enregistrés
- [x] Messages de confirmation/succès/erreur
- [x] Documentation complète

---

✅ **La fonctionnalité de rafraîchissement des chaînes est maintenant opérationnelle !**
