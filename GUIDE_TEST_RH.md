# 🧪 GUIDE DE TEST - NOUVELLES FONCTIONNALITÉS RH

## 🎯 ÉTAPES DE TEST

### ✅ TEST 1: Interface Moderne des Employés

**URL:** `http://127.0.0.1:8000/dashboard/rh/employees/`

**1. Connexion**
```
Username: rh
Password: RH2025@Admin
```

**2. Vérifications:**
- [ ] La page affiche des **cartes** pour chaque employé (pas un tableau)
- [ ] Chaque carte montre:
  - [ ] Avatar avec initiales (ex: "KZ" pour Kolo ZK)
  - [ ] Nom complet
  - [ ] ID employé (ex: EMP018)
  - [ ] Badge coloré du département
  - [ ] Poste/rôle
  - [ ] Email et téléphone
  - [ ] Date d'embauche
  - [ ] Dernière connexion avec indicateur coloré
  - [ ] Boutons Modifier et Supprimer

**3. Test des Statistiques (en haut):**
- [ ] Voir "Total Employés"
- [ ] Voir "Actifs"
- [ ] Voir "Connectés Aujourd'hui"
- [ ] Voir "Départements"

**4. Test des Filtres:**
- [ ] Sélectionner "Finance" dans le filtre département
  - Résultat: Voir uniquement le DAF
- [ ] Sélectionner "Ventes" dans le filtre département
  - Résultat: Voir les caissiers
- [ ] Sélectionner "Logistique" dans le filtre département
  - Résultat: Voir les gestionnaires de stock
- [ ] Changer pour "Tous les départements"
  - Résultat: Voir tous les employés

**5. Test Vue Alternative:**
- [ ] Cliquer sur "📋 Vue Tableau"
  - Résultat: Voir l'interface classique en tableau

---

### ✅ TEST 2: Historique des Présences

**URL:** `http://127.0.0.1:8000/dashboard/rh/historique-presences/`

**1. Test Onglet "Aujourd'hui":**
- [ ] Cliquer sur "📅 Aujourd'hui"
- [ ] Vérifier les statistiques:
  - [ ] Nombre de présents (vert)
  - [ ] Nombre d'absents (rouge)
  - [ ] Nombre de retards (orange)
  - [ ] Taux de présence (bleu)
- [ ] Vérifier le tableau des présences du jour

**2. Test Onglet "Cette Semaine":**
- [ ] Cliquer sur "📆 Cette Semaine"
- [ ] Vérifier que le tableau montre les présences de lundi à aujourd'hui
- [ ] Vérifier les heures d'arrivée et de départ
- [ ] Vérifier le temps travaillé

**3. Test Onglet "Ce Mois":**
- [ ] Cliquer sur "📊 Ce Mois"
- [ ] Vérifier que le **calendrier** s'affiche
- [ ] Voir les jours avec présences (vert)
- [ ] Voir les jours avec absences (rouge)
- [ ] Tester navigation:
  - [ ] Cliquer "⬅ Mois Précédent"
  - [ ] Cliquer "Aujourd'hui"
  - [ ] Cliquer "Mois Suivant ➡"

**4. Test Filtres:**
- [ ] Sélectionner un employé spécifique
  - Résultat: Voir uniquement ses présences
- [ ] Sélectionner un département
  - Résultat: Voir présences de tout le département
- [ ] Sélectionner des dates personnalisées
  - Résultat: Voir présences entre ces dates

**5. Test Export Excel:**
- [ ] Cliquer sur "📊 Exporter en Excel"
- [ ] Vérifier qu'un fichier `.xlsx` est téléchargé
- [ ] Ouvrir le fichier Excel
- [ ] Vérifier que toutes les données sont présentes

**6. Test Export PDF:**
- [ ] Cliquer sur "📄 Exporter en PDF"
- [ ] Vérifier que l'aperçu d'impression s'ouvre
- [ ] Vérifier que la mise en page est correcte

---

### ✅ TEST 3: Correction des Départements

**Exécuter le script:**
```bash
python corriger_departements.py
```

**Vérifications:**
- [ ] Le script s'exécute sans erreur
- [ ] Voir le nombre de corrections effectuées
- [ ] Voir la répartition par département
- [ ] Vérifier que:
  - [ ] DG est dans "Direction Générale"
  - [ ] DAF est dans "Finance"
  - [ ] RH est dans "Ressources Humaines"
  - [ ] Gestionnaires Stock dans "Logistique"
  - [ ] Caissiers dans "Ventes"
  - [ ] Marketing dans "Marketing"

**Vérifier dans l'interface:**
- [ ] Retourner sur `/dashboard/rh/employees/`
- [ ] Vérifier que les badges de département sont corrects
- [ ] Filtrer par département et vérifier la cohérence

---

### ✅ TEST 4: Dernières Connexions

**Préparation:**
1. Se déconnecter du compte RH
2. Se connecter avec un compte employé (ex: caissier)
3. Se déconnecter
4. Se reconnecter avec RH

**Vérifications:**
- [ ] Aller sur `/dashboard/rh/employees/`
- [ ] Trouver la carte de l'employé qui vient de se connecter
- [ ] Vérifier l'indicateur de connexion:
  - [ ] 🟢 Vert si connexion < 1h
  - [ ] 🔵 Bleu si connexion aujourd'hui
  - [ ] 🟠 Orange si connexion cette semaine
  - [ ] ⚫ Gris si connexion ancienne
- [ ] Vérifier le texte "Il y a X minutes/heures"

---

### ✅ TEST 5: Avatars et Photos

**Test avec initiales (par défaut):**
- [ ] Voir que chaque carte affiche les initiales de l'employé
- [ ] Ex: "KZ" pour "Kolo ZK"
- [ ] Vérifier que le fond est bleu dégradé

**Test avec photo (si disponible):**
- [ ] Si un employé a une photo, elle s'affiche
- [ ] La photo est circulaire avec bordure

---

## 📊 SCÉNARIOS D'UTILISATION RÉELS

### Scénario 1: Trouver tous les employés de Finance
```
1. Aller sur /dashboard/rh/employees/
2. Filtre département: "Finance"
3. Voir le DAF et autres comptables
```

### Scénario 2: Voir qui était présent hier
```
1. Aller sur /dashboard/rh/historique-presences/
2. Onglet: "Cette Semaine"
3. Regarder la ligne avec la date d'hier
4. Voir les statuts (Présent/Absent/Retard)
```

### Scénario 3: Générer rapport mensuel pour Direction
```
1. Aller sur /dashboard/rh/historique-presences/
2. Onglet: "Ce Mois"
3. Optionnel: Filtrer par département si besoin
4. Cliquer "Exporter en Excel"
5. Envoyer le fichier à la direction
```

### Scénario 4: Identifier les employés qui ne se sont pas connectés depuis longtemps
```
1. Aller sur /dashboard/rh/employees/
2. Regarder les indicateurs de connexion
3. Chercher les ⚫ gris (anciennes connexions)
4. Contacter ces employés si nécessaire
```

### Scénario 5: Vérifier les retards du mois
```
1. Aller sur /dashboard/rh/historique-presences/
2. Onglet: "Ce Mois"
3. Regarder la statistique "⏰ Retards"
4. Dans le tableau, filtrer pour voir qui
5. Prendre des mesures si nécessaire
```

---

## 🐛 PROBLÈMES POSSIBLES ET SOLUTIONS

### Problème 1: "Module 'openpyxl' not found"
**Solution:**
```bash
pip install openpyxl
```

### Problème 2: Les statistiques sont à zéro
**Cause:** Pas de données de présence
**Solution:** 
- Créer des présences test
- Ou attendre que les employés se connectent

### Problème 3: Les photos ne s'affichent pas
**Cause:** Pas de photos uploadées
**Normal:** Le système affiche les initiales par défaut
**Pour ajouter des photos:**
1. Aller sur "Modifier" un employé
2. Uploader une photo
3. Sauvegarder

### Problème 4: Tous les employés sont encore dans "Ventes"
**Solution:**
```bash
python corriger_departements.py
```

### Problème 5: L'export Excel ne télécharge pas
**Vérification:**
- Vérifier que openpyxl est installé
- Vérifier qu'il y a des données à exporter
- Essayer avec une période différente

---

## ✅ CHECKLIST FINALE

### Interface Moderne
- [ ] Vue cartes fonctionnelle
- [ ] Avatars/initiales visibles
- [ ] Badges département colorés
- [ ] Dernières connexions affichées
- [ ] Statistiques correctes
- [ ] Filtres fonctionnels
- [ ] Passage vue cartes ↔ tableau

### Historique Présences
- [ ] 4 onglets fonctionnent
- [ ] Statistiques correctes
- [ ] Tableau de données complet
- [ ] Filtres fonctionnels
- [ ] Vue calendrier (mois)
- [ ] Export Excel OK
- [ ] Export PDF OK

### Départements
- [ ] Script de correction fonctionne
- [ ] Départements correctement assignés
- [ ] Cohérence rôle ↔ département
- [ ] Répartition équilibrée

---

## 📝 RAPPORT DE TEST

**Date du test:** ____________________

**Testeur:** ____________________

### Résultats

| Fonctionnalité | Status | Commentaires |
|----------------|--------|--------------|
| Interface moderne employés | ⬜ OK ⬜ KO | |
| Statistiques temps réel | ⬜ OK ⬜ KO | |
| Filtres avancés | ⬜ OK ⬜ KO | |
| Dernières connexions | ⬜ OK ⬜ KO | |
| Historique présences - Jour | ⬜ OK ⬜ KO | |
| Historique présences - Semaine | ⬜ OK ⬜ KO | |
| Historique présences - Mois | ⬜ OK ⬜ KO | |
| Vue calendrier | ⬜ OK ⬜ KO | |
| Export Excel | ⬜ OK ⬜ KO | |
| Export PDF | ⬜ OK ⬜ KO | |
| Correction départements | ⬜ OK ⬜ KO | |

### Bugs identifiés
1. ____________________________________________________
2. ____________________________________________________
3. ____________________________________________________

### Suggestions d'amélioration
1. ____________________________________________________
2. ____________________________________________________
3. ____________________________________________________

---

**✅ Tests complétés avec succès !**

*Guide créé le 20 octobre 2025*
