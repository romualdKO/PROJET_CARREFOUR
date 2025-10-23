# 🧪 Guide de Test - Scénario 8.1.1 : Gestion Commandes Fournisseurs

## 📋 Vue d'ensemble du Scénario

**Contexte :** Le responsable des stocks reçoit une alerte indiquant que le stock de "Farine T45 1kg" est critique (50 unités restantes, seuil : 100 unités).

**Objectif :** Commander automatiquement 500 unités auprès du fournisseur "Moulin de Côte d'Ivoire" avec gestion complète du workflow.

---

## ✅ Étapes de Test

### 1️⃣ **Vérification de l'Alerte Stock** ⚠️

**URL :** `http://127.0.0.1:8000/dashboard/stock/`

**Actions :**
- ✅ Connectez-vous avec un compte STOCK/ADMIN/MANAGER
- ✅ Vérifiez que le dashboard affiche :
  - **Valeur Stock (FCFA)** : Doit maintenant afficher une valeur (ex: 2,450,000 FCFA)
  - **Stock Critique** : Doit afficher au moins 1 produit
- ✅ Dans la section "⚠️ Alertes Stock Critique", vérifiez :
  - Produit : "Farine T45 1kg"
  - Stock actuel : 50 unités
  - Seuil critique : 100 unités
  - Alerte rouge visible

**Résultat attendu :**
```
⚠️ Alertes Stock Critique
┌─────────────────────────┐
│ Farine T45 1kg          │
│ Stock: 50 unités        │ [ROUGE]
└─────────────────────────┘
```

---

### 2️⃣ **Accès à la Création de Commande** ➕

**URL :** Cliquer sur "➕ Nouvelle Commande Fournisseur"

**Interface attendue :**

**Colonne gauche : Produits critiques**
```
⚠️ Produits à Réapprovisionner (1)
┌──────────────────────────────────────┐
│ 🔴 Farine T45 1kg                    │
│ Stock: 50 / Seuil: 100               │
│ 💡 Recommandé: 500 unités            │
│ 📦 Moulin de CI | ⏱️ Délai: 3 jours  │
│                [Sélectionner →]      │
└──────────────────────────────────────┘
```

**Colonne droite : Formulaire**
- Champ "🏢 Fournisseur" : Liste déroulante
- Champ "📦 Produit" : Liste déroulante
- Champ "📊 Quantité" : Input numérique
- Card "MONTANT ESTIMÉ" : Calcul automatique
- Card "LIVRAISON PRÉVUE" : Date + délai

---

### 3️⃣ **Sélection Automatique** 🎯

**Action :** Cliquer sur le bouton "Sélectionner →" pour Farine T45

**Résultat attendu :**
- ✅ Fournisseur auto-rempli : "Moulin de Côte d'Ivoire"
- ✅ Produit auto-sélectionné : "Farine T45 1kg"
- ✅ Quantité pré-remplie : 500
- ✅ Info fournisseur affichée : "📅 Livraison estimée: [DATE] (dans 3 jours)"
- ✅ Alerte produit : "⚠️ ALERTE! Stock bas (50/100). Réapprovisionnement recommandé."
- ✅ Calcul automatique :
  ```
  Prix unitaire: 1,200 FCFA
  500 unités × 1,200 FCFA = 600,000 FCFA
  ```

---

### 4️⃣ **Création de la Commande** 📝

**Action :** Cliquer sur "✅ Créer la Commande"

**Résultat attendu :**
- ✅ Redirection vers `/commandes-fournisseurs/`
- ✅ Message de succès :
  ```
  ✅ Commande créée! 500 unités de Farine T45 1kg commandées 
  auprès de Moulin de Côte d'Ivoire. 
  Livraison prévue le [DATE].
  ```
- ✅ Nouvelle commande visible dans le tableau avec :
  - Statut : **EN_ATTENTE** (badge jaune 🟡)
  - Fournisseur : Moulin de Côte d'Ivoire
  - Montant : 600,000 FCFA
  - Livraison prévue : [DATE]

---

### 5️⃣ **Validation de la Commande** ✅

**URL :** `/commandes-fournisseurs/`

**Action :** Cliquer sur le bouton "✅ Valider" pour la commande créée

**Résultat attendu :**
- ✅ Message : "✅ Commande #[ID] validée! Envoyée au fournisseur Moulin de Côte d'Ivoire."
- ✅ Statut change : **EN_ATTENTE** → **VALIDEE** (badge bleu 🔵)
- ✅ Bouton "✅ Valider" disparaît
- ✅ Nouveau bouton apparaît : "📦 Recevoir"

**KPIs attendus :**
```
Total: X commandes
En Attente: (X-1) commandes
Validées: 1 commande ← DOIT AUGMENTER
Livrées: Y commandes
```

---

### 6️⃣ **Réception de la Commande** 📦

**Action :** Cliquer sur "📦 Recevoir"

**Résultat attendu :**
- ✅ Message : "✅ Commande #[ID] reçue! Stocks mis à jour automatiquement."
- ✅ Statut change : **VALIDEE** → **LIVREE** (badge vert 🟢)
- ✅ Date livraison réelle enregistrée

---

### 7️⃣ **Vérification Mise à Jour Stock** 🔄

**URL :** Retour sur `http://127.0.0.1:8000/dashboard/stock/`

**Vérifications :**

1. **Stock Farine T45** :
   - ✅ Ancien stock : 50 unités
   - ✅ Nouveau stock : **550 unités** (50 + 500)
   - ✅ Statut : **EN_STOCK** (badge vert)
   - ✅ L'alerte rouge a disparu

2. **KPI "Stock Critique"** :
   - ✅ Doit diminuer de 1 (Farine T45 n'est plus critique)

3. **Alertes Stock** :
   - ✅ Section "⚠️ Alertes Stock Critique" ne contient plus Farine T45

4. **Mouvements Stock** :
   - ✅ Nouveau mouvement enregistré :
     ```
     Type: ENTREE (+500)
     Produit: Farine T45 1kg
     Motif: Réception commande #[ID]
     Date: [DATE]
     ```

---

## 🔍 Points de Contrôle Critiques

### ✅ Tests Fonctionnels

| Test | Attendu | Vérifié |
|------|---------|---------|
| **Affichage Valeur Stock** | Nombre formaté (ex: 2,450,000 FCFA) | [ ] |
| **Détection Stock Critique** | Farine T45 alertée (50/100) | [ ] |
| **Calcul Quantité Recommandée** | 500 unités basé sur historique | [ ] |
| **Sélection Automatique** | Formulaire pré-rempli au clic | [ ] |
| **Calcul Montant Total** | 500 × 1,200 = 600,000 FCFA | [ ] |
| **Calcul Date Livraison** | Aujourd'hui + 3 jours | [ ] |
| **Changement Statut (Valider)** | EN_ATTENTE → VALIDEE | [ ] |
| **Changement Statut (Recevoir)** | VALIDEE → LIVREE | [ ] |
| **Mise à Jour Stock** | 50 → 550 unités | [ ] |
| **Résolution Alerte** | Alerte marquée "résolue" | [ ] |
| **Enregistrement Mouvement** | ENTREE +500 créé | [ ] |

---

## 🎯 Flux Complet du Scénario 8.1.1

```
┌─────────────────────────────────────────────────────────┐
│ 1. ALERTE DÉTECTÉE                                      │
│    Stock Farine T45: 50 unités < Seuil: 100            │
│    ⚠️ Dashboard affiche alerte rouge                    │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 2. RECOMMANDATION INTELLIGENTE                          │
│    Analyse historique ventes → Recommande 500 unités   │
│    Fournisseur suggéré: Moulin de CI (délai: 3j)       │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 3. CRÉATION COMMANDE                                     │
│    Clic "Sélectionner" → Formulaire pré-rempli         │
│    Validation → Commande #X créée (EN_ATTENTE)         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 4. VALIDATION AUTOMATIQUE                                │
│    Clic "Valider" → Statut: VALIDEE                    │
│    Envoi automatique au fournisseur                     │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 5. RÉCEPTION & MISE À JOUR                              │
│    Clic "Recevoir" → Statut: LIVREE                    │
│    Stock: 50 → 550 unités                              │
│    MouvementStock créé (+500)                           │
│    Alerte résolue automatiquement                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🐛 Tests de Régression

### Cas Limite à Tester

1. **Produit sans fournisseur** :
   - Affiche "⚠️ Aucun fournisseur défini"
   - Impossible de commander

2. **Quantité invalide** :
   - Saisir 0 ou nombre négatif
   - Doit afficher erreur validation HTML5

3. **Multiple produits critiques** :
   - Créer 3 alertes
   - Vérifier que les 3 apparaissent dans la liste

4. **Calculs dynamiques** :
   - Changer quantité → Montant recalculé instantanément
   - Changer fournisseur → Date livraison recalculée

5. **Filtres** :
   - Filtrer par statut : EN_ATTENTE, VALIDEE, LIVREE
   - Filtrer par fournisseur

---

## 📊 Métriques de Succès

### Performance
- ✅ Temps chargement dashboard < 2s
- ✅ Calculs temps réel instantanés
- ✅ Aucune erreur 500

### UX
- ✅ Interface intuitive (1 clic = produit sélectionné)
- ✅ Messages de feedback clairs
- ✅ Badges colorés (statuts visuels)

### Business Logic
- ✅ Recommandations basées sur données historiques
- ✅ Stocks jamais négatifs
- ✅ Alertes résolues automatiquement
- ✅ Traçabilité complète (MouvementStock)

---

## 🚀 Commandes Utiles

### Vérifier les données
```bash
python manage.py shell
```
```python
from CarrefourApp.models import *

# Vérifier alerte Farine T45
alerte = AlerteStock.objects.filter(produit__nom__icontains='farine').first()
print(f"Produit: {alerte.produit.nom}")
print(f"Stock: {alerte.produit.stock_actuel}")
print(f"Seuil: {alerte.produit.seuil_reapprovisionnement}")

# Vérifier commande créée
commande = CommandeFournisseur.objects.latest('id')
print(f"Fournisseur: {commande.fournisseur.nom}")
print(f"Statut: {commande.statut}")
print(f"Montant: {commande.montant_total()} FCFA")

# Vérifier stock après livraison
farine = Produit.objects.get(nom__icontains='farine t45')
print(f"Nouveau stock: {farine.stock_actuel}")
```

---

## 📝 Notes

- **Bug Fix 1** : Valeur stock n'apparaissait pas → Corrigé (valeur_stock → valeur_stock_vente)
- **Implémentation** : Workflow complet en 4 vues + 1 template création + 1 template liste
- **Automatisations** : Calcul quantité recommandée, date livraison, mise à jour stocks, résolution alertes

---

## ✅ Checklist Finale

Avant de considérer le scénario comme TERMINÉ :

- [ ] Valeur stock affichée correctement
- [ ] Alerte Farine T45 visible (rouge)
- [ ] Boutons "Nouvelle Commande" et "Voir Commandes" fonctionnels
- [ ] Formulaire pré-rempli au clic "Sélectionner"
- [ ] Calculs automatiques (montant, date) corrects
- [ ] Commande créée avec statut EN_ATTENTE
- [ ] Validation → Statut VALIDEE
- [ ] Réception → Stock mis à jour + Statut LIVREE
- [ ] Alerte disparue du dashboard
- [ ] MouvementStock enregistré

**Date du test :** _______________  
**Testeur :** _______________  
**Résultat :** ⬜ PASS | ⬜ FAIL

---

🎉 **Succès du Scénario 8.1.1 !** 🎉

Le système gère maintenant l'intégralité du workflow de réapprovisionnement :
- Détection automatique des stocks critiques
- Recommandations intelligentes basées sur l'historique
- Gestion complète du cycle de vie des commandes
- Mise à jour automatique des stocks
- Résolution automatique des alertes
