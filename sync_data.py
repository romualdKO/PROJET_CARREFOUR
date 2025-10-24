"""
Script pour exporter/importer les données importantes entre collaborateurs
Usage:
    python sync_data.py export  -> Crée data_export.json avec vos données
    python sync_data.py import  -> Importe les données de data_export.json
"""
import os
import django
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from CarrefourApp.models import Employe, Produit, Fournisseur, Client, Categorie

def export_data():
    """Exporter les données importantes dans un fichier JSON"""
    print("📤 Export des données...")
    
    data = {
        'export_date': datetime.now().isoformat(),
        'produits': [],
        'fournisseurs': [],
        'clients': [],
        'employes': []
    }
    
    # Export Produits
    for p in Produit.objects.all():
        data['produits'].append({
            'nom': p.nom,
            'code_barre': p.code_barre,
            'prix_unitaire': float(p.prix_unitaire),
            'stock_actuel': p.stock_actuel,
            'categorie': p.categorie,
            'description': p.description or ''
        })
    
    # Export Fournisseurs
    for f in Fournisseur.objects.all():
        data['fournisseurs'].append({
            'nom': f.nom,
            'email': f.email,
            'telephone': f.telephone,
            'adresse': f.adresse
        })
    
    # Export Clients (sauf système)
    for c in Client.objects.filter(telephone__isnull=False).exclude(telephone='SYSTEM'):
        data['clients'].append({
            'nom': c.nom,
            'telephone': c.telephone,
            'email': c.email or '',
            'niveau_fidelite': c.niveau_fidelite,
            'total_achats': float(c.total_achats)
        })
    
    # Export Employés (sans mots de passe)
    for e in Employe.objects.all():
        data['employes'].append({
            'username': e.username,
            'first_name': e.first_name,
            'last_name': e.last_name,
            'email': e.email,
            'employee_id': e.employee_id,
            'role': e.role,
            'departement': e.departement,
            'telephone': e.telephone
        })
    
    with open('data_export.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Données exportées dans data_export.json")
    print(f"   - {len(data['produits'])} produits")
    print(f"   - {len(data['fournisseurs'])} fournisseurs")
    print(f"   - {len(data['clients'])} clients")
    print(f"   - {len(data['employes'])} employés")
    print("\n💡 Envoyez ce fichier à votre collègue via WhatsApp/Email")


def import_data():
    """Importer les données depuis le fichier JSON"""
    print("📥 Import des données...")
    
    if not os.path.exists('data_export.json'):
        print("❌ Fichier data_export.json introuvable!")
        return
    
    with open('data_export.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📅 Export créé le: {data['export_date']}")
    
    # Import Fournisseurs
    for f_data in data['fournisseurs']:
        Fournisseur.objects.get_or_create(
            nom=f_data['nom'],
            defaults={
                'email': f_data['email'],
                'telephone': f_data['telephone'],
                'adresse': f_data['adresse']
            }
        )
    print(f"✅ {len(data['fournisseurs'])} fournisseurs importés")
    
    # Import Produits
    for p_data in data['produits']:
        Produit.objects.update_or_create(
            code_barre=p_data['code_barre'],
            defaults={
                'nom': p_data['nom'],
                'prix_unitaire': p_data['prix_unitaire'],
                'stock_actuel': p_data['stock_actuel'],
                'categorie': p_data['categorie'],
                'description': p_data['description']
            }
        )
    print(f"✅ {len(data['produits'])} produits importés")
    
    # Import Clients
    for c_data in data['clients']:
        Client.objects.update_or_create(
            telephone=c_data['telephone'],
            defaults={
                'nom': c_data['nom'],
                'email': c_data['email'],
                'niveau_fidelite': c_data['niveau_fidelite'],
                'total_achats': c_data['total_achats']
            }
        )
    print(f"✅ {len(data['clients'])} clients importés")
    
    print("\n✅ Import terminé avec succès!")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python sync_data.py [export|import]")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action == 'export':
        export_data()
    elif action == 'import':
        import_data()
    else:
        print("❌ Action invalide. Utilisez 'export' ou 'import'")
