from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from .models import (
    Employe, Produit, Fournisseur, CommandeFournisseur, 
    LigneCommandeFournisseur, MouvementStock, AlerteStock
)

class FournisseurModelTest(TestCase):
    """Tests du modèle Fournisseur"""
    
    def setUp(self):
        self.fournisseur = Fournisseur.objects.create(
            nom="Test Fournisseur",
            contact="Jean Dupont",
            email="test@fournisseur.com",
            telephone="0123456789",
            adresse="123 Rue Test, Abidjan, Côte d'Ivoire",
            delai_livraison_moyen=5,
            conditions_paiement="30 jours fin de mois"
        )
    
    def test_fournisseur_creation(self):
        """Teste la création d'un fournisseur"""
        self.assertEqual(self.fournisseur.nom, "Test Fournisseur")
        self.assertTrue(self.fournisseur.est_actif)
        self.assertEqual(self.fournisseur.delai_livraison_moyen, 5)
    
    def test_fournisseur_str(self):
        """Teste la représentation string"""
        self.assertEqual(str(self.fournisseur), "Test Fournisseur")


class ProduitModelTest(TestCase):
    """Tests des méthodes du modèle Produit"""
    
    def setUp(self):
        self.produit = Produit.objects.create(
            reference="TEST001",
            nom="Produit Test",
            categorie="ALIMENTAIRE",
            prix_unitaire=Decimal('500.00'),
            prix_achat=Decimal('300.00'),
            stock_actuel=50,
            stock_critique=10,
            seuil_reapprovisionnement=20,
            stock_maximum=200
        )
    
    def test_valeur_stock(self):
        """Teste le calcul de la valeur du stock"""
        self.assertEqual(self.produit.valeur_stock(), Decimal('15000.00'))
    
    def test_valeur_stock_vente(self):
        """Teste le calcul de la valeur potentielle de vente"""
        self.assertEqual(self.produit.valeur_stock_vente(), Decimal('25000.00'))
    
    def test_marge_unitaire(self):
        """Teste le calcul de la marge unitaire"""
        marge = self.produit.prix_unitaire - self.produit.prix_achat
        self.assertEqual(marge, Decimal('200.00'))
    
    def test_besoin_reapprovisionnement(self):
        """Teste la détection du besoin de réapprovisionnement"""
        self.assertFalse(self.produit.besoin_reapprovisionnement())
        
        self.produit.stock_actuel = 15
        self.produit.save()
        self.assertTrue(self.produit.besoin_reapprovisionnement())
