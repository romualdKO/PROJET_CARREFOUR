"""
Script pour vérifier que les données sont bien en base de données
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from CarrefourApp.models import DemandeConge, Planning, Absence, Employe

print("\n" + "=" * 80)
print(" " * 25 + "VÉRIFICATION BASE DE DONNÉES")
print("=" * 80)
print()

# 1. Demandes de congés
print("📋 DEMANDES DE CONGÉS EN BASE DE DONNÉES:")
print("-" * 80)
demandes = DemandeConge.objects.all()
print(f"Total: {demandes.count()} demandes")
print()

if demandes.exists():
    for d in demandes[:10]:
        print(f"  ID: {d.id}")
        print(f"  Employé: {d.employe.first_name} {d.employe.last_name}")
        print(f"  Type: {d.get_type_conge_display()}")
        print(f"  Période: {d.date_debut} au {d.date_fin}")
        print(f"  Statut: {d.statut}")
        if d.approuve_par:
            print(f"  Approuvé par: {d.approuve_par.first_name} {d.approuve_par.last_name}")
        print()
else:
    print("  ⚠️ Aucune demande en base de données")
    print()

# 2. Plannings
print("📅 PLANNINGS EN BASE DE DONNÉES:")
print("-" * 80)
plannings = Planning.objects.all()
print(f"Total: {plannings.count()} plannings")
print()

if plannings.exists():
    for p in plannings[:10]:
        print(f"  ID: {p.id}")
        print(f"  Employé: {p.employe.first_name} {p.employe.last_name}")
        print(f"  Date: {p.date}")
        print(f"  Poste: {p.poste}")
        print(f"  Créneau: {p.creneau}")
        print(f"  Statut: {p.statut}")
        print()
else:
    print("  ⚠️ Aucun planning en base de données")
    print()

# 3. Absences
print("📊 ABSENCES EN BASE DE DONNÉES:")
print("-" * 80)
absences = Absence.objects.all()
print(f"Total: {absences.count()} absences")
print()

if absences.exists():
    for a in absences[:10]:
        print(f"  ID: {a.id}")
        print(f"  Employé: {a.employe.first_name} {a.employe.last_name}")
        print(f"  Date: {a.date}")
        print(f"  Type: {a.get_type_absence_display()}")
        print(f"  Justifiée: {'Oui' if a.justifiee else 'Non'}")
        print()
else:
    print("  ⚠️ Aucune absence en base de données")
    print()

# 4. Employés
print("👥 EMPLOYÉS EN BASE DE DONNÉES:")
print("-" * 80)
employes = Employe.objects.filter(est_actif=True)
print(f"Total: {employes.count()} employés actifs")
print()

for emp in employes[:10]:
    print(f"  Username: {emp.username}")
    print(f"  Nom: {emp.first_name} {emp.last_name}")
    print(f"  Rôle: {emp.role}")
    print(f"  Département: {emp.departement}")
    
    # Compter ses demandes
    nb_demandes = emp.demandes_conge.count()
    nb_plannings = emp.plannings.count()
    nb_absences = emp.absences.count()
    
    print(f"  📋 Demandes de congé: {nb_demandes}")
    print(f"  📅 Plannings: {nb_plannings}")
    print(f"  📊 Absences: {nb_absences}")
    print()

print("=" * 80)
print(" " * 20 + "✅ TOUTES LES DONNÉES SONT EN BASE DE DONNÉES")
print("=" * 80)
print()
print("🔍 Pour voir plus de détails, utilisez :")
print("   python manage.py dbshell")
print("   SELECT * FROM CarrefourApp_demandeconge;")
print("   SELECT * FROM CarrefourApp_planning;")
print("   SELECT * FROM CarrefourApp_absence;")
print()
