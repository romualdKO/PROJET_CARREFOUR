# 📋 SCÉNARIO 8.1.2 - GESTION DES CAISSES

## 🎯 Objectif
Créer un système de caisse complet avec gestion automatique des remises fidélité, promotions et rapport de ventes journalier.

---

## 📝 Cahier des Charges

### Scénario Détaillé
> Une cliente achète plusieurs produits et passe en caisse. L'application gère automatiquement les remises associées à sa carte de fidélité. Après avoir scanné ses articles, l'application propose une remise immédiate de 5% sur son total pour atteindre un seuil promotionnel fixé (exemple : 100€ d'achat minimum pour une remise). À la fin de la journée, l'application génère automatiquement un rapport des ventes pour le manager.

### Fonctionnalités Requises

1. **Interface Caisse**
   - Scanner/Ajouter produits
   - Affichage panier en temps réel
   - Calcul automatique du total
   - Identification client (carte fidélité)

2. **Gestion Remises Automatiques**
   - Remise fidélité selon niveau client (VIP/GOLD/SILVER)
   - Remise promotionnelle 5% si montant ≥ seuil (100€ = 40,000 FCFA)
   - Cumul remises

3. **Finalisation Vente**
   - Choix moyen paiement (Espèces, Carte, Mobile Money)
   - Génération ticket de caisse
   - Mise à jour stock automatique
   - Attribution points fidélité

4. **Rapport Journalier**
   - Nombre de transactions
   - Somme totale des ventes
   - Articles les plus vendus
   - Répartition moyens de paiement
   - Remises accordées
   - CA par caissier

---

## 🗂️ Données Nécessaires

### ✅ Modèles Existants
- ✅ `Vente` - Transactions
- ✅ `LigneVente` - Détails articles
- ✅ `Client` - Clients avec fidélité
- ✅ `Produit` - Articles en stock
- ✅ `Promotion` - Promotions actives
- ✅ `Employe` - Caissiers

### 📊 Structure Vente
```python
class Vente(models.Model):
    numero_transaction = CharField  # T251020001
    caissier = ForeignKey(Employe)
    client = ForeignKey(Client, null=True)  # Optionnel
    montant_total = DecimalField       # Avant remises
    montant_tva = DecimalField
    remise = DecimalField              # Total remises
    montant_final = DecimalField       # Après remises
    moyen_paiement = CharField         # ESPECES/CARTE/MOBILE
    date_vente = DateTimeField
    caisse_numero = CharField          # #01, #02...
```

### 📊 Structure Client
```python
class Client(models.Model):
    numero_client = CharField
    nom, prenom = CharField
    telephone = CharField (unique)
    points_fidelite = IntegerField
    niveau_fidelite = CharField  # VIP/GOLD/SILVER/TOUS
```

---

## 🎨 Interface à Créer

### 1. Page Caisse (`/caisse/`)

```
┌─────────────────────────────────────────────────────────┐
│ 🛒 CAISSE #01                    Caissier: Jean KOUAME  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ [🔍 Scanner Produit (Code/Nom)]  [👤 Client Fidélité] │
│                                                         │
├──────────────────────┬──────────────────────────────────┤
│ PANIER (3 articles)  │ TOTAUX                          │
│                      │                                 │
│ 🍞 Pain de mie       │ Sous-total:    15,000 FCFA     │
│    × 2    3,000 FCFA │ Remise Client:  -750 FCFA (5%) │
│ [➖] [❌]            │ Remise Promo:    -715 FCFA (5%) │
│                      │ TVA (18%):      2,136 FCFA     │
│ 🥛 Lait 1L          │ ─────────────────────────────   │
│    × 3    6,000 FCFA │ TOTAL:        15,671 FCFA      │
│ [➖] [❌]            │                                 │
│                      │ Points gagnés: +15 pts         │
│ 🍚 Riz 5kg          │                                 │
│    × 1    6,000 FCFA │ [💰 ESPÈCES] [💳 CARTE]       │
│ [➖] [❌]            │ [📱 MOBILE MONEY]              │
│                      │                                 │
│ [🗑️ Vider Panier]    │ [✅ VALIDER VENTE]             │
└──────────────────────┴──────────────────────────────────┘
```

### 2. Rapport Journalier (`/caisse/rapport/`)

```
┌─────────────────────────────────────────────────────────┐
│ 📊 RAPPORT VENTES JOURNALIER - 20/10/2025              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 💰 CA Total:        1,250,000 FCFA                     │
│ 🛒 Transactions:    47 ventes                          │
│ 📊 Panier moyen:    26,595 FCFA                        │
│ 💸 Remises:         -62,500 FCFA                       │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ TOP 5 PRODUITS VENDUS                                  │
│ 1. Riz 5kg          × 23    138,000 FCFA              │
│ 2. Huile 1L         × 18     90,000 FCFA              │
│ 3. Lait Nido        × 15     75,000 FCFA              │
│ 4. Pain de mie      × 12     18,000 FCFA              │
│ 5. Farine T45       × 10     12,000 FCFA              │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ MOYENS DE PAIEMENT                                      │
│ 💰 Espèces:         625,000 FCFA (50%)                │
│ 💳 Carte:           437,500 FCFA (35%)                │
│ 📱 Mobile Money:    187,500 FCFA (15%)                │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ CAISSIERS                                               │
│ Jean KOUAME    15 ventes    375,000 FCFA              │
│ Marie DIALLO   20 ventes    500,000 FCFA              │
│ Paul TRAORE    12 ventes    375,000 FCFA              │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Implémentation

### Fichiers à Créer/Modifier

1. **CarrefourApp/views.py**
   - `caisse_vente()` - Interface caisse
   - `caisse_ajouter_produit()` - AJAX ajouter au panier
   - `caisse_retirer_produit()` - AJAX retirer du panier
   - `caisse_identifier_client()` - AJAX charger client
   - `caisse_calculer_totaux()` - AJAX recalculer remises
   - `caisse_valider_vente()` - Finaliser transaction
   - `caisse_rapport_journalier()` - Rapport du jour

2. **templates/caisse/**
   - `index.html` - Interface caisse
   - `rapport_journalier.html` - Rapport ventes

3. **CarrefourApp/urls.py**
   - Routes caisse

4. **static/js/caisse.js** (optionnel)
   - Logique AJAX panier temps réel

---

## 📐 Logique Métier

### Calcul Remises

```python
def calculer_remises(montant_total, client=None):
    remises = {
        'fidelite': 0,
        'promotionnelle': 0,
        'total': 0
    }
    
    # 1. Remise fidélité
    if client:
        if client.niveau_fidelite == 'VIP':
            remises['fidelite'] = montant_total * 0.10  # 10%
        elif client.niveau_fidelite == 'GOLD':
            remises['fidelite'] = montant_total * 0.05  # 5%
        elif client.niveau_fidelite == 'SILVER':
            remises['fidelite'] = montant_total * 0.03  # 3%
    
    # 2. Remise promotionnelle (5% si ≥ 40,000 FCFA)
    if montant_total >= 40000:
        remises['promotionnelle'] = montant_total * 0.05
    
    remises['total'] = remises['fidelite'] + remises['promotionnelle']
    return remises
```

### Attribution Points Fidélité

```python
def attribuer_points(client, montant_final):
    # 1 point par tranche de 1,000 FCFA
    points = int(montant_final / 1000)
    client.points_fidelite += points
    client.save()
    return points
```

### Mise à Jour Stock

```python
def mettre_a_jour_stock(lignes_vente):
    for ligne in lignes_vente:
        produit = ligne.produit
        produit.stock_actuel -= ligne.quantite
        produit.save()
        
        # Créer mouvement stock
        MouvementStock.objects.create(
            produit=produit,
            type_mouvement='SORTIE',
            quantite=-ligne.quantite,
            raison=f'Vente {ligne.vente.numero_transaction}',
            stock_avant=produit.stock_actuel + ligne.quantite,
            stock_apres=produit.stock_actuel
        )
```

---

## ✅ Checklist Implémentation

### Phase 1: Backend
- [ ] Créer vue `caisse_vente()`
- [ ] Créer vue `caisse_valider_vente()`
- [ ] Créer vue `caisse_rapport_journalier()`
- [ ] Ajouter routes dans urls.py
- [ ] Tester calculs remises
- [ ] Tester attribution points

### Phase 2: Frontend
- [ ] Créer template `caisse/index.html`
- [ ] Créer template `caisse/rapport_journalier.html`
- [ ] Ajouter styles CSS
- [ ] Ajouter JavaScript panier dynamique

### Phase 3: Tests
- [ ] Tester vente simple
- [ ] Tester vente avec client VIP
- [ ] Tester remise promotionnelle (≥40,000 FCFA)
- [ ] Tester cumul remises
- [ ] Tester attribution points
- [ ] Tester mise à jour stock
- [ ] Tester rapport journalier

---

## 🎯 Résultats Attendus

### Exemple Transaction

**Cliente:** Marie KOUAME (Niveau: VIP)  
**Panier:**
- Pain de mie × 2 = 3,000 FCFA
- Lait 1L × 3 = 6,000 FCFA
- Riz 5kg × 1 = 6,000 FCFA

**Calculs:**
```
Sous-total:         15,000 FCFA
Remise VIP (10%):   -1,500 FCFA
Total après fidélité: 13,500 FCFA

Remise promo (5%):   -675 FCFA  (car 13,500 < 40,000 → PAS DE REMISE)
TVA (18%):          +2,430 FCFA

MONTANT FINAL:      15,930 FCFA
Points gagnés:      +15 pts
```

**Cas avec remise promo:**
```
Sous-total:         50,000 FCFA
Remise VIP (10%):   -5,000 FCFA
Sous-total:         45,000 FCFA
Remise promo (5%):  -2,250 FCFA (car ≥ 40,000)
TVA (18%):          +7,695 FCFA

MONTANT FINAL:      50,445 FCFA
Points gagnés:      +50 pts
```

---

## 📊 Métriques Succès

- ✅ Temps moyen par transaction < 2 minutes
- ✅ 0 erreur calcul remises
- ✅ Stock mis à jour en temps réel
- ✅ Rapport journalier généré automatiquement
- ✅ Interface intuitive (1 formation = utilisable)

---

**Date création:** 20 Octobre 2025  
**Statut:** 📋 EN PLANIFICATION  
**Priorité:** 🔥 HAUTE
