# 🔧 Fix : Erreur "Root Directory main n'existe pas"

## ❌ Erreur

```
Le répertoire racine « main » n'existe pas. 
Vérifiez le répertoire racine configuré dans les paramètres de votre service.
builder.sh : ligne 51 : cd : /opt/render/project/src/main : 
Aucun fichier ou répertoire de ce type
```

## 🔍 Cause

Render essaie d'accéder à un répertoire `main` qui n'existe pas dans votre projet. Cela arrive quand :
- Le Root Directory est mal configuré
- Render détecte automatiquement un mauvais chemin
- La structure du dépôt GitHub n'est pas celle attendue

## ✅ Solution 1 : Via le Dashboard Render (Rapide)

### Étapes :

1. **Allez sur votre service**
   - https://dashboard.render.com
   - Cliquez sur votre service "iptv-0e41"

2. **Ouvrez les Settings**
   - Cliquez sur "Settings" dans le menu de gauche

3. **Modifiez le Root Directory**
   - Cherchez la section "Build & Deploy"
   - Trouvez le champ **"Root Directory"**
   - **Supprimez** tout ce qui est écrit (laissez vide)
   - OU mettez juste un point : `.`

4. **Sauvegardez**
   - Cliquez sur "Save Changes"

5. **Redéployez**
   - Allez dans l'onglet "Manual Deploy"
   - Cliquez sur "Clear build cache & deploy"

## ✅ Solution 2 : Via render.yaml (Permanent)

### Modification du fichier

Le fichier `render.yaml` a été mis à jour avec `rootDir: .` :

```yaml
services:
  - type: web
    name: serveur-iptv
    env: python
    region: frankfurt
    plan: free
    rootDir: .  # ← AJOUTÉ
    buildCommand: pip install -r requirements.txt
    startCommand: python server.py
    envVars:
      - key: PORT
        value: 8888
      # ... etc
```

### Pousser la modification

```bash
git add render.yaml
git commit -m "Fix: Ajout rootDir dans render.yaml"
git push
```

Render redéploiera automatiquement avec la bonne configuration.

## ✅ Solution 3 : Vérifier la Structure GitHub

### Structure Attendue

Votre dépôt GitHub doit avoir cette structure **à la racine** :

```
votre-depot/
├── server.py
├── config.py
├── database.py
├── multi_service.py
├── admin_panel.py
├── vavoo_service.py
├── requirements.txt
├── render.yaml
├── Procfile
├── runtime.txt
└── ... autres fichiers
```

### Si vos fichiers sont dans un sous-dossier

Si vos fichiers sont dans `serveur_iptv/` ou un autre dossier :

**Option A** : Déplacer les fichiers à la racine
```bash
# Si vos fichiers sont dans serveur_iptv/
mv serveur_iptv/* .
rm -rf serveur_iptv/
git add .
git commit -m "Déplacement des fichiers à la racine"
git push
```

**Option B** : Configurer le Root Directory
```yaml
# Dans render.yaml
rootDir: serveur_iptv
```

## 🔍 Vérification

### Vérifier la structure de votre dépôt GitHub

1. Allez sur https://github.com/denis14213/iptv
2. Vérifiez que vous voyez directement :
   - `server.py`
   - `config.py`
   - `render.yaml`
   - etc.

### Si vous voyez un dossier `main/` ou `serveur_iptv/`

Alors vos fichiers ne sont pas à la racine. Vous devez :
- Soit les déplacer à la racine
- Soit configurer `rootDir` dans render.yaml

## 📝 Commandes Git Utiles

### Vérifier la structure locale
```bash
ls -la
```

Vous devriez voir :
```
server.py
config.py
database.py
render.yaml
...
```

### Vérifier la branche
```bash
git branch
```

Assurez-vous d'être sur `main` ou `master`.

### Pousser les modifications
```bash
git add .
git commit -m "Fix: Configuration Root Directory"
git push origin main
```

## 🆘 Dépannage

### Erreur persiste après modification

1. **Videz le cache de build**
   - Dashboard Render → Manual Deploy → "Clear build cache & deploy"

2. **Vérifiez les logs**
   - Dashboard Render → Logs
   - Cherchez les erreurs de chemin

3. **Recréez le service**
   - Si rien ne fonctionne, supprimez le service
   - Recréez-le avec la bonne configuration

### Vérifier que render.yaml est bien lu

Dans les logs de déploiement, vous devriez voir :
```
==> Using Blueprint render.yaml
```

Si vous ne voyez pas ça, Render n'utilise pas votre render.yaml.

## ✅ Checklist de Résolution

- [ ] Vérifier la structure du dépôt GitHub (fichiers à la racine ?)
- [ ] Modifier Root Directory dans Render Settings (vide ou `.`)
- [ ] OU ajouter `rootDir: .` dans render.yaml
- [ ] Pousser les modifications sur GitHub
- [ ] Vider le cache et redéployer
- [ ] Vérifier les logs de déploiement

## 🎯 Résultat Attendu

Après la correction, vous devriez voir dans les logs :

```
==> Clonage depuis https://github.com/denis14213/iptv
==> Checking out commit abc123 in branch main
==> Running build command 'pip install -r requirements.txt'
==> Installing dependencies...
==> Build successful!
==> Starting service with 'python server.py'
```

---

## 📞 Besoin d'Aide ?

Si l'erreur persiste :

1. Vérifiez la structure exacte de votre dépôt GitHub
2. Partagez un screenshot de la racine de votre dépôt
3. Partagez les logs complets de Render

---

✅ **Une fois corrigé, votre serveur démarrera correctement !**
