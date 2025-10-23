"""
Script de test de connexion
Vérifie si les comptes fonctionnent correctement
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from django.contrib.auth import authenticate
from CarrefourApp.models import Employe

def test_login():
    """Test de connexion pour tous les comptes par défaut"""
    print("\n" + "="*70)
    print("🔐 TEST DE CONNEXION DES COMPTES PAR DÉFAUT")
    print("="*70 + "\n")
    
    comptes_test = [
        ('dg', 'DG2025@Admin'),
        ('daf', 'DAF2025@Admin'),
        ('rh', 'RH2025@Admin'),
        ('stock', 'Stock2025'),
        ('caissier', 'Caissier2025'),
        ('marketing', 'Marketing2025'),
    ]
    
    resultats = []
    
    for username, password in comptes_test:
        # Test d'authentification
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Succès
            employe = Employe.objects.get(username=username)
            status = "✅ SUCCÈS"
            details = f"Rôle: {employe.get_role_display()}, Actif: {employe.est_actif}"
            resultats.append((username, True))
        else:
            # Échec
            status = "❌ ÉCHEC"
            # Vérifier si le compte existe
            if Employe.objects.filter(username=username).exists():
                details = "Compte existe mais mot de passe incorrect"
            else:
                details = "Compte n'existe pas"
            resultats.append((username, False))
        
        print(f"{status} | {username:12} | {password:15} | {details}")
    
    # Résumé
    print("\n" + "="*70)
    succes = sum(1 for _, ok in resultats if ok)
    total = len(resultats)
    
    if succes == total:
        print(f"🎉 TOUS LES TESTS RÉUSSIS ({succes}/{total})")
        print("\n✅ Vous pouvez vous connecter avec n'importe quel compte ci-dessus")
        print("📍 URL: http://127.0.0.1:8000/login/")
    else:
        print(f"⚠️  CERTAINS TESTS ONT ÉCHOUÉ ({total - succes}/{total} échecs)")
        print("\n💡 Solutions:")
        print("  1. Exécutez: python setup_after_clone.py")
        print("  2. Ou exécutez: python reset_default_passwords.py")
    
    print("="*70 + "\n")
    
    return succes == total

if __name__ == '__main__':
    test_login()
