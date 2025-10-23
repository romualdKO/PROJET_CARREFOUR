"""
Script pour corriger et assigner les départements selon les rôles des employés
Tous les employés ne doivent PAS être dans VENTES
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from CarrefourApp.models import Employe

def corriger_departements():
    """
    Assigne les départements appropriés selon le rôle de chaque employé
    """
    
    print("="*70)
    print(" CORRECTION DES DÉPARTEMENTS SELON LES RÔLES")
    print("="*70)
    
    # Mapping role → département approprié
    role_to_departement = {
        'DG': 'DIRECTION',          # Directeur Général → Direction
        'DAF': 'FINANCE',            # Directeur Financier → Finance
        'RH': 'RH',                  # Responsable RH → Ressources Humaines
        'STOCK': 'LOGISTIQUE',       # Gestionnaire Stock → Logistique
        'CAISSIER': 'VENTES',        # Caissier → Ventes
        'MARKETING': 'MARKETING',    # Marketing → Marketing
        'ANALYSTE': 'DIRECTION',     # Analyste → Direction
    }
    
    employes = Employe.objects.all().order_by('role', 'last_name')
    
    print(f"\n📊 Total employés à vérifier: {employes.count()}\n")
    
    corrections = 0
    deja_corrects = 0
    
    for employe in employes:
        departement_correct = role_to_departement.get(employe.role, 'VENTES')
        
        if employe.departement != departement_correct:
            ancien_dept = employe.get_departement_display()
            employe.departement = departement_correct
            employe.save()
            
            nouveau_dept = employe.get_departement_display()
            corrections += 1
            
            print(f"✅ {employe.get_full_name()} ({employe.get_role_display()})")
            print(f"   {employe.employee_id}")
            print(f"   Ancien: {ancien_dept} → Nouveau: {nouveau_dept}")
            print()
        else:
            deja_corrects += 1
            print(f"✓ {employe.get_full_name()} - {employe.get_departement_display()} (déjà correct)")
    
    print("\n" + "="*70)
    print(" RÉSUMÉ")
    print("="*70)
    print(f"📝 Employés vérifiés:     {employes.count()}")
    print(f"✅ Corrections effectuées: {corrections}")
    print(f"✓ Déjà corrects:          {deja_corrects}")
    print()
    
    # Afficher la répartition par département
    print("="*70)
    print(" RÉPARTITION PAR DÉPARTEMENT")
    print("="*70)
    
    from django.db.models import Count
    
    repartition = Employe.objects.values('departement').annotate(
        count=Count('id')
    ).order_by('-count')
    
    for dept in repartition:
        dept_obj = next((d for d in Employe.DEPARTEMENTS if d[0] == dept['departement']), None)
        dept_nom = dept_obj[1] if dept_obj else dept['departement']
        print(f"🏢 {dept_nom}: {dept['count']} employé(s)")
    
    print("\n" + "="*70)
    print(" VÉRIFICATION PAR RÔLE")
    print("="*70)
    
    for role_code, role_nom in Employe.ROLES:
        employes_role = Employe.objects.filter(role=role_code)
        if employes_role.exists():
            print(f"\n💼 {role_nom} ({employes_role.count()}):")
            for emp in employes_role:
                print(f"   - {emp.get_full_name()} → {emp.get_departement_display()}")

def main():
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "CORRECTION DES DÉPARTEMENTS" + " "*26 + "║")
    print("╚" + "="*68 + "╝")
    print()
    
    try:
        corriger_departements()
        print("\n✨ Correction terminée avec succès!\n")
    except Exception as e:
        print(f"\n❌ Erreur lors de la correction: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
