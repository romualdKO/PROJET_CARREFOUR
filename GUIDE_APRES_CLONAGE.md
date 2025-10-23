# 🚀 GUIDE DE DÉMARRAGE RAPIDE - APRÈS CLONAGE

## ⚠️ PROBLÈME : Impossible de se connecter après avoir cloné le projet

### 🔍 Cause du problème
Quand vous clonez le projet depuis Git, la base de données `db.sqlite3` n'est **pas incluse** (elle est dans `.gitignore`). Vous devez donc recréer la base de données et les comptes par défaut sur votre PC.

---

## ✅ SOLUTION COMPLÈTE (À FAIRE UNE SEULE FOIS)

### Étape 1️⃣ : Vérifier l'installation des dépendances
```powershell
pip install -r requirements.txt
```

### Étape 2️⃣ : Créer la base de données
```powershell
python manage.py migrate
```

### Étape 3️⃣ : Créer les comptes par défaut
```powershell
python setup_after_clone.py
```

**✅ C'est tout !** Vos comptes sont maintenant créés.

---

## 🔑 IDENTIFIANTS DE CONNEXION

### 📍 URL de connexion
**http://127.0.0.1:8000/login/**

### 👥 Comptes disponibles

| Rôle | Identifiant | Mot de passe |
|------|------------|--------------|
| **Directeur Général (DG)** | `dg` | `DG2025@Admin` |
| **Directeur Financier (DAF)** | `daf` | `DAF2025@Admin` |
| **Responsable RH** | `rh` | `RH2025@Admin` |
| **Gestionnaire Stock** | `stock` | `Stock2025` |
| **Caissier** | `caissier` | `Caissier2025` |
| **Marketing** | `marketing` | `Marketing2025` |

---

## ⚠️ POINTS IMPORTANTS

### 1. Sensibilité à la casse
Les mots de passe sont **sensibles à la casse** :
- ✅ **CORRECT** : `DG2025@Admin` (D et A en majuscule)
- ❌ **INCORRECT** : `dg2025@admin` (tout en minuscule)
- ❌ **INCORRECT** : `DG2025@ADMIN` (tout en majuscule)

### 2. Identifiants en minuscules
Les identifiants sont **toujours en minuscules** :
- ✅ **CORRECT** : `dg`
- ❌ **INCORRECT** : `DG`
- ❌ **INCORRECT** : `Dg`

### 3. Espace avant/après
Assurez-vous qu'il n'y a **pas d'espace** avant ou après :
- ✅ **CORRECT** : `dg`
- ❌ **INCORRECT** : ` dg` (espace au début)
- ❌ **INCORRECT** : `dg ` (espace à la fin)

---

## 🐛 DÉPANNAGE

### Problème 1 : "Identifiants incorrects" alors que je suis sûr du mot de passe
**Solution :**
```powershell
# Réinitialiser les mots de passe par défaut
python reset_default_passwords.py
```

### Problème 2 : "No such table: CarrefourApp_employe"
**Solution :**
```powershell
# Recréer la base de données
python manage.py migrate
python setup_after_clone.py
```

### Problème 3 : La page de connexion ne retourne rien
**Vérifications :**
1. Le serveur est-il lancé ? `python manage.py runserver`
2. Utilisez-vous la bonne URL ? `http://127.0.0.1:8000/login/`
3. Vérifiez la console du navigateur (F12) pour voir les erreurs

### Problème 4 : "Migrations non appliquées"
**Solution :**
```powershell
python manage.py migrate
```

---

## 📋 CHECKLIST APRÈS CLONAGE

- [ ] J'ai installé les dépendances : `pip install -r requirements.txt`
- [ ] J'ai créé la base de données : `python manage.py migrate`
- [ ] J'ai créé les comptes : `python setup_after_clone.py`
- [ ] Le serveur est lancé : `python manage.py runserver`
- [ ] J'accède à : http://127.0.0.1:8000/login/
- [ ] Je peux me connecter avec un des comptes par défaut

---

## 🎯 ACCÈS AUX MODULES PAR RÔLE

### Directeur Général (DG)
- ✅ Gestion des Stocks
- ✅ Gestion des Caisses
- ✅ Ressources Humaines
- ✅ Fidélisation Client
- ✅ Sécurité et Contrôle
- ✅ Analyses et Indicateurs

### Directeur Financier (DAF)
- ✅ Gestion des Stocks
- ✅ Gestion des Caisses
- ✅ Fidélisation Client
- ✅ Analyses et Indicateurs

### Responsable RH
- ✅ Ressources Humaines
- ✅ Analyses et Indicateurs (RH uniquement)

### Gestionnaire Stock
- ✅ Gestion des Stocks

### Caissier
- ✅ Gestion des Caisses
- ✅ Fidélisation Client (consultation)

### Marketing
- ✅ Fidélisation Client
- ✅ Analyses et Indicateurs (marketing)

---

## 🆘 BESOIN D'AIDE ?

Si vous rencontrez toujours des problèmes :
1. Vérifiez les fichiers de logs dans la console
2. Consultez le fichier `IDENTIFIANTS_CONNEXION.txt`
3. Relancez `python setup_after_clone.py`

---

## 📝 NOTES POUR L'ÉQUIPE

- **NE PAS** commiter le fichier `db.sqlite3` dans Git
- **NE PAS** modifier les mots de passe des comptes système (DG, DAF, RH) en production
- Chaque développeur doit exécuter `setup_after_clone.py` après avoir cloné
- Les comptes de test sont à usage **local uniquement**

---

**Date de création :** 23 octobre 2025  
**Version :** 1.0  
**Projet :** CARREFOUR - Système de Gestion Intégré
