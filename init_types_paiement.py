# Script d'initialisation des types de paiement pour le module Caisse
# À exécuter via: python manage.py shell < init_types_paiement.py

from CarrefourApp.models import TypePaiement

types_paiement = [
    {'nom': 'Espèces', 'code': 'ESPECES', 'icone': 'fa-money-bill-wave'},
    {'nom': 'Carte Bancaire', 'code': 'CB', 'icone': 'fa-credit-card'},
    {'nom': 'Mobile Money (Orange Money)', 'code': 'ORANGE_MONEY', 'icone': 'fa-mobile-alt'},
    {'nom': 'Mobile Money (MTN Money)', 'code': 'MTN_MONEY', 'icone': 'fa-mobile-alt'},
    {'nom': 'Mobile Money (Moov Money)', 'code': 'MOOV_MONEY', 'icone': 'fa-mobile-alt'},
    {'nom': 'Chèque', 'code': 'CHEQUE', 'icone': 'fa-money-check'},
    {'nom': 'Virement', 'code': 'VIREMENT', 'icone': 'fa-exchange-alt'},
]

print("Création des types de paiement...")
created_count = 0

for tp_data in types_paiement:
    tp, created = TypePaiement.objects.get_or_create(
        code=tp_data['code'],
        defaults={
            'nom': tp_data['nom'],
            'icone': tp_data['icone'],
            'est_actif': True
        }
    )
    if created:
        print(f"✅ Créé: {tp.nom}")
        created_count += 1
    else:
        print(f"⏭️  Existe déjà: {tp.nom}")

print(f"\n{created_count} types de paiement créés sur {len(types_paiement)} total.")
print("✅ Initialisation terminée!")
