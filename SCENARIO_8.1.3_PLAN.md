# 📋 SCÉNARIO 8.1.3 : GESTION DU PLANNING ET DES CONGÉS

## 📖 CAHIER DES CHARGES

### Contexte
Sarah, employée de caisse, doit pouvoir :
- Consulter son planning de travail en temps réel
- Voir ses affectations (poste, créneau horaire)
- Faire une demande de congé
- Recevoir des notifications sur l'état de sa demande

Le responsable doit pouvoir :
- Visualiser le planning global de l'équipe
- Recevoir les demandes de congé
- Approuver ou refuser avec commentaire
- Vérifier les disponibilités avant validation
- Voir les heures travaillées et performances

### Fonctionnalités Requises

#### 1. **Planning des Employés**
- ✅ Vue calendrier hebdomadaire/mensuelle
- ✅ Affichage par employé et par poste
- ✅ Créneaux horaires : Matin (6h-14h), Après-midi (14h-22h), Nuit (22h-6h)
- ✅ Postes : Caisse, Rayon, Magasin, Sécurité, etc.
- ✅ Codes couleurs par statut (Présent, Congé, Arrêt maladie, Absent)

#### 2. **Gestion des Absences**
- ✅ Types : Congé payé, Congé maladie, RTT, Absence non justifiée
- ✅ Workflow : Demande → En attente → Approuvée/Refusée
- ✅ Calcul automatique des jours restants
- ✅ Historique des demandes

#### 3. **Suivi des Heures**
- ✅ Pointage entrée/sortie
- ✅ Calcul heures travaillées par jour/semaine/mois
- ✅ Heures supplémentaires
- ✅ Retards et absences

#### 4. **Notifications**
- ✅ Notification au manager : Nouvelle demande de congé
- ✅ Notification à l'employé : Demande approuvée/refusée
- ✅ Notification à l'équipe : Mise à jour du planning
- ✅ Badge sur l'interface avec compteur

## 🗂️ STRUCTURE DE DONNÉES

### Modèles Django Nécessaires

#### 1. **Planning**
```python
class Planning(models.Model):
    employe = ForeignKey(Employe)
    date = DateField()
    poste = CharField(choices=POSTES)  # CAISSE, RAYON, MAGASIN, SECURITE
    creneau = CharField(choices=CRENEAUX)  # MATIN, APRES_MIDI, NUIT
    statut = CharField(choices=STATUTS)  # PRESENT, CONGE, ARRET_MALADIE, ABSENT
    heures_prevues = DecimalField()
    heures_reelles = DecimalField(null=True)
    cree_le = DateTimeField(auto_now_add=True)
```

#### 2. **DemandeConge**
```python
class DemandeConge(models.Model):
    employe = ForeignKey(Employe)
    type_conge = CharField(choices=TYPES_CONGE)  # CONGE_PAYE, MALADIE, RTT
    date_debut = DateField()
    date_fin = DateField()
    nb_jours = IntegerField()
    motif = TextField()
    statut = CharField(choices=STATUTS)  # EN_ATTENTE, APPROUVE, REFUSE
    reponse_manager = TextField(null=True)
    approuve_par = ForeignKey(Employe, null=True)
    date_reponse = DateTimeField(null=True)
    cree_le = DateTimeField(auto_now_add=True)
```

#### 3. **Pointage**
```python
class Pointage(models.Model):
    employe = ForeignKey(Employe)
    date = DateField()
    heure_entree = TimeField()
    heure_sortie = TimeField(null=True)
    heures_travaillees = DecimalField()
    type_journee = CharField()  # NORMAL, SUPPLEMENTAIRE, NUIT
    validee = BooleanField(default=False)
```

#### 4. **Notification**
```python
class Notification(models.Model):
    destinataire = ForeignKey(User)
    titre = CharField()
    message = TextField()
    type_notif = CharField()  # DEMANDE_CONGE, REPONSE_CONGE, PLANNING_MAJ
    lue = BooleanField(default=False)
    lien = CharField(null=True)
    cree_le = DateTimeField(auto_now_add=True)
```

## 🎨 INTERFACES À CRÉER

### 1. **Page Planning Employé** (`/planning/mon-planning/`)
```
┌─────────────────────────────────────────────────────┐
│  📅 MON PLANNING - Sarah Kouadio                    │
│  [← Semaine Précédente]  Sem. 43 (21-27 Oct)  [→]  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Lun 21  │ Mar 22  │ Mer 23  │ Jeu 24  │ Ven 25   │
│  🌅 MATIN│ 🌅 MATIN│ 🌅 MATIN│ 🌅 MATIN│ 🌅 MATIN  │
│  CAISSE  │ CAISSE  │ CAISSE  │ CAISSE  │ CAISSE   │
│  6h-14h  │ 6h-14h  │ 6h-14h  │ 6h-14h  │ 6h-14h   │
│                                                     │
│  [🏖️ Demander un Congé]  [⏰ Mes Pointages]        │
├─────────────────────────────────────────────────────┤
│  📊 Statistiques du Mois                            │
│  ✅ Jours travaillés : 18                           │
│  ⏱️ Heures totales : 144h                           │
│  🏖️ Congés restants : 15 jours                      │
└─────────────────────────────────────────────────────┘
```

### 2. **Formulaire Demande Congé** (`/planning/demander-conge/`)
```
┌─────────────────────────────────────────────────────┐
│  🏖️ NOUVELLE DEMANDE DE CONGÉ                       │
├─────────────────────────────────────────────────────┤
│  Type de congé : [Congé payé ▼]                     │
│  Date début    : [📅 25/10/2025]                    │
│  Date fin      : [📅 25/10/2025]                    │
│  Nb jours      : 1 jour (calculé auto)              │
│  Motif         : [Raisons personnelles...]          │
│                                                     │
│  [❌ Annuler]  [✅ Envoyer la Demande]              │
└─────────────────────────────────────────────────────┘
```

### 3. **Page Planning Manager** (`/planning/equipe/`)
```
┌─────────────────────────────────────────────────────┐
│  📅 PLANNING ÉQUIPE - Semaine 43                    │
│  [Filtre Poste: Tous ▼]  [🔔 3 demandes en attente]│
├─────────────────────────────────────────────────────┤
│  Employé      │ Lun  │ Mar  │ Mer  │ Jeu  │ Ven    │
│  Sarah K.     │ 🌅 C │ 🌅 C │ 🌅 C │ 🏖️   │ 🌅 C   │
│  Marc D.      │ 🌆 R │ 🌆 R │ 🌆 R │ 🌆 R │ 🌆 R   │
│  Julie M.     │ 🌅 C │ 🌅 C │ 🌅 C │ 🌅 C │ 🌅 C   │
│                                                     │
│  C=Caisse, R=Rayon, 🌅=Matin, 🌆=Après-midi, 🏖️=Congé│
├─────────────────────────────────────────────────────┤
│  [➕ Créer Planning]  [📊 Rapport Heures]           │
└─────────────────────────────────────────────────────┘
```

### 4. **Gestion Demandes Congé** (`/planning/demandes-conge/`)
```
┌─────────────────────────────────────────────────────┐
│  🏖️ DEMANDES DE CONGÉ                               │
│  [En attente] [Approuvées] [Refusées] [Toutes]     │
├─────────────────────────────────────────────────────┤
│  🔔 Sarah Kouadio - Congé payé                      │
│     Du 25/10 au 25/10 (1 jour)                      │
│     Motif: Raisons personnelles                     │
│     [✅ Approuver]  [❌ Refuser]  [👁️ Détails]       │
├─────────────────────────────────────────────────────┤
│  ⏳ Marc Diallo - RTT                               │
│     Du 28/10 au 29/10 (2 jours)                     │
│     Motif: Récupération heures sup                  │
│     [✅ Approuver]  [❌ Refuser]  [👁️ Détails]       │
└─────────────────────────────────────────────────────┘
```

### 5. **Page Pointage** (`/planning/pointage/`)
```
┌─────────────────────────────────────────────────────┐
│  ⏰ POINTAGE - Sarah Kouadio                        │
├─────────────────────────────────────────────────────┤
│  📅 Aujourd'hui : Lundi 20 Octobre 2025             │
│  🌅 Créneau : MATIN (6h00 - 14h00)                  │
│                                                     │
│  Heure d'arrivée : 06:05                            │
│  [🟢 Pointer la Sortie]                             │
├─────────────────────────────────────────────────────┤
│  📊 Historique                                      │
│  Lun 20 Oct : 06:05 - --:--  (En cours)            │
│  Ven 17 Oct : 06:00 - 14:10  (8h10)                │
│  Jeu 16 Oct : 06:10 - 14:05  (7h55) ⚠️ Retard      │
└─────────────────────────────────────────────────────┘
```

## 🔄 WORKFLOW

### Demande de Congé
```
1. EMPLOYÉ
   └─> Consulte planning
   └─> Clique "Demander Congé"
   └─> Remplit formulaire (dates, motif)
   └─> Soumet demande
   └─> Statut: EN_ATTENTE

2. SYSTÈME
   └─> Crée DemandeConge
   └─> Envoie notification au MANAGER
   └─> Badge [🔔 1] apparaît

3. MANAGER
   └─> Reçoit notification
   └─> Consulte demande
   └─> Vérifie disponibilités équipe
   └─> Approuve ou Refuse avec commentaire
   
4. SYSTÈME
   └─> Met à jour statut demande
   └─> Si APPROUVÉE: Modifie planning
   └─> Envoie notification à l'employé
   └─> Envoie notification à l'équipe

5. EMPLOYÉ
   └─> Reçoit notification
   └─> Voit planning mis à jour
```

## 📊 CALCULS AUTOMATIQUES

### 1. Nombre de jours ouvrés
```python
def calculer_jours_ouvres(date_debut, date_fin):
    nb_jours = 0
    date_courante = date_debut
    while date_courante <= date_fin:
        if date_courante.weekday() < 5:  # Lun-Ven
            nb_jours += 1
        date_courante += timedelta(days=1)
    return nb_jours
```

### 2. Solde de congés
```python
def calculer_solde_conges(employe):
    conges_acquis = 2.5 * (mois_travailles)  # 2.5 jours/mois
    conges_pris = DemandeConge.objects.filter(
        employe=employe, 
        statut='APPROUVE',
        type_conge='CONGE_PAYE'
    ).aggregate(Sum('nb_jours'))['nb_jours__sum'] or 0
    return conges_acquis - conges_pris
```

### 3. Heures travaillées
```python
def calculer_heures_travaillees(pointages):
    total = 0
    for p in pointages:
        if p.heure_sortie:
            delta = datetime.combine(date.today(), p.heure_sortie) - \
                    datetime.combine(date.today(), p.heure_entree)
            total += delta.total_seconds() / 3600
    return total
```

## 🎯 FONCTIONNALITÉS AVANCÉES

### 1. Vérification Disponibilités
Avant d'approuver un congé, vérifier :
- Minimum 2 caissiers par créneau
- Pas plus de 30% de l'équipe absente
- Compétences nécessaires couvertes

### 2. Notifications Intelligentes
- Badge avec compteur non lus
- Groupe par type (Demandes, Réponses, Mises à jour)
- Marquer comme lue automatiquement après consultation
- Son ou popup pour notifications urgentes

### 3. Statistiques
- Taux d'absentéisme par employé
- Heures supplémentaires
- Retards récurrents
- Prévisions besoins en personnel

## 📝 PLAN D'IMPLÉMENTATION

### Phase 1 : Modèles et Migrations ✅
- [ ] Créer modèle Planning
- [ ] Créer modèle DemandeConge
- [ ] Créer modèle Pointage
- [ ] Créer modèle Notification
- [ ] Faire migrations

### Phase 2 : Vues Employé ✅
- [ ] Vue planning personnel
- [ ] Formulaire demande congé
- [ ] Page pointage
- [ ] Liste mes demandes
- [ ] Centre notifications

### Phase 3 : Vues Manager ✅
- [ ] Planning équipe (calendrier)
- [ ] Gestion demandes congé
- [ ] Rapport heures travaillées
- [ ] Création/modification planning
- [ ] Validation pointages

### Phase 4 : Système Notifications ✅
- [ ] Fonction création notification
- [ ] Badge compteur dans navbar
- [ ] Page liste notifications
- [ ] Marquer comme lu/non lu
- [ ] Notifications temps réel (optionnel)

### Phase 5 : URLs et Templates ✅
- [ ] 8 vues backend
- [ ] 8 templates HTML
- [ ] 8 routes URLs
- [ ] JavaScript pour interactions

## 🧪 SCÉNARIOS DE TEST

### Test 1 : Demande Congé Simple
```
1. Sarah se connecte (role: CAISSIER)
2. Va sur "Mon Planning"
3. Clique "Demander un Congé"
4. Sélectionne : Congé payé, 25/10/2025, 1 jour
5. Motif : "Raisons personnelles"
6. Soumet → Statut EN_ATTENTE
7. Manager reçoit notification [🔔 1]
```

### Test 2 : Approbation Manager
```
1. Manager se connecte
2. Voit badge [🔔 1 nouvelle demande]
3. Clique sur notification
4. Vérifie planning équipe du 25/10
5. Constate : 3 caissiers dispo (OK)
6. Approuve avec message : "Approuvé. Bon repos!"
7. Sarah reçoit notification
8. Planning mis à jour automatiquement
```

### Test 3 : Refus avec Raison
```
1. Marc demande congé 28-29/10 (2 jours)
2. Manager vérifie → Inventaire prévu
3. Refuse avec message : "Désolé, inventaire en cours"
4. Marc reçoit notification de refus
5. Planning inchangé
```

### Test 4 : Pointage Quotidien
```
1. Sarah arrive à 06:05
2. Pointe entrée → Enregistré
3. Travaille toute la matinée
4. À 14:10, pointe sortie
5. Système calcule : 8h05 travaillées
6. Enregistre dans historique
```

## 📦 RÉSULTATS ATTENDUS

### Pour l'Employé
- ✅ Vision claire de son planning
- ✅ Processus simple de demande de congé
- ✅ Suivi de ses heures travaillées
- ✅ Notifications en temps réel
- ✅ Historique de ses demandes

### Pour le Manager
- ✅ Vue d'ensemble de l'équipe
- ✅ Gestion centralisée des absences
- ✅ Validation rapide avec vérifications automatiques
- ✅ Rapports de performances
- ✅ Alertes sur sous-effectifs

### Pour le Système
- ✅ Planning toujours à jour
- ✅ Traçabilité complète
- ✅ Réduction emails/appels
- ✅ Base de données pour paie
- ✅ Prévisions RH facilitées

---

**Prêt à commencer l'implémentation ?** 🚀
