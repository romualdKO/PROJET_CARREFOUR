# 🎟️ GUIDE COMPLET - SYSTÈME DE COUPONS ET FIDÉLISATION

## 📋 TABLE DES MATIÈRES
1. [Vue d'ensemble](#vue-densemble)
2. [Création des coupons](#création-des-coupons)
3. [Application des coupons en caisse](#application-des-coupons-en-caisse)
4. [Système de fidélisation automatique](#système-de-fidélisation-automatique)
5. [Suivi et rapports](#suivi-et-rapports)
6. [Erreurs corrigées](#erreurs-corrigées)

---

## 🎯 VUE D'ENSEMBLE

Le système de **coupons** et **fidélisation** permet de récompenser vos clients et d'augmenter leurs achats. Il existe **DEUX (2) types de remises** :

### **Type 1 : Remises automatiques de fidélité** 🏆
✅ **Appliquées automatiquement** dès qu'un client est identifié  
✅ **Basées sur le niveau du client** :
- **TOUS** (nouveau client) : 0% de remise
- **SILVER** (≥ 5 achats) : 3% de remise
- **GOLD** (≥ 15 achats) : 5% de remise
- **VIP** (≥ 30 achats) : 10% de remise

### **Type 2 : Coupons promotionnels** 🎫
✅ **Appliqués manuellement** en saisissant un code coupon  
✅ **Deux variantes** :
- **GENERIC** : Utilisable par tous les clients (ex: PROMO2025)
- **SPECIAL** : Réservé à un client spécifique (ex: ANNIV-MARIE)

---

## 🎫 CRÉATION DES COUPONS

### **Accès : Interface Marketing**
1. Connexion avec un compte **MARKETING**, **DG** ou **ADMIN**
2. Menu : **Marketing** → **Coupons & Promotions** → **Créer un coupon**

### **Formulaire de création**

#### **Champs obligatoires :**

| Champ | Description | Exemple |
|-------|-------------|---------|
| **Code** | Laissez vide = code auto-généré | GEN4X7Z9A ou SPE2K8M3L |
| **Description** | Nom du coupon | "Réduction rentrée scolaire" |
| **Type de coupon** | GENERIC ou SPECIAL | GENERIC |
| **Type de remise** | POURCENTAGE ou MONTANT_FIXE | POURCENTAGE |
| **Valeur** | Montant de la remise | 15 (= 15% ou 15 000 FCFA) |
| **Date début** | Date de début de validité | 2025-10-22 |
| **Date fin** | Date de fin de validité | 2025-12-31 |

#### **Champs optionnels :**

| Champ | Description | Exemple |
|-------|-------------|---------|
| **Montant minimum** | Achat minimum requis | 50000 (50 000 FCFA) |
| **Niveau fidélité requis** | SILVER, GOLD ou VIP | GOLD |
| **Limite globale** | Nombre max d'utilisations | 100 |
| **Client spécifique** | Si TYPE = SPECIAL | Sélectionner "AKOUA BINTOU" |

### **Exemples pratiques :**

#### 📌 **Exemple 1 : Coupon générique de 10% pour tous**
```
Code : (laissez vide → auto-généré : GEN7K4M2P)
Description : Promotion Fête Nationale
Type de coupon : GENERIC
Type de remise : POURCENTAGE
Valeur : 10
Date début : 2025-11-01
Date fin : 2025-11-07
Montant minimum : 20000
Niveau fidélité requis : (aucun)
Limite globale : 500
Client spécifique : (aucun)
```
→ **Résultat** : Tout client qui achète pour au moins 20 000 FCFA peut utiliser le code **GEN7K4M2P** pour avoir 10% de remise

#### 📌 **Exemple 2 : Coupon spécial VIP de 20 000 FCFA**
```
Code : VIP-NOEL2025
Description : Cadeau de Noël VIP
Type de coupon : GENERIC
Type de remise : MONTANT_FIXE
Valeur : 20000
Date début : 2025-12-15
Date fin : 2025-12-25
Montant minimum : 100000
Niveau fidélité requis : VIP
Limite globale : 50
Client spécifique : (aucun)
```
→ **Résultat** : Seuls les clients VIP qui achètent pour au moins 100 000 FCFA peuvent utiliser ce code

#### 📌 **Exemple 3 : Coupon personnalisé d'anniversaire**
```
Code : (laissez vide → SPE9X2K4L)
Description : Bon anniversaire Marie !
Type de coupon : SPECIAL
Type de remise : POURCENTAGE
Valeur : 25
Date début : 2025-11-05
Date fin : 2025-11-12
Montant minimum : 10000
Niveau fidélité requis : (aucun)
Limite globale : 1
Client spécifique : Marie KOUADIO
```
→ **Résultat** : Seule Marie KOUADIO peut utiliser ce code **une seule fois** pendant sa semaine d'anniversaire

---

## 💳 APPLICATION DES COUPONS EN CAISSE

### **Processus actuel (À IMPLÉMENTER)** ⚠️

Actuellement, le système de coupons **n'est PAS encore intégré dans l'interface de caisse POS**. 

**Ce qui fonctionne déjà :**
✅ Création des coupons dans l'interface Marketing  
✅ Validation automatique des règles (dates, montant minimum, niveau requis)  
✅ Calcul du montant de remise  
✅ Tracking des utilisations  

**Ce qui MANQUE (à développer) :**
❌ Champ pour saisir le code coupon dans la caisse POS  
❌ Bouton "Appliquer le coupon"  
❌ Affichage de la remise coupon en temps réel  
❌ Enregistrement de l'utilisation du coupon avec la transaction  

### **PROPOSITION : Intégration dans la caisse POS**

#### **Étape 1 : Ajouter l'interface coupon dans le template**

**Fichier à modifier :** `templates/caisse/index.html` (ou votre template POS)

**Zone à ajouter** (après la section "Client" et avant "Panier") :

```html
<!-- SECTION COUPON -->
<div class="card mb-3">
    <div class="card-header bg-success text-white">
        🎫 Coupon promotionnel
    </div>
    <div class="card-body">
        <div class="input-group">
            <input 
                type="text" 
                id="code-coupon" 
                class="form-control" 
                placeholder="Entrez le code (ex: PROMO2025)"
                maxlength="20"
            >
            <button 
                type="button" 
                id="btn-appliquer-coupon" 
                class="btn btn-success"
            >
                Appliquer
            </button>
            <button 
                type="button" 
                id="btn-retirer-coupon" 
                class="btn btn-outline-danger d-none"
            >
                ✖ Retirer
            </button>
        </div>
        
        <!-- Zone affichage coupon appliqué -->
        <div id="coupon-applique" class="alert alert-success mt-2 d-none">
            <strong>✅ Coupon appliqué :</strong> <span id="coupon-description"></span><br>
            <small>Remise : <span id="coupon-montant"></span> FCFA</small>
        </div>
        
        <!-- Zone erreur coupon -->
        <div id="coupon-erreur" class="alert alert-danger mt-2 d-none">
            <strong>⚠️ Erreur :</strong> <span id="coupon-message-erreur"></span>
        </div>
    </div>
</div>
```

#### **Étape 2 : Ajouter le JavaScript pour valider le coupon**

**Fichier à modifier :** `static/js/pos.js` (ou votre fichier JS principal)

```javascript
// ======= GESTION DES COUPONS =======

let couponApplique = null;  // Stocke le coupon actuellement appliqué

// Fonction pour appliquer un coupon
function appliquerCoupon() {
    const codeCoupon = document.getElementById('code-coupon').value.trim().toUpperCase();
    
    if (!codeCoupon) {
        afficherErreurCoupon('Veuillez saisir un code coupon');
        return;
    }
    
    const clientId = sessionStorage.getItem('client_id');
    const sousTotal = calculerSousTotal();  // Fonction existante pour calculer le sous-total
    
    // Appel AJAX pour valider le coupon
    fetch('/pos/valider-coupon/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            code: codeCoupon,
            client_id: clientId,
            montant_achat: sousTotal
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            couponApplique = data.coupon;
            afficherCouponApplique(data.coupon);
            recalculerTotaux();  // Fonction existante pour recalculer les totaux
        } else {
            afficherErreurCoupon(data.error);
        }
    })
    .catch(error => {
        console.error('Erreur validation coupon:', error);
        afficherErreurCoupon('Erreur serveur. Réessayez.');
    });
}

// Fonction pour retirer le coupon
function retirerCoupon() {
    couponApplique = null;
    document.getElementById('coupon-applique').classList.add('d-none');
    document.getElementById('btn-retirer-coupon').classList.add('d-none');
    document.getElementById('code-coupon').value = '';
    recalculerTotaux();
}

// Fonction pour afficher le coupon appliqué
function afficherCouponApplique(coupon) {
    document.getElementById('coupon-description').textContent = coupon.description;
    document.getElementById('coupon-montant').textContent = coupon.montant_remise.toLocaleString();
    document.getElementById('coupon-applique').classList.remove('d-none');
    document.getElementById('coupon-erreur').classList.add('d-none');
    document.getElementById('btn-retirer-coupon').classList.remove('d-none');
}

// Fonction pour afficher une erreur
function afficherErreurCoupon(message) {
    document.getElementById('coupon-message-erreur').textContent = message;
    document.getElementById('coupon-erreur').classList.remove('d-none');
    document.getElementById('coupon-applique').classList.add('d-none');
    
    // Masquer après 5 secondes
    setTimeout(() => {
        document.getElementById('coupon-erreur').classList.add('d-none');
    }, 5000);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('btn-appliquer-coupon').addEventListener('click', appliquerCoupon);
    document.getElementById('btn-retirer-coupon').addEventListener('click', retirerCoupon);
    
    // Permettre Enter pour appliquer le coupon
    document.getElementById('code-coupon').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            appliquerCoupon();
        }
    });
});

// IMPORTANT : Modifier la fonction de validation de vente existante
function validerVente() {
    // ... votre code existant ...
    
    // AJOUTER le coupon dans les données envoyées
    const donneesVente = {
        paiements: paiements,
        client_id: sessionStorage.getItem('client_id'),
        coupon_code: couponApplique ? couponApplique.code : null  // ← NOUVEAU
    };
    
    fetch('/pos/valider-vente/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(donneesVente)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Réinitialiser le coupon après validation
            couponApplique = null;
            document.getElementById('code-coupon').value = '';
            document.getElementById('coupon-applique').classList.add('d-none');
            
            // ... reste du code ...
        }
    });
}
```

#### **Étape 3 : Créer la vue Django pour valider le coupon**

**Fichier à modifier :** `CarrefourApp/views.py`

```python
@login_required
def pos_valider_coupon(request):
    """
    AJAX - Valide un code coupon et retourne les informations
    """
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        code = data.get('code', '').strip().upper()
        client_id = data.get('client_id')
        montant_achat = Decimal(str(data.get('montant_achat', 0)))
        
        if not code:
            return JsonResponse({
                'success': False,
                'error': 'Code coupon requis'
            })
        
        try:
            # Rechercher le coupon
            coupon = Coupon.objects.get(code=code)
            
            # Récupérer le client si fourni
            client = None
            if client_id:
                client = Client.objects.get(id=client_id)
            
            # Valider le coupon
            est_valide, message = coupon.est_valide(client=client, montant_achat=montant_achat)
            
            if not est_valide:
                return JsonResponse({
                    'success': False,
                    'error': message
                })
            
            # Calculer le montant de remise
            montant_remise = coupon.calculer_remise(montant_achat)
            
            return JsonResponse({
                'success': True,
                'coupon': {
                    'id': coupon.id,
                    'code': coupon.code,
                    'description': coupon.description,
                    'type_remise': coupon.type_remise,
                    'valeur': float(coupon.valeur),
                    'montant_remise': float(montant_remise)
                }
            })
            
        except Coupon.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Code coupon invalide ou expiré'
            })
        except Client.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Client introuvable'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Erreur serveur: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})
```

#### **Étape 4 : Modifier la vue de validation de vente**

**Dans `pos_valider_vente` existante, ajouter :**

```python
@login_required
def pos_valider_vente(request):
    """
    Valide la vente et enregistre le(s) paiement(s)
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        paiements = data.get('paiements', [])
        client_id = data.get('client_id')
        coupon_code = data.get('coupon_code')  # ← NOUVEAU
        
        # ... code existant ...
        
        try:
            # Associer le client si fourni
            if client_id:
                client = Client.objects.get(id=client_id)
                transaction.client = client
                client.derniere_visite = timezone.now()
                client.save()
            
            # ✅ NOUVEAU : Appliquer le coupon si fourni
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                    
                    # Valider le coupon
                    est_valide, message = coupon.est_valide(
                        client=client, 
                        montant_achat=transaction.montant_total
                    )
                    
                    if est_valide:
                        # Calculer la remise
                        montant_remise_coupon = coupon.calculer_remise(transaction.montant_total)
                        
                        # Appliquer la remise à la transaction
                        transaction.montant_remise += montant_remise_coupon
                        transaction.montant_final -= montant_remise_coupon
                        transaction.save()
                        
                        # Créer l'enregistrement d'utilisation
                        UtilisationCoupon.objects.create(
                            coupon=coupon,
                            client=client,
                            transaction=transaction,
                            montant_remise=montant_remise_coupon
                        )
                        
                        # Marquer le coupon comme utilisé
                        coupon.marquer_utilise()
                        
                        print(f"🎫 COUPON APPLIQUÉ: {coupon.code} - Remise: {montant_remise_coupon} FCFA")
                    else:
                        print(f"⚠️ COUPON INVALIDE: {message}")
                        
                except Coupon.DoesNotExist:
                    print(f"⚠️ COUPON INTROUVABLE: {coupon_code}")
            
            # ... reste du code existant ...
```

#### **Étape 5 : Ajouter la route URL**

**Fichier à modifier :** `CarrefourApp/urls.py`

```python
urlpatterns = [
    # ... vos URLs existantes ...
    
    # Coupons (NOUVEAU)
    path('pos/valider-coupon/', views.pos_valider_coupon, name='pos_valider_coupon'),
]
```

---

## 🏆 SYSTÈME DE FIDÉLISATION AUTOMATIQUE

### **Comment ça fonctionne ?**

Le système de fidélisation est **100% automatique** et fonctionne **dès maintenant** :

#### **1️⃣ Identification du client**
- Le caissier saisit le **téléphone** du client
- Si le client existe → récupération de ses données
- Si nouveau → création automatique avec niveau **TOUS**

#### **2️⃣ Calcul automatique de la remise fidélité**
✅ **Déjà implémenté dans le code**

```python
# Dans la vue caisse_vente (ligne ~3900)
if client:
    if client.niveau_fidelite == 'VIP':
        pourcentage_fidelite = 10
        remise_fidelite = sous_total * 0.10
    elif client.niveau_fidelite == 'GOLD':
        pourcentage_fidelite = 5
        remise_fidelite = sous_total * 0.05
    elif client.niveau_fidelite == 'SILVER':
        pourcentage_fidelite = 3
        remise_fidelite = sous_total * 0.03
```

#### **3️⃣ Attribution des points**
✅ **Déjà implémenté**

```python
# Après validation de la vente
if client:
    points_gagnes = int(montant_final / 1000)  # 1 point par 1000 FCFA
    client.points_fidelite += points_gagnes
    client.save()
```

#### **4️⃣ Upgrade automatique de niveau**
✅ **Déjà implémenté dans le modèle Client**

```python
# Le niveau est recalculé automatiquement
def save(self, *args, **kwargs):
    # Calcul automatique du niveau selon le nombre d'achats
    nb_achats = self.nombre_achats()
    
    if nb_achats >= 30:
        self.niveau_fidelite = 'VIP'
    elif nb_achats >= 15:
        self.niveau_fidelite = 'GOLD'
    elif nb_achats >= 5:
        self.niveau_fidelite = 'SILVER'
    else:
        self.niveau_fidelite = 'TOUS'
    
    super().save(*args, **kwargs)
```

### **Exemple concret d'utilisation**

**Scénario : Marie KOUADIO fait son 16ème achat**

1. **Avant l'achat :**
   - Niveau actuel : SILVER (15 achats)
   - Remise : 3%
   - Points : 425

2. **Panier actuel :**
   - Sous-total : 75 000 FCFA
   - Remise fidélité (3%) : 2 250 FCFA
   - Total après remise : 72 750 FCFA

3. **Après validation :**
   - Nombre d'achats : 16
   - **Niveau UPGRADÉ automatiquement → GOLD** 🎉
   - Points gagnés : 72 (72 750 / 1000)
   - Total points : 497

4. **Prochain achat :**
   - Remise : **5%** (niveau GOLD)

---

## 📊 SUIVI ET RAPPORTS

### **Interface Marketing - Dashboard CRM**

**Accès :** Menu Marketing → Dashboard CRM

**KPIs disponibles :**

1. **Taux d'identification** : % de clients identifiés
2. **Répartition des niveaux** : VIP, GOLD, SILVER, TOUS
3. **Taux d'utilisation des coupons** : Génériques vs Spéciaux
4. **Marge nette après remises** : Impact des remises sur le CA
5. **Taux de rétention** : Clients actifs ce mois vs mois précédent
6. **Fréquence d'achat** : Par niveau de fidélité
7. **Top coupons** : Les plus utilisés
8. **CA par niveau** : Contribution de chaque segment

### **Rapports disponibles**

#### **1. Rapport des coupons utilisés**
```
Menu : Marketing → Coupons → Rapport d'utilisation
```

Affiche :
- Nombre d'utilisations par coupon
- Montant total des remises accordées
- Clients ayant utilisé les coupons
- Date et montant de chaque utilisation

#### **2. Rapport fidélité par client**
```
Menu : Marketing → Clients → Fiche client
```

Affiche :
- Historique des achats
- Points accumulés
- Progression du niveau
- Coupons utilisés

---

## 🔧 ERREURS CORRIGÉES

### **1. FieldError: Cannot resolve keyword 'remise'**

**Erreur :**
```
Cannot resolve keyword 'remise' into field. Choices are: caissier, client, 
date_modification, date_transaction, id, lignes, montant_final, montant_remise, 
montant_total, notes, numero_ticket, paiements, statut, utilisationcoupon
```

**Cause :** Le champ s'appelle `montant_remise` et non `remise`

**Correction appliquée :**
```python
# AVANT (INCORRECT)
remises_total = ventes.aggregate(total=Sum('remise'))['total'] or 0

# APRÈS (CORRECT)
remises_total = ventes.aggregate(total=Sum('montant_remise'))['total'] or 0
```

**Fichiers modifiés :**
- `CarrefourApp/views.py` - ligne 4394 (caissier_mes_ventes)
- `CarrefourApp/views.py` - ligne 3540 (export_ventes_excel)

### **2. Transaction.session does not exist**

**Erreur :**
```
'Transaction' object has no attribute 'session'
```

**Cause :** Le modèle Transaction n'a pas de relation avec SessionPresence

**Correction appliquée :**
```python
# AVANT (INCORRECT)
.select_related('client', 'session')

# APRÈS (CORRECT)
.select_related('client')
```

**Fichier modifié :**
- `CarrefourApp/views.py` - ligne 4380 (caissier_mes_ventes)

### **3. NoReverseMatch: 'dashboard' is not a valid view**

**Erreur :**
```
Reverse for 'dashboard' not found. 'dashboard' is not a valid view function or pattern name.
```

**Cause :** Tentative d'accès à une URL non définie

**Solution :** Utiliser `get_dashboard_by_role(request.user)` pour rediriger vers le bon dashboard

---

## ✅ RÉSUMÉ DES ACTIONS

### **Ce qui est DÉJÀ fonctionnel :**

✅ Création de coupons (GENERIC et SPECIAL)  
✅ Validation automatique des règles de coupon  
✅ Calcul de remise (POURCENTAGE et MONTANT_FIXE)  
✅ Système de fidélisation automatique (niveaux, points, remises)  
✅ Upgrade automatique de niveau  
✅ Tracking des utilisations de coupons  
✅ Dashboard CRM avec statistiques  

### **Ce qui doit être DÉVELOPPÉ :**

❌ Interface de saisie du code coupon dans la caisse POS  
❌ Validation du coupon en temps réel côté JavaScript  
❌ Enregistrement de l'utilisation du coupon avec la transaction  
❌ Affichage de la remise coupon sur le ticket  

### **Priorité de développement :**

**1. URGENT** : Intégrer l'interface coupon dans le POS (voir Étapes 1-5)  
**2. MOYEN** : Ajouter les coupons dans les rapports de caisse  
**3. FAIBLE** : Générer des coupons automatiques pour les anniversaires  

---

## 📞 SUPPORT

Si vous avez des questions :
1. Relisez la section correspondante de ce guide
2. Vérifiez que les erreurs listées ont bien été corrigées
3. Testez d'abord en mode DEBUG pour voir les logs

---

**Document généré le : 22 octobre 2025**  
**Version du système : Django 5.2**  
**Auteur : Assistant GitHub Copilot**
