# =====================================================
# SPRINT 6 - DOCKERFILE PRODUCTION
# =====================================================

FROM python:3.13-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Répertoire de travail
WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput || true

# Créer un utilisateur non-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Port d'écoute
EXPOSE 8000

# Script de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "Carrefour.wsgi:application"]
