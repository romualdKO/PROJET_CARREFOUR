# =====================================================
# SPRINT 5 - TESTS E2E & INTÉGRATION
# =====================================================

from django.test import TestCase, Client as TestClient
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

from .models import (
    Employe, Produit, Client, Transaction, LigneTransaction,
    TypePaiement, SessionCaisse, CarteFidelite, Campagne, SegmentClient
)


class POSWorkflowTestCase(TestCase):
    """Tests du workflow complet de la caisse (POS)"""
    
    def setUp(self):
        # Créer un utilisateur caissier
        self.user = User.objects.create_user(
            username='caissier1',
            password='test123',
            first_name='Jean',
            last_name='Dupont'
        )
        self.employe = Employe.objects.create(
            user=self.user,
            poste='Caissier',
            salaire=150000
        )
        
        # Créer des produits
        self.produit1 = Produit.objects.create(
            nom='Produit A',
            prix_vente=1000,
            prix_achat=700,
            stock_actuel=50,
            stock_minimum=10,
            stock_maximum=100,
            categorie='ALIMENTATION',
            reference='PROD001'
        )
        
        self.produit2 = Produit.objects.create(
            nom='Produit B',
            prix_vente=2000,
            prix_achat=1500,
            stock_actuel=30,
            stock_minimum=5,
            stock_maximum=50,
            categorie='BOISSONS',
            reference='PROD002'
        )
        
        # Créer un type de paiement
        self.type_paiement = TypePaiement.objects.create(
            nom='Espèces',
            code='ESPECES',
            est_actif=True
        )
        
        # Créer un client
        self.client_customer = Client.objects.create(
            nom='Martin',
            prenom='Pierre',
            telephone='0102030405',
            email='pierre@example.com'
        )
        
        # Ouvrir une session de caisse
        self.session = SessionCaisse.objects.create(
            caissier=self.user,
            fonds_ouverture=10000
        )
        
        self.test_client = TestClient()
        self.test_client.login(username='caissier1', password='test123')
    
    def test_01_ouvrir_session_caisse(self):
        """Test ouverture session caisse"""
        # Fermer la session créée dans setUp
        self.session.est_cloturee = True
        self.session.save()
        
        response = self.test_client.post('/pos/ouvrir-session/', {
            'fonds_ouverture': 15000
        })
        
        # Vérifier redirection
        self.assertEqual(response.status_code, 302)
        
        # Vérifier session créée
        session = SessionCaisse.objects.filter(
            caissier=self.user,
            est_cloturee=False
        ).first()
        self.assertIsNotNone(session)
        self.assertEqual(session.fonds_ouverture, 15000)
    
    def test_02_creer_transaction(self):
        """Test création d'une transaction"""
        response = self.test_client.post('/pos/nouvelle-transaction/', {}, 
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('transaction_id', data)
        
        # Vérifier transaction créée
        transaction = Transaction.objects.get(id=data['transaction_id'])
        self.assertEqual(transaction.statut, 'EN_COURS')
        self.assertEqual(transaction.caissier, self.user)
    
    def test_03_ajouter_produits_au_panier(self):
        """Test ajout de produits au panier"""
        # Créer une transaction
        transaction = Transaction.objects.create(
            caissier=self.user,
            statut='EN_COURS'
        )
        
        # Ajouter produit 1
        response = self.test_client.post('/pos/ajouter-produit/', {
            'transaction_id': transaction.id,
            'produit_id': self.produit1.id,
            'quantite': 2
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # Vérifier ligne ajoutée
        ligne = LigneTransaction.objects.filter(
            transaction=transaction,
            produit=self.produit1
        ).first()
        self.assertIsNotNone(ligne)
        self.assertEqual(ligne.quantite, 2)
        self.assertEqual(ligne.prix_unitaire, self.produit1.prix_vente)
    
    def test_04_valider_vente_complete(self):
        """Test workflow complet: transaction + produits + paiement"""
        # Créer transaction
        transaction = Transaction.objects.create(
            caissier=self.user,
            statut='EN_COURS',
            client=self.client_customer
        )
        
        # Ajouter lignes
        LigneTransaction.objects.create(
            transaction=transaction,
            produit=self.produit1,
            quantite=3,
            prix_unitaire=self.produit1.prix_vente
        )
        
        LigneTransaction.objects.create(
            transaction=transaction,
            produit=self.produit2,
            quantite=1,
            prix_unitaire=self.produit2.prix_vente
        )
        
        # Sauvegarder stocks initiaux
        stock_p1_avant = self.produit1.stock_actuel
        stock_p2_avant = self.produit2.stock_actuel
        
        # Valider la vente
        montant_total = (3 * 1000) + (1 * 2000)  # 5000 FCFA
        
        response = self.test_client.post('/pos/valider-vente/', {
            'transaction_id': transaction.id,
            'paiements': [
                {
                    'type_paiement_id': self.type_paiement.id,
                    'montant': montant_total
                }
            ]
        }, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # Vérifier transaction validée
        transaction.refresh_from_db()
        self.assertEqual(transaction.statut, 'VALIDEE')
        self.assertEqual(transaction.montant_final, montant_total)
        
        # Vérifier stocks décrémentes
        self.produit1.refresh_from_db()
        self.produit2.refresh_from_db()
        self.assertEqual(self.produit1.stock_actuel, stock_p1_avant - 3)
        self.assertEqual(self.produit2.stock_actuel, stock_p2_avant - 1)
    
    def test_05_cloturer_session(self):
        """Test clôture de session"""
        # Créer quelques transactions
        for i in range(3):
            Transaction.objects.create(
                caissier=self.user,
                statut='VALIDEE',
                montant_final=5000
            )
        
        response = self.test_client.post('/pos/cloturer-session/', {
            'fonds_reel': 25000
        })
        
        self.assertEqual(response.status_code, 302)
        
        # Vérifier session clôturée
        self.session.refresh_from_db()
        self.assertTrue(self.session.est_cloturee)
        self.assertIsNotNone(self.session.date_cloture)


class CRMWorkflowTestCase(TestCase):
    """Tests du workflow CRM"""
    
    def setUp(self):
        self.client_customer = Client.objects.create(
            nom='Dubois',
            prenom='Marie',
            telephone='0612345678',
            email='marie@example.com',
            points_fidelite=0,
            total_achats=0
        )
        
        self.test_client = TestClient()
    
    def test_01_creer_carte_fidelite(self):
        """Test création de carte de fidélité"""
        carte = CarteFidelite.objects.create(
            client=self.client_customer,
            solde_points=0,
            statut='ACTIVE'
        )
        
        self.assertIsNotNone(carte.numero_carte)
        self.assertTrue(carte.numero_carte.startswith('CARD'))
        self.assertEqual(carte.statut, 'ACTIVE')
    
    def test_02_crediter_points(self):
        """Test crédit de points"""
        carte = CarteFidelite.objects.create(
            client=self.client_customer
        )
        
        solde_avant = carte.solde_points
        carte.crediter_points(100, motif="Achat de 10000 FCFA")
        
        self.assertEqual(carte.solde_points, solde_avant + 100)
        
        # Vérifier opération créée
        operation = carte.operations.first()
        self.assertEqual(operation.type_operation, 'CREDIT')
        self.assertEqual(operation.points, 100)
    
    def test_03_debiter_points(self):
        """Test débit de points"""
        carte = CarteFidelite.objects.create(
            client=self.client_customer,
            solde_points=200
        )
        
        success = carte.debiter_points(50, motif="Échange récompense")
        
        self.assertTrue(success)
        self.assertEqual(carte.solde_points, 150)
        
        # Test débit insuffisant
        success = carte.debiter_points(200, motif="Trop de points")
        self.assertFalse(success)
        self.assertEqual(carte.solde_points, 150)  # Inchangé
    
    def test_04_segment_clients(self):
        """Test segmentation clients"""
        # Créer plusieurs clients
        Client.objects.create(
            nom='Client1', prenom='Test1',
            telephone='0601', total_achats=5000,
            niveau_fidelite='BRONZE'
        )
        Client.objects.create(
            nom='Client2', prenom='Test2',
            telephone='0602', total_achats=15000,
            niveau_fidelite='ARGENT'
        )
        Client.objects.create(
            nom='Client3', prenom='Test3',
            telephone='0603', total_achats=50000,
            niveau_fidelite='OR'
        )
        
        # Créer segment pour clients OR
        segment = SegmentClient.objects.create(
            nom='Clients Premium',
            niveau_fidelite='OR'
        )
        
        clients = segment.get_clients()
        self.assertEqual(clients.count(), 1)
        self.assertEqual(clients.first().nom, 'Client3')
    
    def test_05_creer_campagne(self):
        """Test création de campagne marketing"""
        segment = SegmentClient.objects.create(
            nom='Tous les clients'
        )
        
        campagne = Campagne.objects.create(
            titre='Promotion Été',
            description='Offre spéciale été',
            type_campagne='SMS',
            statut='PROGRAMMEE',
            date_debut=timezone.now(),
            date_fin=timezone.now() + timezone.timedelta(days=30),
            segment_cible=segment,
            message='Profitez de -20% ce mois-ci!',
            nb_destinataires=100
        )
        
        self.assertEqual(campagne.titre, 'Promotion Été')
        self.assertEqual(campagne.statut, 'PROGRAMMEE')
        self.assertEqual(campagne.taux_ouverture(), 0)  # Pas encore envoyée


class StockManagementTestCase(TestCase):
    """Tests de gestion de stock"""
    
    def test_01_calcul_valeur_stock(self):
        """Test calcul valeur du stock"""
        produit = Produit.objects.create(
            nom='Test Produit',
            prix_achat=500,
            prix_vente=800,
            stock_actuel=20,
            stock_minimum=5,
            stock_maximum=50,
            categorie='AUTRES',
            reference='TEST001'
        )
        
        valeur = produit.valeur_stock()
        self.assertEqual(valeur, 10000)  # 20 * 500
    
    def test_02_besoin_reapprovisionnement(self):
        """Test alerte réapprovisionnement"""
        produit = Produit.objects.create(
            nom='Produit Alerte',
            prix_achat=100,
            prix_vente=150,
            stock_actuel=3,  # En dessous du minimum
            stock_minimum=10,
            stock_maximum=50,
            categorie='AUTRES',
            reference='ALERTE001'
        )
        
        self.assertTrue(produit.besoin_reapprovisionnement())
    
    def test_03_marge_produit(self):
        """Test calcul de marge"""
        produit = Produit.objects.create(
            nom='Produit Marge',
            prix_achat=700,
            prix_vente=1000,
            stock_actuel=10,
            stock_minimum=5,
            stock_maximum=20,
            categorie='AUTRES',
            reference='MARGE001'
        )
        
        marge = produit.marge()
        self.assertEqual(marge, 300)  # 1000 - 700


# Exécution des tests:
# python manage.py test CarrefourApp.tests_e2e
