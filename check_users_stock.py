import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from CarrefourApp.models import Employe

print("Liste des utilisateurs avec accès au module Stock:\n")
employes = Employe.objects.all()
for emp in employes:
    print(f"Username: {emp.username}, Rôle: {emp.role}, Accès Stock: {emp.acces_stocks}")
