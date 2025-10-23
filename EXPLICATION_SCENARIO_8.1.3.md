# 📋 SCÉNARIO 8.1.3 - EXPLICATION COMPLÈTE DU FLUX

## 🎯 COMMENT ÇA FONCTIONNE ?

### 1️⃣ L'EMPLOYÉ FAIT SA DEMANDE (dans SON espace)

**Page : `/planning/demander-conge/`**

```
┌─────────────────────────────────────────┐
│  👤 EMPLOYÉ (Sarah Kouadio)             │
│                                         │
│  1. Se connecte avec son compte         │
│     Username: sarah.kouadio             │
│     Password: ********                  │
│                                         │
│  2. Va sur "Mon Planning"               │
│     → Voit son planning personnel       │
│                                         │
│  3. Clique "Demander un Congé"          │
│     → Remplit le formulaire :           │
│        - Type : Congé payé              │
│        - Du : 25/10/2025                │
│        - Au : 25/10/2025                │
│        - Motif : Rendez-vous médical    │
│                                         │
│  4. Clique "Envoyer la Demande"         │
│     ✅ ENREGISTRÉ EN BASE DE DONNÉES    │
│                                         │
└─────────────────────────────────────────┘
```

**Ce qui se passe dans le code (views.py ligne 3918-3948) :**

```python
@login_required
def demander_conge(request):
    # 1. Vérifier que c'est un employé
    if not hasattr(request.user, 'employe'):
        return redirect('dashboard')
    
    # 2. Quand l'employé soumet le formulaire
    if request.method == 'POST':
        employe = request.user.employe  # ← L'EMPLOYÉ CONNECTÉ
        
        # 3. Récupérer les données du formulaire
        type_conge = request.POST.get('type_conge')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        motif = request.POST.get('motif', '')
        
        # 4. CRÉER LA DEMANDE EN BASE DE DONNÉES ✅
        demande = DemandeConge.objects.create(
            employe=employe,           # ← QUI fait la demande
            type_conge=type_conge,     # ← QUEL type
            date_debut=date_debut,     # ← QUAND début
            date_fin=date_fin,         # ← QUAND fin
            motif=motif,               # ← POURQUOI
            statut='EN_ATTENTE'        # ← Statut initial
        )
        
        # 5. Enregistré en base ! ✅
        messages.success(request, 'Demande envoyée!')
        return redirect('mon_planning')
```

---

### 2️⃣ LE RH VOIT LA DEMANDE (dans SON espace)

**Page : `/rh/demandes-conges/`**

```
┌─────────────────────────────────────────┐
│  👔 RH / MANAGER                        │
│                                         │
│  1. Se connecte avec son compte RH      │
│     Username: rh.admin                  │
│     Password: ********                  │
│                                         │
│  2. Va sur "Gérer Demandes de Congés"  │
│     → Voit TOUTES les demandes :        │
│                                         │
│     📋 Demande #123                     │
│     Employé: Sarah Kouadio              │
│     Type: Congé payé                    │
│     Du 25/10 au 25/10 (1 jour)          │
│     Statut: ⏳ EN_ATTENTE               │
│                                         │
│  3. Clique "Traiter"                    │
│     → Peut :                            │
│        ✅ Approuver (+ commentaire)     │
│        ❌ Rejeter (+ commentaire)       │
│                                         │
│  4. Clique "Approuver"                  │
│     ✅ BASE DE DONNÉES MISE À JOUR      │
│                                         │
└─────────────────────────────────────────┘
```

**Ce qui se passe dans le code (views.py ligne 4014-4048) :**

```python
@login_required
def rh_traiter_demande(request, demande_id):
    # 1. Vérifier que c'est un RH/Manager
    if request.user.role not in ['RH', 'MANAGER', 'ADMIN']:
        return redirect('dashboard')
    
    # 2. Récupérer LA DEMANDE depuis la base de données
    demande = DemandeConge.objects.get(id=demande_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        commentaire_rh = request.POST.get('commentaire_rh', '')
        
        # 3. MODIFIER LA DEMANDE EN BASE DE DONNÉES ✅
        if action == 'approuver':
            demande.statut = 'APPROUVE'           # ← Changement statut
            demande.approuve_par = request.user.employe
            demande.date_traitement = timezone.now()
            demande.commentaire_rh = commentaire_rh
            demande.save()  # ← ENREGISTRÉ EN BASE ! ✅
            
        elif action == 'rejeter':
            demande.statut = 'REJETE'
            demande.approuve_par = request.user.employe
            demande.date_traitement = timezone.now()
            demande.commentaire_rh = commentaire_rh
            demande.save()  # ← ENREGISTRÉ EN BASE ! ✅
```

---

### 3️⃣ L'EMPLOYÉ VOIT LA RÉPONSE

**Page : `/planning/mes-demandes/`**

```
┌─────────────────────────────────────────┐
│  👤 EMPLOYÉ (Sarah)                     │
│                                         │
│  1. Retourne sur "Mes Demandes"         │
│                                         │
│  2. Voit sa demande mise à jour :       │
│                                         │
│     📋 Demande #123                     │
│     Type: Congé payé                    │
│     Du 25/10 au 25/10                   │
│     Statut: ✅ APPROUVÉ                 │
│                                         │
│     💬 Commentaire RH:                  │
│     "Approuvé. Bon repos!"              │
│                                         │
│     Traité par: M. Dupont (RH)          │
│     Le: 20/10/2025 15:30                │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📊 TOUTES LES DONNÉES VONT EN BASE DE DONNÉES !

### Table `CarrefourApp_demandeconge`

| id | employe_id | type_conge | date_debut | date_fin | motif | statut | approuve_par_id | date_traitement | commentaire_rh |
|----|------------|------------|------------|----------|-------|---------|-----------------|-----------------|----------------|
| 1 | 5 (Sarah) | CONGE_PAYE | 2025-10-25 | 2025-10-25 | Rendez-vous médical | APPROUVE | 2 (RH) | 2025-10-20 15:30 | Approuvé. Bon repos! |
| 2 | 7 (Marc) | RTT | 2025-10-28 | 2025-10-29 | Récup heures sup | EN_ATTENTE | NULL | NULL | NULL |

### Table `CarrefourApp_planning`

| id | employe_id | date | poste | creneau | statut | heures_prevues |
|----|------------|------|-------|---------|---------|----------------|
| 1 | 5 (Sarah) | 2025-10-20 | CAISSE | MATIN | PRESENT | 8.0 |
| 2 | 5 (Sarah) | 2025-10-21 | CAISSE | MATIN | PRESENT | 8.0 |
| 3 | 5 (Sarah) | 2025-10-25 | CAISSE | MATIN | CONGE | 0.0 |

### Table `CarrefourApp_absence`

| id | employe_id | date | type_absence | justifiee | commentaire |
|----|------------|------|--------------|-----------|-------------|
| 1 | 7 (Marc) | 2025-10-15 | MALADIE | True | Certificat médical fourni |
| 2 | 5 (Sarah) | 2025-10-10 | RETARD | False | Retard 15min |

---

## ✅ CONFIRMATION : TOUT EST EN BASE DE DONNÉES

### 1. Demandes de congés ✅
- Stockées dans : `CarrefourApp_demandeconge`
- Champs : employe, type_conge, dates, motif, statut, approuve_par, etc.

### 2. Plannings ✅
- Stockés dans : `CarrefourApp_planning`
- Champs : employe, date, poste, creneau, heures, statut

### 3. Absences ✅
- Stockées dans : `CarrefourApp_absence`
- Champs : employe, date, type_absence, justifiee, commentaire

### 4. Pointages ✅
- Stockés dans : `CarrefourApp_pointage`
- Champs : employe, date, heure_entree, heure_sortie, heures_travaillees

### 5. Notifications ✅
- Stockées dans : `CarrefourApp_notification`
- Champs : destinataire, titre, message, type, lue

---

## 🔍 POUR VÉRIFIER EN BASE DE DONNÉES

### Ouvrir le shell Django :
```bash
python manage.py shell
```

### Voir toutes les demandes :
```python
from CarrefourApp.models import DemandeConge

# Voir toutes les demandes
for demande in DemandeConge.objects.all():
    print(f"{demande.employe.first_name} - {demande.type_conge} - {demande.statut}")
```

### Voir les demandes d'un employé :
```python
from CarrefourApp.models import Employe, DemandeConge

# Employé Sarah
sarah = Employe.objects.get(username='sarah.kouadio')

# Ses demandes
for demande in sarah.demandes_conge.all():
    print(f"{demande.date_debut} au {demande.date_fin} - {demande.statut}")
```

---

## 🎯 RÉSUMÉ

### L'EMPLOYÉ dans SON espace :
1. ✅ Voit son planning personnel
2. ✅ Fait une demande de congé (ENREGISTRÉE EN BASE)
3. ✅ Voit ses demandes et leur statut
4. ✅ Change son mot de passe

### LE RH dans SON espace :
1. ✅ Voit TOUTES les demandes
2. ✅ Approuve ou Rejette (MISE À JOUR EN BASE)
3. ✅ Enregistre les absences (SAUVEGARDÉ EN BASE)
4. ✅ Réinitialise les mots de passe

### TOUT EST EN BASE DE DONNÉES ✅
- DemandeConge (demandes de congés)
- Planning (plannings)
- Absence (absences)
- Pointage (pointages)
- Notification (notifications)

**RIEN n'est perdu ! Tout est persistant !** 🎉
