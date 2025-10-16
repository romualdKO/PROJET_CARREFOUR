"""
Script pour réinitialiser les mots de passe des comptes par défaut
Utiliser ce script pour créer ou mettre à jour les comptes DG, DAF et RH
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from CarrefourApp.models import Employe

def reset_default_passwords():
    """Crée ou met à jour les mots de passe des comptes par défaut"""
    
    print("\n" + "="*70)
    print("RÉINITIALISATION DES MOTS DE PASSE PAR DÉFAUT")
    print("="*70 + "\n")
    
    # Compte DG
    try:
        dg = Employe.objects.get(username='dg')
        dg.set_password('DG2025@Admin')
        dg.is_staff = True
        dg.is_superuser = True
        dg.role = 'DG'
        dg.est_actif = True
        dg.save()
        print("✅ Compte DG mis à jour")
        print(f"   Identifiant: dg")
        print(f"   Mot de passe: DG2025@Admin")
        print(f"   Rôle: {dg.get_role_display()}")
    except Employe.DoesNotExist:
        dg = Employe.objects.create_user(
            username='dg',
            email='dg@carrefour.com',
            password='DG2025@Admin',
            first_name='Directeur',
            last_name='Général',
            role='DG',
            is_staff=True,
            is_superuser=True,
            est_actif=True
        )
        print("✅ Compte DG créé")
        print(f"   Identifiant: dg")
        print(f"   Mot de passe: DG2025@Admin")
    
    print()
    
    # Compte DAF
    try:
        daf = Employe.objects.get(username='daf')
        daf.set_password('DAF2025@Admin')
        daf.is_staff = True
        daf.role = 'DAF'
        daf.est_actif = True
        daf.save()
        print("✅ Compte DAF mis à jour")
        print(f"   Identifiant: daf")
        print(f"   Mot de passe: DAF2025@Admin")
        print(f"   Rôle: {daf.get_role_display()}")
    except Employe.DoesNotExist:
        daf = Employe.objects.create_user(
            username='daf',
            email='daf@carrefour.com',
            password='DAF2025@Admin',
            first_name='Directeur',
            last_name='Financier',
            role='DAF',
            is_staff=True,
            est_actif=True
        )
        print("✅ Compte DAF créé")
        print(f"   Identifiant: daf")
        print(f"   Mot de passe: DAF2025@Admin")
    
    print()
    
    # Compte RH
    try:
        rh = Employe.objects.get(username='rh')
        rh.set_password('RH2025@Admin')
        rh.is_staff = True
        rh.role = 'RH'
        rh.est_actif = True
        rh.save()
        print("✅ Compte RH mis à jour")
        print(f"   Identifiant: rh")
        print(f"   Mot de passe: RH2025@Admin")
        print(f"   Rôle: {rh.get_role_display()}")
    except Employe.DoesNotExist:
        rh = Employe.objects.create_user(
            username='rh',
            email='rh@carrefour.com',
            password='RH2025@Admin',
            first_name='Responsable',
            last_name='Ressources Humaines',
            role='RH',
            is_staff=True,
            est_actif=True
        )
        print("✅ Compte RH créé")
        print(f"   Identifiant: rh")
        print(f"   Mot de passe: RH2025@Admin")
    
    print("\n" + "="*70)
    print("RÉSUMÉ DES COMPTES PAR DÉFAUT")
    print("="*70)
    print("┌─────┬─────────────┬──────────────────┬─────────────────────────────┐")
    print("│ Rôle│ Identifiant │ Mot de passe     │ Email                       │")
    print("├─────┼─────────────┼──────────────────┼─────────────────────────────┤")
    print("│ DG  │ dg          │ DG2025@Admin     │ dg@carrefour.com            │")
    print("│ DAF │ daf         │ DAF2025@Admin    │ daf@carrefour.com           │")
    print("│ RH  │ rh          │ RH2025@Admin     │ rh@carrefour.com            │")
    print("└─────┴─────────────┴──────────────────┴─────────────────────────────┘")
    print("="*70)
    print("\n⚠️  IMPORTANT: Communiquez ces identifiants à vos collaborateurs")
    print("⚠️  Les mots de passe sont sensibles à la casse (majuscules/minuscules)")
    print("\n✅ Tous les comptes sont maintenant opérationnels !\n")

if __name__ == '__main__':
    reset_default_passwords()
