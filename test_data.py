#!/usr/bin/env python
"""Script de test pour vérifier les données réalistes"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from CarrefourApp.models import *
from django.db.models import Sum, Count, Avg
from datetime import timedelta
from django.utils import timezone

print("\n" + "="*60)
print("📊 VÉRIFICATION DES DONNÉES RÉALISTES")
print("="*60)

# 1. Statistiques générales
print("\n✅ STATISTIQUES GÉNÉRALES:")
print(f"   • Ventes: {Vente.objects.count()}")
print(f"   • Clients: {Client.objects.count()}")
print(f"   • Produits: {Produit.objects.count()}")
print(f"   • Fournisseurs: {Fournisseur.objects.count()}")
print(f"   • Alertes Stock: {AlerteStock.objects.count()}")
print(f"   • Présences: {Presence.objects.count()}")
print(f"   • Demandes congés: {Conge.objects.count()}")

# 2. Clients fidèles
print("\n👥 CLIENTS FIDÈLES (Top 5):")
for client in Client.objects.order_by('-points_fidelite')[:5]:
    print(f"   • {client.get_full_name()}: {client.niveau_fidelite} - {client.points_fidelite} pts")

# 3. Produits critiques
print("\n⚠️  ALERTES STOCK:")
alertes = AlerteStock.objects.filter(est_resolue=False).select_related('produit')
if alertes.exists():
    for alerte in alertes:
        p = alerte.produit
        print(f"   🔴 {p.nom}: {p.stock_actuel}/{p.stock_critique} unités")
else:
    print("   ✅ Aucune alerte active")

# 4. Analyse des ventes
print("\n💰 ANALYSE DES VENTES:")
total_ca = Vente.objects.aggregate(ca=Sum('montant_final'))['ca'] or 0
total_remise = Vente.objects.aggregate(rem=Sum('remise'))['rem'] or 0
print(f"   • CA Total: {total_ca:,.0f} FCFA")
print(f"   • Remises accordées: {total_remise:,.0f} FCFA")
print(f"   • Panier moyen: {total_ca/Vente.objects.count():,.0f} FCFA")

# 5. Ventes par jour (derniers 7 jours)
print("\n📈 VENTES PAR JOUR (7 derniers jours):")
today = timezone.now().date()
for i in range(7):
    date = today - timedelta(days=i)
    nb_ventes = Vente.objects.filter(date_vente__date=date).count()
    ca_jour = Vente.objects.filter(date_vente__date=date).aggregate(ca=Sum('montant_final'))['ca'] or 0
    print(f"   • {date.strftime('%d/%m/%Y')}: {nb_ventes} ventes - {ca_jour:,.0f} FCFA")

# 6. Produits les plus vendus
print("\n🏆 TOP 5 PRODUITS VENDUS:")
from collections import Counter
lignes = LigneVente.objects.select_related('produit').all()
produits_vendus = Counter()
for ligne in lignes:
    produits_vendus[ligne.produit.nom] += ligne.quantite

for nom, qte in produits_vendus.most_common(5):
    print(f"   • {nom}: {qte} unités")

# 7. Présences employés
print("\n👤 PRÉSENCES EMPLOYÉS (Aujourd'hui):")
presences_today = Presence.objects.filter(date=today)
if presences_today.exists():
    statuts = presences_today.values('statut').annotate(nb=Count('id'))
    for s in statuts:
        print(f"   • {s['statut']}: {s['nb']} employé(s)")
else:
    print("   ℹ️  Aucune présence enregistrée aujourd'hui")

# 8. Demandes de congés
print("\n📅 DEMANDES DE CONGÉS EN ATTENTE:")
conges_pending = Conge.objects.filter(statut='EN_ATTENTE')
if conges_pending.exists():
    for conge in conges_pending:
        print(f"   • {conge.employe.first_name} {conge.employe.last_name}: {conge.date_debut} → {conge.date_fin}")
else:
    print("   ✅ Aucune demande en attente")

print("\n" + "="*60)
print("✨ VÉRIFICATION TERMINÉE")
print("="*60 + "\n")
