"""
Script pour résoudre le problème de migrations conflictuelles
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

def main():
    print("=" * 60)
    print("🔧 RÉSOLUTION DES MIGRATIONS CONFLICTUELLES")
    print("=" * 60)
    
    recorder = MigrationRecorder(connection)
    
    # Afficher les migrations actuellement appliquées
    print("\n📋 Migrations actuellement enregistrées:")
    applied = recorder.migration_qs.filter(app='CarrefourApp').order_by('id')
    for mig in applied:
        print(f"  ✓ {mig.name}")
    
    print("\n" + "=" * 60)
    print("💡 ANALYSE DU PROBLÈME")
    print("=" * 60)
    print("""
Vous avez deux branches parallèles de migrations:
  
Branch A (déjà appliquée):
  0005_employe_est_compte_systeme
  0006_fournisseur_alertestock_commandefournisseur_and_more
  0007_produit_description_produit_est_actif_and_more
  0008_auto_20251017_2255
  ...jusqu'à 0015

Branch B (non appliquée):
  0005_remove_promotion_produits_remove_vente_caissier_and_more
  0006_categorie_fournisseur_commandeapprovisionnement_and_more
  0007_remove_produit_imageurl_produit_image
  0008_remove_produit_code
  0016_merge (fusion des deux branches)

Solution: Marquer la branche B comme "fake" (déjà appliquée)
car les changements ont probablement déjà été faits manuellement.
""")
    
    response = input("\n❓ Voulez-vous marquer ces migrations comme appliquées? (oui/non): ").strip().lower()
    
    if response not in ['oui', 'o', 'yes', 'y']:
        print("❌ Opération annulée.")
        return
    
    # Migrations à faker
    migrations_to_fake = [
        '0005_remove_promotion_produits_remove_vente_caissier_and_more',
        '0006_categorie_fournisseur_commandeapprovisionnement_and_more',
        '0007_remove_produit_imageurl_produit_image',
        '0008_remove_produit_code',
        '0016_merge_20251023_0853',
    ]
    
    print("\n" + "=" * 60)
    print("🚀 APPLICATION DES CORRECTIONS")
    print("=" * 60)
    
    for migration_name in migrations_to_fake:
        exists = recorder.migration_qs.filter(
            app='CarrefourApp',
            name=migration_name
        ).exists()
        
        if not exists:
            print(f"  ✅ Marquage: {migration_name}")
            recorder.record_applied('CarrefourApp', migration_name)
        else:
            print(f"  ⏭️  Déjà appliquée: {migration_name}")
    
    print("\n" + "=" * 60)
    print("✅ RÉSOLUTION TERMINÉE!")
    print("=" * 60)
    print("\n📝 Prochaines étapes:")
    print("  1. Vérifiez: python manage.py showmigrations CarrefourApp")
    print("  2. Si tout est OK: python manage.py runserver")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Opération annulée par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
