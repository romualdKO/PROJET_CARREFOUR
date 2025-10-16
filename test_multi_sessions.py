"""
Script de test pour le système de présence multi-sessions
Test le scénario où un employé se connecte et déconnecte plusieurs fois dans la journée
"""

import os
import django
from datetime import datetime, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from django.utils import timezone
from CarrefourApp.models import Employe, Presence, SessionPresence

def test_multi_sessions():
    """
    Test le scénario suivant:
    - Connexion à 08:00, déconnexion à 10:00 (2h)
    - Connexion à 14:00, déconnexion à 17:00 (3h)
    - Total: 5h actives
    """
    print("\n" + "="*70)
    print("TEST DU SYSTÈME DE PRÉSENCE MULTI-SESSIONS")
    print("="*70)
    
    # 1. Trouver ou créer un employé de test
    try:
        employe = Employe.objects.filter(est_actif=True).first()
        if not employe:
            print("❌ Aucun employé actif trouvé dans la base de données")
            return
        
        print(f"\n✅ Employé de test: {employe.get_full_name()} (ID: {employe.id})")
        print(f"   Horaire de travail: {employe.heure_debut_travail} - {employe.heure_fin_travail}")
        print(f"   Durée pause: {employe.duree_pause} minutes")
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de l'employé: {e}")
        return
    
    # 2. Nettoyer les données existantes pour aujourd'hui
    today = timezone.now().date()
    SessionPresence.objects.filter(employe=employe, date=today).delete()
    Presence.objects.filter(employe=employe, date=today).delete()
    print(f"\n🧹 Nettoyage des présences existantes pour {today}")
    
    # 3. Simuler première session (08:00 - 10:00)
    print("\n" + "-"*70)
    print("SESSION 1: 08:00 - 10:00 (2 heures)")
    print("-"*70)
    
    session1 = SessionPresence.objects.create(
        employe=employe,
        date=today,
        heure_connexion=time(8, 0),
        heure_deconnexion=time(10, 0)
    )
    print(f"✅ Session 1 créée: {session1.heure_connexion} - {session1.heure_deconnexion}")
    print(f"   Durée active: {session1.duree_active:.2f}h")
    
    # Créer/Mettre à jour la présence
    presence, created = Presence.objects.get_or_create(
        employe=employe,
        date=today,
        defaults={'heure_premiere_arrivee': time(8, 0)}
    )
    presence.heure_derniere_depart = time(10, 0)
    presence.save()  # Ceci va calculer le statut automatiquement
    
    print(f"\n📊 État de la présence après session 1:")
    print(f"   Première arrivée: {presence.heure_premiere_arrivee}")
    print(f"   Dernière départ: {presence.heure_derniere_depart}")
    print(f"   Temps actif total: {presence.temps_actif_total:.2f}h")
    print(f"   Heures travaillées: {presence.calculer_heures_travaillees():.2f}h")
    print(f"   Statut: {presence.statut} ({presence.get_statut_display()})")
    
    # 4. Simuler deuxième session (14:00 - 17:00)
    print("\n" + "-"*70)
    print("SESSION 2: 14:00 - 17:00 (3 heures)")
    print("-"*70)
    
    session2 = SessionPresence.objects.create(
        employe=employe,
        date=today,
        heure_connexion=time(14, 0),
        heure_deconnexion=time(17, 0)
    )
    print(f"✅ Session 2 créée: {session2.heure_connexion} - {session2.heure_deconnexion}")
    print(f"   Durée active: {session2.duree_active:.2f}h")
    
    # Mettre à jour la présence
    presence.heure_derniere_depart = time(17, 0)
    presence.save()  # Ceci va recalculer le statut avec les 2 sessions
    
    print(f"\n📊 État de la présence après session 2:")
    print(f"   Première arrivée: {presence.heure_premiere_arrivee}")
    print(f"   Dernière départ: {presence.heure_derniere_depart}")
    print(f"   Temps actif total: {presence.temps_actif_total:.2f}h")
    print(f"   Heures travaillées: {presence.calculer_heures_travaillees():.2f}h")
    print(f"   Statut: {presence.statut} ({presence.get_statut_display()})")
    
    # 5. Vérification des sessions
    print("\n" + "-"*70)
    print("RÉSUMÉ DES SESSIONS")
    print("-"*70)
    
    sessions = SessionPresence.objects.filter(employe=employe, date=today)
    total_duree = sum(s.duree_active for s in sessions)
    
    print(f"\nNombre de sessions: {sessions.count()}")
    for i, session in enumerate(sessions, 1):
        print(f"\nSession {i}:")
        print(f"  Connexion: {session.heure_connexion}")
        print(f"  Déconnexion: {session.heure_deconnexion}")
        print(f"  Durée: {session.duree_active:.2f}h")
    
    print(f"\n📈 TOTAL:")
    print(f"  Somme durées sessions: {total_duree:.2f}h")
    print(f"  Temps actif total (modèle): {presence.temps_actif_total:.2f}h")
    print(f"  Durée pause: {employe.duree_pause / 60:.2f}h")
    print(f"  Heures travaillées (actif - pause): {presence.calculer_heures_travaillees():.2f}h")
    
    # 6. Calcul des seuils
    heures_requises = presence.calculer_heures_requises()
    seuil_60 = heures_requises * 0.6
    
    print(f"\n🎯 VALIDATION STATUT:")
    print(f"  Heures requises (théorique - pause): {heures_requises:.2f}h")
    print(f"  Seuil 60%: {seuil_60:.2f}h")
    print(f"  Heures travaillées (actif - pause): {presence.calculer_heures_travaillees():.2f}h")
    
    if presence.calculer_heures_travaillees() >= seuil_60:
        print(f"  ✅ {presence.calculer_heures_travaillees():.2f}h >= {seuil_60:.2f}h → Statut valide")
    else:
        print(f"  ❌ {presence.calculer_heures_travaillees():.2f}h < {seuil_60:.2f}h → Absence partielle")
    
    print(f"  Statut final: {presence.get_statut_display()}")
    
    print("\n" + "="*70)
    print("✅ TEST TERMINÉ AVEC SUCCÈS")
    print("="*70 + "\n")

if __name__ == "__main__":
    test_multi_sessions()
