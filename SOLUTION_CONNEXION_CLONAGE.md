# 🎯 SOLUTION : Problème de connexion après clonage

## 📝 Contexte

Votre collègue peut accéder aux modules avec les identifiants par défaut, mais **vous ne pouvez pas** après avoir cloné le projet.

## 🔍 Explication du problème

Quand vous clonez un projet Git, **la base de données SQLite n'est PAS incluse** (elle est dans `.gitignore`). 

Votre collègue a :
- ✅ Une base de données avec les comptes créés
- ✅ Les mots de passe configurés

Vous avez :
- ❌ Pas de base de données (ou vide)
- ❌ Aucun compte créé

**Résultat :** Les identifiants ne fonctionnent pas car les comptes n'existent pas dans votre base de données locale !

---

## ✅ SOLUTION RAPIDE (Option 1 - Recommandée)

### Une seule commande :

```powershell
python install_after_clone.py
```

Cette commande va :
1. Créer la base de données
2. Créer tous les comptes par défaut
3. Tester que tout fonctionne

**Ensuite lancez le serveur :**
```powershell
python manage.py runserver
```

---

## ✅ SOLUTION MANUELLE (Option 2)

Si vous préférez faire étape par étape :

### Étape 1 : Installer les dépendances
```powershell
pip install -r requirements.txt
```

### Étape 2 : Créer la base de données
```powershell
python manage.py migrate
```

### Étape 3 : Créer les comptes
```powershell
python setup_after_clone.py
```

### Étape 4 : Tester
```powershell
python test_connexion.py
```

### Étape 5 : Lancer le serveur
```powershell
python manage.py runserver
```

---

## 🔑 Identifiants de connexion

**URL :** http://127.0.0.1:8000/login/

| Rôle | Identifiant | Mot de passe |
|------|------------|--------------|
| Directeur Général | `dg` | `DG2025@Admin` |
| Directeur Financier | `daf` | `DAF2025@Admin` |
| Responsable RH | `rh` | `RH2025@Admin` |
| Gestionnaire Stock | `stock` | `Stock2025` |
| Caissier | `caissier` | `Caissier2025` |
| Marketing | `marketing` | `Marketing2025` |

---

## ⚠️ Points d'attention

### 1. Sensibilité à la casse
```
✅ CORRECT   : DG2025@Admin
❌ INCORRECT : dg2025@admin
❌ INCORRECT : DG2025@ADMIN
```

### 2. Identifiants en minuscules
```
✅ CORRECT   : dg
❌ INCORRECT : DG
❌ INCORRECT : Dg
```

### 3. Pas d'espace
```
✅ CORRECT   : dg
❌ INCORRECT :  dg  (espaces)
```

---

## 🐛 Dépannage

### Problème : "Identifiants incorrects"

**Cause :** Les comptes n'existent pas ou les mots de passe sont incorrects.

**Solution :**
```powershell
python reset_default_passwords.py
python test_connexion.py
```

### Problème : "No such table"

**Cause :** La base de données n'a pas été créée.

**Solution :**
```powershell
python manage.py migrate
python setup_after_clone.py
```

### Problème : La page ne retourne rien

**Vérifications :**
1. Le serveur est-il lancé ? → `python manage.py runserver`
2. Bonne URL ? → `http://127.0.0.1:8000/login/`
3. Ouvrez la console du navigateur (F12) pour voir les erreurs

### Problème : "Migrations non appliquées"

**Solution :**
```powershell
python resolve_migrations.py
```

---

## 📊 Scripts disponibles

| Script | Description |
|--------|-------------|
| `install_after_clone.py` | Installation automatique complète |
| `setup_after_clone.py` | Crée les comptes et types de paiement |
| `test_connexion.py` | Teste tous les comptes |
| `reset_default_passwords.py` | Réinitialise les mots de passe |
| `resolve_migrations.py` | Résout les conflits de migrations |

---

## 🎓 Pour votre équipe

### Quand un nouveau développeur clone le projet :

1. **Cloner le repo**
   ```bash
   git clone <url-du-repo>
   cd PROJET_CARREFOUR
   ```

2. **Installer et configurer**
   ```powershell
   pip install -r requirements.txt
   python install_after_clone.py
   ```

3. **Lancer**
   ```powershell
   python manage.py runserver
   ```

4. **Se connecter**
   - URL : http://127.0.0.1:8000/login/
   - Utiliser un des comptes ci-dessus

---

## 📌 Important

- ✅ **Chaque développeur** doit exécuter `install_after_clone.py` après avoir cloné
- ✅ Ne **jamais** commiter le fichier `db.sqlite3`
- ✅ Les comptes par défaut sont pour le **développement local uniquement**
- ✅ En production, utilisez des mots de passe sécurisés

---

## 📚 Documentation complète

- `GUIDE_APRES_CLONAGE.md` - Guide détaillé
- `AIDE_CONNEXION.md` - Aide rapide
- `IDENTIFIANTS_CONNEXION.txt` - Liste des identifiants

---

**Date :** 23 octobre 2025  
**Problème résolu :** Connexion impossible après clonage  
**Statut :** ✅ Résolu
