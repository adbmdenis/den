# 🌐 GUIDE D'HÉBERGEMENT - SYSTÈME IPTV

## 📋 APERÇU DE TON SYSTÈME

Ton système actuel:
- **Backend Python** (Flask/FastAPI)
- **Base de données** SQLite
- **Streaming IPTV** (M3U playlists)
- **Panel Admin** (HTML/JavaScript)
- **Port actuel:** 8888
- **IP locale:** 192.168.1.19

---

## 🎯 OPTIONS D'HÉBERGEMENT

### Option 1: VPS (Virtual Private Server) ⭐ RECOMMANDÉ
**Meilleur choix pour ton système IPTV**

#### Avantages
✅ Contrôle total du serveur
✅ Peut gérer le streaming vidéo
✅ IP dédiée
✅ Bande passante élevée
✅ Peut installer ce que tu veux

#### Fournisseurs Recommandés

**1. OVH (France/Canada)**
- Prix: 3-10€/mois
- Datacenter en France
- Bande passante illimitée
- Support français
- 🔗 https://www.ovhcloud.com/fr/vps/

**2. Contabo (Allemagne)**
- Prix: 5-15€/mois
- Excellent rapport qualité/prix
- Beaucoup de RAM et stockage
- Bande passante élevée
- 🔗 https://contabo.com

**3. Hetzner (Allemagne)**
- Prix: 4-20€/mois
- Très performant
- Réseau rapide
- Bon pour streaming
- 🔗 https://www.hetzner.com

**4. DigitalOcean**
- Prix: 6-20$/mois
- Interface simple
- Documentation excellente
- Datacenter mondial
- 🔗 https://www.digitalocean.com

#### Configuration Minimale Recommandée
```
CPU:     2 cores
RAM:     4 GB
Disque:  50 GB SSD
Bande:   2-5 TB/mois
OS:      Ubuntu 22.04 LTS
```

#### Configuration Optimale
```
CPU:     4 cores
RAM:     8 GB
Disque:  100 GB SSD
Bande:   10 TB/mois
OS:      Ubuntu 22.04 LTS
```

---

### Option 2: Cloud Platform (AWS, Azure, Google Cloud)
**Pour grande échelle**

#### AWS (Amazon Web Services)
- **EC2:** Serveur virtuel
- **RDS:** Base de données managée
- **S3:** Stockage fichiers
- **CloudFront:** CDN pour streaming
- Prix: Variable (10-100€/mois)
- 🔗 https://aws.amazon.com

#### Google Cloud Platform
- **Compute Engine:** VM
- **Cloud SQL:** Base de données
- **Cloud Storage:** Fichiers
- Prix: Variable (10-80€/mois)
- 🔗 https://cloud.google.com

#### Avantages
✅ Scalabilité automatique
✅ Haute disponibilité
✅ Services managés
✅ CDN intégré

#### Inconvénients
❌ Plus complexe
❌ Plus cher
❌ Facturation variable

---

### Option 3: Hébergement Partagé
**❌ NON RECOMMANDÉ pour IPTV**

Pourquoi éviter:
- ❌ Ressources limitées
- ❌ Pas de contrôle serveur
- ❌ Restrictions sur streaming
- ❌ Bande passante limitée
- ❌ Peut bloquer ton service

---

### Option 4: Serveur Dédié
**Pour très grande échelle**

#### Quand choisir
- Plus de 1000 utilisateurs simultanés
- Streaming haute qualité (4K)
- Besoin de performances maximales

#### Fournisseurs
- **OVH:** 40-200€/mois
- **Hetzner:** 40-150€/mois
- **Online.net:** 30-180€/mois

#### Configuration Type
```
CPU:     8-16 cores
RAM:     32-64 GB
Disque:  2x 1TB SSD (RAID)
Bande:   Illimitée
```

---

## 🔍 COMMENT CHOISIR?

### Selon le Nombre d'Utilisateurs

**1-50 utilisateurs**
- VPS Basic (2 CPU, 4GB RAM)
- Prix: 5-10€/mois
- Fournisseur: Contabo, OVH

**50-200 utilisateurs**
- VPS Medium (4 CPU, 8GB RAM)
- Prix: 15-25€/mois
- Fournisseur: Hetzner, OVH

**200-1000 utilisateurs**
- VPS High (8 CPU, 16GB RAM)
- Prix: 40-60€/mois
- Fournisseur: Hetzner, AWS

**1000+ utilisateurs**
- Serveur Dédié ou Cloud
- Prix: 100-500€/mois
- Fournisseur: OVH, AWS, Hetzner

---

## 📊 COMPARAISON DÉTAILLÉE

### VPS Recommandés pour IPTV

| Fournisseur | Prix/mois | CPU | RAM | Disque | Bande | Note |
|-------------|-----------|-----|-----|--------|-------|------|
| **Contabo VPS S** | 5€ | 4 | 8GB | 200GB | 32TB | ⭐⭐⭐⭐⭐ |
| **OVH VPS Starter** | 3.50€ | 1 | 2GB | 20GB | Illimité | ⭐⭐⭐ |
| **Hetzner CX21** | 5.40€ | 2 | 4GB | 40GB | 20TB | ⭐⭐⭐⭐ |
| **DigitalOcean Basic** | 6$ | 1 | 1GB | 25GB | 1TB | ⭐⭐⭐ |
| **Hetzner CX31** | 9.50€ | 2 | 8GB | 80GB | 20TB | ⭐⭐⭐⭐⭐ |

**🏆 MEILLEUR CHOIX:** Contabo VPS S (5€/mois) - Excellent rapport qualité/prix

---

## 🚀 ÉTAPES POUR DÉPLOYER

### Étape 1: Choisir et Commander le VPS

1. **Aller sur le site** (ex: Contabo)
2. **Choisir VPS S ou M**
3. **Sélectionner:**
   - OS: Ubuntu 22.04 LTS
   - Région: Europe (France/Allemagne)
   - Période: Mensuel
4. **Commander et payer**
5. **Recevoir les accès par email** (IP, root password)

### Étape 2: Configurer le Serveur

```bash
# Se connecter en SSH
ssh root@VOTRE_IP

# Mettre à jour le système
apt update && apt upgrade -y

# Installer Python et dépendances
apt install python3 python3-pip python3-venv nginx -y

# Créer un utilisateur
adduser iptv
usermod -aG sudo iptv

# Se connecter avec le nouvel utilisateur
su - iptv
```

### Étape 3: Transférer Ton Code

```bash
# Sur ton PC local
# Compresser ton projet
cd C:\Users\ADBM\Downloads\vavoo-main\vavoo-main
tar -czf serveur_iptv.tar.gz serveur_iptv/

# Transférer vers le serveur
scp serveur_iptv.tar.gz iptv@VOTRE_IP:/home/iptv/

# Sur le serveur
ssh iptv@VOTRE_IP
tar -xzf serveur_iptv.tar.gz
cd serveur_iptv
```

### Étape 4: Installer les Dépendances

```bash
# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les packages
pip install flask requests sqlite3

# Tester le serveur
python server.py
```

### Étape 5: Configurer Nginx (Reverse Proxy)

```bash
# Créer la configuration
sudo nano /etc/nginx/sites-available/iptv

# Contenu:
server {
    listen 80;
    server_name VOTRE_IP;

    location / {
        proxy_pass http://127.0.0.1:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Activer
sudo ln -s /etc/nginx/sites-available/iptv /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Étape 6: Configurer le Service Systemd

```bash
# Créer le service
sudo nano /etc/systemd/system/iptv.service

# Contenu:
[Unit]
Description=IPTV Server
After=network.target

[Service]
Type=simple
User=iptv
WorkingDirectory=/home/iptv/serveur_iptv
Environment="PATH=/home/iptv/serveur_iptv/venv/bin"
ExecStart=/home/iptv/serveur_iptv/venv/bin/python server.py
Restart=always

[Install]
WantedBy=multi-user.target

# Activer et démarrer
sudo systemctl enable iptv
sudo systemctl start iptv
sudo systemctl status iptv
```

### Étape 7: Configurer le Firewall

```bash
# Installer UFW
sudo apt install ufw -y

# Configurer
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### Étape 8: Obtenir un Nom de Domaine (Optionnel)

**Fournisseurs de domaines:**
- **Namecheap:** 8-12€/an
- **OVH:** 6-10€/an
- **Gandi:** 12-15€/an

**Configuration DNS:**
```
Type: A
Nom: @
Valeur: VOTRE_IP_VPS
TTL: 3600
```

### Étape 9: Installer SSL (HTTPS)

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtenir certificat SSL
sudo certbot --nginx -d votre-domaine.com

# Renouvellement automatique
sudo certbot renew --dry-run
```

---

## 💰 ESTIMATION DES COÛTS

### Configuration Starter (50 utilisateurs)
```
VPS Contabo S:        5€/mois
Domaine:              1€/mois (12€/an)
Backup:               2€/mois
Total:                8€/mois
```

### Configuration Medium (200 utilisateurs)
```
VPS Hetzner CX31:     9.50€/mois
Domaine:              1€/mois
Backup:               3€/mois
CDN (optionnel):      5€/mois
Total:                18.50€/mois
```

### Configuration Pro (1000 utilisateurs)
```
VPS Hetzner CX51:     25€/mois
Domaine:              1€/mois
Backup:               5€/mois
CDN:                  15€/mois
Monitoring:           3€/mois
Total:                49€/mois
```

---

## 🔒 SÉCURITÉ IMPORTANTE

### 1. Changer le Port SSH
```bash
sudo nano /etc/ssh/sshd_config
# Port 22 → Port 2222
sudo systemctl restart sshd
```

### 2. Désactiver Root Login
```bash
sudo nano /etc/ssh/sshd_config
# PermitRootLogin no
sudo systemctl restart sshd
```

### 3. Installer Fail2Ban
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
```

### 4. Sauvegardes Automatiques
```bash
# Script de backup
nano ~/backup.sh

#!/bin/bash
tar -czf /home/iptv/backup-$(date +%Y%m%d).tar.gz /home/iptv/serveur_iptv
find /home/iptv/backup-*.tar.gz -mtime +7 -delete

# Cron job (tous les jours à 3h)
crontab -e
0 3 * * * /home/iptv/backup.sh
```

---

## 📈 MONITORING

### Installer Monitoring
```bash
# Installer htop
sudo apt install htop -y

# Installer netdata (monitoring web)
bash <(curl -Ss https://my-netdata.io/kickstart.sh)

# Accéder: http://VOTRE_IP:19999
```

### Commandes Utiles
```bash
# Voir les logs
sudo journalctl -u iptv -f

# Voir l'utilisation
htop

# Voir les connexions
netstat -tulpn | grep 8888

# Redémarrer le service
sudo systemctl restart iptv
```

---

## 🎯 RECOMMANDATION FINALE

### Pour Débuter (Budget Limité)
**Contabo VPS S - 5€/mois**
- 4 CPU, 8GB RAM, 200GB SSD
- Parfait pour 50-200 utilisateurs
- Excellent rapport qualité/prix

### Pour Production (Recommandé)
**Hetzner CX31 - 9.50€/mois**
- 2 CPU, 8GB RAM, 80GB SSD
- Réseau rapide et fiable
- Support excellent
- Datacenter en Allemagne

### Pour Grande Échelle
**Hetzner CX51 - 25€/mois**
- 8 CPU, 16GB RAM, 160GB SSD
- Peut gérer 500-1000 utilisateurs
- Performance maximale

---

## 📞 PROCHAINES ÉTAPES

1. **Choisir un fournisseur** (Contabo ou Hetzner)
2. **Commander le VPS** (Ubuntu 22.04)
3. **Recevoir les accès** (IP + password)
4. **Suivre le guide de déploiement** (ci-dessus)
5. **Tester le système**
6. **Configurer le domaine** (optionnel)
7. **Activer SSL** (HTTPS)

---

## 💡 CONSEILS IMPORTANTS

✅ **Commence petit:** VPS à 5€/mois suffit pour débuter
✅ **Teste d'abord:** Prends un mois pour tester
✅ **Sauvegarde régulièrement:** Backup automatique quotidien
✅ **Surveille les ressources:** Utilise htop et netdata
✅ **Sécurise bien:** Firewall, Fail2Ban, SSH sécurisé
✅ **Utilise un domaine:** Plus professionnel qu'une IP
✅ **Active HTTPS:** Obligatoire pour la sécurité

❌ **Évite:**
- Hébergement partagé (trop limité)
- VPS trop petit (< 2GB RAM)
- Pas de backup (risque de perte de données)
- Laisser le port SSH 22 (risque de hack)

---

## 📚 RESSOURCES UTILES

**Tutoriels:**
- DigitalOcean Tutorials: https://www.digitalocean.com/community/tutorials
- Linode Guides: https://www.linode.com/docs/guides/

**Outils:**
- SSH Client: PuTTY (Windows), Terminal (Mac/Linux)
- FTP Client: FileZilla, WinSCP
- Monitoring: Netdata, Grafana

**Support:**
- Forum OVH: https://community.ovh.com
- Reddit: r/selfhosted, r/webhosting

---

**Besoin d'aide pour le déploiement? Je peux créer des scripts automatisés!**
