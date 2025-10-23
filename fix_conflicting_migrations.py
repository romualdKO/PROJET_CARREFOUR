"""
Script pour résoudre les migrations conflictuelles
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

def fix_migrations():
    """Marque les migrations conflictuelles comme appliquées"""
    recorder = MigrationRecorder(connection)
    
    # Liste des migrations à faker
    migrations_to_fake = [
        ('CarrefourApp', '0005_remove_promotion_produits_remove_vente_caissier_and_more'),
        ('CarrefourApp', '0006_categorie_fournisseur_commandeapprovisionnement_and_more'),
        ('CarrefourApp', '0007_remove_produit_imageurl_produit_image'),
        ('CarrefourApp', '0008_remove_produit_code'),
        ('CarrefourApp', '0016_merge_20251023_0853'),
    ]
    
    print("🔧 Résolution des migrations conflictuelles...\n")
    
    for app_name, migration_name in migrations_to_fake:
        # Vérifier si la migration est déjà enregistrée
        exists = recorder.migration_qs.filter(
            app=app_name,
            name=migration_name
        ).exists()
        
        if not exists:
            print(f"✅ Marquage de {migration_name} comme appliquée...")
            recorder.record_applied(app_name, migration_name)
        else:
            print(f"⏭️  {migration_name} déjà marquée comme appliquée")
    
    print("\n✅ Résolution terminée!")
    print("\nVérifiez maintenant avec: python manage.py showmigrations CarrefourApp")

if __name__ == '__main__':
    try:
        fix_migrations()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
