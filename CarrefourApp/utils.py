from django.db.models import Max
from .models import Produit
# Utility function to generate a unique product ID
def generer_id_produit():
    dernier = Produit.objects.aggregate(max_id=Max('idProduit'))['max_id']
    if dernier:
        num = int(dernier.replace('PROD', '')) + 1
    else:
        num = 1
    return f'PROD{num:03d}'
