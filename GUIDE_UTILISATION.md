# 🛒 GUIDE D'UTILISATION - APPLICATION CARREFOUR

## 📋 TABLE DES MATIÈRES
1. [Démarrage Initial](#démarrage-initial)
2. [Module Stock](#module-stock)
3. [Module Caisse/POS](#module-caisse-pos)
4. [Module CRM](#module-crm)
5. [Module Analytics](#module-analytics)
6. [Dépannage](#dépannage)

---

## 🚀 DÉMARRAGE INITIAL

### Étape 1: Vérifier l'état de l'application
```powershell
cd "c:\Users\HP\OneDrive - Ecole Supérieure Africaine des Technologies de l'Information et de la Communication (ESATIC)\Bureau\PROJET_CARREFOUR"
python manage.py check
```
✅ **Résultat attendu:** `System check identified no issues (0 silenced).`

### Étape 2: Créer un superutilisateur (si pas déjà fait)
```powershell
python manage.py createsuperuser
```
- **Username:** admin
- **Email:** admin@carrefour.com
- **Password:** admin123 (ou votre choix)

### Étape 3: Lancer le serveur
```powershell
python manage.py runserver
```
✅ **Serveur actif sur:** `http://127.0.0.1:8000`

### Étape 4: Accéder à l'admin Django
🌐 **URL:** `http://127.0.0.1:8000/admin/`
- Connectez-vous avec le superutilisateur

---

## 📦 MODULE STOCK

### A. Créer des Fournisseurs

#### Via l'Interface Web:
1. **URL:** `http://127.0.0.1:8000/stock/fournisseurs/`
2. Cliquer sur **"Nouveau Fournisseur"**
3. Remplir le formulaire:
   - **Nom:** SODECI
   - **Email:** contact@sodeci.ci
   - **Téléphone:** 0102030405
   - **Adresse:** Abidjan, Plateau
   - **Ville:** Abidjan
   - **Pays:** Côte d'Ivoire
4. Cliquer **"Enregistrer"**

#### Via l'Admin Django:
1. **URL:** `http://127.0.0.1:8000/admin/CarrefourApp/fournisseur/`
2. Cliquer **"Add Fournisseur"**
3. Remplir et sauvegarder

**✅ Créer 3-5 fournisseurs pour les tests**

---

### B. Créer des Produits

#### Via l'Admin (Plus rapide):
1. **URL:** `http://127.0.0.1:8000/admin/CarrefourApp/produit/`
2. **Exemples de produits à créer:**

| Nom | Référence | Prix Achat | Prix Vente | Stock Actuel | Stock Min | Stock Max | Catégorie |
|-----|-----------|------------|------------|--------------|-----------|-----------|-----------|
| Riz Uncle Ben's 1kg | RIZ001 | 800 | 1200 | 50 | 10 | 100 | ALIMENTATION |
| Coca Cola 1.5L | COCA001 | 500 | 750 | 100 | 20 | 200 | BOISSONS |
| Pain de mie | PAIN001 | 300 | 450 | 30 | 5 | 50 | BOULANGERIE |
| Lait Nido 400g | LAIT001 | 1500 | 2200 | 40 | 10 | 80 | PRODUITS_LAITIERS |
| Savon Dove | SAV001 | 600 | 900 | 60 | 15 | 100 | HYGIENE |

**✅ Créer 10-15 produits pour simuler un magasin réel**

---

### B.2 Modifier un Produit avec Image

#### 📝 Accéder à la Modification:
1. **URL:** `http://127.0.0.1:8000/dashboard/stock/`
2. Cliquer sur le bouton **"✏️ Modifier"** à côté d'un produit

#### 📸 Ajouter/Modifier l'Image du Produit:
1. Cliquer sur **"📷 Choisir une nouvelle image"**
2. Sélectionner une image (JPG, PNG, GIF - max 5MB)
3. **Prévisualisation instantanée** de l'image
4. L'ancienne image est automatiquement supprimée lors de l'enregistrement

#### ✏️ Modifier les Informations:
- **Informations Générales:**
  - Nom du produit
  - Référence (doit être unique)
  - Catégorie
  - Code-barre
  - Description

- **Prix et Fournisseur:**
  - Prix d'achat (FCFA)
  - Prix de vente (FCFA)
  - Fournisseur principal

- **Stock et Seuils:**
  - Stock actuel (si modifié, un mouvement de stock est créé automatiquement)
  - Stock critique (alerte rouge)
  - Seuil de réapprovisionnement (alerte orange)
  - Stock minimum
  - Stock maximum

#### ⚠️ Validations Automatiques:
- ✅ Prix de vente ≤ prix d'achat → Confirmation demandée
- ✅ Seuil réappro > stock critique
- ✅ Stock max > seuil réappro
- ✅ Référence unique (pas de doublon)
- ✅ Image max 5MB

#### 💡 Fonctionnalités Intelligentes:
- **Traçabilité:** Si vous changez le stock actuel, un mouvement est créé automatiquement
- **Historique:** Tous les changements sont enregistrés
- **Validation:** Le système vous alerte en cas d'incohérence

---

### C. Passer une Commande Fournisseur

1. **URL:** `http://127.0.0.1:8000/stock/commandes/`
2. Cliquer **"Nouvelle Commande"**
3. Sélectionner un **Fournisseur**
4. **Ajouter des lignes:**
   - Produit: Riz Uncle Ben's
   - Quantité: 50
   - Prix unitaire: 800 FCFA
5. Sauvegarder
6. **Résultat:** Numéro de commande auto-généré (ex: CMD20251019001)

---

### D. Dashboard Stock

**URL:** `http://127.0.0.1:8000/dashboard/stock/`

**Ce que vous verrez:**
- 📊 Valeur totale du stock
- 📈 Marge globale
- ⚠️ Nombre d'alertes stock bas
- 📦 Nombre de produits
- 🔄 Mouvements du mois
- 🏢 Nombre de fournisseurs
- 📋 Commandes en cours
- 💰 Valeur des commandes
- 📉 Taux de rotation

---

## 💰 MODULE CAISSE/POS

### A. Ouvrir une Session de Caisse

1. **URL:** `http://127.0.0.1:8000/pos/ouvrir-session/`
2. **Fonds d'ouverture:** 50000 FCFA
3. **Cocher les 3 cases:**
   - ✅ Le fonds de caisse a été vérifié
   - ✅ Le terminal de paiement fonctionne
   - ✅ L'imprimante est prête
4. Cliquer **"Ouvrir la Session"**

**✅ Sans session ouverte, vous ne pouvez pas vendre!**

---

### B. Effectuer une Vente (Interface POS)

1. **URL:** `http://127.0.0.1:8000/pos/`

#### Interface divisée en 2 parties:

**Partie gauche - Grille de produits:**
- 🔍 Barre de recherche en haut
- 🏷️ Filtres par catégorie
- 📦 Cartes produits avec:
  - Nom du produit
  - Prix
  - Badge de stock (Vert/Orange/Rouge)

**Partie droite - Panier:**
- Liste des produits ajoutés
- Boutons +/- pour quantités
- Total en temps réel
- Bouton **"Valider la Vente"**

---

#### Workflow d'une vente:

**Étape 1: Cliquer "Nouvelle Transaction"**
- Bouton bleu en haut à droite
- Une transaction est créée (statut: EN_COURS)

**Étape 2: Ajouter des produits**
- Cliquer sur un produit dans la grille
- Il s'ajoute au panier
- Le stock disponible est affiché
- Vous pouvez augmenter/diminuer la quantité avec +/-

**Étape 3: Sélectionner un client (optionnel)**
- Si le client a une carte fidélité, sélectionnez-le
- Sinon, laissez vide (vente anonyme)

**Étape 4: Valider la vente**
- Cliquer **"Valider la Vente"**
- Modal de paiement s'ouvre

**Étape 5: Enregistrer le paiement**
- **Montant total affiché** (ex: 5000 FCFA)
- **Sélectionner type de paiement:**
  - 💵 Espèces
  - 💳 Carte Bancaire
  - 📱 Orange Money
  - 📱 MTN Money
  - 📱 Moov Money
  - 📝 Chèque
  - 🏦 Virement

**Exemple avec Espèces:**
1. Cliquer sur **"Espèces"**
2. Entrer **"Montant reçu"**: 10000 FCFA
3. **Rendu automatique calculé**: 5000 FCFA
4. Cliquer **"Confirmer le Paiement"**

**✅ Résultat:**
- Ticket généré (ex: TKT20251019001)
- Stock automatiquement déduit
- Mouvement de stock créé
- Points fidélité crédités (si client)

---

### C. Support Paiements Multiples

**Exemple:** Client paye 2000 FCFA en espèces + 3000 FCFA par Orange Money

1. Premier paiement:
   - Type: Espèces
   - Montant: 2000 FCFA
2. Deuxième paiement:
   - Type: Orange Money
   - Montant: 3000 FCFA
3. Total: 5000 FCFA ✅

---

### D. Clôturer la Session

1. **URL:** `http://127.0.0.1:8000/pos/cloturer-session/`

**Ce que vous verrez:**
- 💰 **Fonds d'ouverture:** 50000 FCFA
- 🛒 **Nombre de ventes:** 15
- 💵 **Total des ventes:** 45000 FCFA
- 📊 **Fonds théorique:** 95000 FCFA (50000 + 45000)

**Répartition par type de paiement:**
| Type | Montant |
|------|---------|
| Espèces | 30000 FCFA |
| Orange Money | 10000 FCFA |
| Carte Bancaire | 5000 FCFA |

**Comptage physique:**
1. Compter l'argent dans la caisse
2. Entrer **"Fonds réel"**: 94500 FCFA (exemple)
3. **Écart calculé automatiquement:** -500 FCFA (manquant)
   - 🟢 Vert si équilibré (0 FCFA)
   - 🔴 Rouge si manque
   - 🟢 Vert clair si surplus
4. Ajouter des **Notes:** "Erreur de rendu 500 FCFA à la vente 12"
5. Cliquer **"Clôturer la Session"**

---

### E. Dashboard Caisse

**URL:** `http://127.0.0.1:8000/dashboard/caisse/`

**Affichage:**
- 📊 Session actuelle (ouverte/fermée)
- 💰 Chiffre d'affaires du jour
- 🛒 Nombre de ventes du jour
- 📋 Dernières transactions (10)
- 📅 Historique des sessions (5 dernières)

---

## 👥 MODULE CRM

### A. Liste des Clients

**URL:** `http://127.0.0.1:8000/crm/clients/`

**Statistiques affichées:**
- 👤 Total clients
- ✅ Clients actifs
- 🥉 Clients Bronze
- 🥈 Clients Argent
- 🥇 Clients Or
- 💎 Clients Platine

**Filtres disponibles:**
- 🔍 Recherche (nom, téléphone, numéro client)
- 🏆 Niveau de fidélité
- ✅/❌ Statut (actif/inactif)

---

### B. Profil d'un Client

**URL:** `http://127.0.0.1:8000/crm/clients/<id>/`

**Informations affichées:**

**Bloc 1 - Identité:**
- Nom complet
- Numéro client
- Téléphone, Email
- Adresse, Ville
- Date de naissance
- Niveau de fidélité (Badge coloré)
- Statut (Actif/Inactif)

**Bloc 2 - Statistiques:**
- ⭐ Points de fidélité
- 💰 Total achats
- 🛒 Nombre d'achats
- 📊 Panier moyen

**Bloc 3 - Carte de Fidélité:**
- Numéro carte (CARD20251019001)
- Date d'émission
- Solde points
- Statut carte
- Date d'expiration
- Bouton **"Créditer des Points"**

**Onglets:**
1. **Transactions Récentes** (10 dernières)
2. **Historique Points** (20 dernières opérations)

---

### C. Créer une Carte de Fidélité

**Depuis le profil client:**
1. Cliquer **"Créer une Carte"**
2. Numéro généré automatiquement
3. Solde initial = points actuels du client
4. Opération initiale créée

---

### D. Créditer des Points

**URL:** `http://127.0.0.1:8000/crm/clients/<id>/crediter-points/`

1. **Points à créditer:** 100
2. **Motif:** "Achat de 10000 FCFA"
3. Cliquer **"Créditer"**

**Résultat:**
- Solde carte mis à jour
- Opération créée dans l'historique
- Points client mis à jour

---

### E. Segments Clients

**URL:** `http://127.0.0.1:8000/crm/segments/`

**Créer un segment:**
1. Cliquer **"Nouveau Segment"**
2. **Nom:** "Clients Premium"
3. **Critères:**
   - Niveau: OR
   - Montant minimum: 50000 FCFA
   - Montant maximum: (vide)
4. Sauvegarder

**Utilité:** Cibler des clients spécifiques pour les campagnes

---

### F. Campagnes Marketing

**URL:** `http://127.0.0.1:8000/crm/campagnes/`

**Créer une campagne:**
1. Cliquer **"Nouvelle Campagne"**
2. **Titre:** "Promotion Fin d'Année"
3. **Type:** SMS
4. **Date début:** 01/12/2025
5. **Date fin:** 31/12/2025
6. **Segment cible:** Clients Premium
7. **Message:** "Profitez de -20% sur tous nos produits du 1er au 31 décembre!"
8. Sauvegarder

**Lancer la campagne:**
1. Aller sur la campagne
2. Cliquer **"Lancer"** (icône avion)
3. Nombre de destinataires calculé automatiquement
4. Simulation d'envoi (dans la vraie vie: API SMS)

**Statistiques:**
- 📨 Nombre destinataires
- ✅ Nombre envoyés
- 📖 Nombre ouverts
- 📊 Taux d'ouverture

---

## 📊 MODULE ANALYTICS

### A. Dashboard Analytique

**URL:** `http://127.0.0.1:8000/dashboard/analytics/`

**4 KPIs en haut:**
- 💰 CA du mois
- 📊 Panier moyen
- 👥 Clients actifs (+nouveaux)
- 📦 Valeur stock (+ alertes)

**Graphiques Chart.js:**
1. **Évolution CA (30 jours)** - Line chart
2. **Répartition clients** - Donut (Bronze/Argent/Or/Platine)
3. **CA par jour de la semaine** - Bar chart
4. **Top 10 produits** - Horizontal bar

**Tableau performances caissiers:**
- Rang
- Nom caissier
- Nombre ventes
- CA total
- Panier moyen

---

### B. Export Excel

**URL:** `http://127.0.0.1:8000/analytics/export/ventes/`

**Paramètres (optionnels):**
- Date début
- Date fin

**Résultat:**
- Fichier Excel téléchargé: `ventes_20251019.xlsx`
- Colonnes: Date, N° Ticket, Caissier, Client, Montant Total, Remise, Montant Final, Statut
- En-têtes stylisés (bleu)
- Largeurs auto-ajustées

---

### C. Rapport Mensuel

**URL:** `http://127.0.0.1:8000/analytics/rapport-mensuel/`

**Paramètres:**
- `?annee=2025&mois=10` (dans l'URL)

**Contenu:**
- Résumé exécutif (4 KPIs)
- Top 5 produits du mois
- Performances caissiers
- Détail jour par jour (tableau complet)
- Bouton **"Imprimer"** (PDF via navigateur)

---

## 🧪 SCÉNARIO DE TEST COMPLET

### Test 1: Vente Simple
```
1. Ouvrir session caisse (50000 FCFA)
2. Créer nouvelle transaction
3. Ajouter: Riz (x2) + Coca Cola (x3)
4. Total: 2400 + 2250 = 4650 FCFA
5. Payer en espèces (5000 FCFA)
6. Rendu: 350 FCFA
7. Vérifier: Stock Riz: 50→48, Stock Coca: 100→97
```

### Test 2: Vente avec Client Fidélité
```
1. Sélectionner client "Pierre Martin"
2. Ajouter produits (Total: 10000 FCFA)
3. Valider vente
4. Vérifier profil client:
   - Points +100 (1 point = 100 FCFA)
   - Total achats +10000
   - Dernière visite mise à jour
```

### Test 3: Clôture avec Écart
```
1. Faire 5 ventes dans la session
2. Clôturer session
3. Fonds théorique: 75000 FCFA
4. Compter: 74800 FCFA
5. Écart: -200 FCFA (manque)
6. Noter la raison
```

### Test 4: Campagne Marketing
```
1. Créer segment "Clients Gold" (niveau OR)
2. Créer campagne SMS
3. Message: "Offre spéciale -15%"
4. Lancer campagne
5. Vérifier nb destinataires = nb clients OR
```

### Test 5: Alerte Stock
```
1. Vendre produit jusqu'à stock < stock_minimum
2. Vérifier dashboard stock: alerte rouge
3. Créer commande fournisseur
4. Vérifier alerte disparaît après réception
```

---

## 🛠️ DÉPANNAGE

### Problème: Session déjà ouverte
**Erreur:** "Vous avez déjà une session ouverte"
**Solution:** Clôturer la session actuelle d'abord

### Problème: Stock insuffisant
**Erreur:** "Stock insuffisant pour ce produit"
**Solution:** Vérifier stock actuel du produit, passer commande fournisseur

### Problème: Page d'admin inaccessible
**Solution:** 
```powershell
python manage.py createsuperuser
```

### Problème: Aucun type de paiement
**Solution:**
```powershell
python manage.py shell
exec(open('init_types_paiement.py').read())
```

### Problème: Graphiques ne s'affichent pas
**Vérification:** Chart.js chargé? Ouvrir console navigateur (F12)

---

## 📱 ACCÈS RAPIDE - TOUS LES LIENS

### Stock
- Dashboard: `http://127.0.0.1:8000/dashboard/stock/`
- Fournisseurs: `http://127.0.0.1:8000/stock/fournisseurs/`
- Commandes: `http://127.0.0.1:8000/stock/commandes/`
- Alertes: `http://127.0.0.1:8000/dashboard/stock/alertes/`

### Caisse
- Ouvrir session: `http://127.0.0.1:8000/pos/ouvrir-session/`
- Interface POS: `http://127.0.0.1:8000/pos/`
- Clôturer: `http://127.0.0.1:8000/pos/cloturer-session/`
- Dashboard: `http://127.0.0.1:8000/dashboard/caisse/`

### CRM
- Clients: `http://127.0.0.1:8000/crm/clients/`
- Segments: `http://127.0.0.1:8000/crm/segments/`
- Campagnes: `http://127.0.0.1:8000/crm/campagnes/`

### Analytics
- Dashboard: `http://127.0.0.1:8000/dashboard/analytics/`
- Export Excel: `http://127.0.0.1:8000/analytics/export/ventes/`
- Rapport: `http://127.0.0.1:8000/analytics/rapport-mensuel/`

### Admin
- Admin Django: `http://127.0.0.1:8000/admin/`

---

## ✅ CHECKLIST DE TEST

- [ ] Créer 3 fournisseurs
- [ ] Créer 10 produits
- [ ] Passer 2 commandes fournisseurs
- [ ] Ouvrir session caisse
- [ ] Faire 5 ventes (dont 2 avec client)
- [ ] Tester paiement multiple
- [ ] Clôturer session
- [ ] Créer 3 cartes fidélité
- [ ] Créditer/débiter points
- [ ] Créer 1 segment
- [ ] Créer 1 campagne
- [ ] Voir dashboard analytics
- [ ] Exporter ventes Excel
- [ ] Générer rapport mensuel

---

## 🎯 BON TEST! 🚀
