"""
Script pour générer des données de test pour le Scénario 8.1.3
Planning, Demandes de Congé, Pointages, Notifications
"""

import os
import django
from datetime import datetime, timedelta, time, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carrefour.settings')
django.setup()

from CarrefourApp.models import Employe, Planning, DemandeConge, Pointage, Notification
from django.utils import timezone

def creer_planning_test():
    """Créer planning pour la semaine"""
    print("\n📅 Création du planning de test...")
    
    # Récupérer les employés
    try:
        sarah = Employe.objects.get(username='sarah.kouadio')
    except Employe.DoesNotExist:
        sarah = Employe.objects.create_user(
            username='sarah.kouadio',
            first_name='Sarah',
            last_name='Kouadio',
            email='sarah@carrefour.ci',
            role='CAISSIER',
            departement='VENTES',
            telephone='0707070707',
            password='sarah123'
        )
        print(f"✅ Employée créée: Sarah Kouadio (sarah.kouadio / sarah123)")
    
    try:
        marc = Employe.objects.get(username='marc.diallo')
    except Employe.DoesNotExist:
        marc = Employe.objects.create_user(
            username='marc.diallo',
            first_name='Marc',
            last_name='Diallo',
            email='marc@carrefour.ci',
            role='STOCK',
            departement='LOGISTIQUE',
            telephone='0708080808',
            password='marc123'
        )
        print(f"✅ Employé créé: Marc Diallo (marc.diallo / marc123)")
    
    try:
        julie = Employe.objects.get(username='julie.mensah')
    except Employe.DoesNotExist:
        julie = Employe.objects.create_user(
            username='julie.mensah',
            first_name='Julie',
            last_name='Mensah',
            email='julie@carrefour.ci',
            role='CAISSIER',
            departement='VENTES',
            telephone='0709090909',
            password='julie123'
        )
        print(f"✅ Employée créée: Julie Mensah (julie.mensah / julie123)")
    
    try:
        manager = Employe.objects.get(role='MANAGER')
    except Employe.DoesNotExist:
        manager = Employe.objects.create_user(
            username='manager',
            first_name='Responsable',
            last_name='Ventes',
            email='manager@carrefour.ci',
            role='MANAGER',
            departement='VENTES',
            telephone='0701010101',
            password='manager123',
            is_staff=True
        )
        print(f"✅ Manager créé: Responsable Ventes (manager / manager123)")
    
    # Créer planning pour la semaine prochaine (21-27 Oct 2025)
    Planning.objects.all().delete()
    
    today = date(2025, 10, 20)  # Lundi 20 octobre
    
    plannings_crees = 0
    
    # Sarah - CAISSE MATIN toute la semaine
    for i in range(7):  # 7 jours
        jour = today + timedelta(days=i)
        if jour.weekday() < 5:  # Lun-Ven uniquement
            Planning.objects.create(
                employe=sarah,
                date=jour,
                poste='CAISSE',
                creneau='MATIN',
                statut='PRESENT',
                heures_prevues=8.0
            )
            plannings_crees += 1
    
    # Marc - RAYON APRES-MIDI toute la semaine
    for i in range(7):
        jour = today + timedelta(days=i)
        if jour.weekday() < 5:
            Planning.objects.create(
                employe=marc,
                date=jour,
                poste='RAYON',
                creneau='APRES_MIDI',
                statut='PRESENT',
                heures_prevues=8.0
            )
            plannings_crees += 1
    
    # Julie - CAISSE MATIN toute la semaine
    for i in range(7):
        jour = today + timedelta(days=i)
        if jour.weekday() < 5:
            Planning.objects.create(
                employe=julie,
                date=jour,
                poste='CAISSE',
                creneau='MATIN',
                statut='PRESENT',
                heures_prevues=8.0
            )
            plannings_crees += 1
    
    print(f"✅ {plannings_crees} plannings créés")
    return sarah, marc, julie, manager


def creer_demandes_conge(sarah, marc, manager):
    """Créer demandes de congé de test"""
    print("\n🏖️ Création des demandes de congé...")
    
    DemandeConge.objects.all().delete()
    
    # Demande 1: Sarah demande 1 jour de congé (EN_ATTENTE)
    demande1 = DemandeConge.objects.create(
        employe=sarah,
        type_conge='CONGE_PAYE',
        date_debut=date(2025, 10, 24),  # Jeudi
        date_fin=date(2025, 10, 24),
        motif="Raisons personnelles - rendez-vous médical",
        statut='EN_ATTENTE'
    )
    print(f"✅ Demande créée: {demande1}")
    
    # Demande 2: Marc demande 2 jours RTT (EN_ATTENTE)
    demande2 = DemandeConge.objects.create(
        employe=marc,
        type_conge='RTT',
        date_debut=date(2025, 10, 28),  # Lundi
        date_fin=date(2025, 10, 29),     # Mardi
        motif="Récupération heures supplémentaires",
        statut='EN_ATTENTE'
    )
    print(f"✅ Demande créée: {demande2}")
    
    # Demande 3: Sarah - Congé approuvé (historique)
    demande3 = DemandeConge.objects.create(
        employe=sarah,
        type_conge='CONGE_PAYE',
        date_debut=date(2025, 10, 10),
        date_fin=date(2025, 10, 11),
        motif="Congé familial",
        statut='APPROUVE',
        approuve_par=manager,
        reponse_manager="Approuvé. Bon repos!",
        date_reponse=timezone.now() - timedelta(days=5)
    )
    print(f"✅ Demande créée: {demande3}")
    
    return demande1, demande2


def creer_pointages(sarah, marc, julie):
    """Créer pointages de test"""
    print("\n⏰ Création des pointages...")
    
    Pointage.objects.all().delete()
    
    today = date(2025, 10, 20)
    pointages_crees = 0
    
    # Pointages des 5 derniers jours pour chaque employé
    for i in range(5):
        jour = today - timedelta(days=i+1)
        
        # Sarah - Toujours à l'heure
        Pointage.objects.create(
            employe=sarah,
            date=jour,
            heure_entree=time(6, 0),
            heure_sortie=time(14, 10) if i == 0 else time(14, 5),
            type_journee='NORMAL',
            validee=True
        )
        pointages_crees += 1
        
        # Marc - Quelques retards
        retard = i * 5  # 0, 5, 10, 15, 20 minutes
        Pointage.objects.create(
            employe=marc,
            date=jour,
            heure_entree=time(14, retard),
            heure_sortie=time(22, 10),
            type_journee='NORMAL',
            validee=True
        )
        pointages_crees += 1
        
        # Julie - Ponctuelle
        Pointage.objects.create(
            employe=julie,
            date=jour,
            heure_entree=time(6, 5),
            heure_sortie=time(14, 0),
            type_journee='NORMAL',
            validee=True
        )
        pointages_crees += 1
    
    # Pointage d'aujourd'hui (en cours) pour Sarah
    Pointage.objects.create(
        employe=sarah,
        date=today,
        heure_entree=time(6, 5),
        heure_sortie=None,  # Pas encore sortie
        type_journee='NORMAL',
        validee=False
    )
    pointages_crees += 1
    
    print(f"✅ {pointages_crees} pointages créés")


def creer_notifications(sarah, marc, manager, demande1, demande2):
    """Créer notifications de test"""
    print("\n🔔 Création des notifications...")
    
    Notification.objects.all().delete()
    
    # Notification pour manager: nouvelle demande Sarah
    Notification.objects.create(
        destinataire=manager,
        titre="Nouvelle demande de congé",
        message=f"{sarah.get_full_name()} a fait une demande de congé payé du 24/10 au 24/10 (1 jour)",
        type_notif='DEMANDE_CONGE',
        lue=False,
        lien='/planning/demandes-conge/'
    )
    
    # Notification pour manager: nouvelle demande Marc
    Notification.objects.create(
        destinataire=manager,
        titre="Nouvelle demande de congé",
        message=f"{marc.get_full_name()} a fait une demande de RTT du 28/10 au 29/10 (2 jours)",
        type_notif='DEMANDE_CONGE',
        lue=False,
        lien='/planning/demandes-conge/'
    )
    
    # Notification pour Sarah: congé approuvé (ancien)
    Notification.objects.create(
        destinataire=sarah,
        titre="Demande de congé approuvée ✅",
        message=f"Votre demande de congé payé du 10/10 au 11/10 a été approuvée par {manager.get_full_name()}",
        type_notif='REPONSE_CONGE',
        lue=True,
        lien='/planning/mes-demandes/',
        lue_le=timezone.now() - timedelta(days=5)
    )
    
    # Notification planning mis à jour
    Notification.objects.create(
        destinataire=sarah,
        titre="Planning mis à jour 📅",
        message="Votre planning de la semaine prochaine est disponible",
        type_notif='PLANNING_MAJ',
        lue=False,
        lien='/planning/mon-planning/'
    )
    
    print(f"✅ {Notification.objects.count()} notifications créées")


def afficher_resume():
    """Afficher résumé des données créées"""
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES DONNÉES DE TEST - SCÉNARIO 8.1.3")
    print("="*60)
    
    print(f"\n👥 EMPLOYÉS: {Employe.objects.count()}")
    print(f"   • Caissiers: {Employe.objects.filter(role='CAISSIER').count()}")
    print(f"   • Stock: {Employe.objects.filter(role='STOCK').count()}")
    print(f"   • Managers: {Employe.objects.filter(role='MANAGER').count()}")
    
    print(f"\n📅 PLANNINGS: {Planning.objects.count()}")
    print(f"   • Poste Caisse: {Planning.objects.filter(poste='CAISSE').count()}")
    print(f"   • Poste Rayon: {Planning.objects.filter(poste='RAYON').count()}")
    
    print(f"\n🏖️ DEMANDES DE CONGÉ: {DemandeConge.objects.count()}")
    print(f"   • En attente: {DemandeConge.objects.filter(statut='EN_ATTENTE').count()}")
    print(f"   • Approuvées: {DemandeConge.objects.filter(statut='APPROUVE').count()}")
    
    print(f"\n⏰ POINTAGES: {Pointage.objects.count()}")
    print(f"   • Validés: {Pointage.objects.filter(validee=True).count()}")
    print(f"   • En attente: {Pointage.objects.filter(validee=False).count()}")
    
    print(f"\n🔔 NOTIFICATIONS: {Notification.objects.count()}")
    print(f"   • Non lues: {Notification.objects.filter(lue=False).count()}")
    print(f"   • Lues: {Notification.objects.filter(lue=True).count()}")
    
    print("\n" + "="*60)
    print("✅ COMPTES DE TEST CRÉÉS")
    print("="*60)
    print("\n👤 Sarah Kouadio (Caissière)")
    print("   Username: sarah.kouadio")
    print("   Password: sarah123")
    print("   Planning: CAISSE - MATIN (Lun-Ven)")
    print("   Demande en attente: 1 jour (24/10)")
    
    print("\n👤 Marc Diallo (Gestionnaire Stock)")
    print("   Username: marc.diallo")
    print("   Password: marc123")
    print("   Planning: RAYON - APRÈS-MIDI (Lun-Ven)")
    print("   Demande en attente: 2 jours RTT (28-29/10)")
    
    print("\n👤 Julie Mensah (Caissière)")
    print("   Username: julie.mensah")
    print("   Password: julie123")
    print("   Planning: CAISSE - MATIN (Lun-Ven)")
    
    print("\n👤 Responsable Ventes (Manager)")
    print("   Username: manager")
    print("   Password: manager123")
    print("   Notifications: 2 demandes en attente")
    
    print("\n" + "="*60)


if __name__ == '__main__':
    print("\n🚀 Démarrage génération données Scénario 8.1.3...")
    
    sarah, marc, julie, manager = creer_planning_test()
    demande1, demande2 = creer_demandes_conge(sarah, marc, manager)
    creer_pointages(sarah, marc, julie)
    creer_notifications(sarah, marc, manager, demande1, demande2)
    
    afficher_resume()
    
    print("\n✅ Données de test créées avec succès!")
    print("\n🔗 URLs à tester:")
    print("   • http://127.0.0.1:8000/planning/mon-planning/")
    print("   • http://127.0.0.1:8000/planning/demander-conge/")
    print("   • http://127.0.0.1:8000/planning/equipe/")
    print("   • http://127.0.0.1:8000/planning/demandes-conge/")
    print("   • http://127.0.0.1:8000/planning/pointage/")
    print("   • http://127.0.0.1:8000/planning/notifications/")
    print()
