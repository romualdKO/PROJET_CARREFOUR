"""
Script de test pour vérifier l'authentification des comptes par défaut
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from django.contrib.auth import authenticate
from CarrefourApp.models import Employe

def test_authentication():
    """Teste l'authentification de tous les comptes par défaut"""
    
    print("\n" + "="*70)
    print("TEST D'AUTHENTIFICATION DES COMPTES PAR DÉFAUT")
    print("="*70 + "\n")
    
    comptes = [
        {'username': 'dg', 'password': 'DG2025@Admin', 'role': 'DG'},
        {'username': 'daf', 'password': 'DAF2025@Admin', 'role': 'DAF'},
        {'username': 'rh', 'password': 'RH2025@Admin', 'role': 'RH'},
    ]
    
    resultats = {'success': 0, 'failed': 0}
    
    for compte in comptes:
        username = compte['username']
        password = compte['password']
        role_attendu = compte['role']
        
        print(f"Test du compte : {username.upper()}")
        print(f"  Identifiant : {username}")
        print(f"  Mot de passe : {password}")
        
        # Test 1 : Vérifier que le compte existe
        try:
            employe = Employe.objects.get(username=username)
            print(f"  ✅ Compte trouvé dans la base de données")
            print(f"     - Nom : {employe.get_full_name()}")
            print(f"     - Rôle : {employe.get_role_display()}")
            print(f"     - Email : {employe.email}")
            print(f"     - Actif : {'Oui' if employe.est_actif else 'Non'}")
            print(f"     - Staff : {'Oui' if employe.is_staff else 'Non'}")
        except Employe.DoesNotExist:
            print(f"  ❌ ERREUR : Compte non trouvé !")
            resultats['failed'] += 1
            print()
            continue
        
        # Test 2 : Tester l'authentification
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                print(f"  ✅ AUTHENTIFICATION RÉUSSIE")
                print(f"     Le compte {username} peut se connecter avec succès")
                resultats['success'] += 1
            else:
                print(f"  ❌ ERREUR : Compte inactif !")
                resultats['failed'] += 1
        else:
            print(f"  ❌ ERREUR : Authentification échouée !")
            print(f"     Le mot de passe ne correspond pas ou le compte n'existe pas")
            
            # Informations de débogage
            try:
                employe = Employe.objects.get(username=username)
                print(f"     Débogage :")
                print(f"     - Compte existe : Oui")
                print(f"     - is_active : {employe.is_active}")
                print(f"     - Suggestion : Exécutez 'python reset_default_passwords.py'")
            except:
                print(f"     Débogage : Compte inexistant")
            
            resultats['failed'] += 1
        
        print()
    
    # Résumé
    print("="*70)
    print("RÉSUMÉ DES TESTS")
    print("="*70)
    print(f"✅ Réussis : {resultats['success']}/{len(comptes)}")
    print(f"❌ Échoués : {resultats['failed']}/{len(comptes)}")
    print("="*70)
    
    if resultats['success'] == len(comptes):
        print("\n🎉 TOUS LES TESTS SONT RÉUSSIS !")
        print("✅ Tous les comptes peuvent se connecter avec succès")
        print("\n📋 Partagez ces identifiants avec vos collaborateurs :")
        print("\n┌─────┬─────────────┬──────────────────┐")
        print("│ Rôle│ Identifiant │ Mot de passe     │")
        print("├─────┼─────────────┼──────────────────┤")
        print("│ DG  │ dg          │ DG2025@Admin     │")
        print("│ DAF │ daf         │ DAF2025@Admin    │")
        print("│ RH  │ rh          │ RH2025@Admin     │")
        print("└─────┴─────────────┴──────────────────┘")
    else:
        print("\n⚠️  ATTENTION : Certains tests ont échoué !")
        print("💡 Solution : Exécutez le script suivant pour réinitialiser les mots de passe :")
        print("   python reset_default_passwords.py")
    
    print()

if __name__ == '__main__':
    test_authentication()
