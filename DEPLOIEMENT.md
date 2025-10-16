# 🚀 Guide de Déploiement - SuperMarché Plus

## 📋 Prérequis Serveur

- **OS** : Ubuntu 20.04 LTS ou supérieur (recommandé) / Windows Server
- **Python** : 3.13 ou supérieur
- **Mémoire** : Minimum 2 GB RAM (4 GB recommandé)
- **Disque** : Minimum 10 GB d'espace libre
- **Serveur Web** : Nginx ou Apache
- **Base de données** : PostgreSQL (production) ou SQLite (développement)

## 🔧 Installation Production (Linux)

### 1. Préparer le Serveur

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer les dépendances système
sudo apt install -y python3.13 python3.13-venv python3-pip nginx postgresql postgresql-contrib git

# Créer un utilisateur pour l'application
sudo useradd -m -s /bin/bash supermarche
sudo su - supermarche
```

### 2. Cloner et Configurer l'Application

```bash
# Cloner le dépôt
cd /home/supermarche
git clone https://github.com/romualdKO/PROJET_CARREFOUR.git
cd PROJET_CARREFOUR

# Créer l'environnement virtuel
python3.13 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 3. Configurer PostgreSQL

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Dans le shell PostgreSQL
CREATE DATABASE supermarche_db;
CREATE USER supermarche_user WITH PASSWORD 'MotDePasseSecurise123!';
ALTER ROLE supermarche_user SET client_encoding TO 'utf8';
ALTER ROLE supermarche_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE supermarche_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE supermarche_db TO supermarche_user;
\q
```

### 4. Configurer Django pour Production

Créer un fichier `.env` à la racine du projet :

```bash
# .env
SECRET_KEY=votre-cle-secrete-super-longue-et-aleatoire-ici
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com,IP_SERVEUR

# Base de données
DB_ENGINE=django.db.backends.postgresql
DB_NAME=supermarche_db
DB_USER=supermarche_user
DB_PASSWORD=MotDePasseSecurise123!
DB_HOST=localhost
DB_PORT=5432
```

Modifier `Carrefour/settings.py` :

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Base de données
if os.getenv('DB_ENGINE'):
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE'),
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }

# Sécurité
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Fichiers statiques
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 5. Migrations et Fichiers Statiques

```bash
# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Créer les comptes par défaut
python init_default_accounts.py
```

### 6. Configurer Gunicorn

Créer `/etc/systemd/system/supermarche.service` :

```ini
[Unit]
Description=SuperMarche Plus Gunicorn daemon
After=network.target

[Service]
User=supermarche
Group=www-data
WorkingDirectory=/home/supermarche/PROJET_CARREFOUR
ExecStart=/home/supermarche/PROJET_CARREFOUR/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/supermarche.sock \
          Carrefour.wsgi:application

[Install]
WantedBy=multi-user.target
```

Démarrer le service :

```bash
sudo systemctl start supermarche
sudo systemctl enable supermarche
sudo systemctl status supermarche
```

### 7. Configurer Nginx

Créer `/etc/nginx/sites-available/supermarche` :

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/supermarche/PROJET_CARREFOUR;
    }

    location /media/ {
        root /home/supermarche/PROJET_CARREFOUR;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/supermarche.sock;
    }
}
```

Activer le site :

```bash
sudo ln -s /etc/nginx/sites-available/supermarche /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Configurer SSL avec Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com
```

## 🐳 Déploiement avec Docker (Alternative)

### 1. Créer docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: supermarche_db
      POSTGRES_USER: supermarche_user
      POSTGRES_PASSWORD: MotDePasseSecurise123!
    restart: always

  web:
    build: .
    command: gunicorn Carrefour.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
    restart: always

  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web
    restart: always

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### 2. Lancer avec Docker

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python init_default_accounts.py
```

## 🔐 Sécurité

### Checklist Sécurité Production

- [ ] DEBUG=False dans settings.py
- [ ] SECRET_KEY complexe et secrète
- [ ] ALLOWED_HOSTS correctement configuré
- [ ] SSL/HTTPS activé (Let's Encrypt)
- [ ] Cookies sécurisés (SECURE_*_COOKIE)
- [ ] Fichiers sensibles dans .gitignore (.env, db.sqlite3)
- [ ] Permissions fichiers correctes (750 pour dossiers, 640 pour fichiers)
- [ ] Firewall configuré (UFW)
- [ ] Mots de passe par défaut changés
- [ ] Backup automatique de la base de données
- [ ] Logs d'accès et d'erreurs activés
- [ ] Limiter les tentatives de connexion (django-ratelimit)

### Configuration Firewall (UFW)

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
sudo ufw status
```

## 📊 Monitoring et Maintenance

### 1. Logs

```bash
# Logs Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs Gunicorn/Django
sudo journalctl -u supermarche -f

# Logs Docker
docker-compose logs -f web
```

### 2. Backup Base de Données

Script de backup automatique `/home/supermarche/backup_db.sh` :

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/supermarche/backups"
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
PGPASSWORD="MotDePasseSecurise123!" pg_dump -U supermarche_user -h localhost supermarche_db > $BACKUP_DIR/backup_$DATE.sql

# Garder seulement les 30 derniers backups
find $BACKUP_DIR -type f -name "backup_*.sql" -mtime +30 -delete

echo "Backup créé : backup_$DATE.sql"
```

Configurer cron :

```bash
crontab -e
# Ajouter : Backup tous les jours à 2h du matin
0 2 * * * /home/supermarche/backup_db.sh
```

### 3. Mise à Jour de l'Application

```bash
cd /home/supermarche/PROJET_CARREFOUR
source venv/bin/activate

# Sauvegarder la base de données
python manage.py dumpdata > backup_before_update.json

# Récupérer les mises à jour
git pull origin main

# Installer les nouvelles dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Redémarrer le service
sudo systemctl restart supermarche
```

## 📈 Performance

### Optimisations Recommandées

1. **Cache Redis**
```bash
pip install redis django-redis

# Dans settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. **Compression Gzip (Nginx)**
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
```

3. **CDN pour fichiers statiques** (Cloudflare, AWS CloudFront)

## 🆘 Dépannage

### Service ne démarre pas
```bash
sudo systemctl status supermarche
sudo journalctl -xe -u supermarche
```

### Erreur 502 Bad Gateway
```bash
# Vérifier que le socket existe
ls -la /run/supermarche.sock

# Vérifier les permissions
sudo chown supermarche:www-data /run/supermarche.sock
```

### Base de données inaccessible
```bash
# Vérifier PostgreSQL
sudo systemctl status postgresql
sudo -u postgres psql -c "\l"
```

## 📞 Support

Pour assistance au déploiement :
- 📧 Email : devops@supermarche-plus.com
- 📚 Documentation : https://github.com/romualdKO/PROJET_CARREFOUR/wiki

---

**Version** : 1.0.0  
**Dernière mise à jour** : Octobre 2025
