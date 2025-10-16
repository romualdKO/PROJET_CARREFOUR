# 🚀 Démarrage Rapide - Projet Carrefour

## ⚡ Installation en 3 Étapes (Avec Base de Données Incluse)

```bash
# 1️⃣ Cloner le projet
git clone https://github.com/romualdKO/PROJET_CARREFOUR.git
cd PROJET_CARREFOUR

# 2️⃣ Installer les dépendances
pip install -r requirements.txt

# 3️⃣ Démarrer le serveur
python manage.py runserver
```

**C'est tout ! 🎉** La base de données avec toutes les données de test est déjà incluse.

---

## 🌐 Accès au Site

Ouvrez votre navigateur : **http://127.0.0.1:8000/**

---

## 🔐 Identifiants de Connexion

### Comptes Administrateurs

| Rôle | Identifiant | Mot de passe | Dashboard |
|------|-------------|--------------|-----------|
| **Directeur Général** | `dg` | `DG2025@Admin` | Vue d'ensemble complète |
| **Directeur Financier** | `daf` | `DAF2025@Admin` | Gestion caisse/finances |
| **Responsable RH** | `rh` | `RH2025@Admin` | Gestion personnel/présences |

### ⚠️ Important
- Les mots de passe sont **sensibles à la casse**
- Exemple : `DG2025@Admin` (pas `dg2025@admin`)

---

## 📊 Données Incluses

La base de données contient déjà :

✅ **Comptes administrateurs** (DG, DAF, RH)  
✅ **Employés de test** (~15-20 employés fictifs)  
✅ **Produits de démonstration** (Alimentaire, Boissons, Hygiène, etc.)  
✅ **Présences et sessions** (Données de test pour le système multi-sessions)  

**Vous pouvez commencer à tester immédiatement !**

---

## 🎯 Premiers Pas

### 1. Connectez-vous en tant que RH

```
URL : http://127.0.0.1:8000/login/
Identifiant : rh
Mot de passe : RH2025@Admin
```

**Explorez :**
- 👥 Gestion des employés
- ⏰ Suivi des présences (système multi-sessions)
- 📊 Statistiques du personnel

### 2. Testez le système de présence multi-sessions

Le système permet maintenant aux employés de se connecter/déconnecter **plusieurs fois par jour** :

**Exemple :**
```
08:00 - Connexion
12:00 - Déconnexion (pause déjeuner)
14:00 - Connexion
18:00 - Déconnexion

→ Temps actif total : 6h
→ Statut calculé automatiquement
```

### 3. Connectez-vous en tant que DG

```
Identifiant : dg
Mot de passe : DG2025@Admin
```

**Explorez :**
- 📈 Dashboard avec vue d'ensemble
- 📊 Statistiques de ventes
- 👥 Aperçu du personnel
- 📦 État des stocks

### 4. Testez la gestion financière (DAF)

```
Identifiant : daf
Mot de passe : DAF2025@Admin
```

**Explorez :**
- 💰 Gestion de la caisse
- 📊 Rapports financiers
- 🧾 Historique des transactions

---

## 🧪 Scripts de Test Disponibles

### Tester l'authentification

```bash
python test_authentication.py
```

Vérifie que tous les comptes peuvent se connecter.

### Tester le système multi-sessions

```bash
python test_multi_sessions.py
```

Simule plusieurs connexions/déconnexions dans la journée.

### Réinitialiser les mots de passe

```bash
python reset_default_passwords.py
```

Réinitialise les mots de passe des comptes DG, DAF, RH.

---

## 📱 Accès Admin Django

Pour accéder à l'interface d'administration Django :

```
URL : http://127.0.0.1:8000/admin/
```

Utilisez le compte **DG** qui a les droits superuser :
```
Identifiant : dg
Mot de passe : DG2025@Admin
```

**Fonctionnalités admin :**
- Voir tous les modèles (Employés, Produits, Présences, etc.)
- Modifier directement les données
- Gérer les permissions

---

## 🔄 Si Vous Voulez Repartir de Zéro

### Option 1 : Réinitialiser la base existante

```bash
# Windows
del db.sqlite3
python manage.py migrate
python init_default_accounts.py

# Linux/Mac
rm db.sqlite3
python manage.py migrate
python init_default_accounts.py
```

### Option 2 : Créer des données de test personnalisées

```bash
# Après avoir réinitialisé la base
python create_sample_data.py
```

---

## 🆘 Dépannage Rapide

### Problème : "Port 8000 already in use"

```bash
# Windows
taskkill /F /IM python.exe

# Linux/Mac
pkill python

# Puis redémarrer
python manage.py runserver
```

### Problème : "No module named 'django'"

```bash
pip install -r requirements.txt
```

### Problème : "table doesn't exist"

```bash
python manage.py migrate
```

### Problème : Impossible de se connecter

```bash
# Réinitialiser les mots de passe
python reset_default_passwords.py

# Tester
python test_authentication.py
```

---

## 📚 Documentation Complète

Pour plus de détails :

- 📖 [`README.md`](README.md) - Documentation principale
- 🔐 [`GUIDE_CONNEXION.md`](GUIDE_CONNEXION.md) - Guide de connexion détaillé
- 📊 [`DATABASE_README.md`](DATABASE_README.md) - Informations sur la base de données
- 🎯 [`SYSTEME_MULTI_SESSIONS.md`](SYSTEME_MULTI_SESSIONS.md) - Système de présence
- 🛠️ [`INSTALLATION_COLLABORATEURS.md`](INSTALLATION_COLLABORATEURS.md) - Guide complet

---

## ✨ Fonctionnalités Principales

### 🎯 Système de Présence Multi-Sessions (Nouveau !)

- ✅ Connexions/déconnexions illimitées par jour
- ✅ Calcul automatique du temps actif total
- ✅ Statut automatique (Présent/Retard/Absent)
- ✅ Règle des 60% du temps de travail

### 👥 Gestion des Employés

- ✅ CRUD complet (Créer, Lire, Modifier, Supprimer)
- ✅ Différents rôles (DG, DAF, RH, STOCK, CAISSIER, etc.)
- ✅ Horaires de travail personnalisables
- ✅ Gestion des départements

### 📦 Gestion des Stocks

- ✅ Inventaire complet des produits
- ✅ Alertes de stock critique
- ✅ Catégories multiples
- ✅ Suivi des fournisseurs

### 💰 Gestion Financière

- ✅ Système de caisse
- ✅ Rapports financiers
- ✅ Suivi des transactions
- ✅ Analyse des ventes

---

## 🎓 Exemple de Workflow

### Scénario : Ajouter un Nouvel Employé

1. **Connectez-vous en tant que RH**
   ```
   http://127.0.0.1:8000/login/
   Identifiant : rh / Mot de passe : RH2025@Admin
   ```

2. **Accédez à la gestion des employés**
   ```
   Dashboard RH → Gestion des Employés → Ajouter
   ```

3. **Remplissez le formulaire**
   - Prénom, Nom
   - Email, Téléphone
   - Rôle et Département
   - Horaires de travail

4. **Créez le compte**
   - L'employé peut maintenant se connecter
   - Ses présences seront suivies automatiquement

### Scénario : Consulter les Présences

1. **Connectez-vous en tant que RH**

2. **Accédez aux présences**
   ```
   Dashboard RH → Gestion des Présences
   ```

3. **Visualisez**
   - Première arrivée / Dernière départ
   - Temps actif total
   - Statut automatique
   - Détails des sessions multiples

---

## 🚀 Prêt à Développer ?

### Structure du Projet

```
PROJET_CARREFOUR/
├── Carrefour/           # Configuration Django
├── CarrefourApp/        # Application principale
│   ├── models.py        # Modèles (Employe, Presence, etc.)
│   ├── views.py         # Vues et logique métier
│   ├── urls.py          # Routes
│   └── admin.py         # Configuration admin
├── templates/           # Templates HTML
├── static/             # CSS, JS, Images
├── db.sqlite3          # Base de données (incluse)
└── manage.py           # Commandes Django
```

### Commandes Utiles

```bash
# Créer une migration
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Shell Django
python manage.py shell

# Collecter les fichiers statiques
python manage.py collectstatic
```

---

## 💡 Conseils

✅ **Utilisez la base de données incluse** pour les tests  
✅ **Changez les mots de passe** avant tout déploiement  
✅ **Testez les scripts** (`test_authentication.py`, `test_multi_sessions.py`)  
✅ **Consultez la documentation** pour plus de détails  
✅ **Explorez l'admin Django** pour voir la structure des données  

---

## 🎉 Vous êtes Prêt !

Avec ces 3 commandes, vous avez un système complet et fonctionnel :

```bash
git clone https://github.com/romualdKO/PROJET_CARREFOUR.git
cd PROJET_CARREFOUR
pip install -r requirements.txt
python manage.py runserver
```

**Bonne exploration ! 🚀**

---

**Version** : 2.0.0  
**Date** : 16 octobre 2025  
**Statut** : ✅ Opérationnel avec base de données complète
