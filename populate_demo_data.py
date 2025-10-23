"""
Script pour peupler la base de données avec des données de démonstration
Exécuter: python manage.py shell < populate_demo_data.py
"""

import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from django.utils import timezone
from CarrefourApp.models import (
    Employe, Produit, Categorie, Fournisseur, Client, 
    Promotion, Transaction, LigneTransaction, Vente, LigneVente,
    SessionCaisse, Presence, Conge, Formation, Reclamation
)

print("🚀 Début du peuplement de la base de données...")

# 1. Créer des clients
print("\n📋 Création de clients fidèles...")
clients_data = [
    {'nom': 'Aminata', 'prenom': 'Traore', 'telephone': '0707010101', 'niveau_fidelite': 'VIP', 'points': 4270},
    {'nom': 'Kouassi', 'prenom': 'Jean', 'telephone': '0707020202', 'niveau_fidelite': 'GOLD', 'points': 2150},
]

clients = []
for data in clients_data:
    client, created = Client.objects.get_or_create(
        telephone=data['telephone'],
        defaults={
            'nom': data['nom'],
            'prenom': data['prenom'],
            'niveau_fidelite': data['niveau_fidelite'],
            'points_fidelite': data['points'],
            'date_inscription': timezone.now() - timedelta(days=random.randint(30, 180))
        }
    )
    if created:
        print(f"  ✅ Client créé: {client.nom} {client.prenom} ({client.niveau_fidelite})")
    clients.append(client)

# 2. Créer des fournisseurs
print("\n📦 Création de fournisseurs...")
fournisseurs_data = [
    {'nom': 'CFAO Distribution', 'contact': 'contact@cfao.ci', 'telephone': '0122334455'},
    {'nom': 'PROSUMA', 'contact': 'info@prosuma.ci', 'telephone': '0122334466'},
    {'nom': 'SODECI Alimentaire', 'contact': 'ventes@sodeci.ci', 'telephone': '0122334477'},
]

fournisseurs = []
for data in fournisseurs_data:
    fournisseur, created = Fournisseur.objects.get_or_create(
        telephone=data['telephone'],
        defaults={
            'nom': data['nom'],
            'contact': data['contact']
        }
    )
    if created:
        print(f"  ✅ Fournisseur créé: {fournisseur.nom}")
    fournisseurs.append(fournisseur)

# 3. Créer des produits
print("\n🛒 Création de produits...")
produits_data = [
    {'ref': 'ALI001', 'nom': 'Riz Parfumé 5kg', 'cat': 'ALIMENTAIRE', 'prix': 12000, 'achat': 9500, 'stock': 45},
    {'ref': 'ALI002', 'nom': 'Huile Végétale 5L', 'cat': 'ALIMENTAIRE', 'prix': 8500, 'achat': 7000, 'stock': 30},
    {'ref': 'BOI001', 'nom': 'Coca-Cola 1.5L', 'cat': 'BOISSONS', 'prix': 1000, 'achat': 650, 'stock': 120},
    {'ref': 'BOI002', 'nom': 'Eau Minérale 1.5L', 'cat': 'BOISSONS', 'prix': 500, 'achat': 300, 'stock': 200},
    {'ref': 'HYG001', 'nom': 'Savon Dove 100g', 'cat': 'HYGIENE', 'prix': 850, 'achat': 600, 'stock': 80},
    {'ref': 'HYG002', 'nom': 'Dentifrice Signal', 'cat': 'HYGIENE', 'prix': 1200, 'achat': 900, 'stock': 60},
]

produits = []
for data in produits_data:
    produit, created = Produit.objects.get_or_create(
        reference=data['ref'],
        defaults={
            'nom': data['nom'],
            'categorie': data['cat'],
            'prix_unitaire': data['prix'],
            'prix_achat': data['achat'],
            'stock_actuel': data['stock'],
            'stock_critique': 10,
            'fournisseur': random.choice(fournisseurs)
        }
    )
    if created:
        print(f"  ✅ Produit créé: {produit.nom} - Stock: {produit.stock_actuel}")
    produits.append(produit)

# 4. Créer des promotions
print("\n🎁 Création de promotions...")
promo, created = Promotion.objects.get_or_create(
    titre="Promotion Weekend",
    defaults={
        'description': 'Réduction sur tous les produits alimentaires',
        'reduction': Decimal('15.00'),
        'date_debut': timezone.now().date(),
        'date_fin': timezone.now().date() + timedelta(days=7),
        'est_active': True
    }
)
if created:
    promo.produits.set([p for p in produits if p.categorie == 'ALIMENTAIRE'])
    print(f"  ✅ Promotion créée: {promo.titre} - {promo.reduction}%")

# 5. Créer des ventes (pour avoir des statistiques)
print("\n💰 Création de ventes de démonstration...")
caissier = Employe.objects.filter(role='CAISSIER', est_actif=True).first()

if caissier:
    for i in range(20):
        vente = Vente.objects.create(
            caissier=caissier,
            client=random.choice(clients) if random.random() > 0.3 else None,
            date_vente=timezone.now() - timedelta(days=random.randint(0, 30)),
            moyen_paiement=random.choice(['ESPECES', 'ORANGE_MONEY', 'CB', 'MTN_MONEY']),
            statut='VALIDEE'
        )
        
        # Ajouter 1-4 lignes de produits
        nb_produits = random.randint(1, 4)
        total = 0
        for _ in range(nb_produits):
            produit = random.choice(produits)
            quantite = random.randint(1, 3)
            prix = produit.prix_unitaire
            
            LigneVente.objects.create(
                vente=vente,
                produit=produit,
                quantite=quantite,
                prix_unitaire=prix,
                montant_ligne=prix * quantite
            )
            total += prix * quantite
        
        vente.montant_total = total
        vente.montant_final = total
        vente.save()
    
    print(f"  ✅ {20} ventes créées")
else:
    print("  ⚠️  Aucun caissier trouvé, ventes non créées")

# 6. Créer des présences
print("\n👤 Création de présences...")
employes_actifs = Employe.objects.filter(est_actif=True)
for emp in employes_actifs:
    for i in range(5):
        date = timezone.now().date() - timedelta(days=i)
        Presence.objects.get_or_create(
            employe=emp,
            date=date,
            defaults={
                'statut': random.choice(['PRESENT', 'PRESENT', 'PRESENT', 'RETARD']),
                'heure_arrivee': '08:00',
                'heure_depart': '17:00'
            }
        )
print(f"  ✅ Présences créées pour {employes_actifs.count()} employés")

# 7. Créer une formation
print("\n🎓 Création de formation...")
formation, created = Formation.objects.get_or_create(
    titre="Formation Service Client",
    defaults={
        'description': 'Améliorer la relation client',
        'date_debut': timezone.now().date(),
        'date_fin': timezone.now().date() + timedelta(days=2),
        'nombre_participants': employes_actifs.count()
    }
)
if created:
    formation.participants.set(employes_actifs)
    print(f"  ✅ Formation créée: {formation.titre}")

print("\n✨ Base de données peuplée avec succès !")
print(f"  📊 Clients: {Client.objects.count()}")
print(f"  📦 Fournisseurs: {Fournisseur.objects.count()}")
print(f"  🛒 Produits: {Produit.objects.count()}")
print(f"  🎁 Promotions: {Promotion.objects.count()}")
print(f"  💰 Ventes: {Vente.objects.count()}")
print(f"  👤 Présences: {Presence.objects.count()}")
print(f"  🎓 Formations: {Formation.objects.count()}")
