# 🛒 SuperMarché Plus - Application de Gestion Intégrée

Application web complète de gestion pour supermarchés développée avec Django, respectant les maquettes fournies avec un design moderne en bleu (#2563EB) et vert (#28A745).

## 🎯 Fonctionnalités

### 1. **Page d'Accueil**
- Logo et présentation du système
- Menu de navigation (Accueil, À propos, Services, Contact)
- Section hero avec call-to-action
- Présentation des 6 modules principaux

### 2. **Authentification**
- Connexion sécurisée pour employés
- Identifiant employé + mot de passe
- Redirection automatique selon le rôle utilisateur
- Option "Se souvenir de moi"

### 3. **Tableau de Bord Principal**
- Sélection du profil utilisateur
- 6 tuiles cliquables selon les rôles :
  - Direction Générale 👑
  - Responsable RH 👥
  - Gestionnaire Stock 📦
  - Caissier 💰
  - Marketing 💝
  - Analyste 📊

### 4. **Module Directeur Général (DG)** ✅
- **KPIs globaux** : CA, Bénéfice Net, Transactions, ROI
- **Graphique évolution du CA** : 6 derniers mois avec objectifs
- **Analyse des marges** : Revenus, Coûts, Bénéfices
- **Top produits** : Par catégorie avec barres de progression
- **Indicateurs opérationnels** : Temps caisse, Satisfaction client, Productivité
- **Rapports détaillés** : Tableau exportable avec filtres

### 5. **Module Directeur Administratif et Financier (DAF)**
- Vue financière consolidée
- Évolution du chiffre d'affaires
- Analyse des marges (brute et nette)
- Analyse budgétaire par catégorie
- Modes de paiement
- Alertes financières
- Gestion de la trésorerie

### 6. **Module Ressources Humaines (RH)** ✅
- Gestion des employés avec ID auto-généré
- Tableau de bord : Total employés, Présences, Congés, Formations
- Liste complète des employés avec statuts
- Gestion des plannings et présences
- Suivi des congés (types : annuel, maladie, maternité, sans solde)
- Gestion des formations
- Activités récentes

### 7. **Module Gestion des Stocks**
- Inventaire complet des produits
- Alertes de stock critique (automatiques)
- Valeur totale du stock
- Gestion des références produits
- Gestion des fournisseurs
- Commandes en cours
- Codes-barres

### 8. **Module Caisses et Ventes**
- Interface Point de Vente (POS) simplifiée
- Support multi-paiements : Espèces, Carte, Mobile Money
- Calcul automatique TVA (18%)
- Historique des transactions
- Statistiques du jour : CA, Transactions, Panier moyen
- Caisses actives
- Synchronisation automatique avec les stocks

### 9. **Module Fidélisation Client (Marketing)**
- Gestion des clients fidèles
- Système de points de fidélité
- Niveaux : Tous, Silver, Gold, VIP
- Promotions actives
- Gestion des réclamations
- Activités récentes (nouveaux clients, points utilisés)
- Campagnes SMS (simulé)

### 10. **Module Analytics**
- KPIs temps réel : CA, Transactions, Panier moyen, Marge
- Graphique évolution des ventes (7 jours)
- Performance globale (gauge à 85%)
- Top produits vendus
- Répartition par catégorie (pie chart)
- Moyens de paiement

## 🎨 Design

### Palette de couleurs
```css
--primary-blue: #2563EB
--primary-green: #28A745
--light-blue: #EFF6FF
--light-green: #F0FDF4
--dark-blue: #1E40AF
--dark-green: #15803D
```

### Caractéristiques
- Interface moderne et fluide
- Design responsive (mobile + desktop)
- Icônes claires et cohérentes
- Tableaux et graphiques interactifs (Chart.js)
- Transitions et animations CSS
- Cards avec hover effects
- Sidebar fixe avec navigation

## 📊 Modèles de Données

### Employe (utilisateur personnalisé)
- Hérite de AbstractUser
- Champs : employee_id, role, departement, telephone, photo
- Autorisations : acces_stocks, acces_caisse, acces_fidelisation, acces_rapports
- ID auto-généré (format: EMP001, EMP002, etc.)

### Produit
- Référence unique, nom, catégorie, prix
- Stock actuel, stock critique
- Statuts : EN_STOCK, CRITIQUE, RUPTURE
- Fournisseur, code-barre
- Calcul automatique du statut

### Vente
- Numéro de transaction auto-généré (format: T241015001)
- Caissier, Client (optionnel)
- Montants : total, TVA, remise, final
- Moyen de paiement
- Numéro de caisse

### LigneVente
- Lien avec Vente et Produit
- Quantité, prix unitaire, montant ligne

### Client
- Informations : nom, prénom, téléphone, email
- Points de fidélité
- Niveau : TOUS, SILVER, GOLD, VIP (calculé automatiquement)
- Total achats, dernière visite

### Autres modèles
- **Promotion** : titre, description, réduction, dates
- **Presence** : employé, date, heures
- **Conge** : employé, type, dates, statut, approbation
- **Formation** : titre, dates, participants
- **Reclamation** : client, sujet, statut, traitement

## 🚀 Installation et Lancement

### Prérequis
```bash
Python 3.8+
Django 5.2+
```

### Installation
```bash
# Cloner le projet
cd PROJET_CARREFOUR

# Installer les dépendances
pip install -r requirements.txt

# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer les données de démonstration
Get-Content create_sample_data.py | python manage.py shell

# Lancer le serveur
python manage.py runserver
```

### Accès à l'application
```
URL: http://127.0.0.1:8000/
```

## 🔐 Identifiants de Test

### Super Administrateur (DG)
```
Username: admin
Password: admin123
Rôle: Directeur Général
Accès: Tous les modules
```

### Autres employés
```
Username: marie / Password: password123 (RH)
Username: jean / Password: password123 (Stock)
Username: fatou / Password: password123 (Caissier)
Username: yao / Password: password123 (Marketing)
Username: ama / Password: password123 (Analyste)
```

## 📁 Structure du Projet

```
PROJET_CARREFOUR/
├── Carrefour/              # Configuration Django
│   ├── settings.py        # Paramètres (DB, STATIC, AUTH_USER_MODEL)
│   ├── urls.py            # URLs principales
│   └── wsgi.py
├── CarrefourApp/           # Application principale
│   ├── models.py          # Modèles de données (10 modèles)
│   ├── views.py           # Vues (15+ vues)
│   ├── urls.py            # Routes de l'app
│   ├── admin.py           # Configuration admin Django
│   └── migrations/        # Migrations de base de données
├── templates/              # Templates HTML
│   ├── home.html          # Page d'accueil
│   ├── login.html         # Connexion
│   ├── about.html         # À propos
│   ├── contact.html       # Contact
│   └── dashboard/         # Dashboards par rôle
│       ├── main.html      # Sélection de profil
│       ├── dg.html        # Dashboard DG (complet)
│       ├── daf.html       # Dashboard DAF
│       ├── rh.html        # Dashboard RH
│       ├── stock.html     # Dashboard Stock
│       ├── caisse.html    # Dashboard Caisse
│       ├── marketing.html # Dashboard Marketing
│       └── analytics.html # Dashboard Analytics
├── static/                 # Fichiers statiques
│   ├── css/
│   │   └── style.css      # Styles personnalisés (450+ lignes)
│   └── js/
├── create_sample_data.py   # Script de données de test
├── requirements.txt        # Dépendances Python
└── README.md              # Ce fichier
```

## 📊 Données de Démonstration

Le script `create_sample_data.py` crée :
- **7 employés** (1 DG + 6 employés variés)
- **10 produits** (alimentaire, hygiène, boissons)
- **2 clients** avec niveaux de fidélité
- **50 ventes** (réparties sur 30 jours)
- **49 présences** (7 jours pour 7 employés)
- **1 promotion** active
- **1 formation** en cours

## 🎯 Flux de Navigation

```
Accueil → Connexion → Sélection de Profil → Dashboard spécifique au rôle
```

### Redirections automatiques selon le rôle:
- `DG` → `/dashboard/dg/`
- `DAF` → `/dashboard/daf/`
- `RH` → `/dashboard/rh/`
- `STOCK` → `/dashboard/stock/`
- `CAISSIER` → `/dashboard/caisse/`
- `MARKETING` → `/dashboard/marketing/`
- `ANALYSTE` → `/dashboard/analytics/`

## 📈 Graphiques et Visualisations

Utilisation de **Chart.js** pour :
- Graphiques en ligne (évolution CA, ventes)
- Graphiques en barres (marges, produits)
- Graphiques en camembert (catégories, paiements)
- Gauges (performance globale)

## 🔧 Technologies Utilisées

- **Backend**: Django 5.2
- **Base de données**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: HTML5, CSS3 (CSS Variables)
- **Graphiques**: Chart.js
- **Icons**: Emojis Unicode
- **Responsive**: CSS Grid & Flexbox

## 🎨 Fonctionnalités UI/UX

- ✅ Design moderne et professionnel
- ✅ Palette de couleurs cohérente (bleu/vert)
- ✅ Navigation intuitive avec sidebar
- ✅ Cards avec effets hover
- ✅ Badges de statut colorés
- ✅ Tableaux interactifs
- ✅ Formulaires stylisés
- ✅ Messages de notification
- ✅ Animations CSS fluides
- ✅ Responsive design (mobile/tablet/desktop)

## 🔒 Sécurité

- Authentification Django intégrée
- Protection CSRF
- Gestion des permissions par rôle
- Autorisations d'accès aux modules
- Mots de passe hashés (PBKDF2)
- Middleware de sécurité Django

## 📝 Notes Importantes

1. **Base de données** : Configurée en SQLite pour le développement. Pour la production, décommenter la configuration PostgreSQL dans `settings.py`.

2. **Fichiers statiques** : En production, exécuter `python manage.py collectstatic`.

3. **Images** : Les dossiers `media/` pour les uploads ne sont pas créés par défaut. Ils seront créés automatiquement au premier upload.

4. **Données de test** : Les données créées sont fictives et à but de démonstration uniquement.

5. **Admin Django** : Accessible via `/admin/` avec les identifiants du super utilisateur.

## 🚧 Développements Futurs

- [ ] Templates complets pour DAF, Stock, Caisse, Marketing, Analytics
- [ ] Formulaires d'ajout/modification (employés, produits, clients)
- [ ] Système de notifications en temps réel
- [ ] Export PDF/Excel des rapports
- [ ] API REST avec Django REST Framework
- [ ] Tests unitaires et d'intégration
- [ ] Déploiement Docker
- [ ] CI/CD avec GitHub Actions

## 📧 Support

Pour toute question ou problème :
- Consulter la documentation Django : https://docs.djangoproject.com/
- Vérifier les logs du serveur dans le terminal
- Consulter `db.sqlite3` avec un viewer SQLite

## 📄 Licence

Ce projet est développé à des fins éducatives dans le cadre du PROJET_CARREFOUR.

---

**Développé avec ❤️ en respectant les maquettes fournies**

🎨 Design: Bleu (#2563EB) & Vert (#28A745)
🏗️ Framework: Django 5.2
📊 Charts: Chart.js
✨ UI: Modern & Professional
