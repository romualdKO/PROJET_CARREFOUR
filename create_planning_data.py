"""
Script pour créer des données de test pour le Scénario 8.1.3
Gestion du planning et des congés
"""

import os
import django
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from django.utils import timezone
from CarrefourApp.models import (
    Employe, Planning, DemandeConge, Absence
)

def creer_donnees_test():
    print("=" * 80)
    print(" " * 20 + "CRÉATION DONNÉES TEST - SCÉNARIO 8.1.3")
    print("=" * 80)
    print()
    
    # 1. Récupérer les employés
    print("📌 Étape 1: Récupération des employés")
    employes = list(Employe.objects.filter(est_actif=True))
    if not employes:
        print("❌ Aucun employé trouvé. Créez d'abord des employés.")
        return
    
    print(f"✅ {len(employes)} employés trouvés")
    for emp in employes[:5]:
        print(f"   - {emp.get_full_name()} ({emp.role})")
    print()
    
    # 2. Créer des plannings pour la semaine
    print("📌 Étape 2: Création des plannings")
    aujourd_hui = timezone.now().date()
    debut_semaine = aujourd_hui - timedelta(days=aujourd_hui.weekday())
    
    postes = ['CAISSE', 'RAYON', 'RECEPTION', 'SERVICE_CLIENT']
    creneaux = ['MATIN', 'APRES_MIDI']
    
    plannings_crees = 0
    for i in range(14):  # 2 semaines
        date_planning = debut_semaine + timedelta(days=i)
        
        for employe in employes[:8]:  # 8 premiers employés
            if date_planning.weekday() < 6:  # Pas le dimanche
                creneau = creneaux[i % len(creneaux)]
                
                planning, created = Planning.objects.get_or_create(
                    employe=employe,
                    date=date_planning,
                    creneau=creneau,
                    defaults={
                        'poste': postes[i % len(postes)],
                        'statut': 'PRESENT',
                        'heures_prevues': 8.0,
                        'heures_reelles': 8.0,
                    }
                )
                
                if created:
                    plannings_crees += 1
    
    print(f"✅ {plannings_crees} plannings créés")
    print()
    
    # 3. Créer des demandes de congés
    print("📌 Étape 3: Création des demandes de congés")
    types_conges = ['CONGE_PAYE', 'CONGE_MALADIE', 'RTT']
    statuts = ['EN_ATTENTE', 'APPROUVE', 'REFUSE']
    
    demandes_creees = 0
    for i, employe in enumerate(employes[:10]):
        for j in range(2):  # 2 demandes par employé
            date_debut = aujourd_hui + timedelta(days=(i * 7) + (j * 14))
            date_fin = date_debut + timedelta(days=3)
            
            demande, created = DemandeConge.objects.get_or_create(
                employe=employe,
                date_debut=date_debut,
                date_fin=date_fin,
                defaults={
                    'type_conge': types_conges[j % len(types_conges)],
                    'motif': f'Demande de congé pour raisons personnelles (test {i}-{j})',
                    'statut': statuts[j % len(statuts)],
                    'cree_le': timezone.now() - timedelta(days=(j * 3)),
                }
            )
            
            # Si approuvé ou rejeté, ajouter des infos de traitement
            if created and demande.statut != 'EN_ATTENTE':
                rh = Employe.objects.filter(role='RH').first()
                if rh:
                    demande.approuve_par = rh
                    demande.date_reponse = timezone.now() - timedelta(days=(j * 2))
                    if demande.statut == 'APPROUVE':
                        demande.reponse_manager = "Demande approuvée. Bon congé!"
                    else:
                        demande.reponse_manager = "Demande rejetée - Manque de personnel."
                    demande.save()
            
            if created:
                demandes_creees += 1
    
    print(f"✅ {demandes_creees} demandes de congés créées")
    print()
    
    # 4. Créer des absences
    print("📌 Étape 4: Création des absences")
    types_absences = ['MALADIE', 'CONGE', 'ABSENCE_INJUSTIFIEE', 'AUTRE']
    
    absences_creees = 0
    for i, employe in enumerate(employes[:8]):
        for j in range(3):  # 3 absences par employé
            date_absence = aujourd_hui - timedelta(days=(i * 2) + (j * 7))
            
            absence, created = Absence.objects.get_or_create(
                employe=employe,
                date=date_absence,
                defaults={
                    'type_absence': types_absences[j % len(types_absences)],
                    'justifiee': j % 2 == 0,  # Alternance justifiée/non justifiée
                    'commentaire': f'Certificat médical fourni' if j % 2 == 0 else '',
                }
            )
            
            if created:
                absences_creees += 1
    
    print(f"✅ {absences_creees} absences créées")
    print()
    
    # 5. Statistiques finales
    print("=" * 80)
    print(" " * 25 + "STATISTIQUES FINALES")
    print("=" * 80)
    print()
    
    total_plannings = Planning.objects.count()
    total_demandes = DemandeConge.objects.count()
    total_absences = Absence.objects.count()
    
    print(f"📊 Plannings totaux: {total_plannings}")
    print(f"📊 Demandes de congés totales: {total_demandes}")
    print(f"   - En attente: {DemandeConge.objects.filter(statut='EN_ATTENTE').count()}")
    print(f"   - Approuvées: {DemandeConge.objects.filter(statut='APPROUVE').count()}")
    print(f"   - Rejetées: {DemandeConge.objects.filter(statut='REFUSE').count()}")
    print(f"📊 Absences totales: {total_absences}")
    print(f"   - Justifiées: {Absence.objects.filter(justifiee=True).count()}")
    print(f"   - Non justifiées: {Absence.objects.filter(justifiee=False).count()}")
    print()
    
    # 6. URLs de test
    print("=" * 80)
    print(" " * 30 + "URLS DE TEST")
    print("=" * 80)
    print()
    print("🔹 ESPACE EMPLOYÉ:")
    print("   - Mon planning: http://127.0.0.1:8000/planning/mon-planning/")
    print("   - Demander un congé: http://127.0.0.1:8000/planning/demander-conge/")
    print("   - Mes demandes: http://127.0.0.1:8000/planning/mes-demandes/")
    print("   - Changer mon mot de passe: http://127.0.0.1:8000/planning/changer-mot-de-passe/")
    print()
    print("🔹 ESPACE RH/MANAGER:")
    print("   - Gérer demandes de congés: http://127.0.0.1:8000/rh/demandes-conges/")
    print("   - Gérer absences: http://127.0.0.1:8000/rh/gestion-absences/")
    print("   - Réinitialiser MDP: http://127.0.0.1:8000/rh/reinitialiser-mdp/")
    print()
    
    print("=" * 80)
    print(" " * 25 + "✅ SCRIPT TERMINÉ AVEC SUCCÈS")
    print("=" * 80)

if __name__ == '__main__':
    try:
        creer_donnees_test()
    except Exception as e:
        print(f"❌ Erreur lors de la création des données: {str(e)}")
        import traceback
        traceback.print_exc()
