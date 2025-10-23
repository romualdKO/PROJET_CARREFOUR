import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from CarrefourApp.models import CommandeFournisseur

print("Vérification des lignes de commande:\n")
for i in range(1, 11):
    try:
        cmd = CommandeFournisseur.objects.get(id=i)
        nb_lignes = cmd.lignes.count()
        print(f"Commande #{cmd.id}: {nb_lignes} ligne(s)")
    except CommandeFournisseur.DoesNotExist:
        print(f"Commande #{i}: n'existe pas")
