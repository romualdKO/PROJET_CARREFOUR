# 🚨 AIDE : Impossible de se connecter après clonage

## 🎯 Résumé du problème
Vous avez cloné le projet mais vous ne pouvez pas vous connecter avec les identifiants par défaut.

## ✅ Solution en 3 commandes

Ouvrez PowerShell dans le dossier du projet et exécutez :

```powershell
# 1. Installer les dépendances (si pas déjà fait)
pip install -r requirements.txt

# 2. Créer la base de données
python manage.py migrate

# 3. Créer les comptes par défaut
python setup_after_clone.py
```

**C'est tout !** 🎉

## 🔑 Identifiants à utiliser

| Identifiant | Mot de passe |
|------------|--------------|
| `dg` | `DG2025@Admin` |
| `daf` | `DAF2025@Admin` |
| `rh` | `RH2025@Admin` |
| `stock` | `Stock2025` |
| `caissier` | `Caissier2025` |
| `marketing` | `Marketing2025` |

## 🌐 Lancer l'application

```powershell
python manage.py runserver
```

Puis accédez à : **http://127.0.0.1:8000/login/**

## ⚠️ Points importants

- Les mots de passe sont **sensibles à la casse** : `DG2025@Admin` (pas `dg2025@admin`)
- Les identifiants sont en **minuscules** : `dg` (pas `DG`)
- Pas d'espace avant/après

## 🧪 Tester vos comptes

Pour vérifier si tout fonctionne :

```powershell
python test_connexion.py
```

Vous devriez voir ✅ SUCCÈS pour tous les comptes.

## 🆘 Toujours bloqué ?

Si ça ne fonctionne toujours pas :

```powershell
# Réinitialiser les mots de passe
python reset_default_passwords.py

# Tester à nouveau
python test_connexion.py
```

## 📚 Plus d'informations

Consultez le fichier `GUIDE_APRES_CLONAGE.md` pour plus de détails.
