import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from CarrefourApp.models import Employe

def create_default_accounts():
    """Crée les comptes par défaut pour DG, DAF et RH"""
    
    # Compte DG par défaut
    if not Employe.objects.filter(username='dg').exists():
        dg = Employe.objects.create_user(
            username='dg',
            email='dg@supermarche.com',
            password='DG2025@Admin',
            first_name='Directeur',
            last_name='Général',
            role='DG',
            acces_dashboard_dg=True,
            acces_dashboard_daf=False,
            acces_dashboard_rh=False,
            acces_dashboard_stock=False
        )
        print("✅ Compte DG créé - Identifiant: dg / Mot de passe: DG2025@Admin")
    else:
        print("ℹ️  Compte DG existe déjà")
    
    # Compte DAF par défaut
    if not Employe.objects.filter(username='daf').exists():
        daf = Employe.objects.create_user(
            username='daf',
            email='daf@supermarche.com',
            password='DAF2025@Admin',
            first_name='Directeur',
            last_name='Financier',
            role='DAF',
            acces_dashboard_dg=False,
            acces_dashboard_daf=True,
            acces_dashboard_rh=False,
            acces_dashboard_stock=False
        )
        print("✅ Compte DAF créé - Identifiant: daf / Mot de passe: DAF2025@Admin")
    else:
        print("ℹ️  Compte DAF existe déjà")
    
    # Compte RH par défaut
    if not Employe.objects.filter(username='rh').exists():
        rh = Employe.objects.create_user(
            username='rh',
            email='rh@supermarche.com',
            password='RH2025@Admin',
            first_name='Responsable',
            last_name='RH',
            role='RH',
            acces_dashboard_dg=False,
            acces_dashboard_daf=False,
            acces_dashboard_rh=True,
            acces_dashboard_stock=False
        )
        print("✅ Compte RH créé - Identifiant: rh / Mot de passe: RH2025@Admin")
    else:
        print("ℹ️  Compte RH existe déjà")
    
    print("\n" + "="*60)
    print("COMPTES PAR DÉFAUT")
    print("="*60)
    print("DG  -> Identifiant: dg  | Mot de passe: DG2025@Admin")
    print("DAF -> Identifiant: daf | Mot de passe: DAF2025@Admin")
    print("RH  -> Identifiant: rh  | Mot de passe: RH2025@Admin")
    print("="*60)

if __name__ == '__main__':
    create_default_accounts()
