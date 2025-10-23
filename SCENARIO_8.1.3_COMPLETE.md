# ✅ SCÉNARIO 8.1.3 - GESTION DU PLANNING ET DES CONGÉS

## 📋 RÉSUMÉ D'IMPLÉMENTATION

### ✨ Fonctionnalités Implémentées

#### 🧑‍💼 **ESPACE EMPLOYÉ**

1. **📅 Mon Planning** (`/planning/mon-planning/`)
   - Consultation du planning de la semaine
   - Statistiques personnelles (heures travaillées, shifts)
   - Historique des demandes de congés en attente
   - Liste des absences enregistrées
   - Actions rapides (demander congé, changer MDP)

2. **✉️ Demander un Congé** (`/planning/demander-conge/`)
   - Formulaire de demande avec validation
   - Types de congés : Congé payé, Maladie, RTT, Maternité, Paternité
   - Sélection de dates (du/au)
   - Champ motif optionnel
   - Envoi direct au service RH

3. **📄 Mes Demandes** (`/planning/mes-demandes/`)
   - Historique complet des demandes
   - Statuts : En attente ⏳ / Approuvé ✅ / Rejeté ❌
   - Détails de chaque demande (motif, commentaire RH)
   - Modal avec informations complètes

4. **🔒 Changer mon Mot de Passe** (`/planning/changer-mot-de-passe/`)
   - Formulaire sécurisé
   - Vérification de l'ancien mot de passe
   - Validation de la correspondance des nouveaux MDP
   - Minimum 6 caractères
   - Conseils de sécurité

#### 👔 **ESPACE RH/MANAGER**

5. **📋 Gestion des Demandes de Congés** (`/rh/demandes-conges/`)
   - Vue d'ensemble des demandes (statistiques)
   - Filtres par statut (En attente / Approuvées / Rejetées)
   - Détails de chaque demande
   - **Actions :**
     - ✅ Approuver avec commentaire
     - ❌ Rejeter avec motif
   - Mise à jour automatique du statut

6. **📊 Gestion des Absences** (`/rh/gestion-absences/`)
   - Enregistrement manuel des absences
   - Types : Maladie, Congé, Absence injustifiée, Retard
   - Marquage "Justifiée" / "Non justifiée"
   - Commentaire (certificat médical, etc.)
   - Liste des 50 dernières absences

7. **🔐 Réinitialiser Mot de Passe** (`/rh/reinitialiser-mdp/`)
   - Sélection de l'employé dans la liste
   - Générateur de mot de passe aléatoire
   - MDP temporaire par défaut : "Carrefour2025"
   - Conseils de sécurité
   - L'employé peut changer son MDP après connexion

---

## 📊 MODÈLES DE DONNÉES CRÉÉS

### 1. **Planning**
```python
class Planning(models.Model):
    employe = ForeignKey(Employe)
    date = DateField()
    poste = CharField(CAISSE, RAYON, MAGASIN, SECURITE, RECEPTION, SERVICE_CLIENT)
    creneau = CharField(MATIN, APRES_MIDI, NUIT)
    statut = CharField(PRESENT, CONGE, ARRET_MALADIE, ABSENT)
    heures_prevues = DecimalField()
    heures_reelles = DecimalField()
    notes = TextField()
```

### 2. **DemandeConge**
```python
class DemandeConge(models.Model):
    employe = ForeignKey(Employe)
    type_conge = CharField(CONGE_PAYE, CONGE_MALADIE, RTT, MATERNITE, PATERNITE)
    date_debut = DateField()
    date_fin = DateField()
    nb_jours = IntegerField() # Calcul automatique des jours ouvrés
    motif = TextField()
    statut = CharField(EN_ATTENTE, APPROUVE, REFUSE)
    reponse_manager = TextField()
    approuve_par = ForeignKey(Employe)
    date_reponse = DateTimeField()
```

### 3. **Absence**
```python
class Absence(models.Model):
    employe = ForeignKey(Employe)
    date = DateField()
    type_absence = CharField(MALADIE, CONGE, ABSENCE_INJUSTIFIEE, RETARD, AUTRE)
    justifiee = BooleanField()
    commentaire = TextField()
```

### 4. **Notification** (Préparé pour future utilisation)
```python
class Notification(models.Model):
    destinataire = ForeignKey(Employe)
    titre = CharField()
    message = TextField()
    type_notif = CharField(DEMANDE_CONGE, REPONSE_CONGE, PLANNING_MAJ, etc.)
    lue = BooleanField()
    lien = CharField()
```

### 5. **Pointage** (Préparé pour future utilisation)
```python
class Pointage(models.Model):
    employe = ForeignKey(Employe)
    date = DateField()
    heure_entree = TimeField()
    heure_sortie = TimeField()
    heures_travaillees = DecimalField() # Calcul automatique
    type_journee = CharField(NORMAL, SUPPLEMENTAIRE, NUIT, FERIE)
    retard_minutes = IntegerField() # Calcul automatique
    validee = BooleanField()
```

---

## 🔄 WORKFLOW COMPLET

### Scénario : Sarah demande un congé

```
1. SARAH (Employée)
   ├─> Se connecte à son espace
   ├─> Consulte son planning (/planning/mon-planning/)
   ├─> Clique "Demander un Congé"
   ├─> Remplit le formulaire :
   │    - Type : Congé payé
   │    - Du : 24/10/2025
   │    - Au : 24/10/2025
   │    - Motif : "Rendez-vous médical"
   ├─> Soumet la demande
   └─> Statut : ⏳ EN_ATTENTE

2. SYSTÈME
   ├─> Crée DemandeConge dans la BDD
   ├─> Calcule nb_jours automatiquement (jours ouvrés)
   └─> [Future] Envoie notification au RH

3. RESPONSABLE RH
   ├─> Se connecte à son espace
   ├─> Va sur "Gestion Demandes de Congés" (/rh/demandes-conges/)
   ├─> Voit la demande de Sarah avec badge [⏳ En attente]
   ├─> Clique "Traiter"
   ├─> Vérifie :
   │    - Période demandée
   │    - Disponibilité de l'équipe
   │    - Solde de congés restants
   ├─> Option A : APPROUVE
   │    - Ajoute commentaire : "Approuvé. Bon repos!"
   │    - Soumet
   └─> Option B : REJETE
        - Ajoute motif : "Inventaire prévu ce jour"
        - Soumet

4. SYSTÈME (après validation RH)
   ├─> Met à jour le statut de la demande
   ├─> Enregistre :
   │    - approuve_par = RH
   │    - date_reponse = maintenant
   │    - reponse_manager = commentaire
   ├─> [Future] Envoie notification à Sarah
   └─> [Future] Si APPROUVE : Met à jour Planning

5. SARAH (après réponse)
   ├─> Se reconnecte
   ├─> Va sur "Mes Demandes" (/planning/mes-demandes/)
   ├─> Voit le statut :
   │    ✅ APPROUVE → Badge vert + commentaire RH
   │    ❌ REFUSE → Badge rouge + motif
   └─> Consulte son planning mis à jour
```

---

## 🎯 FONCTIONNALITÉS AVANCÉES IMPLÉMENTÉES

### 🔢 **Calculs Automatiques**

1. **Nombre de jours ouvrés** (dans DemandeConge.save())
   - Calcule automatiquement les jours Lundi-Vendredi
   - Exclut les week-ends
   - Sauvegarde dans `nb_jours`

2. **Heures travaillées** (dans Pointage.save())
   - Calcule la différence entre heure_sortie et heure_entree
   - Gère le passage minuit (shifts de nuit)
   - Arrondi à 2 décimales

3. **Retard en minutes** (dans Pointage.save())
   - Compare heure_entree réelle vs heure_prevue
   - Calcule les minutes de retard
   - Sauvegarde dans `retard_minutes`

### 🎨 **Interface Utilisateur**

- **Design** : Bootstrap 5, responsive
- **Icônes** : Émojis pour meilleure lisibilité
- **Badges de statut** :
  - ⏳ Jaune → En attente
  - ✅ Vert → Approuvé
  - ❌ Rouge → Rejeté
- **Cartes statistiques** :
  - Nombre coloré + label
  - Vue d'ensemble rapide
- **Modals** : Détails complets sans quitter la page
- **Formulaires** : Validation HTML5 + JavaScript

### 🔒 **Sécurité & Permissions**

1. **Accès Employé** :
   - Voit uniquement SON planning
   - Peut demander des congés
   - Peut changer SON mot de passe

2. **Accès RH/Manager** :
   - Voit TOUTES les demandes
   - Peut approuver/rejeter
   - Peut enregistrer absences
   - Peut réinitialiser MDP de n'importe qui

3. **Vérifications** :
   - `@login_required` sur toutes les vues
   - Vérification du rôle (`request.user.role`)
   - Redirection si non autorisé

---

## 📦 FICHIERS CRÉÉS

### **Backend (views.py)** - +300 lignes
- `mon_planning()` - Consultation planning employé
- `demander_conge()` - Formulaire demande congé
- `mes_demandes_conges()` - Historique demandes
- `changer_mot_de_passe()` - Modification MDP
- `rh_demandes_conges()` - Gestion demandes (RH)
- `rh_traiter_demande()` - Approuver/Rejeter
- `rh_gestion_absences()` - Enregistrement absences
- `rh_reinitialiser_mdp()` - Reset MDP employé

### **Frontend (templates/planning/)** - 8 fichiers
1. `mon_planning.html` - Dashboard employé (200 lignes)
2. `demander_conge.html` - Formulaire demande (80 lignes)
3. `mes_demandes.html` - Historique avec modals (150 lignes)
4. `changer_mot_de_passe.html` - Formulaire sécurisé (100 lignes)
5. `rh_demandes_conges.html` - Gestion RH (200 lignes)
6. `rh_gestion_absences.html` - Enregistrement absences (150 lignes)
7. `rh_reinitialiser_mdp.html` - Reset MDP (180 lignes)

### **Configuration (urls.py)** - 8 nouvelles routes
```python
# Espace Employé
path('planning/mon-planning/', mon_planning)
path('planning/demander-conge/', demander_conge)
path('planning/mes-demandes/', mes_demandes_conges)
path('planning/changer-mot-de-passe/', changer_mot_de_passe)

# Espace RH
path('rh/demandes-conges/', rh_demandes_conges)
path('rh/traiter-demande/<int:demande_id>/', rh_traiter_demande)
path('rh/gestion-absences/', rh_gestion_absences)
path('rh/reinitialiser-mdp/', rh_reinitialiser_mdp)
```

### **Scripts Utilitaires**
- `create_planning_data.py` - Générateur de données de test
  - 96 plannings sur 2 semaines
  - 16 demandes de congés (8 en attente, 8 approuvées)
  - 24 absences (16 justifiées, 8 non justifiées)

---

## 🧪 DONNÉES DE TEST CRÉÉES

### Employés (8 actifs)
- KONAN ROMUALD (STOCK)
- YOYO L'empereur (CAISSIER)
- KONE ISSOUF (CAISSIER)
- Directeur Général (DG)
- Directeur Financier (DAF)
- Responsable RH (RH)
- ... et autres

### Plannings (96 total)
- 2 semaines de planning
- Postes : CAISSE, RAYON, RECEPTION, SERVICE_CLIENT
- Créneaux : MATIN (6h-14h), APRES_MIDI (14h-22h)
- 8 heures par shift

### Demandes de Congés (16 total)
- **8 EN_ATTENTE** → À traiter par RH
- **8 APPROUVE** → Déjà validées
- Types variés : Congé payé, Maladie, RTT

### Absences (24 total)
- **16 justifiées** → Certificat médical fourni
- **8 non justifiées** → Sans justification

---

## 🔗 URLS DE TEST

### 🧑 **Pour les Employés :**
```
Mon Planning         : http://127.0.0.1:8000/planning/mon-planning/
Demander un Congé    : http://127.0.0.1:8000/planning/demander-conge/
Mes Demandes         : http://127.0.0.1:8000/planning/mes-demandes/
Changer Mon MDP      : http://127.0.0.1:8000/planning/changer-mot-de-passe/
```

### 👔 **Pour RH/Managers :**
```
Demandes de Congés   : http://127.0.0.1:8000/rh/demandes-conges/
Gestion Absences     : http://127.0.0.1:8000/rh/gestion-absences/
Réinitialiser MDP    : http://127.0.0.1:8000/rh/reinitialiser-mdp/
```

---

## 📈 STATISTIQUES DU CODE

| Composant | Quantité | Lignes de Code |
|-----------|----------|----------------|
| **Modèles** | 5 | ~400 lignes |
| **Vues** | 8 | ~300 lignes |
| **Templates** | 7 | ~1,100 lignes |
| **URLs** | 8 routes | ~20 lignes |
| **Migrations** | 2 fichiers | Auto-générées |
| **Scripts** | 1 | ~200 lignes |
| **TOTAL** | | **~2,020 lignes** |

---

## ✅ CHECKLIST DE VALIDATION

### Backend ✅
- [x] Modèles créés et migrés
- [x] Vues pour employés implémentées
- [x] Vues pour RH implémentées
- [x] Calculs automatiques (jours ouvrés, heures, retards)
- [x] Permissions et sécurité
- [x] Gestion des erreurs

### Frontend ✅
- [x] Templates responsives
- [x] Formulaires avec validation
- [x] Modals pour détails
- [x] Badges de statut
- [x] Cartes statistiques
- [x] Design cohérent

### Configuration ✅
- [x] URLs configurées
- [x] Models enregistrés dans admin.py
- [x] Migrations appliquées
- [x] Données de test générées

### Documentation ✅
- [x] Plan détaillé (SCENARIO_8.1.3_PLAN.md)
- [x] Document de complétion (ce fichier)
- [x] Commentaires dans le code
- [x] Script de test documenté

---

## 🚀 PROCHAINES ÉTAPES (Optionnel)

### Améliorations Possibles

1. **Système de Notifications**
   - Notifications en temps réel
   - Badge avec compteur non lus
   - Email automatique pour demandes/réponses

2. **Planning Visuel**
   - Vue calendrier graphique
   - Drag & drop pour réorganiser
   - Export PDF/Excel

3. **Pointage Avancé**
   - QR Code / Badge RFID
   - Application mobile
   - Géolocalisation

4. **Analytics RH**
   - Taux d'absentéisme
   - Prédictions besoins en personnel
   - Rapports mensuels automatiques

5. **Validation Automatique**
   - Règles métier (min caissiers, max absences)
   - Alertes sous-effectif
   - Suggestions de remplacement

---

## 🎓 COMPÉTENCES DÉMONTRÉES

### Django
- ✅ Modèles avec relations complexes
- ✅ Vues fonctionnelles avec permissions
- ✅ Formulaires avec validation
- ✅ Calculs automatiques dans save()
- ✅ Gestion des sessions utilisateur

### Base de Données
- ✅ Relations ForeignKey
- ✅ Contraintes unique_together
- ✅ Agrégations (Sum, Count)
- ✅ Filtres complexes
- ✅ Migrations Django

### Frontend
- ✅ Bootstrap 5 responsive
- ✅ JavaScript (validation, modals)
- ✅ Template Django (boucles, conditions)
- ✅ UX/UI moderne
- ✅ Formulaires interactifs

### Architecture
- ✅ Séparation Employé/RH
- ✅ Workflow complet
- ✅ Calculs métier
- ✅ Sécurité & permissions
- ✅ Documentation exhaustive

---

## 📞 SUPPORT

Pour toute question ou problème :
1. Consultez les commentaires dans le code
2. Référez-vous à `SCENARIO_8.1.3_PLAN.md`
3. Utilisez `create_planning_data.py` pour réinitialiser les données
4. Vérifiez les logs Django pour les erreurs

---

**✅ Scénario 8.1.3 TERMINÉ ET FONCTIONNEL !**

*Document créé le 20 Octobre 2025*
*Projet : CARREFOUR - Gestion Planning & Congés*
