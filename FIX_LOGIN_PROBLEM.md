# 🔧 Correction : Problème de Connexion Admin

## ❌ Problème

```
Erreur: Identifiants invalides
```

Le mot de passe par défaut `Super@2024!` ne fonctionne pas.

## 🔍 Cause

Les variables d'environnement sur Render sont différentes de celles par défaut.

## ✅ Solution 1 : Vérifier les Variables d'Environnement sur Render

### Étapes :

1. **Allez sur Render Dashboard**
   - https://dashboard.render.com
   - Cliquez sur votre service "iptv-0e41"

2. **Ouvrez Environment**
   - Cliquez sur "Environment" dans le menu de gauche

3. **Vérifiez ces variables** :
   ```
   SUPER_ADMIN_USERNAME = ?
   SUPER_ADMIN_PASSWORD = ?
   ```

4. **Notez les valeurs** et utilisez-les pour vous connecter

### Si les variables n'existent pas :

1. **Ajoutez-les** :
   ```
   SUPER_ADMIN_USERNAME = superadmin
   SUPER_ADMIN_PASSWORD = VotreMotDePasseSecurise123!
   ```

2. **Cliquez sur "Save Changes"**

3. **Attendez le redémarrage** (1-2 minutes)

4. **Testez la connexion** avec les nouveaux identifiants

## ✅ Solution 2 : Utiliser les Identifiants Actuels

Si vous connaissez les identifiants actuels, utilisez-les simplement.

### Test de Connexion

```bash
python test_admin_functions.py
```

Si ça fonctionne, notez les identifiants quelque part en sécurité.

## ✅ Solution 3 : Réinitialiser via la Base de Données (Avancé)

⚠️ **Attention** : Ceci nécessite un accès SSH à Render (plan payant) ou un redéploiement.

### Option A : Redéployer avec de Nouvelles Variables

1. **Sur Render Dashboard** → Environment
2. **Modifiez** `SUPER_ADMIN_PASSWORD`
3. **Save Changes**
4. **Manual Deploy** → "Clear build cache & deploy"

### Option B : Via SSH (Plan Payant uniquement)

```bash
# Se connecter au serveur
render ssh

# Réinitialiser le mot de passe
python reset_admin_password.py NouveauMotDePasse123!
```

## 🧪 Test de Connexion

### Méthode 1 : Via le Script

```bash
python test_admin_functions.py
```

### Méthode 2 : Via curl

```bash
curl -X POST https://iptv-0e41.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"superadmin","password":"VotreMotDePasse"}'
```

### Méthode 3 : Via le Navigateur

1. Allez sur https://iptv-0e41.onrender.com/login
2. Entrez vos identifiants
3. Si ça fonctionne, vous serez redirigé vers /admin

## 📝 Identifiants à Tester

Essayez ces combinaisons :

### Combinaison 1 (Par défaut)
```
Username: superadmin
Password: Super@2024!
```

### Combinaison 2 (Variables Render)
```
Username: [Vérifier sur Render]
Password: [Vérifier sur Render]
```

### Combinaison 3 (Possibles)
```
Username: admin
Password: admin
```

```
Username: superadmin
Password: superadmin
```

## 🔒 Après Avoir Trouvé les Identifiants

1. **Connectez-vous** au panel admin

2. **Changez le mot de passe** :
   - Allez dans "Paramètres"
   - Entrez l'ancien mot de passe
   - Entrez le nouveau mot de passe
   - Confirmez
   - Cliquez sur "Modifier"

3. **Notez les nouveaux identifiants** dans un endroit sûr

## 🆘 Si Rien ne Fonctionne

### Option 1 : Recréer le Service

1. **Supprimez** le service actuel sur Render
2. **Recréez-le** avec le Blueprint
3. **Définissez** les variables d'environnement correctement :
   ```
   SUPER_ADMIN_USERNAME=superadmin
   SUPER_ADMIN_PASSWORD=VotreMotDePasseSecurise123!
   ```

### Option 2 : Modifier render.yaml

1. **Éditez** `render.yaml` localement :
   ```yaml
   envVars:
     - key: SUPER_ADMIN_USERNAME
       value: superadmin
     - key: SUPER_ADMIN_PASSWORD
       value: MonNouveauMotDePasse123!
   ```

2. **Poussez** sur GitHub :
   ```bash
   git add render.yaml
   git commit -m "Fix: Mise à jour des identifiants admin"
   git push
   ```

3. **Attendez** le redéploiement automatique

## 📞 Vérification des Variables sur Render

### Via l'Interface Web

1. Dashboard → Votre service
2. Environment
3. Cherchez `SUPER_ADMIN_USERNAME` et `SUPER_ADMIN_PASSWORD`

### Via les Logs

1. Dashboard → Logs
2. Cherchez des lignes comme :
   ```
   [DB] Super admin cree: superadmin
   ```

## ✅ Checklist de Résolution

- [ ] Vérifier les variables d'environnement sur Render
- [ ] Tester avec les identifiants par défaut
- [ ] Tester avec d'autres combinaisons
- [ ] Modifier les variables sur Render si nécessaire
- [ ] Redéployer le service
- [ ] Tester la connexion
- [ ] Changer le mot de passe une fois connecté
- [ ] Noter les nouveaux identifiants

## 🎯 Résultat Attendu

Après correction, vous devriez pouvoir :

```bash
python test_admin_functions.py
```

Et voir :

```
✅ Connexion réussie !
Token: abc123...
```

---

## 📝 Notes Importantes

1. **Ne commitez JAMAIS** les mots de passe dans Git
2. **Utilisez des mots de passe forts** (12+ caractères)
3. **Changez le mot de passe** après la première connexion
4. **Sauvegardez** les identifiants dans un gestionnaire de mots de passe

---

✅ **Une fois corrigé, toutes les fonctionnalités fonctionneront !**
