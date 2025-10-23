"""
🚀 INSTALLATION AUTOMATIQUE APRÈS CLONAGE
Exécute toutes les étapes nécessaires en une seule commande
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n{'='*70}")
    print(f"📌 {description}")
    print(f"{'='*70}")
    print(f"Commande: {command}\n")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution:")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    print("\n" + "="*70)
    print("🚀 INSTALLATION AUTOMATIQUE DU PROJET CARREFOUR")
    print("="*70)
    print("\nCe script va configurer automatiquement votre environnement.\n")
    
    # Vérifier si on est dans le bon dossier
    if not os.path.exists('manage.py'):
        print("❌ ERREUR: manage.py non trouvé!")
        print("Veuillez exécuter ce script depuis le dossier racine du projet.")
        sys.exit(1)
    
    print("✅ Dossier du projet détecté")
    
    # Étape 1: Migrations
    print("\n" + "="*70)
    print("ÉTAPE 1/3 : Création de la base de données")
    print("="*70)
    
    if not run_command("python manage.py migrate", "Application des migrations"):
        print("\n⚠️  Les migrations ont échoué. Continuer quand même? (o/n)")
        if input().lower() != 'o':
            sys.exit(1)
    
    # Étape 2: Création des comptes
    print("\n" + "="*70)
    print("ÉTAPE 2/3 : Création des comptes par défaut")
    print("="*70)
    
    if not run_command("python setup_after_clone.py", "Création des comptes"):
        print("\n❌ La création des comptes a échoué!")
        sys.exit(1)
    
    # Étape 3: Test des connexions
    print("\n" + "="*70)
    print("ÉTAPE 3/3 : Test des connexions")
    print("="*70)
    
    run_command("python test_connexion.py", "Vérification des comptes")
    
    # Résumé final
    print("\n" + "="*70)
    print("✅ INSTALLATION TERMINÉE AVEC SUCCÈS!")
    print("="*70)
    print("\n📋 Prochaines étapes:\n")
    print("1️⃣  Lancer le serveur:")
    print("   python manage.py runserver\n")
    print("2️⃣  Accéder à l'application:")
    print("   http://127.0.0.1:8000/login/\n")
    print("3️⃣  Se connecter avec un compte:")
    print("   • DG       : dg / DG2025@Admin")
    print("   • DAF      : daf / DAF2025@Admin")
    print("   • RH       : rh / RH2025@Admin")
    print("   • Stock    : stock / Stock2025")
    print("   • Caissier : caissier / Caissier2025")
    print("   • Marketing: marketing / Marketing2025")
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Installation annulée par l'utilisateur.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERREUR INATTENDUE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
