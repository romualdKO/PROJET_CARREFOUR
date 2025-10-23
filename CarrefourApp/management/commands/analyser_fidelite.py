"""
Commande de gestion pour analyser et mettre à jour automatiquement 
les niveaux de fidélité des clients selon leur comportement d'achat.

Usage:
    python manage.py analyser_fidelite
    python manage.py analyser_fidelite --generer-coupons  # Génère aussi des coupons
    python manage.py analyser_fidelite --dry-run  # Mode test sans modification
"""

from django.core.management.base import BaseCommand
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta, date
from CarrefourApp.models import Client, Transaction, Vente, Coupon
from decimal import Decimal


class Command(BaseCommand):
    help = 'Analyse le comportement des clients et met à jour leurs niveaux de fidélité'

    def add_arguments(self, parser):
        parser.add_argument(
            '--generer-coupons',
            action='store_true',
            help='Génère des coupons spéciaux pour les clients fidèles après analyse',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mode test: affiche les changements sans les appliquer',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        generer_coupons = options['generer_coupons']
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('🔍 ANALYSE INTELLIGENTE DE FIDÉLITÉ'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('⚠️  MODE TEST (dry-run) - Aucune modification ne sera appliquée'))
        
        # Récupérer tous les clients actifs
        clients = Client.objects.filter(est_actif=True)
        
        stats = {
            'total_clients': clients.count(),
            'upgrades': 0,
            'downgrades': 0,
            'inchanges': 0,
            'coupons_generes': 0
        }
        
        self.stdout.write(f'\n📊 Analyse de {stats["total_clients"]} clients actifs...\n')
        
        for client in clients:
            ancien_niveau = client.niveau_fidelite
            nouveau_niveau = self.calculer_niveau_intelligent(client)
            
            if nouveau_niveau != ancien_niveau:
                if self.niveau_superieur(nouveau_niveau, ancien_niveau):
                    stats['upgrades'] += 1
                    symbole = '⬆️'
                    style = self.style.SUCCESS
                else:
                    stats['downgrades'] += 1
                    symbole = '⬇️'
                    style = self.style.WARNING
                
                self.stdout.write(
                    style(f'{symbole} {client.get_full_name()} : {ancien_niveau} → {nouveau_niveau}')
                )
                
                if not dry_run:
                    client.niveau_fidelite = nouveau_niveau
                    client.save()
                    
                    # Générer un coupon si upgrade et option activée
                    if generer_coupons and self.niveau_superieur(nouveau_niveau, ancien_niveau):
                        coupon = self.generer_coupon_fidelite(client, nouveau_niveau)
                        if coupon:
                            stats['coupons_generes'] += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'   🎁 Coupon {coupon.code} généré')
                            )
            else:
                stats['inchanges'] += 1
        
        # Résumé
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('📈 RÉSUMÉ DE L\'ANALYSE'))
        self.stdout.write('=' * 70)
        self.stdout.write(f'Total clients analysés : {stats["total_clients"]}')
        self.stdout.write(self.style.SUCCESS(f'✅ Upgrades (promotions) : {stats["upgrades"]}'))
        self.stdout.write(self.style.WARNING(f'⚠️  Downgrades (rétrogradations) : {stats["downgrades"]}'))
        self.stdout.write(f'➡️  Inchangés : {stats["inchanges"]}')
        
        if generer_coupons:
            self.stdout.write(self.style.SUCCESS(f'🎁 Coupons générés : {stats["coupons_generes"]}'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\n⚠️  AUCUNE MODIFICATION APPLIQUÉE (mode dry-run)'))
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ ANALYSE TERMINÉE ET MODIFICATIONS APPLIQUÉES'))

    def calculer_niveau_intelligent(self, client):
        """
        Calcule le niveau de fidélité basé sur plusieurs critères:
        - Fréquence d'achat (achats par mois)
        - Récence (jours depuis dernier achat)
        - Montant total dépensé
        - Régularité des achats
        """
        
        # Période d'analyse: derniers 6 mois
        today = timezone.now().date()
        six_mois_ago = today - timedelta(days=180)
        trois_mois_ago = today - timedelta(days=90)
        
        # Essayer d'abord avec Transaction
        try:
            achats_6_mois = Transaction.objects.filter(
                client=client,
                statut='VALIDEE',
                date_transaction__date__gte=six_mois_ago
            )
            achats_3_mois = achats_6_mois.filter(date_transaction__date__gte=trois_mois_ago)
            
            nb_achats_6_mois = achats_6_mois.count()
            nb_achats_3_mois = achats_3_mois.count()
            montant_total = achats_6_mois.aggregate(total=Sum('montant_final'))['total'] or 0
            
            # Récence (jours depuis dernier achat)
            dernier_achat = achats_6_mois.order_by('-date_transaction').first()
            if dernier_achat:
                recence = (today - dernier_achat.date_transaction.date()).days
            else:
                recence = 999  # Pas d'achat récent
                
        except:
            # Si Transaction n'existe pas, utiliser Vente
            achats_6_mois = Vente.objects.filter(
                client=client,
                date_vente__date__gte=six_mois_ago
            )
            achats_3_mois = achats_6_mois.filter(date_vente__date__gte=trois_mois_ago)
            
            nb_achats_6_mois = achats_6_mois.count()
            nb_achats_3_mois = achats_3_mois.count()
            montant_total = achats_6_mois.aggregate(total=Sum('montant_final'))['total'] or 0
            
            dernier_achat = achats_6_mois.order_by('-date_vente').first()
            if dernier_achat:
                recence = (today - dernier_achat.date_vente.date()).days
            else:
                recence = 999
        
        # Calcul de la fréquence (achats/mois)
        frequence_6_mois = nb_achats_6_mois / 6.0
        frequence_3_mois = nb_achats_3_mois / 3.0
        
        # Score composite (0-100)
        score = 0
        
        # Critère 1: Fréquence récente (40 points max)
        if frequence_3_mois >= 4:
            score += 40
        elif frequence_3_mois >= 2:
            score += 30
        elif frequence_3_mois >= 1:
            score += 20
        elif frequence_3_mois >= 0.5:
            score += 10
        
        # Critère 2: Régularité sur 6 mois (30 points max)
        if frequence_6_mois >= 3:
            score += 30
        elif frequence_6_mois >= 2:
            score += 20
        elif frequence_6_mois >= 1:
            score += 10
        
        # Critère 3: Récence (20 points max)
        if recence <= 7:
            score += 20
        elif recence <= 14:
            score += 15
        elif recence <= 30:
            score += 10
        elif recence <= 60:
            score += 5
        
        # Critère 4: Montant dépensé (10 points max)
        if montant_total >= 500000:  # 500k FCFA
            score += 10
        elif montant_total >= 200000:
            score += 7
        elif montant_total >= 100000:
            score += 5
        elif montant_total >= 50000:
            score += 3
        
        # Attribution du niveau basé sur le score
        if score >= 75:
            return 'VIP'
        elif score >= 50:
            return 'GOLD'
        elif score >= 25:
            return 'SILVER'
        else:
            return 'TOUS'

    def niveau_superieur(self, niveau1, niveau2):
        """Compare deux niveaux et retourne True si niveau1 > niveau2"""
        ordre = {'TOUS': 0, 'SILVER': 1, 'GOLD': 2, 'VIP': 3}
        return ordre.get(niveau1, 0) > ordre.get(niveau2, 0)

    def generer_coupon_fidelite(self, client, nouveau_niveau):
        """Génère un coupon de félicitation pour le nouveau niveau"""
        
        # Vérifier qu'il n'a pas déjà un coupon actif récent
        coupon_recent = Coupon.objects.filter(
            client=client,
            type_coupon='SPECIAL',
            statut='ACTIF',
            est_utilise=False,
            date_creation__gte=timezone.now() - timedelta(days=30)
        ).exists()
        
        if coupon_recent:
            return None
        
        # Valeur du coupon selon le niveau
        valeurs = {
            'SILVER': 3,   # 3%
            'GOLD': 5,     # 5%
            'VIP': 10      # 10%
        }
        
        descriptions = {
            'SILVER': 'Félicitations pour votre statut SILVER!',
            'GOLD': 'Bravo! Vous êtes maintenant GOLD!',
            'VIP': 'Bienvenue dans le club VIP exclusif!'
        }
        
        valeur = valeurs.get(nouveau_niveau, 0)
        if valeur == 0:
            return None
        
        coupon = Coupon.objects.create(
            type_coupon='SPECIAL',
            type_remise='POURCENTAGE',
            valeur=valeur,
            description=descriptions.get(nouveau_niveau, 'Coupon de fidélité'),
            date_debut=date.today(),
            date_fin=date.today() + timedelta(days=30),
            client=client,
            statut='ACTIF'
        )
        
        return coupon
