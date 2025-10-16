# 🔐 Comptes par Défaut - SuperMarché Plus

## 📋 Liste des Comptes

Après l'exécution du script `init_default_accounts.py`, les comptes suivants sont disponibles :

| Rôle | Username | Password | Accès Dashboard | Email |
|------|----------|----------|-----------------|-------|
| **Directeur Général** | `directeur` | `Admin2024!` | `/dashboard/dg/` | directeur@supermarche.com |
| **Directeur Admin & Finance** | `daf` | `Finance2024!` | `/dashboard/daf/` | daf@supermarche.com |
| **Responsable RH** | `rh` | `RH2024!` | `/dashboard/rh/` | rh@supermarche.com |
| **Gestionnaire Stock** | `stock` | `Stock2024!` | `/dashboard/stock/` | stock@supermarche.com |
| **Caissier** | `caisse` | `Caisse2024!` | `/dashboard/caisse/` | caisse@supermarche.com |
| **Responsable Marketing** | `marketing` | `Marketing2024!` | `/dashboard/marketing/` | marketing@supermarche.com |
| **Analyste** | `analyste` | `Analyste2024!` | `/dashboard/analytics/` | analyste@supermarche.com |

## 🚨 Sécurité - IMPORTANT

### ⚠️ Changement des Mots de Passe (OBLIGATOIRE en Production)

**AVANT de déployer en production, vous DEVEZ changer tous les mots de passe par défaut !**

#### Méthode 1 : Via l'Interface Django Admin

1. Aller sur `http://votre-domaine.com/admin/`
2. Se connecter avec un compte superuser
3. Aller dans "Employes"
4. Sélectionner l'employé
5. Cliquer sur "Changer le mot de passe"
6. Entrer un nouveau mot de passe sécurisé

#### Méthode 2 : Via le Shell Django

```python
python manage.py shell

from CarrefourApp.models import Employe

# Changer le mot de passe d'un employé
emp = Employe.objects.get(username='directeur')
emp.set_password('NouveauMotDePasseSecurise123!')
emp.save()

# Répéter pour tous les comptes
```

#### Méthode 3 : Script Python

Créer un fichier `change_passwords.py` :

```python
from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

Employe = get_user_model()

# Nouveaux mots de passe sécurisés
passwords = {
    'directeur': 'VotreMotDePasseSecurise1!',
    'daf': 'VotreMotDePasseSecurise2!',
    'rh': 'VotreMotDePasseSecurise3!',
    'stock': 'VotreMotDePasseSecurise4!',
    'caisse': 'VotreMotDePasseSecurise5!',
    'marketing': 'VotreMotDePasseSecurise6!',
    'analyste': 'VotreMotDePasseSecurise7!',
}

for username, password in passwords.items():
    try:
        emp = Employe.objects.get(username=username)
        emp.set_password(password)
        emp.save()
        print(f"✅ Mot de passe changé pour {username}")
    except Employe.DoesNotExist:
        print(f"❌ Employé {username} non trouvé")
```

Exécuter :
```bash
python change_passwords.py
```

## 🔑 Règles de Mots de Passe Sécurisés

Pour la production, utilisez des mots de passe qui respectent ces critères :

- **Minimum 12 caractères**
- **Au moins une majuscule** (A-Z)
- **Au moins une minuscule** (a-z)
- **Au moins un chiffre** (0-9)
- **Au moins un caractère spécial** (!@#$%^&*)
- **Pas de mots du dictionnaire**
- **Différent pour chaque compte**

### Exemples de Bons Mots de Passe
- `K9#mP2$xL7@qW3!`
- `Tr0piC@l$unSh1ne!`
- `B1u3$kyR@inb0w#`
- `P@ssW0rd!2024$Secure`

### ❌ Exemples de Mauvais Mots de Passe
- `password123` (trop simple)
- `admin` (trop court)
- `Admin2024!` (mot de passe par défaut - NE PAS UTILISER)
- `12345678` (que des chiffres)

## 👥 Détails des Rôles

### 👑 Directeur Général (DG)
**Accès :**
- Vue d'ensemble globale
- Tous les KPIs
- Tous les rapports
- Tous les modules (lecture)

**Responsabilités :**
- Supervision générale
- Décisions stratégiques
- Validation des objectifs
- Analyse de performance

---

### 💼 Directeur Administratif et Financier (DAF)
**Accès :**
- Module Finance
- Rapports financiers
- Analyse des marges
- Trésorerie

**Responsabilités :**
- Gestion financière
- Suivi budgétaire
- Analyse des coûts
- Rapports de rentabilité

---

### 👥 Responsable RH
**Accès :**
- Module RH complet
- Gestion des employés (CRUD)
- Présences automatiques
- Congés et formations
- Planifications

**Responsabilités :**
- Recrutement et intégration
- Configuration des horaires de travail
- Suivi des présences et absences
- Approbation des congés
- Organisation des formations
- Gestion administrative du personnel

---

### 📦 Gestionnaire Stock
**Accès :**
- Module Stock
- Gestion des produits
- Gestion des fournisseurs
- Alertes de rupture
- Inventaires

**Responsabilités :**
- Maintien des niveaux de stock
- Commandes fournisseurs
- Réception marchandises
- Inventaires réguliers
- Gestion des périmés

---

### 💰 Caissier
**Accès :**
- Module Caisse
- Enregistrement des ventes
- Moyens de paiement
- Génération de tickets
- Historique des transactions

**Responsabilités :**
- Encaissement des clients
- Gestion de la caisse
- Service client
- Remise de tickets
- Fermeture de caisse

---

### 💝 Responsable Marketing
**Accès :**
- Module Marketing
- Gestion des clients fidèles
- Création de promotions
- Campagnes marketing
- Statistiques de fidélisation

**Responsabilités :**
- Fidélisation clients
- Création de promotions
- Campagnes publicitaires
- Analyse des ventes
- Programmes de fidélité

---

### 📊 Analyste
**Accès :**
- Module Analyse
- Tous les tableaux de bord
- Tous les graphiques
- Exports de données
- Rapports personnalisés

**Responsabilités :**
- Analyse des données
- Création de rapports
- Prévisions
- Recommandations stratégiques
- Business Intelligence

## 🎯 Configuration des Horaires de Travail

Chaque employé peut avoir des horaires personnalisés :

| Champ | Valeur par Défaut | Description |
|-------|-------------------|-------------|
| **Heure Début** | 08:00 | Heure de début de journée |
| **Heure Fin** | 17:00 | Heure de fin de journée |
| **Pause** | 90 minutes | Durée de la pause déjeuner |

### Modification des Horaires (RH)

1. Se connecter en tant que RH
2. Aller dans "Employés"
3. Cliquer sur "✏️ Modifier" pour l'employé
4. Configurer les horaires dans la section "Configuration des Horaires de Travail"
5. Enregistrer

## 📝 Système de Présence Automatique

### Comment ça Fonctionne

1. **Connexion** : L'employé se connecte pendant ses horaires de travail
   - ✅ Présence créée automatiquement avec heure d'arrivée

2. **Travail** : L'employé utilise l'application normalement

3. **Déconnexion** : L'employé se déconnecte en fin de journée
   - ✅ Heure de départ enregistrée automatiquement
   - ✅ Statut calculé automatiquement (Présent/Retard/Absent)

### Règles de Calcul du Statut

- 🟢 **PRÉSENT** : Arrivée ≤ 15 min de retard + au moins 60% des heures travaillées
- 🟡 **RETARD** : Arrivée 16-60 min de retard + au moins 60% des heures travaillées
- 🔴 **ABSENT** : Arrivée > 60 min de retard OU moins de 60% des heures travaillées

## 🔄 Création de Nouveaux Comptes

Le RH peut créer de nouveaux employés via l'interface :

1. Se connecter en tant que RH
2. Aller dans "Nouvel Employé"
3. Remplir le formulaire :
   - Username (unique)
   - Password (min 8 caractères)
   - Informations personnelles
   - Rôle et département
   - **Horaires de travail** (nouveau)
4. Enregistrer

L'ID employé est généré automatiquement : `EMP-YYYYMMDD-XXX`

## 🆘 Support

Pour assistance sur les comptes :
- 📧 Email : support@supermarche-plus.com
- 📞 Téléphone : +225 XX XX XX XX

---

**⚠️ RAPPEL IMPORTANT :** Changez TOUS les mots de passe par défaut avant la mise en production !

**Version** : 1.0.0  
**Date** : Octobre 2025
