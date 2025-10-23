"""
Script pour corriger les problèmes d'intégrité référentielle avant la migration
"""
import os
import django
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from django.db import connection

def fix_integrity_issues():
    """Supprime les enregistrements avec des références invalides"""
    with connection.cursor() as cursor:
        print("🔍 Vérification des problèmes d'intégrité...")
        
        # 1. Vérifier et supprimer les mouvements de stock avec produits inexistants
        cursor.execute("""
            SELECT COUNT(*) FROM CarrefourApp_mouvementstock 
            WHERE produit_id NOT IN (SELECT id FROM CarrefourApp_produit)
        """)
        count_mouvements = cursor.fetchone()[0]
        
        if count_mouvements > 0:
            print(f"⚠️  Trouvé {count_mouvements} mouvement(s) de stock avec références invalides")
            cursor.execute("""
                DELETE FROM CarrefourApp_mouvementstock 
                WHERE produit_id NOT IN (SELECT id FROM CarrefourApp_produit)
            """)
            print(f"✅ {count_mouvements} mouvement(s) de stock supprimé(s)")
        else:
            print("✅ Aucun problème trouvé dans CarrefourApp_mouvementstock")
        
        # 2. Vérifier et supprimer les lignes de vente avec produits inexistants
        cursor.execute("""
            SELECT COUNT(*) FROM CarrefourApp_lignevente 
            WHERE produit_id NOT IN (SELECT id FROM CarrefourApp_produit)
        """)
        count_lignes = cursor.fetchone()[0]
        
        if count_lignes > 0:
            print(f"⚠️  Trouvé {count_lignes} ligne(s) de vente avec références invalides")
            cursor.execute("""
                DELETE FROM CarrefourApp_lignevente 
                WHERE produit_id NOT IN (SELECT id FROM CarrefourApp_produit)
            """)
            print(f"✅ {count_lignes} ligne(s) de vente supprimée(s)")
        else:
            print("✅ Aucun problème trouvé dans CarrefourApp_lignevente")
        
        # 3. Vérifier et supprimer les lignes de commande avec produits inexistants
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM CarrefourApp_lignecommandefournisseur 
                WHERE produit_id NOT IN (SELECT id FROM CarrefourApp_produit)
            """)
            count_commandes = cursor.fetchone()[0]
            
            if count_commandes > 0:
                print(f"⚠️  Trouvé {count_commandes} ligne(s) de commande avec références invalides")
                cursor.execute("""
                    DELETE FROM CarrefourApp_lignecommandefournisseur 
                    WHERE produit_id NOT IN (SELECT id FROM CarrefourApp_produit)
                """)
                print(f"✅ {count_commandes} ligne(s) de commande supprimée(s)")
            else:
                print("✅ Aucun problème trouvé dans CarrefourApp_lignecommandefournisseur")
        except Exception as e:
            print(f"⚠️  Table CarrefourApp_lignecommandefournisseur non vérifiée: {e}")
        
        print("\n✅ Nettoyage terminé!")
        print("Vous pouvez maintenant relancer: python manage.py migrate")

if __name__ == '__main__':
    try:
        fix_integrity_issues()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
