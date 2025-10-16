# 🧪 Guide de Test - Système de Présence Automatique

## 📋 Checklist de Tests

### ✅ Phase 1 : Configuration des Horaires

#### Test 1.1 : Création d'un Employé avec Horaires
**Étapes :**
1. Se connecter en tant que RH
2. Aller sur `/dashboard/rh/create-employee/`
3. Vérifier que la section "⏰ Configuration des Horaires de Travail" est visible
4. Vérifier les valeurs par défaut :
   - Heure Début : 08:00
   - Heure Fin : 17:00
   - Pause : 90 minutes
5. Créer un employé de test avec :
   - Username : `test_employe`
   - Password : `Test1234!`
   - Prénom : Test
   - Nom : Employé
   - Rôle : CAISSIER
   - Horaires : 08:00 - 17:00, pause 90min

**Résultat attendu :**
- ✅ Section horaires affichée avec encadré jaune explicatif
- ✅ Employé créé avec succès
- ✅ Message de confirmation avec identifiants

#### Test 1.2 : Modification des Horaires d'un Employé
**Étapes :**
1. Se connecter en tant que RH
2. Aller sur `/dashboard/rh/employees/`
3. Cliquer sur "✏️ Modifier" pour l'employé créé
4. Vérifier que les horaires actuels sont affichés
5. Modifier les horaires :
   - Heure Début : 09:00
   - Heure Fin : 18:00
   - Pause : 60 minutes
6. Enregistrer les modifications

**Résultat attendu :**
- ✅ Section horaires affichée avec valeurs actuelles
- ✅ Modification enregistrée avec succès
- ✅ Message de confirmation

---

### ✅ Phase 2 : Test du Système Automatique

#### Test 2.1 : Connexion Pendant les Horaires de Travail (PRÉSENT)
**Étapes :**
1. Se déconnecter du compte RH
2. Se connecter avec `test_employe` / `Test1234!` à **08:10** (10 min de retard)
3. Vérifier l'accès au dashboard caissier
4. Se déconnecter à **17:00**
5. Se reconnecter en tant que RH
6. Aller sur `/dashboard/rh/presences/`
7. Vérifier la présence de l'employé test

**Résultat attendu :**
- ✅ Présence enregistrée automatiquement
- ✅ Heure arrivée : 08:10
- ✅ Heure départ : 17:00
- ✅ Heures travaillées : ~7h20 (8h50 - 1h30 pause)
- ✅ Pourcentage : ~97.8% (vert)
- ✅ Statut : **PRÉSENT** (retard ≤15min + ≥60% heures)

#### Test 2.2 : Connexion avec Retard Modéré (RETARD)
**Étapes :**
1. Créer une nouvelle présence ou supprimer la présence du test précédent
2. Se connecter avec `test_employe` à **08:45** (45 min de retard)
3. Se déconnecter à **17:00**
4. Vérifier la présence en tant que RH

**Résultat attendu :**
- ✅ Présence enregistrée automatiquement
- ✅ Heure arrivée : 08:45
- ✅ Heure départ : 17:00
- ✅ Heures travaillées : ~6h45 (8h15 - 1h30 pause)
- ✅ Pourcentage : ~90% (vert)
- ✅ Statut : **RETARD** (15-60min de retard + ≥60% heures)

#### Test 2.3 : Connexion avec Grand Retard (ABSENT)
**Étapes :**
1. Se connecter avec `test_employe` à **09:15** (1h15 de retard)
2. Se déconnecter à **17:00**
3. Vérifier la présence en tant que RH

**Résultat attendu :**
- ✅ Présence enregistrée automatiquement
- ✅ Heure arrivée : 09:15
- ✅ Heure départ : 17:00
- ✅ Statut : **ABSENT** (retard >60min, peu importe heures travaillées)

#### Test 2.4 : Départ Anticipé - Heures Insuffisantes (ABSENT)
**Étapes :**
1. Se connecter avec `test_employe` à **08:05**
2. Se déconnecter à **13:00** (parti tôt)
3. Vérifier la présence en tant que RH

**Résultat attendu :**
- ✅ Présence enregistrée automatiquement
- ✅ Heure arrivée : 08:05
- ✅ Heure départ : 13:00
- ✅ Heures travaillées : ~3h25 (4h55 - 1h30 pause)
- ✅ Pourcentage : ~45.6% (rouge)
- ✅ Statut : **ABSENT** (<60% des heures requises)

#### Test 2.5 : Connexion Hors Horaires (Pas de Présence)
**Étapes :**
1. Se connecter avec `test_employe` à **22:00** (soirée)
2. Consulter le dashboard
3. Se déconnecter
4. Vérifier les présences du jour en tant que RH

**Résultat attendu :**
- ✅ Connexion réussie
- ✅ **Aucune présence créée** (hors horaires de travail)
- ❌ Pas d'enregistrement dans le tableau des présences

#### Test 2.6 : Oubli de Déconnexion
**Étapes :**
1. Se connecter avec `test_employe` à **08:00**
2. **Ne pas se déconnecter** (fermer le navigateur directement)
3. Vérifier la présence en tant que RH

**Résultat attendu :**
- ✅ Présence créée avec heure_arrivee : 08:00
- ❌ heure_depart : Vide
- ⚠️ Statut : Calculé sur base des heures disponibles
- 👨‍💼 RH peut cliquer sur "✏️ Modifier" pour ajouter manuellement l'heure de départ

---

### ✅ Phase 3 : Interface RH

#### Test 3.1 : Page Liste des Présences
**Étapes :**
1. Se connecter en tant que RH
2. Aller sur `/dashboard/rh/presences/`

**Résultat attendu :**
- ✅ Message affiché : "ℹ️ Les présences sont enregistrées automatiquement..."
- ❌ **Pas de bouton "Ajouter Présence"**
- ✅ Tableau avec 8 colonnes (Employé, Poste, Arrivée, Départ, H.Travaillées, %Présence, Statut, Actions)
- ✅ Pourcentage avec couleur : vert si ≥60%, rouge si <60%
- ✅ Boutons "✏️ Modifier" et "🗑️ Supprimer" présents
- ✅ Statistiques : cartes Présents, Retards, Absents avec nombres corrects

#### Test 3.2 : Modification Manuelle d'une Présence
**Étapes :**
1. Sur la page des présences, cliquer sur "✏️ Modifier" pour une présence
2. Modifier l'heure de départ
3. Enregistrer

**Résultat attendu :**
- ✅ Formulaire de modification s'affiche
- ✅ Modification enregistrée
- ✅ Statut recalculé automatiquement
- ✅ Redirection vers la liste des présences

#### Test 3.3 : Suppression d'une Présence
**Étapes :**
1. Sur la page des présences, cliquer sur "🗑️ Supprimer" pour une présence
2. Confirmer la suppression

**Résultat attendu :**
- ✅ Page de confirmation affichée
- ✅ Présence supprimée après confirmation
- ✅ Message de succès
- ✅ Redirection vers la liste des présences

---

### ✅ Phase 4 : Calculs et Règles

#### Test 4.1 : Vérification des Calculs
Pour chaque présence testée, vérifier manuellement :

**Exemple : Arrivée 08:10, Départ 17:00**
```
Horaires configurés : 08:00 - 17:00, pause 90min
Heures requises : 17:00 - 08:00 = 9h
Heures requises (sans pause) : 9h - 1h30 = 7h30 = 7.5h

Temps présent : 17:00 - 08:10 = 8h50min
Temps travaillé : 8h50min - 1h30min = 7h20min = 7.33h
Pourcentage : (7.33 / 7.5) × 100 = 97.8%

Retard : 08:10 - 08:00 = 10 minutes

Règles :
- Retard 10min ≤ 15min ✅
- Pourcentage 97.8% ≥ 60% ✅
→ Statut : PRÉSENT ✅
```

**Résultat attendu :**
- ✅ Tous les calculs correspondent aux formules
- ✅ Les statuts sont corrects selon les règles

---

## 🔍 Points de Vérification Critiques

### Configuration Base de Données
```bash
# Vérifier que la migration est appliquée
python manage.py showmigrations

# Doit afficher :
# CarrefourApp
#  [X] 0001_initial
#  [X] 0002_alter_employe_departement_and_more
#  [X] 0003_presence_tolerance_retard
```

### Vérification des Champs du Modèle Employe
```python
# Dans la console Django (python manage.py shell)
from CarrefourApp.models import Employe

# Créer ou récupérer un employé
emp = Employe.objects.first()

# Vérifier les champs horaires
print(emp.heure_debut_travail)  # Devrait afficher 08:00:00
print(emp.heure_fin_travail)    # Devrait afficher 17:00:00
print(emp.duree_pause)          # Devrait afficher 90
```

### Vérification des Champs du Modèle Presence
```python
# Dans la console Django
from CarrefourApp.models import Presence
from django.utils import timezone

# Récupérer une présence
pres = Presence.objects.filter(date=timezone.now().date()).first()

# Vérifier les champs et méthodes
print(pres.heure_arrivee)
print(pres.heure_depart)
print(pres.tolerance_retard)  # Devrait afficher 60
print(pres.statut)

# Vérifier les calculs
print(pres.calculer_heures_requises())
print(pres.calculer_heures_travaillees())
print(pres.calculer_pourcentage_presence())
```

---

## 🐛 Scénarios de Bug Potentiels

### Scénario 1 : Double Présence
**Test :**
1. Se connecter à 08:00
2. Se déconnecter
3. Se reconnecter à 10:00
4. Se déconnecter

**Résultat attendu :**
- ✅ Une seule présence créée (get_or_create)
- ✅ heure_arrivee reste 08:00 (première connexion)
- ✅ heure_depart est 10:00 (dernière déconnexion)

### Scénario 2 : Changement de Jour
**Test :**
1. Se connecter un jour à 08:00
2. Ne pas se déconnecter
3. Le lendemain, se connecter à nouveau à 08:00

**Résultat attendu :**
- ✅ Deux présences distinctes (une par jour)
- ✅ Première présence : heure_arrivee sans heure_depart
- ✅ Deuxième présence : nouvelle heure_arrivee

### Scénario 3 : Modification d'Horaires Après Présence
**Test :**
1. Employé se connecte à 08:00 (horaires 08:00-17:00)
2. RH modifie les horaires à 09:00-18:00
3. Vérifier le statut de la présence existante

**Résultat attendu :**
- ✅ Présence conserve les calculs basés sur les nouveaux horaires
- ⚠️ Statut peut changer (08:00 devient une heure avant le début)

---

## 📊 Rapport de Test à Compléter

### Test Exécuté le : _______________
### Testé par : _______________

| Test | Statut | Commentaires |
|------|--------|--------------|
| 1.1 - Création employé avec horaires | ☐ ✅ ☐ ❌ | |
| 1.2 - Modification horaires | ☐ ✅ ☐ ❌ | |
| 2.1 - Connexion présent | ☐ ✅ ☐ ❌ | |
| 2.2 - Connexion retard | ☐ ✅ ☐ ❌ | |
| 2.3 - Connexion absent (retard) | ☐ ✅ ☐ ❌ | |
| 2.4 - Absent (heures insuffisantes) | ☐ ✅ ☐ ❌ | |
| 2.5 - Connexion hors horaires | ☐ ✅ ☐ ❌ | |
| 2.6 - Oubli déconnexion | ☐ ✅ ☐ ❌ | |
| 3.1 - Interface liste présences | ☐ ✅ ☐ ❌ | |
| 3.2 - Modification manuelle | ☐ ✅ ☐ ❌ | |
| 3.3 - Suppression présence | ☐ ✅ ☐ ❌ | |
| 4.1 - Vérification calculs | ☐ ✅ ☐ ❌ | |

### Bugs Identifiés :
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Améliorations Suggérées :
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

---

## 🚀 Prochaines Étapes

Après validation des tests :
- [ ] Former le personnel RH sur le nouveau système
- [ ] Créer un guide utilisateur pour les employés
- [ ] Configurer les horaires de tous les employés existants
- [ ] Mettre en production avec période d'observation
- [ ] Collecter les retours utilisateurs
- [ ] Ajuster la tolérance de retard si nécessaire (actuellement 60min)

---

**Version** : 1.0  
**Date** : Octobre 2025  
**Serveur de test** : http://127.0.0.1:8000/
