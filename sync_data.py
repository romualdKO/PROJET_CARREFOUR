"""
Script de synchronisation des données entre collègues
Utilisation :
  python sync_data.py export   -> Exporte les données en JSON
  python sync_data.py import   -> Importe les données depuis JSON
"""

import os
import sys
import django
import json
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from django.core import serializers
from CarrefourApp.models import (
    Employe, Produit, Fournisseur, Client, 
    Vente, LigneVente, Transaction, CommandeFournisseur, MouvementStock,
    AlerteStock, TypePaiement, Coupon, LigneTransaction,
    LigneCommandeFournisseur, UtilisationCoupon, Presence,
    Conge, Formation, Paiement, Promotion, SessionPresence, Reclamation
)

# Fichier de sauvegarde
BACKUP_FILE = 'data_backup.json'

def export_data():
    """Exporter toutes les données importantes en JSON"""
    print("🔄 Exportation des données en cours...")
    
    # Liste des modèles à exporter (dans l'ordre des dépendances)
    models_to_export = [
        # Données de base
        ('TypePaiement', TypePaiement),
        ('Employe', Employe),
        
        # Produits et fournisseurs
        ('Fournisseur', Fournisseur),
        ('Produit', Produit),
        
        # Clients et fidélité
        ('Client', Client),
        ('Coupon', Coupon),
        
        # Commandes fournisseurs
        ('CommandeFournisseur', CommandeFournisseur),
        ('LigneCommandeFournisseur', LigneCommandeFournisseur),
        
        # Ventes et transactions
        ('Vente', Vente),
        ('LigneVente', LigneVente),
        ('Transaction', Transaction),
        ('LigneTransaction', LigneTransaction),
        ('UtilisationCoupon', UtilisationCoupon),
        ('Paiement', Paiement),
        
        # Stock et alertes
        ('MouvementStock', MouvementStock),
        ('AlerteStock', AlerteStock),
        
        # RH
        ('SessionPresence', SessionPresence),
        ('Presence', Presence),
        ('Conge', Conge),
        ('Formation', Formation),
        
        # Autres
        ('Promotion', Promotion),
        ('Reclamation', Reclamation),
    ]
    
    all_data = {}
    total_objects = 0
    
    for model_name, model_class in models_to_export:
        try:
            objects = model_class.objects.all()
            count = objects.count()
            
            if count > 0:
                # Sérialiser en JSON
                serialized = serializers.serialize('json', objects, 
                                                  use_natural_foreign_keys=False,
                                                  use_natural_primary_keys=False)
                all_data[model_name] = json.loads(serialized)
                total_objects += count
                print(f"  ✅ {model_name}: {count} objets exportés")
            else:
                print(f"  ⚪ {model_name}: Aucun objet")
                
        except Exception as e:
            print(f"  ❌ Erreur lors de l'export de {model_name}: {str(e)}")
    
    # Sauvegarder dans le fichier
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'export_date': datetime.now().isoformat(),
            'total_objects': total_objects,
            'data': all_data
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Exportation terminée : {total_objects} objets sauvegardés dans '{BACKUP_FILE}'")
    print(f"📦 Taille du fichier : {os.path.getsize(BACKUP_FILE) / 1024:.2f} KB")
    print(f"\n💡 Partagez ce fichier avec votre collègue pour synchroniser les données")


def import_data():
    """Importer les données depuis le fichier JSON"""
    if not os.path.exists(BACKUP_FILE):
        print(f"❌ Erreur : Le fichier '{BACKUP_FILE}' n'existe pas")
        print("   Assurez-vous d'avoir reçu le fichier de votre collègue")
        return
    
    print("🔄 Importation des données en cours...")
    print("⚠️  ATTENTION : Cela va remplacer les données existantes !")
    
    response = input("Voulez-vous continuer ? (oui/non) : ")
    if response.lower() not in ['oui', 'o', 'yes', 'y']:
        print("❌ Importation annulée")
        return
    
    try:
        with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
            backup = json.load(f)
        
        export_date = backup.get('export_date', 'inconnu')
        total_objects = backup.get('total_objects', 0)
        data = backup.get('data', {})
        
        print(f"\n📅 Date d'exportation : {export_date}")
        print(f"📦 Nombre total d'objets : {total_objects}")
        print("\n🔄 Importation en cours...\n")
        
        imported_count = 0
        
        # Importer dans l'ordre
        for model_name, objects in data.items():
            if objects:
                try:
                    # Désérialiser et sauvegarder
                    for obj in serializers.deserialize('json', json.dumps(objects)):
                        obj.save()
                        imported_count += 1
                    
                    print(f"  ✅ {model_name}: {len(objects)} objets importés")
                    
                except Exception as e:
                    print(f"  ❌ Erreur lors de l'import de {model_name}: {str(e)}")
        
        print(f"\n✅ Importation terminée : {imported_count} objets importés")
        
    except json.JSONDecodeError:
        print(f"❌ Erreur : Le fichier '{BACKUP_FILE}' n'est pas un JSON valide")
    except Exception as e:
        print(f"❌ Erreur lors de l'importation : {str(e)}")


def show_help():
    """Afficher l'aide"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║         Script de Synchronisation des Données                ║
╚══════════════════════════════════════════════════════════════╝

📖 UTILISATION :
  python sync_data.py export   -> Exporter les données
  python sync_data.py import   -> Importer les données
  python sync_data.py help     -> Afficher cette aide

📋 WORKFLOW RECOMMANDÉ :

  👤 Personne A (qui a les dernières données) :
    1. python sync_data.py export
    2. Partager 'data_backup.json' avec l'équipe (Git, email, etc.)
  
  👥 Personne B (qui veut synchroniser) :
    1. Récupérer 'data_backup.json'
    2. python sync_data.py import
    3. Continuer à travailler avec les données à jour

⚠️  IMPORTANT :
  - Le fichier 'data_backup.json' contient TOUTES les données
  - L'import remplace les données existantes
  - Faites une sauvegarde avant d'importer
  - Ne commitez PAS 'data_backup.json' sur Git si le fichier est volumineux

💡 ALTERNATIVE :
  Ajoutez 'data_backup.json' au .gitignore et partagez-le autrement
  (Google Drive, OneDrive, email, etc.)
    """)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'export':
        export_data()
    elif command == 'import':
        import_data()
    elif command == 'help':
        show_help()
    else:
        print(f"❌ Commande inconnue : {command}")
        show_help()
        sys.exit(1)
