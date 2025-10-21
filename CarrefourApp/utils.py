from django.db.models import Max
from .models_stock import *

# Utility function to generate a unique product ID
def generer_id_produit():
    dernier = Produit.objects.aggregate(max_id=Max('idProduit'))['max_id']
    if dernier:
        num = int(dernier.replace('PROD', '')) + 1
    else:
        num = 1
    return f'PROD{num:03d}'
# Utility function to generate a unique supplier ID
def generer_id_fournisseur():
    dernier_fournisseur = Fournisseur.objects.order_by('-idFournisseur').first()
    if dernier_fournisseur:
        dernier_id = int(dernier_fournisseur.idFournisseur.replace('FOUR', ''))
        nouveau_id = dernier_id + 1
    else:
        nouveau_id = 1
    return f"FOUR{nouveau_id:03d}"


