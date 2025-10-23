# 🎫 GUIDE D'UTILISATION - COUPONS AUTOMATIQUES

## ✅ CE QUI A ÉTÉ IMPLÉMENTÉ

### **1. APPLICATION AUTOMATIQUE DES COUPONS**

Le système applique **automatiquement** les coupons selon ces règles :

#### **🔄 Coupons GÉNÉRIQUES (GENERIC)**
✅ S'appliquent **automatiquement** si toutes les conditions sont remplies :
- Coupon actif (statut = ACTIF)
- Dans la période de validité (date début ≤ aujourd'hui ≤ date fin)
- Montant d'achat ≥ montant minimum requis
- Client a le niveau de fidélité requis (si spécifié)
- Limite d'utilisation non atteinte

🎯 **Le système choisit automatiquement le coupon le PLUS AVANTAGEUX** (valeur la plus élevée)

#### **📋 Coupons SPÉCIAUX (SPECIAL)**
✅ S'affichent dans la liste des coupons disponibles
✅ Sont marqués comme "Personnel"
⚠️ Actuellement appliqués automatiquement si toutes les conditions sont remplies
💡 Peut être modifié pour nécessiter une confirmation manuelle

---

## 🖥️ AFFICHAGE DANS L'INTERFACE CAISSE

### **Zone 1 : Liste des coupons disponibles** (panneau jaune 🎫)

**Emplacement :** Sous la section "Client Fidélité" (panneau de gauche)

**Affichage pour chaque coupon :**
```
🎫 Coupons Disponibles
┌─────────────────────────────────────────┐
│ GEN7K4M2P         ✓ APPLIQUÉ            │
│ Promotion Fête Nationale                │
│ -10%                     -7 500 FCFA    │
└─────────────────────────────────────────┘
│ SPE9X2K4L                   Personnel   │
│ Bon anniversaire Marie !                │
│ -25%                    -18 750 FCFA    │
└─────────────────────────────────────────┘
```

**Légende :**
- ✅ Badge vert "APPLIQUÉ" = Coupon actif, remise déjà calculée
- 🔵 Badge bleu "Personnel" = Coupon SPECIAL réservé à ce client
- 💰 Montant en vert = Remise calculée en temps réel

### **Zone 2 : Détail des remises** (tableau récapitulatif)

**Emplacement :** Dans le panneau de droite, section "Totaux"

**Affichage :**
```
┌──────────────────────────────────────────┐
│ Sous-total:              75 000 FCFA    │
│ Remise Client (5%):      -3 750 FCFA    │ ← Fidélité automatique
│ Remise Promo (5%):       -3 563 FCFA    │ ← Si ≥ 40 000 FCFA
│ 🎫 Coupon: GEN7K4M2P                     │ ← NOUVEAU !
│    Promotion Fête Nationale              │
│                          -7 500 FCFA    │
│ ────────────────────────────────────────│
│ Total Remises:          -14 813 FCFA    │
│ TVA (18%):              +10 834 FCFA    │
│ ════════════════════════════════════════│
│ MONTANT FINAL:           71 021 FCFA    │ ← Avec toutes les remises
└──────────────────────────────────────────┘
```

---

## 🧪 COMMENT TESTER LE SYSTÈME

### **ÉTAPE 1 : Créer des coupons de test**

#### **Coupon 1 : Générique de 10% sans condition**
```
Page : Marketing → Coupons & Promotions → Créer un coupon

Code : (laisser vide → auto-généré)
Description : Test coupon 10%
Type de coupon : GENERIC
Type de remise : POURCENTAGE
Valeur : 10
Date début : 2025-10-20
Date fin : 2025-12-31
Montant minimum : 1000
Niveau fidélité requis : (aucun)
Limite globale : (vide = illimité)
Client spécifique : (aucun)

→ Cliquer sur "Enregistrer"
→ Noter le code généré (ex: GEN7K4M2P)
```

#### **Coupon 2 : Générique de 20 000 FCFA pour achats ≥ 100 000 FCFA**
```
Code : MEGA-PROMO
Description : Super réduction 20 000 F
Type de coupon : GENERIC
Type de remise : MONTANT_FIXE
Valeur : 20000
Date début : 2025-10-20
Date fin : 2025-12-31
Montant minimum : 100000
Niveau fidélité requis : (aucun)
```

#### **Coupon 3 : Spécial VIP de 25%**
```
Code : VIP-SPECIAL
Description : Offre réservée VIP
Type de coupon : GENERIC
Type de remise : POURCENTAGE
Valeur : 25
Date début : 2025-10-20
Date fin : 2025-12-31
Montant minimum : 50000
Niveau fidélité requis : VIP
```

#### **Coupon 4 : Personnel pour un client spécifique**
```
Code : (laisser vide)
Description : Bon anniversaire !
Type de coupon : SPECIAL
Type de remise : POURCENTAGE
Valeur : 15
Date début : 2025-10-20
Date fin : 2025-12-31
Montant minimum : 5000
Niveau fidélité requis : (aucun)
Client spécifique : (choisir un client existant)
```

---

### **ÉTAPE 2 : Tester en caisse**

#### **Test 1 : Coupon générique appliqué automatiquement**

1. **Aller à la caisse**
   - Menu : Caisse → Vente

2. **Ajouter des produits pour 15 000 FCFA**
   - Exemple : 10x Eau minérale à 1 500 FCFA

3. **Observer l'affichage :**
   - ✅ Panneau "🎫 Coupons Disponibles" apparaît
   - ✅ Coupon "Test coupon 10%" avec badge "✓ APPLIQUÉ"
   - ✅ Montant : -1 500 FCFA affiché

4. **Vérifier le récapitulatif :**
   ```
   Sous-total:           15 000 FCFA
   🎫 Coupon: GEN7K4M2P
      Test coupon 10%    -1 500 FCFA
   TVA (18%):            +2 430 FCFA
   ──────────────────────────────────
   MONTANT FINAL:        15 930 FCFA
   ```

5. **Valider la vente**
   - Choisir un moyen de paiement
   - Vérifier que la remise est bien appliquée

---

#### **Test 2 : Cumul fidélité + coupon**

1. **Identifier un client GOLD (5% de remise)**
   - Saisir le téléphone d'un client GOLD

2. **Ajouter des produits pour 50 000 FCFA**

3. **Observer l'affichage :**
   ```
   Sous-total:              50 000 FCFA
   Remise Client (5%):      -2 500 FCFA  ← Fidélité
   Remise Promo (5%):       -2 375 FCFA  ← ≥ 40 000 F
   🎫 Coupon: GEN7K4M2P
      Test coupon 10%       -5 000 FCFA  ← Coupon
   ────────────────────────────────────
   Total Remises:           -9 875 FCFA
   TVA (18%):               +7 223 FCFA
   ════════════════════════════════════
   MONTANT FINAL:           47 348 FCFA
   ```

4. **Points à gagner :** +47 points (47 348 / 1000)

---

#### **Test 3 : Coupon VIP non applicable**

1. **Identifier un client SILVER ou GOLD**
   - Pas de niveau VIP

2. **Ajouter des produits pour 60 000 FCFA**

3. **Observer :**
   - ❌ Coupon "VIP-SPECIAL" n'apparaît PAS
   - ✅ Seuls les coupons applicables s'affichent

---

#### **Test 4 : Montant minimum non atteint**

1. **Ajouter des produits pour 80 000 FCFA**
   - Moins que 100 000 FCFA

2. **Observer :**
   - ✅ Coupon "Test coupon 10%" appliqué (-8 000 F)
   - ❌ Coupon "MEGA-PROMO" (20 000 F) non affiché
   - Raison : Montant minimum 100 000 F pas atteint

3. **Ajouter plus de produits pour atteindre 105 000 FCFA**

4. **Observer :**
   - ✅ Maintenant coupon "MEGA-PROMO" apparaît ET est appliqué
   - ✅ Remise de -20 000 FCFA visible
   - 💡 Le système choisit le meilleur (20 000 > 10 500)

---

#### **Test 5 : Coupon personnel**

1. **Identifier le client spécifique** (celui assigné au coupon SPECIAL)

2. **Ajouter des produits pour 10 000 FCFA**

3. **Observer :**
   - ✅ Panneau "🎫 Coupons Disponibles" affiche 2 coupons :
     - Coupon générique 10% (✓ APPLIQUÉ)
     - Coupon personnel 15% (🔵 Personnel)

4. **Résultat actuel :**
   - Les deux coupons s'affichent
   - Le générique est appliqué automatiquement
   - Le spécial est visible mais pas appliqué (car moins avantageux)

---

### **ÉTAPE 3 : Vérifier l'enregistrement**

#### **Dans l'interface Marketing**

1. **Aller à : Marketing → Coupons → Liste des coupons**

2. **Cliquer sur un coupon utilisé**

3. **Vérifier :**
   - Nombre d'utilisations : devrait être ≥ 1
   - Statut : Reste ACTIF (sauf si limite atteinte)

4. **Aller à : Marketing → Coupons → Rapport d'utilisation**

5. **Voir :**
   - Date d'utilisation
   - Client associé
   - Montant de la remise
   - Numéro de transaction/vente

---

### **ÉTAPE 4 : Vérifier dans la base de données**

```sql
-- Voir les coupons créés
SELECT id, code, description, type_coupon, type_remise, valeur, statut, nb_utilisations
FROM CarrefourApp_coupon
WHERE statut = 'ACTIF'
ORDER BY date_creation DESC;

-- Voir les utilisations de coupons
SELECT 
    c.code,
    c.description,
    cl.nom || ' ' || cl.prenom as client,
    uc.montant_remise,
    uc.date_utilisation,
    v.numero_transaction
FROM CarrefourApp_utilisationcoupon uc
JOIN CarrefourApp_coupon c ON uc.coupon_id = c.id
LEFT JOIN CarrefourApp_client cl ON uc.client_id = cl.id
LEFT JOIN CarrefourApp_vente v ON uc.vente_id = v.id
ORDER BY uc.date_utilisation DESC;

-- Vérifier le total des remises accordées aujourd'hui
SELECT 
    DATE(date_utilisation) as jour,
    COUNT(*) as nb_utilisations,
    SUM(montant_remise) as total_remises
FROM CarrefourApp_utilisationcoupon
WHERE DATE(date_utilisation) = DATE('now')
GROUP BY DATE(date_utilisation);
```

---

## 📊 LOGS DANS LA CONSOLE

Lors de la validation d'une vente avec coupon, vous verrez :

```
🎫 COUPON APPLIQUÉ: GEN7K4M2P - Remise: 5000.00 FCFA
👤 ASSOCIATION CLIENT - ID: 12
   ✅ Client associé: Marie KOUADIO (ID: 12)
   ✅ Dernière visite mise à jour
📦 MISE À JOUR DU STOCK - Transaction TKT20251023015
   ✅ Eau Minérale 1.5L: 350 → 340 (10 vendus)
📦 STOCK MIS À JOUR pour 1 produits
🎫 UTILISATION COUPON ENREGISTRÉE: GEN7K4M2P
👤 DONNÉES CLIENT MISES À JOUR: Marie KOUADIO - 17 achats
```

---

## 🎯 COMPORTEMENT ATTENDU

### **Scénario 1 : Panier vide**
- ❌ Aucun coupon affiché
- Raison : Pas de montant à calculer

### **Scénario 2 : Panier avec produits, pas de client**
- ✅ Coupons GÉNÉRIQUES sans condition de client affichés
- ❌ Coupons nécessitant un niveau de fidélité non affichés
- ❌ Coupons SPÉCIAUX non affichés

### **Scénario 3 : Client SILVER + Panier 30 000 F**
- ✅ Remise fidélité 3% : -900 F
- ✅ Coupon générique 10% appliqué : -3 000 F
- ❌ Coupon VIP 25% non affiché (niveau insuffisant)
- ✅ Total remises : -3 900 F

### **Scénario 4 : Client VIP + Panier 120 000 F**
- ✅ Remise fidélité 10% : -12 000 F
- ✅ Remise promo 5% : -5 400 F (calculée après fidélité)
- ✅ Coupon MEGA-PROMO 20 000 F appliqué
- ✅ Total remises : -37 400 F
- 💰 Économie massive visible !

### **Scénario 5 : Plusieurs coupons éligibles**
- ✅ Tous les coupons éligibles s'affichent
- ✅ Le PLUS AVANTAGEUX est appliqué automatiquement
- 🔢 Comparaison : 10% de 50 000 = 5 000 F vs 20 000 F fixe
- 🎯 Résultat : 20 000 F appliqué (meilleur)

---

## ⚙️ PERSONNALISATIONS POSSIBLES

### **Option 1 : Appliquer tous les coupons éligibles (cumul)**

**Modifier dans `views.py` ligne ~3920 :**
```python
# AVANT (un seul coupon)
if coupon.type_coupon == 'GENERIC' and coupon_applique is None:
    coupon_applique = coupon
    remise_coupon = remise_calculee
    coupons_disponibles[-1]['est_applique'] = True

# APRÈS (tous les coupons)
if coupon.type_coupon == 'GENERIC':
    remise_coupon += remise_calculee
    coupons_disponibles[-1]['est_applique'] = True
```

### **Option 2 : Forcer la sélection manuelle des coupons SPECIAL**

**Modifier dans `views.py` ligne ~3920 :**
```python
# Ne pas appliquer automatiquement les SPECIAL
if coupon.type_coupon == 'GENERIC' and coupon_applique is None:
    coupon_applique = coupon
    remise_coupon = remise_calculee
    coupons_disponibles[-1]['est_applique'] = True
# Les SPECIAL resteront visibles mais pas appliqués
```

### **Option 3 : Limiter à 1 coupon par transaction**

**Ajouter après la ligne `if est_valide:` :**
```python
if est_valide and coupon_applique is None:  # Prendre seulement le premier
    remise_coupon = remise_calculee
    coupon_applique = coupon
    coupons_disponibles[-1]['est_applique'] = True
    break  # Sortir de la boucle
```

---

## 🚀 PROCHAINES AMÉLIORATIONS POSSIBLES

1. **Saisie manuelle de code coupon**
   - Ajouter un champ texte dans l'interface
   - Bouton "Appliquer ce coupon"
   - Permet d'utiliser des codes communiqués par SMS/email

2. **Notification client**
   - Afficher un popup : "Vous avez un coupon de 15% disponible !"
   - Proposer de l'appliquer

3. **Génération automatique**
   - Créer un coupon d'anniversaire automatiquement
   - Créer un coupon de bienvenue pour nouveaux clients

4. **Historique client**
   - Afficher les coupons déjà utilisés par le client
   - Proposer des coupons similaires

5. **QR Code**
   - Générer un QR code pour chaque coupon
   - Scanner le QR code en caisse

---

## 📞 SUPPORT

**Problème : Les coupons ne s'affichent pas**
→ Vérifier que :
- Le coupon a le statut ACTIF
- La date du jour est entre date_début et date_fin
- Le montant du panier ≥ montant_minimum
- Le client a le niveau requis (si spécifié)

**Problème : Le coupon est affiché mais pas appliqué**
→ Vérifier dans le code :
- Ligne ~3920 dans `views.py`
- Condition `if coupon.type_coupon == 'GENERIC' and coupon_applique is None:`

**Problème : Plusieurs coupons mais seul le dernier est appliqué**
→ C'est le comportement actuel (prendre le PLUS AVANTAGEUX)
→ Voir Option 1 pour appliquer tous les coupons

---

**Document créé le : 23 octobre 2025**  
**Version : 2.0 - Application automatique**  
**Auteur : Assistant GitHub Copilot**
