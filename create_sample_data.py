# Script pour créer des données de démonstration
# À exécuter dans le shell Django: python manage.py shell < create_sample_data.py

from CarrefourApp.models import *
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random

print("🔄 Création des données de démonstration...")

# Supprimer les données existantes
print("Suppression des anciennes données...")
Employe.objects.all().delete()
Produit.objects.all().delete()
Client.objects.all().delete()
Vente.objects.all().delete()

# Créer le super utilisateur DG
print("📊 Création du Directeur Général...")
dg = Employe.objects.create_superuser(
    username='admin',
    email='admin@supermarche.com',
    password='admin123',
    first_name='Jean-Baptiste',
    last_name='KONE',
    role='DG',
    departement='DIRECTION',
    telephone='+225 07 XX XX XX XX',
    acces_stocks=True,
    acces_caisse=True,
    acces_fidelisation=True,
    acces_rapports=True
)

# Créer d'autres employés
print("👥 Création des employés...")
employes_data = [
    ('marie', 'Marie', 'Kouamé', 'RH', 'RH', '+225 05 XX XX XX XX'),
    ('jean', 'Jean', 'Kouassi', 'STOCK', 'LOGISTIQUE', '+225 07 XX XX XX XX'),
    ('fatou', 'Fatou', 'Diallo', 'CAISSIER', 'VENTES', '+225 01 XX XX XX XX'),
    ('kouadio', 'Kouadio', 'Michel', 'CAISSIER', 'VENTES', '+225 05 XX XX XX XX'),
    ('yao', 'Yao', 'Marcel', 'MARKETING', 'MARKETING', '+225 07 XX XX XX XX'),
    ('ama', 'Ama', 'Traore', 'ANALYSTE', 'FINANCE', '+225 01 XX XX XX XX'),
]

for username, first, last, role, dept, tel in employes_data:
    emp = Employe.objects.create_user(
        username=username,
        password='password123',
        first_name=first,
        last_name=last,
        role=role,
        departement=dept,
        telephone=tel,
        acces_stocks=(role in ['STOCK', 'DG']),
        acces_caisse=(role in ['CAISSIER', 'DG']),
        acces_fidelisation=(role in ['MARKETING', 'DG']),
        acces_rapports=(role in ['ANALYSTE', 'DG', 'DAF'])
    )
    print(f"   ✅ {emp.get_full_name()} ({emp.employee_id})")

# Créer des produits
print("📦 Création des produits...")
produits_data = [
    ('RIZ001', 'Riz Parfumé 5kg', 'ALIMENTAIRE', 4500, 3000, 145, 'SACO'),
    ('LAI002', 'Lait Président 1L', 'ALIMENTAIRE', 850, 600, 5, 'Président'),
    ('HUI003', 'Huile de palme 1L', 'ALIMENTAIRE', 1500, 1000, 287, 'Palmci'),
    ('SUC004', 'Sucre blanc 1kg', 'ALIMENTAIRE', 650, 450, 256, 'SOSUCO'),
    ('SAV003', 'Savon Lux 200g', 'HYGIENE', 650, 400, 78, 'Unilever'),
    ('DEN004', 'Dentifrice Colgate', 'HYGIENE', 850, 550, 142, 'Colgate'),
    ('PAI001', 'Pain de mie Casino', 'ALIMENTAIRE', 450, 280, 3, 'Casino'),
    ('LAI004', 'Lait Nido 400g', 'ALIMENTAIRE', 1200, 800, 167, 'Nestlé'),
    ('EAU001', 'Eau minérale Awafina', 'BOISSONS', 250, 150, 450, 'Awafina'),
    ('JUS002', 'Jus Tampico 1L', 'BOISSONS', 800, 500, 234, 'Tampico'),
]

for ref, nom, cat, prix_v, prix_a, stock, fourn in produits_data:
    p = Produit.objects.create(
        reference=ref,
        nom=nom,
        categorie=cat,
        prix_unitaire=Decimal(str(prix_v)),
        prix_achat=Decimal(str(prix_a)),
        stock_actuel=stock,
        stock_critique=20,
        fournisseur=fourn,
        code_barre=f'22500{ref}'
    )
    print(f"   ✅ {p.nom} ({p.reference})")

# Créer des clients
print("👤 Création des clients...")
clients_data = [
    ('Aminata', 'Traoré', '+225 07 XX XX XX', 2450),
    ('Kouamé', 'Jean-UX Pilot', '+225 05 XX XX XX', 1820),
    ('Fatou', 'Diabaté', '+225 07 XX XX XX', 950),
    ('Yao', 'Marcel', '+225 09 XX XX XX', 1050),
]

for prenom, nom, tel, points in clients_data:
    c = Client.objects.create(
        nom=nom,
        prenom=prenom,
        telephone=tel,
        points_fidelite=points,
        email=f'{prenom.lower()}.{nom.lower()}@email.com'
    )
    print(f"   ✅ {c.nom} {c.prenom} - {c.niveau_fidelite}")

# Créer des ventes
print("💰 Création des ventes...")
caissiers = Employe.objects.filter(role='CAISSIER')
clients = Client.objects.all()
produits = list(Produit.objects.all())

for i in range(50):
    # Ventes sur les 30 derniers jours
    date_vente = timezone.now() - timedelta(days=random.randint(0, 30))
    
    vente = Vente.objects.create(
        caissier=random.choice(caissiers),
        client=random.choice(clients) if random.random() > 0.3 else None,
        montant_total=0,
        montant_final=0,
        moyen_paiement=random.choice(['ESPECES', 'CARTE', 'MOBILE']),
        date_vente=date_vente
    )
    
    # Ajouter 2-5 produits par vente
    nb_produits = random.randint(2, 5)
    total = Decimal('0')
    
    for _ in range(nb_produits):
        produit = random.choice(produits)
        quantite = random.randint(1, 3)
        
        LigneVente.objects.create(
            vente=vente,
            produit=produit,
            quantite=quantite,
            prix_unitaire=produit.prix_unitaire
        )
        
        total += produit.prix_unitaire * quantite
    
    tva = total * Decimal('0.18')
    vente.montant_total = total
    vente.montant_tva = tva
    vente.montant_final = total + tva
    vente.save()
    
    if i % 10 == 0:
        print(f"   ✅ {i+1} ventes créées...")

print(f"   ✅ Total: 50 ventes créées")

# Créer des présences
print("📅 Création des présences...")
employes = Employe.objects.filter(est_actif=True)
today = timezone.now().date()

for emp in employes:
    for i in range(7):
        date = today - timedelta(days=i)
        Presence.objects.create(
            employe=emp,
            date=date,
            est_present=random.random() > 0.1,
            heure_arrivee=timezone.now().time() if random.random() > 0.1 else None
        )

print("   ✅ Présences créées pour 7 jours")

# Créer des promotions
print("🎁 Création des promotions...")
promo = Promotion.objects.create(
    titre='Promotion Weekend',
    description='Réduction sur tous les produits alimentaires',
    reduction=Decimal('15.00'),
    date_debut=today,
    date_fin=today + timedelta(days=7),
    est_active=True
)
print(f"   ✅ {promo.titre}")

# Créer des congés
print("🏖️ Création des congés...")
for emp in list(employes)[:3]:
    Conge.objects.create(
        employe=emp,
        type_conge=random.choice(['ANNUEL', 'MALADIE']),
        date_debut=today + timedelta(days=random.randint(1, 10)),
        date_fin=today + timedelta(days=random.randint(11, 20)),
        motif='Congé annuel',
        statut=random.choice(['EN_ATTENTE', 'APPROUVE'])
    )
print("   ✅ 3 congés créés")

# Créer des formations
print("🎓 Création des formations...")
formation = Formation.objects.create(
    titre='Service Client',
    description='Formation sur les techniques de service client',
    date_debut=today - timedelta(days=5),
    date_fin=today + timedelta(days=5),
    nombre_participants=12,
    est_terminee=False
)
formation.participants.add(*list(employes)[:3])
print(f"   ✅ {formation.titre}")

print("\n✨ Données de démonstration créées avec succès!")
print("\n📋 Résumé:")
print(f"   - Employés: {Employe.objects.count()}")
print(f"   - Produits: {Produit.objects.count()}")
print(f"   - Clients: {Client.objects.count()}")
print(f"   - Ventes: {Vente.objects.count()}")
print(f"   - Présences: {Presence.objects.count()}")
print(f"   - Promotions: {Promotion.objects.count()}")
print(f"   - Congés: {Conge.objects.count()}")
print(f"   - Formations: {Formation.objects.count()}")
print("\n🔑 Identifiants de connexion:")
print("   Username: admin")
print("   Password: admin123")
