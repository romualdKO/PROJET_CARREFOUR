# 🔐 Guide de Connexion - Projet Carrefour

## 📋 Comptes de Test et Démonstration

Ce document contient les identifiants des comptes par défaut pour tester et utiliser le système.

---

## 👥 Comptes Administrateurs

### 🎯 Directeur Général (DG)

```
Identifiant : dg
Mot de passe : DG2025@Admin
```

**Accès :**
- ✅ Dashboard Directeur Général
- ✅ Vue d'ensemble complète
- ✅ Tous les rapports
- ✅ Accès administrateur

---

### 💰 Directeur Administratif et Financier (DAF)

```
Identifiant : daf
Mot de passe : DAF2025@Admin
```

**Accès :**
- ✅ Dashboard Financier
- ✅ Gestion de la caisse
- ✅ Rapports financiers
- ✅ Suivi des ventes

---

### 👔 Responsable Ressources Humaines (RH)

```
Identifiant : rh
Mot de passe : RH2025@Admin
```

**Accès :**
- ✅ Dashboard RH
- ✅ Gestion des employés
- ✅ Gestion des présences
- ✅ Suivi du personnel

---

## ⚠️ Instructions Importantes

### 1. **Sensibilité à la casse**
Les mots de passe sont **sensibles à la casse**. Assurez-vous de respecter les majuscules et minuscules :
- ✅ Correct : `DG2025@Admin`
- ❌ Incorrect : `dg2025@admin`
- ❌ Incorrect : `DG2025@ADMIN`

### 2. **Caractères spéciaux**
Le caractère `@` doit être saisi exactement :
- ✅ Correct : `DG2025@Admin`
- ❌ Incorrect : `DG2025Admin`

### 3. **Première connexion**
Lors de votre première connexion :
1. Saisissez l'identifiant (en minuscules)
2. Saisissez le mot de passe (avec majuscules et @)
3. Cliquez sur "Se connecter"
4. Vous serez redirigé vers votre dashboard

### 4. **Changement de mot de passe**
Pour des raisons de sécurité, il est recommandé de :
- Changer le mot de passe après la première connexion
- Utiliser un mot de passe fort (8 caractères minimum, avec majuscules, minuscules, chiffres et caractères spéciaux)

---

## 🔧 En cas de problème de connexion

### Problème : "Identifiants invalides"

**Solutions :**

1. **Vérifier la casse du mot de passe**
   - Le mot de passe commence par une MAJUSCULE
   - Exemple : `DG2025@Admin` (pas `dg2025@admin`)

2. **Vérifier l'identifiant**
   - L'identifiant est en MINUSCULES
   - Exemples : `dg`, `daf`, `rh` (pas `DG`, `DAF`, `RH`)

3. **Vérifier le caractère @**
   - Assurez-vous d'utiliser le bon caractère arobase `@`
   - Ne pas confondre avec d'autres caractères

4. **Copier-coller le mot de passe**
   - Si possible, copiez le mot de passe depuis ce document
   - Évitez les espaces avant ou après

5. **Réinitialiser les mots de passe**
   - Si le problème persiste, contactez l'administrateur système
   - Il peut exécuter le script `reset_default_passwords.py`

---

## 🖥️ Accès au système

### URL de connexion
```
http://127.0.0.1:8000/login/
```
ou
```
http://localhost:8000/login/
```

### Démarrer le serveur (pour l'administrateur)
```bash
python manage.py runserver
```

---

## 📊 Fonctionnalités par Rôle

### Directeur Général (DG)
- 📈 Vue d'ensemble des ventes
- 👥 Statistiques du personnel
- 📦 État des stocks
- 💰 Performance financière
- 📊 Tous les rapports

### Directeur Financier (DAF)
- 💵 Gestion de la caisse
- 📊 Rapports financiers
- 💳 Suivi des transactions
- 📈 Analyse des ventes
- 🧾 Historique des opérations

### Responsable RH (RH)
- 👥 Gestion des employés (CRUD)
- ⏰ Gestion des présences
- 📅 Suivi du temps de travail
- 📊 Statistiques du personnel
- ✅ Validation automatique des présences

---

## 🔄 Système de Présence Automatique

### Nouvelle fonctionnalité : Sessions multiples

Les employés peuvent maintenant :
- ✅ Se connecter et déconnecter **plusieurs fois par jour**
- ✅ Le système calcule automatiquement le **temps actif total**
- ✅ Le statut (Présent/Retard/Absent) est calculé automatiquement
- ✅ Pas besoin de modification manuelle

**Exemple :**
```
08:00 - Connexion
10:00 - Déconnexion  (Session 1: 2h)
14:00 - Connexion
17:00 - Déconnexion  (Session 2: 3h)

→ Temps actif total : 5h
→ Statut calculé automatiquement
```

---

## 📞 Support

### Pour réinitialiser les mots de passe (Administrateur système)

Exécutez le script suivant :
```bash
python reset_default_passwords.py
```

Ce script va :
- ✅ Réinitialiser les mots de passe aux valeurs par défaut
- ✅ Activer tous les comptes
- ✅ Vérifier que les rôles sont corrects

---

## 📝 Notes pour les Développeurs

### Structure des comptes

```python
# Compte DG
username: 'dg'
role: 'DG'
is_staff: True
is_superuser: True

# Compte DAF
username: 'daf'
role: 'DAF'
is_staff: True

# Compte RH
username: 'rh'
role: 'RH'
is_staff: True
```

### Scripts disponibles

- `reset_default_passwords.py` : Réinitialise les mots de passe par défaut
- `init_default_accounts.py` : Ancien script (à ne plus utiliser)
- `test_multi_sessions.py` : Test du système de présence multi-sessions

---

## ✅ Checklist de connexion

Avant de contacter le support, vérifiez :

- [ ] Le serveur est démarré (`python manage.py runserver`)
- [ ] L'URL est correcte (`http://127.0.0.1:8000/login/`)
- [ ] L'identifiant est en minuscules
- [ ] Le mot de passe respecte la casse (majuscules/minuscules)
- [ ] Le caractère @ est bien présent
- [ ] Pas d'espaces avant ou après le mot de passe
- [ ] Vous utilisez le bon compte (dg, daf, ou rh)

---

**Date de mise à jour** : 16 octobre 2025  
**Version** : 2.0.0  
**Statut** : ✅ Comptes opérationnels

---

## 🎯 Résumé Rapide

| Rôle | Identifiant | Mot de passe | Dashboard |
|------|-------------|--------------|-----------|
| **DG** | `dg` | `DG2025@Admin` | Directeur Général |
| **DAF** | `daf` | `DAF2025@Admin` | Financier |
| **RH** | `rh` | `RH2025@Admin` | Ressources Humaines |

**⚠️ Important** : Les mots de passe sont sensibles à la casse !
