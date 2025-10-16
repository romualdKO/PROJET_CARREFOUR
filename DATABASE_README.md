# 📊 Base de Données de Test - db.sqlite3

## ℹ️ À Propos

Ce fichier contient une **base de données SQLite pré-remplie** avec des données de test pour faciliter le développement et les tests du projet Carrefour.

---

## 📦 Contenu de la Base de Données

### 👥 Comptes Administrateurs

| Rôle | Identifiant | Mot de passe | Description |
|------|-------------|--------------|-------------|
| **DG** | `dg` | `DG2025@Admin` | Directeur Général - Accès complet |
| **DAF** | `daf` | `DAF2025@Admin` | Directeur Financier - Gestion caisse/finances |
| **RH** | `rh` | `RH2025@Admin` | Responsable RH - Gestion personnel |

### 👨‍💼 Employés de Test

La base contient plusieurs employés fictifs avec différents rôles :
- Caissiers
- Gestionnaires de stock
- Analystes
- Équipe marketing
- Etc.

**Exemples d'employés** :
- Marie Kouamé (CAISSIER)
- Jean Kouassi (STOCK)
- Aïcha Traoré (MARKETING)
- Et plusieurs autres...

### 📦 Produits de Démonstration

La base contient des produits dans plusieurs catégories :
- 🍞 Alimentaire
- 🥤 Boissons
- 🧼 Hygiène
- 👕 Vêtements
- 📱 Électronique
- 🏡 Maison & Jardin

### ⏰ Présences de Test

Des enregistrements de présence pour tester le système de gestion du temps :
- Sessions multiples par jour
- Différents statuts (Présent, Retard, Absent)
- Calculs automatiques du temps de travail

---

## 🚀 Utilisation

### Option 1 : Utiliser la Base de Données Fournie (RECOMMANDÉ)

Après avoir cloné le projet, la base de données est **déjà prête** :

```bash
# 1. Cloner le projet
git clone https://github.com/romualdKO/PROJET_CARREFOUR.git
cd PROJET_CARREFOUR

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Démarrer directement le serveur (migrations déjà appliquées)
python manage.py runserver
```

✅ **Avantage** : Vous avez immédiatement accès à toutes les données de test !

### Option 2 : Recréer une Base de Données Vide

Si vous voulez partir de zéro :

```bash
# 1. Supprimer la base existante
rm db.sqlite3  # Linux/Mac
del db.sqlite3  # Windows

# 2. Créer une nouvelle base vide
python manage.py migrate

# 3. Créer les comptes administrateurs
python init_default_accounts.py

# 4. (Optionnel) Générer des données de test
python create_sample_data.py
```

---

## ⚠️ Important - Sécurité

### 🔐 Mots de Passe par Défaut

Les mots de passe des comptes sont :
- DG : `DG2025@Admin`
- DAF : `DAF2025@Admin`
- RH : `RH2025@Admin`

**⚠️ ATTENTION** : 
- Ces mots de passe sont **UNIQUEMENT pour les tests**
- **NE JAMAIS** utiliser ces mots de passe en production
- Changez-les immédiatement si vous déployez en production

### 🚫 NE PAS Utiliser en Production

Cette base de données est **UNIQUEMENT pour le développement et les tests** :
- ❌ Ne contient pas de données sensibles réelles
- ❌ Pas optimisée pour la production
- ❌ Pas de sauvegardes
- ❌ Pas de sécurité renforcée

Pour la production, utilisez :
- PostgreSQL ou MySQL
- Mots de passe forts et uniques
- Variables d'environnement pour les secrets
- Sauvegardes régulières

---

## 🔄 Mise à Jour de la Base de Données

### Si de Nouvelles Migrations Sont Ajoutées

```bash
# Appliquer les nouvelles migrations
python manage.py migrate
```

### Si Vous Voulez Mettre à Jour les Données

```bash
# Réinitialiser les mots de passe
python reset_default_passwords.py

# Ajouter plus de données de test
python create_sample_data.py
```

---

## 📊 Statistiques de la Base

Voici approximativement ce que contient la base :

- **Employés** : ~15-20 comptes de test
- **Produits** : ~50-100 produits dans diverses catégories
- **Présences** : Plusieurs jours de données de présence
- **Sessions** : Enregistrements de sessions de connexion multiples

---

## 🛠️ Commandes Utiles

### Accéder à la Console Django

```bash
python manage.py shell
```

Exemples de requêtes :

```python
from CarrefourApp.models import Employe, Produit, Presence

# Voir tous les employés
Employe.objects.all()

# Voir les employés actifs
Employe.objects.filter(est_actif=True)

# Voir les produits en stock critique
Produit.objects.filter(statut='CRITIQUE')

# Voir les présences d'aujourd'hui
from datetime import date
Presence.objects.filter(date=date.today())
```

### Créer un Superutilisateur Admin

```bash
python manage.py createsuperuser
```

Accès admin : `http://127.0.0.1:8000/admin/`

---

## 🧪 Tests

Pour vérifier que tout fonctionne :

```bash
# Test des connexions
python test_authentication.py

# Test du système multi-sessions
python test_multi_sessions.py
```

---

## 📝 Structure des Tables

### Table Employe
- Informations personnelles
- Rôle et département
- Horaires de travail
- Autorisations d'accès

### Table Presence
- Suivi quotidien
- Première arrivée / Dernière départ
- Temps actif total
- Statut calculé automatiquement

### Table SessionPresence
- Enregistrement de chaque connexion/déconnexion
- Calcul automatique de la durée
- Support des sessions multiples par jour

### Table Produit
- Informations produit
- Prix et stock
- Catégorie et fournisseur
- Statut de stock

---

## 🔍 Vérifier le Contenu

### Compter les enregistrements :

```bash
python manage.py shell
```

```python
from CarrefourApp.models import Employe, Produit, Presence, SessionPresence

print(f"Employés : {Employe.objects.count()}")
print(f"Produits : {Produit.objects.count()}")
print(f"Présences : {Presence.objects.count()}")
print(f"Sessions : {SessionPresence.objects.count()}")
```

---

## 🆘 Dépannage

### Erreur : "table doesn't exist"

```bash
python manage.py migrate
```

### Erreur : "database is locked"

Fermez tous les processus qui utilisent la base :
```bash
# Windows
taskkill /F /IM python.exe

# Linux/Mac
pkill python
```

### Réinitialiser Complètement

```bash
# Sauvegarder l'ancienne base
cp db.sqlite3 db.sqlite3.backup  # Linux/Mac
copy db.sqlite3 db.sqlite3.backup  # Windows

# Supprimer et recréer
rm db.sqlite3
python manage.py migrate
python init_default_accounts.py
```

---

## 📚 Documentation Complémentaire

- [`QUICKSTART.md`](QUICKSTART.md) - Démarrage rapide
- [`GUIDE_CONNEXION.md`](GUIDE_CONNEXION.md) - Guide de connexion
- [`INSTALLATION_COLLABORATEURS.md`](INSTALLATION_COLLABORATEURS.md) - Guide d'installation complet
- [`SYSTEME_MULTI_SESSIONS.md`](SYSTEME_MULTI_SESSIONS.md) - Documentation du système de présence

---

## ✅ Avantages de cette Approche

**Pourquoi nous partageons la base SQLite** :

1. ✅ **Démarrage instantané** : Pas besoin de créer des données de test
2. ✅ **Cohérence** : Tout le monde a les mêmes données
3. ✅ **Tests réalistes** : Données variées pour tester toutes les fonctionnalités
4. ✅ **Simplicité** : Un simple `git clone` et c'est prêt
5. ✅ **Apprentissage** : Les nouveaux développeurs voient comment structurer les données

---

**Date de création** : 16 octobre 2025  
**Version** : 2.0.0  
**Statut** : ✅ Prêt pour les tests et le développement

---

## 🎯 Résumé Rapide

```bash
# Installation complète en 3 étapes
git clone https://github.com/romualdKO/PROJET_CARREFOUR.git
cd PROJET_CARREFOUR
pip install -r requirements.txt
python manage.py runserver

# Connexion immédiate avec :
# - dg / DG2025@Admin
# - daf / DAF2025@Admin
# - rh / RH2025@Admin
```

**C'est tout ! 🎉**
