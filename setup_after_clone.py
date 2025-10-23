"""
Script de configuration après clonage du projet
Crée tous les comptes et données nécessaires
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from CarrefourApp.models import Employe, TypePaiement
from django.contrib.auth.hashers import make_password

def create_payment_types():
    """Crée les types de paiement par défaut"""
    print("\n" + "="*60)
    print("📝 CRÉATION DES TYPES DE PAIEMENT")
    print("="*60)
    
    types_paiement = [
        {'nom': 'Espèces', 'code': 'ESPECES'},
        {'nom': 'Carte Bancaire', 'code': 'CB'},
        {'nom': 'Carte de Crédit', 'code': 'CREDIT'},
        {'nom': 'Mobile Money', 'code': 'MOBILE'},
        {'nom': 'Chèque', 'code': 'CHEQUE'},
    ]
    
    for tp_data in types_paiement:
        tp, created = TypePaiement.objects.get_or_create(
            code=tp_data['code'],
            defaults={'nom': tp_data['nom']}
        )
        if created:
            print(f"  ✅ Type de paiement créé: {tp_data['nom']}")
        else:
            print(f"  ⏭️  Type de paiement existant: {tp_data['nom']}")

def create_default_accounts():
    """Crée les comptes par défaut pour DG, DAF, RH, Stock, Caissier, Marketing"""
    print("\n" + "="*60)
    print("👥 CRÉATION DES COMPTES PAR DÉFAUT")
    print("="*60)
    
    comptes = [
        {
            'username': 'dg',
            'email': 'dg@carrefour.com',
            'password': 'DG2025@Admin',
            'first_name': 'Directeur',
            'last_name': 'Général',
            'role': 'DG',
            'departement': 'DIRECTION',
            'employee_id': 'EMP001',
            'est_compte_systeme': True,
            'acces_stocks': True,
            'acces_caisse': True,
            'acces_fidelisation': True,
            'acces_rapports': True,
        },
        {
            'username': 'daf',
            'email': 'daf@carrefour.com',
            'password': 'DAF2025@Admin',
            'first_name': 'Directeur',
            'last_name': 'Financier',
            'role': 'DAF',
            'departement': 'FINANCE',
            'employee_id': 'EMP002',
            'est_compte_systeme': True,
            'acces_stocks': True,
            'acces_caisse': True,
            'acces_fidelisation': True,
            'acces_rapports': True,
        },
        {
            'username': 'rh',
            'email': 'rh@carrefour.com',
            'password': 'RH2025@Admin',
            'first_name': 'Responsable',
            'last_name': 'RH',
            'role': 'RH',
            'departement': 'RH',
            'employee_id': 'EMP003',
            'est_compte_systeme': True,
            'acces_stocks': False,
            'acces_caisse': False,
            'acces_fidelisation': False,
            'acces_rapports': True,
        },
        {
            'username': 'stock',
            'email': 'stock@carrefour.com',
            'password': 'Stock2025',
            'first_name': 'Gestionnaire',
            'last_name': 'Stock',
            'role': 'STOCK',
            'departement': 'LOGISTIQUE',
            'employee_id': 'EMP004',
            'est_compte_systeme': False,
            'acces_stocks': True,
            'acces_caisse': False,
            'acces_fidelisation': False,
            'acces_rapports': False,
        },
        {
            'username': 'caissier',
            'email': 'caissier@carrefour.com',
            'password': 'Caissier2025',
            'first_name': 'Caissier',
            'last_name': 'Principal',
            'role': 'CAISSIER',
            'departement': 'VENTES',
            'employee_id': 'EMP005',
            'est_compte_systeme': False,
            'acces_stocks': False,
            'acces_caisse': True,
            'acces_fidelisation': True,
            'acces_rapports': False,
        },
        {
            'username': 'marketing',
            'email': 'marketing@carrefour.com',
            'password': 'Marketing2025',
            'first_name': 'Responsable',
            'last_name': 'Marketing',
            'role': 'MARKETING',
            'departement': 'MARKETING',
            'employee_id': 'EMP006',
            'est_compte_systeme': False,
            'acces_stocks': False,
            'acces_caisse': False,
            'acces_fidelisation': True,
            'acces_rapports': True,
        },
    ]
    
    for compte_data in comptes:
        username = compte_data.pop('username')
        password = compte_data.pop('password')
        
        if Employe.objects.filter(username=username).exists():
            print(f"  ⏭️  Compte existant: {username}")
            continue
        
        # Créer l'utilisateur
        employe = Employe.objects.create(
            username=username,
            password=make_password(password),
            is_staff=True if compte_data['role'] in ['DG', 'DAF', 'RH'] else False,
            is_superuser=True if compte_data['role'] == 'DG' else False,
            **compte_data
        )
        print(f"  ✅ Compte créé: {username} | Mot de passe: {password}")

def display_credentials():
    """Affiche les identifiants de connexion"""
    print("\n" + "="*60)
    print("🔑 IDENTIFIANTS DE CONNEXION")
    print("="*60)
    print("\n📍 URL: http://127.0.0.1:8000/login/\n")
    
    comptes = [
        ("Directeur Général (DG)", "dg", "DG2025@Admin"),
        ("Directeur Financier (DAF)", "daf", "DAF2025@Admin"),
        ("Responsable RH", "rh", "RH2025@Admin"),
        ("Gestionnaire Stock", "stock", "Stock2025"),
        ("Caissier", "caissier", "Caissier2025"),
        ("Marketing", "marketing", "Marketing2025"),
    ]
    
    for titre, username, password in comptes:
        print(f"┌{'─'*58}┐")
        print(f"│ {titre:<56} │")
        print(f"├{'─'*58}┤")
        print(f"│  Identifiant : {username:<43} │")
        print(f"│  Mot de passe: {password:<43} │")
        print(f"└{'─'*58}┘\n")
    
    print("="*60)
    print("⚠️  ATTENTION:")
    print("  • Les mots de passe sont SENSIBLES à la casse")
    print("  • Les identifiants sont en minuscules")
    print("="*60)

def main():
    print("\n" + "="*60)
    print("🚀 CONFIGURATION APRÈS CLONAGE DU PROJET CARREFOUR")
    print("="*60)
    
    try:
        # Vérifier si la base de données existe
        if not os.path.exists('db.sqlite3'):
            print("\n⚠️  Base de données non trouvée!")
            print("Veuillez d'abord exécuter: python manage.py migrate")
            sys.exit(1)
        
        # Créer les types de paiement
        create_payment_types()
        
        # Créer les comptes par défaut
        create_default_accounts()
        
        # Afficher les identifiants
        display_credentials()
        
        print("\n✅ CONFIGURATION TERMINÉE AVEC SUCCÈS!")
        print("\nVous pouvez maintenant:")
        print("  1. Lancer le serveur: python manage.py runserver")
        print("  2. Accéder à: http://127.0.0.1:8000/login/")
        print("  3. Utiliser les identifiants ci-dessus\n")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
