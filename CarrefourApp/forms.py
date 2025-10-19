#ajout Produit PROJET_CARREFOUR/CarrefourApp/migrations/forms.py
from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
            'idProduit',
            'nom',
            'description',
            'prixAchat',
            'prixVente',
            'quantite',
            'image',
            'categorie'
        ]
