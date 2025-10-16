# 📋 Système de Présence Automatique - Documentation Complète

## 🎯 Vue d'ensemble

Le système de présence a été mis à niveau pour fonctionner **automatiquement** lors de la connexion et déconnexion des employés. Le RH n'a plus besoin d'ajouter manuellement les présences, il configure uniquement les horaires de travail pour chaque employé.

---

## ⚙️ Fonctionnement Automatique

### 1. **À la Connexion (Login)**
Lorsqu'un employé se connecte au système :
- ✅ **Si l'heure actuelle est dans la plage de travail** (entre `heure_debut_travail` et `heure_fin_travail`) :
  - Une présence est créée automatiquement avec l'heure d'arrivée enregistrée
  - La tolérance de retard par défaut est de 60 minutes
- ❌ **Si l'heure est en dehors de la plage de travail** :
  - Aucune présence n'est enregistrée (connexion hors horaires)

### 2. **À la Déconnexion (Logout)**
Lorsqu'un employé se déconnecte du système :
- ✅ **Si une présence existe pour aujourd'hui avec une heure d'arrivée** :
  - L'heure de départ est enregistrée automatiquement
  - Le statut de présence est recalculé automatiquement
- ℹ️ Si l'employé ne se déconnecte pas, l'heure de départ ne sera pas enregistrée

---

## 📊 Règles de Calcul du Statut

Le système calcule automatiquement le statut de chaque présence selon ces règles :

### 🟢 **PRÉSENT**
- Arrivée ≤ 15 minutes après l'heure de début
- **ET** au moins 60% des heures requises travaillées

### 🟡 **RETARD**
- Arrivée entre 16 et 60 minutes après l'heure de début
- **ET** au moins 60% des heures requises travaillées

### 🔴 **ABSENT**
- Arrivée > 60 minutes après l'heure de début
- **OU** moins de 60% des heures requises travaillées

---

## 🔧 Configuration par le RH

### Configuration des Horaires d'un Employé

Le RH configure les horaires de travail via :
1. **Création d'un nouvel employé** (`/dashboard/rh/create-employee/`)
2. **Modification d'un employé** (`/dashboard/rh/employees/<id>/edit/`)

#### Champs de configuration :

| Champ | Description | Valeur par défaut |
|-------|-------------|-------------------|
| **Heure Début** | Heure de début de journée | 08:00 |
| **Heure Fin** | Heure de fin de journée | 17:00 |
| **Pause (minutes)** | Durée de la pause déjeuner | 90 minutes |

### Exemple de Calcul

**Configuration :**
- Heure début : 08:00
- Heure fin : 17:00
- Pause : 90 minutes (1h30)

**Heures requises par jour :**
```
17:00 - 08:00 = 9 heures
9h - 1h30 (pause) = 7h30 = 7.5 heures requises
60% de 7.5h = 4.5 heures minimum
```

**Scénario 1 : PRÉSENT ✅**
- Arrivée : 08:10 (10 min de retard)
- Départ : 17:00
- Heures travaillées : 8h50min - 1h30min = 7h20min
- Pourcentage : 97.8% > 60% ✅
- Statut : **PRÉSENT**

**Scénario 2 : RETARD 🟡**
- Arrivée : 08:45 (45 min de retard)
- Départ : 17:00
- Heures travaillées : 8h15min - 1h30min = 6h45min
- Pourcentage : 90% > 60% ✅
- Statut : **RETARD**

**Scénario 3 : ABSENT 🔴**
- Arrivée : 09:15 (1h15min de retard)
- Départ : 17:00
- Retard > 60 minutes ❌
- Statut : **ABSENT**

**Scénario 4 : ABSENT (heures insuffisantes) 🔴**
- Arrivée : 08:05 (5 min de retard)
- Départ : 13:00 (parti tôt)
- Heures travaillées : 4h55min - 1h30min = 3h25min
- Pourcentage : 45.6% < 60% ❌
- Statut : **ABSENT**

---

## 👥 Interface RH

### 1. **Liste des Présences** (`/dashboard/rh/presences/`)

Affiche :
- 📅 Date sélectionnée (par défaut : aujourd'hui)
- 📊 Statistiques : Présents, Retards, Absents
- 📋 Tableau détaillé avec :
  - Employé et poste
  - Heures d'arrivée et de départ
  - Heures travaillées
  - Pourcentage de présence (vert ≥60%, rouge <60%)
  - Statut calculé automatiquement
  - Actions : ✏️ Modifier / 🗑️ Supprimer

**Note importante :**
- ℹ️ Message affiché : "Les présences sont enregistrées automatiquement à la connexion/déconnexion des employés"
- Le bouton "Ajouter Présence" a été retiré
- Modifier/Supprimer permet de corriger manuellement en cas d'erreur

### 2. **Création d'Employé** (`/dashboard/rh/create-employee/`)

Nouveau : Section "⏰ Configuration des Horaires de Travail" avec :
- Champs pour heure début, heure fin, durée pause
- Valeurs par défaut : 08:00 - 17:00 avec 90min de pause
- Encadré jaune expliquant les règles de présence automatiques

### 3. **Modification d'Employé** (`/dashboard/rh/employees/<id>/edit/`)

Nouveau : Section "⏰ Configuration des Horaires de Travail" avec :
- Champs pré-remplis avec les horaires actuels
- Possibilité de modifier les horaires pour adapter aux besoins spécifiques
- Encadré jaune expliquant les règles de présence automatiques

---

## 🛠️ Implémentation Technique

### Fichiers Modifiés

#### 1. **CarrefourApp/views.py**

**Fonction `login_view` (lignes 24-79)** :
```python
# Après authentification réussie
today = timezone.now().date()
current_time = timezone.now().time()

# Vérifier si dans les horaires de travail
if user.heure_debut_travail <= current_time <= user.heure_fin_travail:
    presence, created = Presence.objects.get_or_create(
        employe=user,
        date=today,
        defaults={'heure_arrivee': current_time, 'tolerance_retard': 60}
    )
    if not created and not presence.heure_arrivee:
        presence.heure_arrivee = current_time
        presence.save()
```

**Fonction `logout_view` (lignes 79-100)** :
```python
# Avant la déconnexion
if request.user.is_authenticated:
    today = timezone.now().date()
    current_time = timezone.now().time()
    
    try:
        presence = Presence.objects.get(employe=request.user, date=today)
        if presence.heure_arrivee and not presence.heure_depart:
            presence.heure_depart = current_time
            presence.save()  # Recalcule automatiquement le statut
    except Presence.DoesNotExist:
        pass
```

**Fonction `rh_employee_edit` (mise à jour)** :
- Ajout de la gestion des champs `heure_debut_travail`, `heure_fin_travail`, `duree_pause`

**Fonction `rh_create_employee` (mise à jour)** :
- Configuration automatique des horaires de travail lors de la création
- Valeurs par défaut : 08:00 - 17:00 avec 90min de pause

#### 2. **CarrefourApp/models.py**

**Modèle Employe (lignes ~35-50)** :
```python
heure_debut_travail = models.TimeField(default='08:00')
heure_fin_travail = models.TimeField(default='17:00')
duree_pause = models.IntegerField(default=90)  # en minutes
```

**Modèle Presence (lignes 240-340)** :
- Méthode `calculer_statut()` : Implémente les règles complexes
- Méthode `calculer_heures_requises()` : Calcule les heures attendues
- Méthode `calculer_heures_travaillees()` : Calcule les heures effectivement travaillées
- Méthode `calculer_pourcentage_presence()` : Calcule le pourcentage
- Méthode `save()` : Recalcule automatiquement le statut avant sauvegarde

#### 3. **templates/dashboard/rh_presences.html**
- Suppression du bouton "Ajouter Présence"
- Ajout d'un message informatif sur le système automatique
- Affichage du pourcentage avec code couleur

#### 4. **templates/dashboard/rh_employee_edit.html**
- Ajout de la section "Configuration des Horaires de Travail"
- 3 champs : heure_debut_travail, heure_fin_travail, duree_pause
- Encadré explicatif des règles

#### 5. **templates/dashboard/rh_create_employee.html**
- Ajout de la section "Configuration des Horaires de Travail"
- Valeurs par défaut dans les champs
- Encadré explicatif des règles

### Migration Appliquée

**0003_presence_tolerance_retard.py** :
- Ajout du champ `tolerance_retard` au modèle Presence
- Valeur par défaut : 60 minutes

---

## 📝 Cas d'Usage

### Cas 1 : Employé Normal
1. **08:05** - Connexion au système
   - ✅ Présence créée avec heure_arrivee = 08:05
2. **17:10** - Déconnexion
   - ✅ Présence mise à jour avec heure_depart = 17:10
   - ✅ Statut calculé : PRÉSENT (9h05 travaillées - 90min pause = 7h35 = 101%)

### Cas 2 : Employé en Retard
1. **08:50** - Connexion (50 min de retard)
   - ✅ Présence créée avec heure_arrivee = 08:50
2. **17:00** - Déconnexion
   - ✅ Statut : RETARD (arrivée entre 15-60min + 90% heures travaillées)

### Cas 3 : Employé Absent
1. **09:30** - Connexion (1h30 de retard)
   - ✅ Présence créée avec heure_arrivee = 09:30
2. **17:00** - Déconnexion
   - 🔴 Statut : ABSENT (retard > 60 minutes)

### Cas 4 : Oubli de Déconnexion
1. **08:00** - Connexion
   - ✅ Présence créée avec heure_arrivee = 08:00
2. **Pas de déconnexion**
   - ⚠️ heure_depart reste vide
   - 👨‍💼 RH peut modifier manuellement pour ajouter l'heure de départ

### Cas 5 : Connexion Hors Horaires
1. **22:00** - Connexion pour consulter
   - ❌ Aucune présence créée (hors horaires de travail)

---

## ✅ Avantages du Système Automatique

1. **🚀 Gain de Temps** : Plus besoin de saisie manuelle
2. **📊 Précision** : Horodatage exact de connexion/déconnexion
3. **🎯 Automatisation** : Calcul automatique du statut selon règles
4. **⚖️ Équité** : Règles uniformes appliquées à tous
5. **🔍 Transparence** : Employés voient directement leur statut
6. **🛠️ Flexibilité** : RH peut corriger manuellement si nécessaire

---

## 🔄 Workflow RH

### Configuration Initiale
1. Créer ou modifier un employé
2. Configurer ses horaires de travail
3. L'employé reçoit ses identifiants

### Suivi Quotidien
1. Consulter le tableau des présences du jour
2. Vérifier les statistiques (Présents/Retards/Absents)
3. Corriger manuellement si erreur détectée

### Gestion Mensuelle
1. Exporter les données de présence
2. Analyser les tendances de ponctualité
3. Ajuster les horaires si nécessaire

---

## 🚨 Points d'Attention

1. **⚠️ Oubli de Déconnexion** : Si un employé oublie de se déconnecter, l'heure de départ ne sera pas enregistrée. Le RH devra la corriger manuellement.

2. **⚠️ Connexion Hors Horaires** : Les connexions en dehors des horaires de travail (soirée, week-end) ne créent pas de présence.

3. **⚠️ Tolérance de 60 minutes** : Le seuil de 60 minutes pour être considéré absent peut être ajusté dans le code si nécessaire.

4. **⚠️ Pause Déjeuner** : La pause est déduite automatiquement du temps de travail. Si un employé ne prend pas de pause ou une pause plus courte, le système utilisera toujours la durée configurée.

---

## 🎯 Prochaines Améliorations Possibles

- [ ] Ajout d'un rapport mensuel automatique par employé
- [ ] Notification automatique au RH si absence non justifiée
- [ ] Interface employé pour consulter son propre historique
- [ ] Export Excel/PDF des présences pour la paie
- [ ] Gestion des congés intégrée aux calculs de présence
- [ ] Gestion des jours fériés
- [ ] Configuration de la tolérance par employé (actuellement fixe à 60min)

---

## 📞 Support

Pour toute question ou problème concernant le système de présence automatique, contactez l'équipe de développement.

**Version du système** : 1.0  
**Date de mise à jour** : Octobre 2025  
**Django** : 5.2  
**Python** : 3.13.5
