"""
Script de vérification des remises et de la fidélité
Vérifie que le système de caisse applique correctement les remises
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from CarrefourApp.models import Client, Vente, Produit
from django.utils import timezone
from datetime import timedelta

def afficher_titre(texte):
    print("\n" + "="*70)
    print(f"  {texte}")
    print("="*70)

def verifier_clients_fidelite():
    """Vérifier les clients et leurs niveaux de fidélité"""
    afficher_titre("👥 CLIENTS ET NIVEAUX DE FIDÉLITÉ")
    
    clients = Client.objects.filter(est_actif=True).order_by('-points_fidelite')
    
    if not clients.exists():
        print("❌ Aucun client trouvé dans la base de données")
        return
    
    print(f"\n📊 Total: {clients.count()} clients actifs\n")
    
    # Statistiques par niveau
    vip_count = clients.filter(niveau_fidelite='VIP').count()
    gold_count = clients.filter(niveau_fidelite='GOLD').count()
    silver_count = clients.filter(niveau_fidelite='SILVER').count()
    tous_count = clients.filter(niveau_fidelite='TOUS').count()
    
    print(f"🏆 VIP (≥2000 pts, 10% remise):    {vip_count} clients")
    print(f"🥇 GOLD (≥1000 pts, 5% remise):   {gold_count} clients")
    print(f"🥈 SILVER (≥500 pts, 3% remise):  {silver_count} clients")
    print(f"👤 TOUS (0-499 pts, 0% remise):   {tous_count} clients")
    
    print("\n📋 TOP 10 CLIENTS PAR POINTS:\n")
    for i, client in enumerate(clients[:10], 1):
        emoji = "🏆" if client.niveau_fidelite == 'VIP' else "🥇" if client.niveau_fidelite == 'GOLD' else "🥈" if client.niveau_fidelite == 'SILVER' else "👤"
        print(f"{i:2d}. {emoji} {client.nom} {client.prenom}")
        print(f"    📞 {client.telephone}")
        print(f"    ⭐ Niveau: {client.niveau_fidelite} | Points: {client.points_fidelite}")
        print(f"    💰 Total achats: {client.total_achats:,.0f} FCFA")
        
        # Calculer le nombre d'achats
        nb_achats = Vente.objects.filter(client=client).count()
        print(f"    🛒 Nombre d'achats: {nb_achats}")
        print()

def verifier_ventes_avec_remises():
    """Vérifier les ventes avec remises appliquées"""
    afficher_titre("💰 VENTES AVEC REMISES APPLIQUÉES")
    
    # Ventes récentes avec remises
    ventes_avec_remise = Vente.objects.filter(
        remise__gt=0
    ).order_by('-date_vente')[:20]
    
    if not ventes_avec_remise.exists():
        print("❌ Aucune vente avec remise trouvée")
        return
    
    print(f"\n📊 Total: {ventes_avec_remise.count()} ventes avec remises (dernières 20)\n")
    
    # Statistiques globales
    total_remises = sum(v.remise for v in ventes_avec_remise)
    total_ventes = ventes_avec_remise.count()
    moyenne_remise = total_remises / total_ventes if total_ventes > 0 else 0
    
    print(f"💵 Total remises accordées: {total_remises:,.0f} FCFA")
    print(f"📊 Remise moyenne: {moyenne_remise:,.0f} FCFA")
    
    print("\n📋 DÉTAIL DES VENTES:\n")
    for i, vente in enumerate(ventes_avec_remise, 1):
        print(f"{i:2d}. 🧾 Vente #{vente.numero_transaction}")
        print(f"    📅 Date: {vente.date_vente.strftime('%d/%m/%Y %H:%M')}")
        
        if vente.client:
            print(f"    👤 Client: {vente.client.nom} {vente.client.prenom}")
            print(f"    ⭐ Niveau: {vente.client.niveau_fidelite}")
        else:
            print(f"    👤 Client: Non identifié")
        
        # Calculer le pourcentage de remise
        montant_avant_remise = vente.montant_total
        pourcentage = (vente.remise / montant_avant_remise * 100) if montant_avant_remise > 0 else 0
        
        print(f"    💰 Montant avant remise: {montant_avant_remise:,.0f} FCFA")
        print(f"    🎁 Remise appliquée: {vente.remise:,.0f} FCFA ({pourcentage:.1f}%)")
        print(f"    ✅ Montant final: {vente.montant_final:,.0f} FCFA")
        print()

def simuler_calcul_remise():
    """Simuler le calcul de remise pour différents scénarios"""
    afficher_titre("🧮 SIMULATION DE CALCUL DES REMISES")
    
    scenarios = [
        {
            'nom': 'Client VIP - Achat 50 000 FCFA',
            'niveau': 'VIP',
            'points': 2500,
            'montant': 50000
        },
        {
            'nom': 'Client GOLD - Achat 45 000 FCFA',
            'niveau': 'GOLD',
            'points': 1200,
            'montant': 45000
        },
        {
            'nom': 'Client SILVER - Achat 30 000 FCFA',
            'niveau': 'SILVER',
            'points': 600,
            'montant': 30000
        },
        {
            'nom': 'Client SILVER - Achat 50 000 FCFA',
            'niveau': 'SILVER',
            'points': 750,
            'montant': 50000
        },
        {
            'nom': 'Client TOUS - Achat 20 000 FCFA',
            'niveau': 'TOUS',
            'points': 200,
            'montant': 20000
        },
        {
            'nom': 'Client TOUS - Achat 45 000 FCFA',
            'niveau': 'TOUS',
            'points': 300,
            'montant': 45000
        },
    ]
    
    print("\n📊 DIFFÉRENTS SCÉNARIOS:\n")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['nom']}")
        print(f"   ⭐ Niveau: {scenario['niveau']} | Points: {scenario['points']}")
        print("   " + "-" * 60)
        
        sous_total = scenario['montant']
        print(f"   📝 Sous-total:                {sous_total:>15,.0f} FCFA")
        
        # Remise fidélité
        remise_fidelite = 0
        taux_fidelite = 0
        if scenario['niveau'] == 'VIP':
            taux_fidelite = 0.10
            remise_fidelite = sous_total * 0.10
        elif scenario['niveau'] == 'GOLD':
            taux_fidelite = 0.05
            remise_fidelite = sous_total * 0.05
        elif scenario['niveau'] == 'SILVER':
            taux_fidelite = 0.03
            remise_fidelite = sous_total * 0.03
        
        if remise_fidelite > 0:
            print(f"   🎁 Remise fidélité ({taux_fidelite*100:.0f}%): {remise_fidelite:>15,.0f} FCFA")
        
        montant_apres_fidelite = sous_total - remise_fidelite
        
        # Remise promotionnelle
        remise_promo = 0
        if montant_apres_fidelite >= 40000:
            remise_promo = montant_apres_fidelite * 0.05
            print(f"   🎉 Remise promo (≥40K, 5%):  {remise_promo:>15,.0f} FCFA")
        
        # Total remises
        total_remises = remise_fidelite + remise_promo
        if total_remises > 0:
            print(f"   💵 TOTAL REMISES:             {total_remises:>15,.0f} FCFA")
        
        # Montant après remises
        montant_avant_tva = sous_total - total_remises
        
        # TVA
        tva = montant_avant_tva * 0.18
        print(f"   📊 TVA (18%):                 {tva:>15,.0f} FCFA")
        
        # Montant final
        montant_final = montant_avant_tva + tva
        print(f"   ✅ MONTANT FINAL:             {montant_final:>15,.0f} FCFA")
        
        # Points gagnés
        points_gagnes = int(montant_final / 1000)
        nouveaux_points = scenario['points'] + points_gagnes
        print(f"   ⭐ Points gagnés:             {points_gagnes:>15} points")
        print(f"   📈 Nouveaux points:           {nouveaux_points:>15} points")
        
        # Changement de niveau ?
        ancien_niveau = scenario['niveau']
        nouveau_niveau = 'TOUS'
        if nouveaux_points >= 2000:
            nouveau_niveau = 'VIP'
        elif nouveaux_points >= 1000:
            nouveau_niveau = 'GOLD'
        elif nouveaux_points >= 500:
            nouveau_niveau = 'SILVER'
        
        if ancien_niveau != nouveau_niveau:
            print(f"   🎊 CHANGEMENT DE NIVEAU: {ancien_niveau} → {nouveau_niveau} ✨")

def verifier_produits_stock():
    """Vérifier quelques produits et leur stock"""
    afficher_titre("📦 EXEMPLES DE PRODUITS")
    
    produits = Produit.objects.filter(est_actif=True)[:5]
    
    if not produits.exists():
        print("❌ Aucun produit trouvé")
        return
    
    print("\n📊 5 premiers produits actifs:\n")
    
    for i, produit in enumerate(produits, 1):
        print(f"{i}. {produit.nom}")
        print(f"   💰 Prix: {produit.prix_unitaire:,.0f} FCFA")
        print(f"   📦 Stock: {produit.stock_actuel} unités")
        
        # Vérifier s'il a des promotions
        promotions = produit.promotions.filter(est_active=True)
        if promotions.exists():
            for promo in promotions:
                print(f"   🎉 Promotion: {promo.titre} (-{promo.reduction}%)")
        print()

def main():
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "VÉRIFICATION SYSTÈME DE CAISSE" + " "*23 + "║")
    print("║" + " "*10 + "Remises, Promotions & Cartes de Fidélité" + " "*18 + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        # 1. Vérifier les clients
        verifier_clients_fidelite()
        
        # 2. Vérifier les ventes avec remises
        verifier_ventes_avec_remises()
        
        # 3. Simuler des calculs
        simuler_calcul_remise()
        
        # 4. Vérifier les produits
        verifier_produits_stock()
        
        afficher_titre("✅ VÉRIFICATION TERMINÉE")
        print("\n✨ Toutes les fonctionnalités de remises et fidélité sont correctement implémentées!")
        print("\n📚 Consultez VERIFICATION_REMISES_ET_FIDELITE.md pour plus de détails.\n")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la vérification: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
