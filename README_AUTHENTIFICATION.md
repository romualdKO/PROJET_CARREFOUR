# 🛒 Système de Gestion de Supermarché - SuperMarché Plus

## 📋 Vue d'ensemble

Application Django complète pour la gestion intégrée d'un supermarché avec interfaces modernes et rôles utilisateurs différenciés.

## 🔐 Système d'Authentification

### Comptes Par Défaut

L'application dispose de 3 comptes administrateurs créés automatiquement :

| Rôle | Identifiant | Mot de passe | Accès |
|------|-------------|--------------|-------|
| **Directeur Général (DG)** | `dg` | `DG2025@Admin` | Dashboard DG (vue globale) |
| **Directeur Financier (DAF)** | `daf` | `DAF2025@Admin` | Dashboard DAF (finances) |
| **Responsable RH** | `rh` | `RH2025@Admin` | Dashboard RH + Création employés |

### Gestion des Employés

#### Création d'Employés (par le RH)

Le Responsable RH a la responsabilité exclusive de créer les comptes pour tous les autres employés :

**Rôles disponibles :**
- 📦 **Gestionnaire de Stock** - Gestion de l'inventaire
- 💰 **Caissier** - Point de vente et transactions
- 📢 **Marketing / Fidélisation** - Programmes de fidélité et promotions
- 📊 **Analyste** - Business Intelligence et rapports
- 👥 **Responsable RH** - Gestion du personnel (uniquement si besoin d'un 2ème RH)

**Processus de création :**
1. Se connecter avec le compte RH (`rh` / `RH2025@Admin`)
2. Aller dans "Dashboard RH"
3. Cliquer sur "➕ Nouvel Employé"
4. Remplir le formulaire :
   - Prénom et Nom
   - Email professionnel
   - Nom d'utilisateur (utilisé pour la connexion)
   - Mot de passe (minimum 8 caractères)
   - Rôle / Poste
   - Accès aux tableaux de bord (optionnel)
5. L'employé reçoit ses identifiants et peut se connecter immédiatement

#### Accès par Rôle

Après connexion, chaque utilisateur est automatiquement redirigé vers son dashboard spécifique :

```python
DG          → Dashboard Direction Générale (vue globale, KPIs stratégiques)
DAF         → Dashboard Financier (comptabilité, trésorerie, budgets)
RH          → Dashboard RH (employés, présences, congés, formations)
STOCK       → Dashboard Stock (inventaire, alertes, commandes)
CAISSIER    → Dashboard Caisse (ventes, transactions, moyens de paiement)
MARKETING   → Dashboard Marketing (fidélisation, promotions, campagnes)
ANALYSTE    → Dashboard Analytics (BI, graphiques avancés, prédictions)
```

## 🚀 Démarrage

### 1. Première Installation

```powershell
# Activer l'environnement virtuel (si nécessaire)
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# Créer les comptes par défaut (DG, DAF, RH)
Get-Content create_default_accounts.py | python manage.py shell

# Créer des données de démonstration (optionnel)
Get-Content create_sample_data.py | python manage.py shell
```

### 2. Lancer le Serveur

```powershell
python manage.py runserver
```

L'application sera accessible sur : **http://127.0.0.1:8000/**

## 📱 Modules Disponibles

### 1. 🏠 Page d'Accueil
- Présentation de l'application
- Liens vers tous les modules
- Boutons "Accéder au module" (requiert connexion)

### 2. 🔐 Connexion
- Authentification sécurisée
- Redirection automatique selon le rôle
- Gestion de session

### 3. 📊 Direction Générale (DG)
- Vue d'ensemble complète
- KPIs stratégiques (CA, Marges, ROI)
- Graphiques Chart.js (évolution CA, top produits)
- Analyses de performance

### 4. 💼 Direction Financière (DAF)
- KPIs financiers
- Évolution du chiffre d'affaires
- Répartition moyens de paiement
- Trésorerie et charges

### 5. 👥 Ressources Humaines (RH)
- Gestion complète des employés
- **Création de comptes employés** ✨
- Liste des employés avec statuts
- Présences et activités récentes
- Congés et formations

### 6. 📦 Gestion des Stocks
- Inventaire complet
- Alertes de stock critique
- Valeur totale du stock
- Gestion des fournisseurs

### 7. 💰 Point de Vente (Caisse)
- Ventes du jour
- Transactions récentes
- Statistiques moyens de paiement
- Actions rapides (remise, promo)

### 8. 📢 Marketing & Fidélisation
- Clients fidèles (VIP/Gold/Silver)
- Points de fidélité distribués
- Promotions actives
- Campagnes marketing

### 9. 📈 Analytics & BI
- Évolution des ventes (7 jours)
- Performance globale (jauge circulaire)
- Top produits par CA
- Répartition par catégorie
- Analyses détaillées avec tendances

## 🎨 Design & Interface

### Charte Graphique
- **Couleur Primaire Bleue** : `#2563EB` (confiance, technologie)
- **Couleur Primaire Verte** : `#28A745` (croissance, succès)
- Interface moderne et responsive
- Composants réutilisables (cards, KPIs, badges)
- Icons emoji pour une meilleure UX

### Composants
- **KPI Cards** : Affichage des indicateurs clés avec tendances
- **Charts** : Graphiques interactifs Chart.js (line, bar, doughnut)
- **Tables** : Tableaux de données paginés et filtrables
- **Badges** : Statuts colorés (success, warning, danger)
- **Sidebar** : Navigation contextuelle par rôle

## 🔧 Technologies

- **Backend** : Django 5.2
- **Frontend** : HTML5, CSS3 (CSS Variables), JavaScript
- **Charts** : Chart.js 3.x
- **Database** : SQLite3 (dev) / PostgreSQL (prod)
- **Authentication** : Django Auth avec Custom User Model

## 📊 Modèles de Données

- **Employe** : Utilisateurs avec rôles et permissions
- **Produit** : Articles en vente avec stock
- **Vente** : Transactions avec numéros automatiques
- **LigneVente** : Détails des ventes par produit
- **Client** : Clients avec programme de fidélité
- **Promotion** : Réductions et offres spéciales
- **Presence** : Suivi des présences employés
- **Conge** : Gestion des congés
- **Formation** : Formations suivies
- **Reclamation** : Réclamations clients

## 🔒 Sécurité

- Mots de passe hashés (Django Password Hashers)
- Protection CSRF activée
- Décorateurs `@login_required` sur toutes les vues sensibles
- Validation des permissions par rôle
- Sessions sécurisées

## 📝 Workflow Typique

### Scénario 1 : Premier lancement
1. Le DG et le DAF se connectent avec leurs comptes par défaut
2. Le RH se connecte et crée les comptes pour l'équipe
3. Chaque employé reçoit ses identifiants
4. Les employés se connectent et accèdent à leurs dashboards respectifs

### Scénario 2 : Nouvel employé
1. Le RH va dans "Dashboard RH" → "➕ Nouvel Employé"
2. Remplit le formulaire (nom, prénom, email, identifiant, mot de passe, rôle)
3. Configure les accès (dashboards autorisés)
4. Valide la création
5. L'employé peut immédiatement se connecter avec ses identifiants

### Scénario 3 : Gestion quotidienne
- **Caissiers** : Gèrent les ventes en temps réel
- **Stock Manager** : Suit l'inventaire et passe les commandes
- **Marketing** : Lance des promotions et suit la fidélisation
- **Analyste** : Génère des rapports et analyses
- **RH** : Gère les présences, congés et formations
- **DAF** : Suit la santé financière
- **DG** : Supervise l'ensemble avec vue stratégique

## 🐛 Débogage

### Port déjà utilisé
```powershell
# Trouver et arrêter le processus
$port = Get-NetTCPConnection -LocalPort 8000 | Select-Object -ExpandProperty OwningProcess
Stop-Process -Id $port -Force

# Relancer le serveur
python manage.py runserver
```

### Réinitialiser la base de données
```powershell
# Supprimer la base
Remove-Item db.sqlite3

# Recréer les migrations
python manage.py makemigrations
python manage.py migrate

# Recréer les comptes par défaut
Get-Content create_default_accounts.py | python manage.py shell
```

## 📞 Support

Pour toute question ou problème :
- Email : support@supermarcheplus.com
- Documentation : Consultez ce README
- Logs : Vérifiez la console du serveur Django

## 📄 Licence

© 2025 SuperMarché Plus - Tous droits réservés
Système de gestion intégré pour supermarchés

---

**Version** : 1.0.0  
**Dernière mise à jour** : 15 Octobre 2025  
**Développé avec** : ❤️ et Django
