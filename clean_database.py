# Script pour SUPPRIMER toutes les données de test
from CarrefourApp.models import *

# Supprimer toutes les données SAUF les comptes admin (DG, DAF, RH)
print("🗑️ Suppression des données de test...")

# Garder uniquement DG, DAF, RH
employes_a_garder = ['dg', 'daf', 'rh']
Employe.objects.exclude(username__in=employes_a_garder).delete()
print("✅ Employés de test supprimés (gardé: DG, DAF, RH)")

# Supprimer toutes les ventes
Vente.objects.all().delete()
LigneVente.objects.all().delete()
print("✅ Ventes supprimées")

# Supprimer tous les clients
Client.objects.all().delete()
print("✅ Clients supprimés")

# Supprimer tous les produits
Produit.objects.all().delete()
print("✅ Produits supprimés")

# Supprimer toutes les promotions
Promotion.objects.all().delete()
print("✅ Promotions supprimées")

# Supprimer toutes les présences
Presence.objects.all().delete()
print("✅ Présences supprimées")

# Supprimer tous les congés
Conge.objects.all().delete()
print("✅ Congés supprimés")

# Supprimer toutes les formations
Formation.objects.all().delete()
print("✅ Formations supprimées")

# Supprimer toutes les réclamations
Reclamation.objects.all().delete()
print("✅ Réclamations supprimées")

print("\n" + "="*60)
print("✅ BASE DE DONNÉES NETTOYÉE")
print("="*60)
print("Comptes conservés:")
print("  - DG  (dg / DG2025@Admin)")
print("  - DAF (daf / DAF2025@Admin)")
print("  - RH  (rh / RH2025@Admin)")
print("\nToutes les autres données ont été supprimées.")
print("L'application affichera maintenant 0 partout.")
print("="*60)
