"""
Commande Django pour peupler la base avec des données réalistes selon le cahier des charges
Usage: python manage.py populate_realistic_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
import random
from datetime import timedelta

from CarrefourApp.models import (
    Employe, Produit, Fournisseur, Client, Promotion,
    Vente, LigneVente, SessionCaisse, Presence, Conge, Formation,
    Reclamation, CommandeFournisseur, MouvementStock, AlerteStock
)


class Command(BaseCommand):
    help = 'Peuple la base de données avec des données réalistes selon le cahier des charges'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n🚀 Début du peuplement de la base de données...\n'))
        
        # Nettoyer uniquement les données de démonstration (par téléphone/référence spécifiques)
        self.stdout.write('🧹 Suppression des anciennes données de démonstration...')
        
        # Supprimer les ventes et lignes de vente existantes (pour régénérer l'historique)
        from django.db.models import Q
        LigneVente.objects.all().delete()
        Vente.objects.all().delete()
        
        Client.objects.filter(telephone__in=['0707888888', '0707999999', '0707777777']).delete()
        Fournisseur.objects.filter(telephone__in=['0707111111', '0707222222', '0707333333']).delete()
        Produit.objects.filter(reference__in=['FAR001', 'RIZ002', 'HUILE003', 'COCA004', 'EAU005', 'SAV006', 'DENT007', 'GOURMET001']).delete()
        AlerteStock.objects.all().delete()
        Presence.objects.all().delete()
        # Supprimer les congés de Sarah si elle existe
        try:
            sarah = Employe.objects.get(first_name='Sarah')
            Conge.objects.filter(employe=sarah).delete()
        except Employe.DoesNotExist:
            pass
        
        self.stdout.write(self.style.SUCCESS('   ✓ Données de démo supprimées\n'))

        # 1. FOURNISSEURS (Scénario 8.1.1)
        self.stdout.write('📦 Création des fournisseurs...')
        fournisseurs_data = [
            {'nom': 'Moulin de Côte d\'Ivoire', 'contact': 'contact@moulin.ci', 'tel': '0707111111', 'delai': 3},
            {'nom': 'PROSUMA Distribution', 'contact': 'ventes@prosuma.ci', 'tel': '0707222222', 'delai': 2},
            {'nom': 'CFAO Alimentaire', 'contact': 'commandes@cfao.ci', 'tel': '0707333333', 'delai': 5},
        ]
        
        fournisseurs = []
        for data in fournisseurs_data:
            f, created = Fournisseur.objects.get_or_create(
                telephone=data['tel'],
                defaults={
                    'nom': data['nom'],
                    'contact': data['contact'],
                    'delai_livraison_moyen': data['delai']
                }
            )
            fournisseurs.append(f)
            if created:
                self.stdout.write(f'  ✅ {f.nom} (Délai: {data["delai"]} jours)')

        # 2. PRODUITS avec stocks critiques (Scénario 8.1.1 - Farine T45)
        self.stdout.write('\n🛒 Création des produits...')
        produits_data = [
            # Produit du scénario - STOCK CRITIQUE !
            {'ref': 'ALI001', 'nom': 'Farine T45 1kg', 'cat': 'ALIMENTAIRE', 'prix': 1500, 'achat': 1000, 'stock': 50, 'seuil': 100, 'commande_sugg': 500},
            # Autres produits
            {'ref': 'ALI002', 'nom': 'Riz Parfumé 5kg', 'cat': 'ALIMENTAIRE', 'prix': 12000, 'achat': 9500, 'stock': 145, 'seuil': 50, 'commande_sugg': 200},
            {'ref': 'ALI003', 'nom': 'Huile Végétale 5L', 'cat': 'ALIMENTAIRE', 'prix': 8500, 'achat': 7000, 'stock': 80, 'seuil': 30, 'commande_sugg': 150},
            {'ref': 'BOI001', 'nom': 'Coca-Cola 1.5L', 'cat': 'BOISSONS', 'prix': 1000, 'achat': 650, 'stock': 220, 'seuil': 50, 'commande_sugg': 300},
            {'ref': 'BOI002', 'nom': 'Eau Minérale 1.5L', 'cat': 'BOISSONS', 'prix': 500, 'achat': 300, 'stock': 350, 'seuil': 100, 'commande_sugg': 500},
            {'ref': 'HYG001', 'nom': 'Savon Dove 100g', 'cat': 'HYGIENE', 'prix': 850, 'achat': 600, 'stock': 120, 'seuil': 40, 'commande_sugg': 200},
            {'ref': 'HYG002', 'nom': 'Dentifrice Signal', 'cat': 'HYGIENE', 'prix': 1200, 'achat': 900, 'stock': 95, 'seuil': 30, 'commande_sugg': 150},
            # Produit saisonnier du scénario 8.1.5
            {'ref': 'GOURMET001', 'nom': 'Glace Vanille 1L', 'cat': 'ALIMENTAIRE', 'prix': 3500, 'achat': 2200, 'stock': 45, 'seuil': 20, 'commande_sugg': 100},
        ]
        
        produits = []
        for data in produits_data:
            p, created = Produit.objects.get_or_create(
                reference=data['ref'],
                defaults={
                    'nom': data['nom'],
                    'categorie': data['cat'],
                    'prix_unitaire': Decimal(str(data['prix'])),
                    'prix_achat': Decimal(str(data['achat'])),
                    'stock_actuel': data['stock'],
                    'stock_critique': data['seuil'],
                    'seuil_reapprovisionnement': data['seuil'],
                    'fournisseur_principal': random.choice(fournisseurs)
                }
            )
            produits.append(p)
            if created:
                statut = '🔴 CRITIQUE' if p.stock_actuel < p.stock_critique else '🟢 OK'
                self.stdout.write(f'  ✅ {p.nom} - Stock: {p.stock_actuel} {statut}')

        # 3. CLIENTS FIDÈLES (Scénario 8.1.2 et 8.1.4 - Monsieur Dupont)
        self.stdout.write('\n👥 Création des clients fidèles...')
        clients_data = [
            {'num': 'CLTDEMO001', 'nom': 'Dupont', 'prenom': 'Jean', 'tel': '0707888888', 'niveau': 'VIP', 'points': 800},
            {'num': 'CLTDEMO002', 'nom': 'Traore', 'prenom': 'Aminata', 'tel': '0707999999', 'niveau': 'GOLD', 'points': 450},
            {'num': 'CLTDEMO003', 'nom': 'Kouassi', 'prenom': 'Marie', 'tel': '0707777777', 'niveau': 'SILVER', 'points': 250},
        ]
        
        clients = []
        for data in clients_data:
            c, created = Client.objects.get_or_create(
                telephone=data['tel'],
                defaults={
                    'numero_client': data['num'],
                    'nom': data['nom'],
                    'prenom': data['prenom'],
                    'niveau_fidelite': data['niveau'],
                    'points_fidelite': data['points'],
                    'date_inscription': timezone.now() - timedelta(days=random.randint(90, 365))
                }
            )
            clients.append(c)
            if created:
                self.stdout.write(f'  ✅ {c.prenom} {c.nom} - {c.niveau_fidelite} ({c.points_fidelite} pts)')

        # 4. PROMOTIONS (Scénario 8.1.2 - Remise 5% à partir de 50000 FCFA)
        self.stdout.write('\n🎁 Création des promotions...')
        promo, created = Promotion.objects.get_or_create(
            titre="Seuil Promotionnel - 5% dès 50000 FCFA",
            defaults={
                'description': 'Remise immédiate de 5% pour tout achat dépassant 50000 FCFA (appliquer manuellement)',
                'reduction': Decimal('5.00'),
                'date_debut': timezone.now().date(),
                'date_fin': timezone.now().date() + timedelta(days=30),
                'est_active': True
            }
        )
        if created:
            promo.produits.set(produits)
            self.stdout.write(f'  ✅ {promo.titre} - {promo.reduction}%')

        # 5. VENTES HISTORIQUES (pour analyse tendances - Scénario 8.1.5)
        self.stdout.write('\n💰 Génération de l\'historique des ventes (30 derniers jours)...')
        caissiers = Employe.objects.filter(role='CAISSIER', est_actif=True)
        
        if caissiers.exists():
            nb_ventes = 0
            for jour in range(30, 0, -1):
                date_vente = timezone.now() - timedelta(days=jour)
                
                # Plus de ventes les vendredis/samedis (Scénario 8.1.5)
                nb_ventes_jour = random.randint(15, 25)
                if date_vente.weekday() in [4, 5]:  # Vendredi, Samedi
                    nb_ventes_jour = random.randint(30, 45)
                
                for _ in range(nb_ventes_jour):
                    caissier = random.choice(caissiers)
                    client = random.choice(clients) if random.random() > 0.4 else None
                    
                    # 2-5 produits par vente
                    nb_produits = random.randint(2, 5)
                    montant_total = Decimal('0')
                    lignes_data = []
                    
                    for _ in range(nb_produits):
                        produit = random.choice(produits)
                        quantite = random.randint(1, 3)
                        prix = produit.prix_unitaire
                        montant = prix * quantite
                        montant_total += montant
                        lignes_data.append({
                            'produit': produit,
                            'quantite': quantite,
                            'prix': prix,
                            'montant': montant
                        })
                    
                    # Calculer remise fidélité si client
                    remise = Decimal('0')
                    if client:
                        if client.niveau_fidelite == 'VIP':
                            remise = montant_total * Decimal('0.10')  # 10%
                        elif client.niveau_fidelite == 'GOLD':
                            remise = montant_total * Decimal('0.05')  # 5%
                    
                    montant_final = montant_total - remise
                    
                    vente = Vente.objects.create(
                        caissier=caissier,
                        client=client,
                        montant_total=montant_total,
                        montant_tva=Decimal('0'),
                        remise=remise,
                        montant_final=montant_final,
                        moyen_paiement=random.choice(['ESPECES', 'CARTE', 'MOBILE'])
                    )
                    # Modifier la date après création
                    vente.date_vente = date_vente
                    vente.save(update_fields=['date_vente'])
                    
                    # Créer les lignes de vente
                    for ligne_data in lignes_data:
                        LigneVente.objects.create(
                            vente=vente,
                            produit=ligne_data['produit'],
                            quantite=ligne_data['quantite'],
                            prix_unitaire=ligne_data['prix'],
                            montant_ligne=ligne_data['montant']
                        )
                    
                    nb_ventes += 1
            
            self.stdout.write(f'  ✅ {nb_ventes} ventes générées sur 30 jours')
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  Aucun caissier trouvé'))

        # 6. ALERTES STOCK CRITIQUES (Scénario 8.1.1)
        self.stdout.write('\n⚠️  Génération des alertes stock...')
        nb_alertes = 0
        for produit in produits:
            if produit.stock_actuel < produit.stock_critique:
                alerte, created = AlerteStock.objects.get_or_create(
                    produit=produit,
                    type_alerte='SEUIL_CRITIQUE',
                    est_resolue=False
                )
                if created:
                    nb_alertes += 1
                    self.stdout.write(f'  🔴 ALERTE: {produit.nom} - Stock: {produit.stock_actuel}/{produit.stock_critique}')
        
        self.stdout.write(f'  ✅ {nb_alertes} alertes générées')

        # 7. PRÉSENCES EMPLOYÉS (Scénario 8.1.3)
        self.stdout.write('\n👤 Génération des présences (7 derniers jours)...')
        employes = Employe.objects.filter(est_actif=True)
        nb_presences = 0
        for emp in employes:
            for i in range(7):
                date = timezone.now().date() - timedelta(days=i)
                from datetime import time
                Presence.objects.get_or_create(
                    employe=emp,
                    date=date,
                    defaults={
                        'statut': random.choices(
                            ['PRESENT', 'PRESENT', 'PRESENT', 'RETARD', 'ABSENT'],
                            weights=[70, 15, 10, 3, 2]
                        )[0],
                        'heure_premiere_arrivee': time(8, 0),
                        'heure_derniere_depart': time(17, 0),
                        'temps_actif_total': 8.0
                    }
                )
                nb_presences += 1
        self.stdout.write(f'  ✅ {nb_presences} présences enregistrées')

        # 8. DEMANDE DE CONGÉ (Scénario 8.1.3 - Sarah)
        self.stdout.write('\n📅 Création de demandes de congés...')
        sarah = Employe.objects.filter(first_name__icontains='sarah').first() or employes.first()
        if sarah:
            conge, created = Conge.objects.get_or_create(
                employe=sarah,
                date_debut=timezone.now().date() + timedelta(days=7),
                defaults={
                    'type_conge': 'ANNUEL',
                    'date_fin': timezone.now().date() + timedelta(days=8),
                    'motif': 'Raisons personnelles',
                    'statut': 'EN_ATTENTE'
                }
            )
            if created:
                self.stdout.write(f'  ✅ Demande de congé créée pour {sarah.get_full_name()}')

        # RÉSUMÉ FINAL
        self.stdout.write(self.style.SUCCESS('\n✨ Base de données peuplée avec succès !\n'))
        self.stdout.write(self.style.SUCCESS('📊 STATISTIQUES:'))
        self.stdout.write(f'  • Fournisseurs: {Fournisseur.objects.count()}')
        self.stdout.write(f'  • Produits: {Produit.objects.count()}')
        self.stdout.write(f'  • Clients: {Client.objects.count()}')
        self.stdout.write(f'  • Ventes: {Vente.objects.count()}')
        self.stdout.write(f'  • Alertes stock: {AlerteStock.objects.filter(est_resolue=False).count()}')
        self.stdout.write(f'  • Présences: {Presence.objects.count()}')
        self.stdout.write(f'  • Demandes congés: {Conge.objects.count()}')
        
        self.stdout.write(self.style.SUCCESS('\n🎯 Scénarios implémentés:'))
        self.stdout.write('  ✅ 8.1.1 - Gestion stocks (Farine T45 critique)')
        self.stdout.write('  ✅ 8.1.2 - Gestion caisses (Remises fidélité)')
        self.stdout.write('  ✅ 8.1.3 - Gestion RH (Planning & congés)')
        self.stdout.write('  ✅ 8.1.4 - CRM (Points M. Dupont)')
        self.stdout.write('  ✅ 8.1.5 - Reporting (Tendances ventes)\n')
