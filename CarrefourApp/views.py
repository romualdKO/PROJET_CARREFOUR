from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import render, redirect
from .forms import ProduitForm
from .models import *
from .utils import generer_id_produit
#Ajout produit PrOJET_CARREFOUR/CarrefourApp/views.py
def ajouter_produit(request):
    if request.method == 'POST':
        # On récupère chaque champ manuellement
        nom = request.POST.get('nom')
        prixAchat = request.POST.get('prixAchat')
        prixVente = request.POST.get('prixVente')
        quantite = request.POST.get('quantite')
        categorie = Categorie.objects.get(pk=request.POST.get('categorie'))
        description = request.POST.get('description', '')
        image = request.FILES.get('image')  # pour le champ image

        # Création du produit
        produit = Produit(
            idProduit=generer_id_produit(),
            nom=nom,
            prixAchat=prixAchat,
            prixVente=prixVente,
            quantite=quantite,
            categorie=categorie,
            description=description,
            image=image
        )
        produit.save()
        return redirect('dashboard_stock')  # ou l'URL de la liste des produits

    # Si c'est un GET, on affiche juste le formulaire
    return render(request, 'dashboard/stock_add_product.html')

# Certains modèles ont été déplacés/supprimés (Vente, LigneVente, Promotion). Importer en sécurité.
try:
    from .models import Vente, LigneVente, Promotion
except Exception:
    Vente = LigneVente = Promotion = None

# Helpers pour compatibilité des champs entre anciens et nouveaux modèles
def _get_prix_unitaire(p):
    return getattr(p, 'prix_unitaire', getattr(p, 'prixVente', 0))

def _get_prix_achat(p):
    return getattr(p, 'prix_achat', getattr(p, 'prixAchat', 0))

def _get_reference(p):
    return getattr(p, 'reference', getattr(p, 'idProduit', ''))

def _get_stock_val(p):
    # retourne la quantité actuelle, prioriser Stock relation
    try:
        return p.stock.quantiteActuelle
    except Exception:
        return getattr(p, 'stock_actuel', getattr(p, 'quantite', 0))

# Page d'accueil
def home(request):
    return render(request, 'home.html')

# Page À propos
def about(request):
    return render(request, 'about.html')

# Page Contact
def contact(request):
    return render(request, 'contact.html')

# Page de connexion
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            user.derniere_connexion_custom = timezone.now()
            user.save()
            
            # 🕐 POINTAGE AUTOMATIQUE D'ARRIVÉE (NOUVELLE SESSION)
            today = timezone.now().date()
            current_time = timezone.now().time()
            
            # Vérifier si l'employé est dans les heures de travail
            if user.heure_debut_travail <= current_time <= user.heure_fin_travail:
                # Importer le modèle SessionPresence
                from .models import SessionPresence
                
                # Créer une nouvelle session de connexion
                SessionPresence.objects.create(
                    employe=user,
                    date=today,
                    heure_connexion=current_time
                )
                
                # Créer ou récupérer la présence du jour
                presence, created = Presence.objects.get_or_create(
                    employe=user,
                    date=today,
                    defaults={
                        'heure_premiere_arrivee': current_time,
                        'tolerance_retard': 60  # 1 heure par défaut
                    }
                )
                
                # Si c'est la première connexion du jour, enregistrer l'heure
                if not created and not presence.heure_premiere_arrivee:
                    presence.heure_premiere_arrivee = current_time
                    presence.save()
            
            # Redirection selon le rôle
            if user.role == 'DG':
                return redirect('dashboard_dg')
            elif user.role == 'DAF':
                return redirect('dashboard_daf')
            elif user.role == 'RH':
                return redirect('dashboard_rh')
            elif user.role == 'STOCK':
                return redirect('dashboard_stock')
            elif user.role == 'CAISSIER':
                return redirect('dashboard_caisse')
            elif user.role == 'MARKETING':
                return redirect('dashboard_marketing')
            elif user.role == 'ANALYSTE':
                return redirect('dashboard_analytics')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Identifiant ou mot de passe incorrect')
    
    return render(request, 'login.html')

# Déconnexion
def logout_view(request):
    # 🕔 POINTAGE AUTOMATIQUE DE DÉPART (FERMER LA SESSION EN COURS)
    if request.user.is_authenticated:
        from .models import SessionPresence
        today = timezone.now().date()
        current_time = timezone.now().time()
        
        try:
            # Trouver la dernière session active (sans heure de déconnexion)
            session_active = SessionPresence.objects.filter(
                employe=request.user,
                date=today,
                heure_deconnexion__isnull=True
            ).last()
            
            if session_active:
                # Fermer la session en enregistrant l'heure de déconnexion
                session_active.heure_deconnexion = current_time
                session_active.save()  # Calcule automatiquement la durée
                
                # Mettre à jour la présence du jour
                try:
                    presence = Presence.objects.get(employe=request.user, date=today)
                    presence.heure_derniere_depart = current_time
                    presence.save()  # Recalcule le statut automatiquement
                except Presence.DoesNotExist:
                    pass
                    
        except Exception as e:
            # En cas d'erreur, continuer la déconnexion normalement
            pass
    
    logout(request)
    return redirect('home')

# Tableau de bord principal (sélection de profil)
@login_required
def dashboard(request):
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard/main.html', context)

# Tableau de bord Direction Générale
@login_required
def dashboard_dg(request):
    # Vérifier les permissions
    if request.user.role != 'DG':
        messages.error(request, "Accès refusé. Vous n'avez pas les permissions pour accéder au module Direction Générale.")
        return redirect('dashboard')
    
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    
    # Ventes du jour
    ventes_jour = Vente.objects.filter(date_vente__date=today)
    ca_jour = ventes_jour.aggregate(total=Sum('montant_final'))['total'] or 0
    
    # Ventes du mois
    ventes_mois = Vente.objects.filter(
        date_vente__month=current_month,
        date_vente__year=current_year
    )
    ca_mois = ventes_mois.aggregate(total=Sum('montant_final'))['total'] or 0
    nb_transactions = ventes_mois.count()
    
    # Panier moyen
    panier_moyen = ca_mois / nb_transactions if nb_transactions > 0 else 0
    
    # ROI (Return on Investment)
    total_ventes = ventes_mois.aggregate(total=Sum('montant_final'))['total'] or 0
    total_achats = 0
    for vente in ventes_mois:
        for ligne in vente.lignes.all():
            total_achats += ligne.produit.prix_achat * ligne.quantite
    
    roi = ((total_ventes - total_achats) / total_achats * 100) if total_achats > 0 else 0
    
    # Évolution du chiffre d'affaires (6 derniers mois)
    ca_evolution = []
    for i in range(5, -1, -1):
        date = today - timedelta(days=i*30)
        ca = Vente.objects.filter(
            date_vente__month=date.month,
            date_vente__year=date.year
        ).aggregate(total=Sum('montant_final'))['total'] or 0
        ca_evolution.append({
            'mois': date.strftime('%b'),
            'ca': float(ca)
        })
    
    # Ventes / analytics : si les modèles Vente / LigneVente / Promotion existent
    top_produits = []
    marges_data = []
    mois_labels = []
    ventes_evolution = []
    try:
        if Vente is not None and LigneVente is not None:
            # Top produits par revenus
            produits_vendus = LigneVente.objects.filter(
                vente__date_vente__month=current_month
            ).values('produit__nom', 'produit__categorie').annotate(
                revenus=Sum('montant_ligne')
            ).order_by('-revenus')[:4]

            for item in produits_vendus:
                top_produits.append({
                    'nom': item.get('produit__nom'),
                    'categorie': item.get('produit__categorie'),
                    'revenus': float(item.get('revenus') or 0)
                })

            # Analyse des marges
            for i in range(5, -1, -1):
                date = today - timedelta(days=i*30)
                ventes = Vente.objects.filter(
                    date_vente__month=date.month,
                    date_vente__year=date.year
                )

                revenus = 0
                couts = 0
                for vente in ventes:
                    revenus += float(getattr(vente, 'montant_final', 0) or 0)
                    # lignes may not exist on the object; guard
                    try:
                        lignes = getattr(vente, 'lignes')
                        for ligne in lignes.all():
                            couts += float(getattr(ligne.produit, 'prix_achat', 0) or 0) * float(getattr(ligne, 'quantite', 0) or 0)
                    except Exception:
                        pass

                benefices = revenus - couts
                mois_labels.append(date.strftime('%b'))
                marges_data.append({
                    'revenus': revenus,
                    'couts': couts,
                    'benefices': benefices
                })

            # Indicateurs opérationnels RÉELS
            nb_ventes_mois = Vente.objects.filter(date_vente__month=current_month).count()
        else:
            nb_ventes_mois = 0

        # Ajusté : utiliser Stock.quantiteActuelle via annotation si besoin
        from .models_stock import Stock
        stock_moyen_qs = Stock.objects.filter(quantiteActuelle__gt=0).aggregate(avg=Avg('quantiteActuelle'))
        stock_moyen = stock_moyen_qs.get('avg') or 1
        taux_rotation_stocks = round(nb_ventes_mois / float(stock_moyen), 2) if stock_moyen > 0 else 0

        # Temps moyen de traitement à la caisse (basé sur le nombre de lignes de vente)
        if LigneVente is not None and Vente is not None:
            lignes_moyennes = LigneVente.objects.filter(vente__date_vente__month=current_month).count() / max(nb_ventes_mois, 1)
        else:
            lignes_moyennes = 0
        temps_moyen_caisse = round(lignes_moyennes * 0.5, 1)  # 0.5 min par article
    except Exception:
        # En cas d'erreur inattendue, fournir des valeurs de repli
        top_produits = []
        marges_data = []
        mois_labels = []
        nb_ventes_mois = 0
        stock_moyen = 1
        taux_rotation_stocks = 0
        lignes_moyennes = 0
        temps_moyen_caisse = 0
    
    # Satisfaction client (basé sur les réclamations)
    total_clients = Client.objects.count() or 1
    reclamations = Reclamation.objects.filter(date_creation__month=current_month).count()
    satisfaction_client = round(100 - (reclamations / total_clients * 100), 1)
    
    # Productivité employés (ventes par employé actif)
    employes_actifs = Employe.objects.filter(est_actif=True).count() or 1
    productivite_employes = round((nb_ventes_mois / employes_actifs), 0)
    
    # Taux de déchets/pertes (produits en rupture ou critique)
    total_produits = Produit.objects.count() or 1
    # compte des produits en stock critique via Stock
    produits_critiques = Stock.objects.filter(quantiteActuelle__lt=10).count()
    taux_dechet = round((produits_critiques / total_produits * 100), 1)
    
    context = {
        'ca_jour': ca_jour,
        'ca_mois': ca_mois,
        'benefice_mois': ca_mois * Decimal('0.182'),
        'nb_transactions': nb_transactions,
        'panier_moyen': panier_moyen,
        'roi': roi,
        'ca_evolution': ca_evolution,
        'top_produits': top_produits,
        'mois_labels': mois_labels,
        'marges_data': marges_data,
        'taux_rotation_stocks': taux_rotation_stocks,
        'temps_moyen_caisse': temps_moyen_caisse,
        'satisfaction_client': satisfaction_client,
        'productivite_employes': productivite_employes,
        'taux_dechet': taux_dechet,
    }
    
    return render(request, 'dashboard/dg.html', context)

# Tableau de bord DAF (Directeur Administratif et Financier)
@login_required
def dashboard_daf(request):
    # Vérifier les permissions
    if request.user.role != 'DAF':
        messages.error(request, "Accès refusé. Vous n'avez pas les permissions pour accéder au module Financier.")
        return redirect('dashboard')
    
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    
    # Chiffre d'affaires mensuel (RÉEL)
    ca_mois = Vente.objects.filter(
        date_vente__month=current_month,
        date_vente__year=current_year
    ).aggregate(total=Sum('montant_final'))['total'] or 0
    
    # Calculer la marge bénéficiaire RÉELLE (revenus - coûts)
    revenus_mois = float(ca_mois)
    couts_mois = 0
    for vente in Vente.objects.filter(date_vente__month=current_month):
        for ligne in vente.lignes.all():
            couts_mois += float(ligne.produit.prix_achat * ligne.quantite)
    
    marge_beneficiaire = ((revenus_mois - couts_mois) / revenus_mois * 100) if revenus_mois > 0 else 0
    
    # Charges mensuelles RÉELLES
    charges_mensuelles = couts_mois
    
    # Trésorerie RÉELLE (CA total - Charges)
    ca_total = Vente.objects.aggregate(total=Sum('montant_final'))['total'] or 0
    tresorerie = float(ca_total) - charges_mensuelles
    
    # Évolution du CA (6 derniers mois)
    ca_evolution = []
    for i in range(5, -1, -1):
        date = today - timedelta(days=i*30)
        ca = Vente.objects.filter(
            date_vente__month=date.month,
            date_vente__year=date.year
        ).aggregate(total=Sum('montant_final'))['total'] or 0
        ca_evolution.append({
            'mois': date.strftime('%b'),
            'ca': float(ca),
            'objectif': float(ca) * 0.95
        })
    
    # Analyse des marges (brute et nette)
    marges_data = []
    for i in range(5, -1, -1):
        date = today - timedelta(days=i*30)
        ca = Vente.objects.filter(
            date_vente__month=date.month,
            date_vente__year=date.year
        ).aggregate(total=Sum('montant_final'))['total'] or 0
        
        marges_data.append({
            'mois': date.strftime('%b'),
            'marge_brute': float(ca) * 0.28,
            'marge_nette': float(ca) * 0.18
        })
    
    # Modes de paiement RÉELS
    moyens_paiement = Vente.objects.filter(
        date_vente__month=current_month
    ).values('moyen_paiement').annotate(
        total=Count('id')
    )
    
    paiement_data = []
    total_ventes = Vente.objects.filter(date_vente__month=current_month).count()
    
    for mp in moyens_paiement:
        pourcentage = (mp['total'] / total_ventes * 100) if total_ventes > 0 else 0
        paiement_data.append({
            'moyen': mp['moyen_paiement'],
            'pourcentage': round(pourcentage, 1)
        })
    
    context = {
        'ca_mois': ca_mois,
        'marge_beneficiaire': round(marge_beneficiaire, 2),
        'charges_mensuelles': charges_mensuelles,
        'tresorerie': tresorerie,
        'ca_evolution': ca_evolution,
        'marges_data': marges_data,
        'paiement_data': paiement_data,
    }
    
    return render(request, 'dashboard/daf.html', context)

# Tableau de bord RH
@login_required
def dashboard_rh(request):
    # Vérifier que l'utilisateur a accès au dashboard RH
    if request.user.role != 'RH':
        messages.error(request, "Accès refusé. Vous n'avez pas les permissions pour accéder au module RH.")
        return redirect('dashboard')
    
    today = timezone.now().date()
    
    # Statistiques employés (VRAIES DONNÉES uniquement)
    total_employes = Employe.objects.filter(est_actif=True).count()
    presences_jour = Presence.objects.filter(date=today, statut__in=['PRESENT', 'RETARD']).count()
    taux_presence = (presences_jour / total_employes * 100) if total_employes > 0 else 0
    
    # Congés en cours (RÉELS)
    conges_en_cours = Conge.objects.filter(
        date_debut__lte=today,
        date_fin__gte=today,
        statut='APPROUVE'
    ).count()
    
    # Formations actives (RÉELLES)
    formations_actives = Formation.objects.filter(
        date_debut__lte=today,
        date_fin__gte=today,
        est_terminee=False
    ).count()
    
    # Liste des employés RÉELS
    employes = Employe.objects.filter(est_actif=True).order_by('-date_joined')
    
    # Activités récentes RÉELLES (derniers 7 jours)
    activites = []
    
    # Nouveaux employés (derniers 7 jours)
    nouveaux = Employe.objects.filter(
        date_embauche__gte=today - timedelta(days=7)
    ).order_by('-date_embauche')[:3]
    
    for emp in nouveaux:
        temps = (today - emp.date_embauche).days
        activites.append({
            'type': 'employe',
            'titre': 'Nouvel employé ajouté',
            'details': f"{emp.get_full_name()} - {emp.get_role_display()}",
            'temps': f"Il y a {temps} jour{'s' if temps > 1 else ''}"
        })
    
    # Congés récents
    conges_recents = Conge.objects.filter(statut='APPROUVE').order_by('-date_demande')[:2]
    for conge in conges_recents:
        duree = (conge.date_fin - conge.date_debut).days
        activites.append({
            'type': 'conge',
            'titre': 'Congé approuvé',
            'details': f"{conge.employe.get_full_name()} - {duree} jours",
            'temps': "Il y a 4h"
        })
    
    # Formations récentes
    formations_recentes = Formation.objects.filter(est_terminee=True).order_by('-date_fin')[:1]
    for formation in formations_recentes:
        activites.append({
            'type': 'formation',
            'titre': 'Formation terminée',
            'details': f"{formation.titre} - {formation.nombre_participants} participants",
            'temps': "Ici"
        })
    
    context = {
        'total_employes': total_employes,
        'presences_jour': presences_jour,
        'taux_presence': taux_presence,
        'conges_en_cours': conges_en_cours,
        'formations_actives': formations_actives,
        'employes': employes,
        'activites': activites,
    }
    
    return render(request, 'dashboard/rh.html', context)

# Tableau de bord Stock
@login_required
def dashboard_stock(request):
    # Vérifier les permissions
    if request.user.role != 'STOCK':
        messages.error(request, "Accès refusé. Vous n'avez pas les permissions pour accéder au module Stock.")
        return redirect('dashboard')
    
    # Statistiques stock (avec les nouveaux modèles)
    total_produits = Produit.objects.count()

    # Utiliser le modèle Stock pour les quantités réelles
    from .models_stock import Stock  # importer localement pour sécurité

    # Utiliser la table Stock pour compter les produits en quantité critique
    try:
        stock_critique = Stock.objects.filter(quantiteActuelle__lt=10).count()
    except Exception:
        # Si Stock n'est pas disponible pour une raison quelconque, fallback sur Produit via attributs calculés
        stock_critique = 0

    # Valeur du stock (quantité actuelle × prix d'achat du produit)
    valeur_stock = 0
    for s in Stock.objects.select_related('produit').all():
        try:
            valeur_stock += s.quantiteActuelle * float(s.produit.prixAchat)
        except Exception:
            # fallback si prix absent
            continue

    commandes_en_cours = 0  # À implémenter avec table CommandeApprovisionnement

    # Produits en stock critique (via Stock)
    produits_critiques_qs = Stock.objects.filter(quantiteActuelle__lt=10).select_related('produit').order_by('quantiteActuelle')[:5]
    produits_critiques = []
    for s in produits_critiques_qs:
        p = s.produit
        # tentative de récupérer un fournisseur via une ligne de commande si disponible
        fournisseur_nom = ''
        ld = p.lignedecommande_set.select_related('commande__fournisseur').first()
        if ld and ld.commande and ld.commande.fournisseur:
            fournisseur_nom = ld.commande.fournisseur.nom

        produits_critiques.append({
            'nom': p.nom,
            'reference': getattr(p, 'idProduit', ''),
            'stock_actuel': s.quantiteActuelle,
            'prix_unitaire': p.prixVente,
            'fournisseur': fournisseur_nom,
            'statut': 'CRITIQUE',
            'image': (p.image.url if getattr(p, 'image', None) and hasattr(p.image, 'url') else (p.image if getattr(p, 'image', None) else None)),
            'get_categorie_display': (p.categorie.nom if getattr(p, 'categorie', None) else ''),
        })

    # Liste des produits — construire des dicts compatibles avec le template existant
    produits = []
    for p in Produit.objects.all().order_by('nom')[:50]:
        # récupérer le stock si présent
        stock_val = None
        try:
            stock_val = p.stock.quantiteActuelle
        except Exception:
            stock_val = getattr(p, 'quantite', 0)

        fournisseur_nom = ''
        ld = p.lignedecommande_set.select_related('commande__fournisseur').first()
        if ld and ld.commande and ld.commande.fournisseur:
            fournisseur_nom = ld.commande.fournisseur.nom

        produits.append({
            'nom': p.nom,
            'reference': getattr(p, 'idProduit', ''),
            'stock_actuel': stock_val,
            'prix_unitaire': p.prixVente,
            'fournisseur': fournisseur_nom,
            'statut': ('EN_STOCK' if stock_val and stock_val > 10 else ('CRITIQUE' if stock_val and stock_val > 0 else 'RUPTURE')),
            'image': (p.image.url if getattr(p, 'image', None) and hasattr(p.image, 'url') else (p.image if getattr(p, 'image', None) else None)),
            'get_categorie_display': (p.categorie.nom if getattr(p, 'categorie', None) else ''),
        })
    
    context = {
        'total_produits': total_produits,
        'stock_critique': stock_critique,
        'valeur_stock': valeur_stock,
        'commandes_en_cours': commandes_en_cours,
        'produits_critiques': produits_critiques,
        'produits': produits,
    }
    
    return render(request, 'dashboard/stock.html', context)

# Tableau de bord Caisse
@login_required
def dashboard_caisse(request):
    # Vérifier les permissions
    if request.user.role != 'CAISSIER':
        messages.error(request, "Accès refusé. Vous n'avez pas les permissions pour accéder au module Caisse.")
        return redirect('dashboard')
    
    today = timezone.now().date()
    
    # Ventes du jour RÉELLES
    ventes_jour = Vente.objects.filter(date_vente__date=today)
    ca_jour = ventes_jour.aggregate(total=Sum('montant_final'))['total'] or 0
    nb_transactions = ventes_jour.count()
    panier_moyen = ca_jour / nb_transactions if nb_transactions > 0 else 0
    
    # Caisses actives RÉELLES (nombre de caissiers actifs aujourd'hui)
    caisses_actives = Employe.objects.filter(
        role='CAISSIER',
        est_actif=True
    ).count()
    total_caisses = Employe.objects.filter(role='CAISSIER').count()
    
    # Transactions récentes
    transactions_recentes = Vente.objects.filter(date_vente__date=today).order_by('-date_vente')[:5]
    
    # Moyens de paiement
    moyens_paiement = Vente.objects.filter(date_vente__date=today).values(
        'moyen_paiement'
    ).annotate(
        total=Count('id')
    )
    
    paiement_stats = []
    for mp in moyens_paiement:
        pourcentage = (mp['total'] / nb_transactions * 100) if nb_transactions > 0 else 0
        paiement_stats.append({
            'moyen': mp['moyen_paiement'],
            'pourcentage': round(pourcentage, 0)
        })
    
    context = {
        'ca_jour': ca_jour,
        'nb_transactions': nb_transactions,
        'panier_moyen': panier_moyen,
        'caisses_actives': caisses_actives,
        'total_caisses': total_caisses,
        'transactions_recentes': transactions_recentes,
        'paiement_stats': paiement_stats,
    }
    
    return render(request, 'dashboard/caisse.html', context)

# Tableau de bord Marketing (Fidélisation)
@login_required
def dashboard_marketing(request):
    # Vérifier les permissions
    if request.user.role != 'MARKETING':
        messages.error(request, "Accès refusé. Vous n'avez pas les permissions pour accéder au module Marketing.")
        return redirect('dashboard')
    
    # Statistiques clients RÉELLES
    clients_fideles = Client.objects.count()
    points_distribues = Client.objects.aggregate(total=Sum('points_fidelite'))['total'] or 0
    promotions_actives = Promotion.objects.filter(est_active=True).count()
    reclamations = Reclamation.objects.filter(statut='EN_COURS').count()
    
    # Nouveaux clients ce mois
    today = timezone.now().date()
    nouveaux_clients = Client.objects.filter(
        date_inscription__month=today.month,
        date_inscription__year=today.year
    ).count()
    
    # Liste des clients par niveau
    clients_vip = Client.objects.filter(niveau_fidelite='VIP').count()
    clients_gold = Client.objects.filter(niveau_fidelite='GOLD').count()
    clients_silver = Client.objects.filter(niveau_fidelite='SILVER').count()
    clients_tous = Client.objects.filter(niveau_fidelite='TOUS').count()
    
    # Liste des clients
    clients = Client.objects.all().order_by('-points_fidelite')
    
    # Activités récentes RÉELLES
    activites = []
    
    # Nouveaux clients récents
    clients_recents = Client.objects.order_by('-date_inscription')[:5]
    for client in clients_recents:
        jours = (timezone.now().date() - client.date_inscription.date()).days
        activites.append({
            'icon': '👤',
            'titre': f'Nouveau client: {client.nom} {client.prenom}',
            'description': f'Niveau: {client.get_niveau_fidelite_display()}',
            'date': client.date_inscription
        })
    
    # Promotions actives récentes
    promotions_recentes = Promotion.objects.filter(est_active=True).order_by('-date_creation')[:3]
    for promo in promotions_recentes:
        activites.append({
            'icon': '%',
            'titre': f'Promotion: {promo.nom}',
            'description': f'Réduction de {promo.pourcentage_reduction}%',
            'date': promo.date_creation
        })
    
    # Réclamations récentes
    reclamations_recentes = Reclamation.objects.order_by('-date_creation')[:2]
    for reclamation in reclamations_recentes:
        activites.append({
            'icon': '⚠️',
            'titre': f'Réclamation de {reclamation.client.nom}',
            'description': reclamation.sujet,
            'date': reclamation.date_creation
        })
    
    # Liste des promotions
    promotions = Promotion.objects.filter(est_active=True)
    for promo in promotions:
        promo.produits_count = promo.produits.count()
    
    # Calcul des pourcentages pour le graphique
    total_clients = max(clients_vip + clients_gold + clients_silver + clients_tous, 1)
    vip_percentage = int((clients_vip / total_clients) * 200)
    gold_percentage = int((clients_gold / total_clients) * 200)
    silver_percentage = int((clients_silver / total_clients) * 200)
    
    context = {
        'clients_fideles': clients_fideles,
        'points_distribues': points_distribues,
        'promotions_actives': promotions_actives,
        'nouveaux_clients': nouveaux_clients,
        'clients_vip': clients_vip,
        'clients_gold': clients_gold,
        'clients_silver': clients_silver,
        'vip_percentage': vip_percentage,
        'gold_percentage': gold_percentage,
        'silver_percentage': silver_percentage,
        'activites': activites,
        'promotions': promotions,
    }
    
    return render(request, 'dashboard/marketing.html', context)

# Tableau de bord Analytics
@login_required
def dashboard_analytics(request):
    # Vérifier les permissions
    if request.user.role != 'ANALYSTE':
        messages.error(request, "Accès refusé. Vous n'avez pas les permissions pour accéder au module Analytics.")
        return redirect('dashboard')
    
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    
    # KPI principaux RÉELS
    ventes_mois = Vente.objects.filter(
        date_vente__month=current_month,
        date_vente__year=current_year
    )
    ca_mois = ventes_mois.aggregate(total=Sum('montant_final'))['total'] or 0
    nb_transactions = ventes_mois.count()
    panier_moyen = ca_mois / nb_transactions if nb_transactions > 0 else 0
    
    # Taux de conversion RÉEL (transactions / nombre de clients)
    nb_clients = Client.objects.count() or 1
    taux_conversion = round((nb_transactions / nb_clients) * 100, 1)
    
    # Satisfaction client RÉELLE (basée sur réclamations)
    reclamations = Reclamation.objects.filter(date_creation__month=current_month).count()
    satisfaction = round(5 - (reclamations / max(nb_clients, 1)) * 5, 1)
    
    # Évolution des ventes
    ventes_evolution = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        ca = Vente.objects.filter(date_vente__date=date).aggregate(
            total=Sum('montant_final')
        )['total'] or 0
        ventes_evolution.append({
            'jour': date.strftime('%a'),
            'ca': float(ca)
        })
    
    # Performance globale (gauge)
    performance = 85
    
    # Top produits vendus
    top_produits = []
    lignes = LigneVente.objects.filter(
        vente__date_vente__month=current_month
    ).values(
        'produit__nom'
    ).annotate(
        total_unites=Sum('quantite')
    ).order_by('-total_unites')[:4]
    
    for ligne in lignes:
        top_produits.append({
            'nom': ligne['produit__nom'],
            'unites': ligne['total_unites']
        })
    
    # Répartition par catégorie (pie chart)
    categories = LigneVente.objects.filter(
        vente__date_vente__month=current_month
    ).values(
        'produit__categorie'
    ).annotate(
        total=Sum('montant_ligne')
    )
    
    categories_data = []
    for cat in categories:
        categories_data.append({
            'categorie': cat['produit__categorie'],
            'total': float(cat['total'])
        })
    
    # Moyens de paiement
    moyens_paiement = Vente.objects.filter(
        date_vente__month=current_month
    ).values('moyen_paiement').annotate(
        total=Count('id')
    )
    
    paiement_data = []
    total_ventes = Vente.objects.filter(date_vente__month=current_month).count()
    
    for mp in moyens_paiement:
        pourcentage = (mp['total'] / total_ventes * 100) if total_ventes > 0 else 0
        paiement_data.append({
            'moyen': mp['moyen_paiement'],
            'pourcentage': round(pourcentage, 0)
        })
    
    # Ajouter des informations aux top produits RÉELS (tendance, marge, stock)
    for produit_data in top_produits:
        try:
            produit = Produit.objects.get(nom=produit_data['produit__nom'])
            pu = _get_prix_unitaire(produit)
            pa = _get_prix_achat(produit)
            try:
                produit_data['marge'] = round(((float(pu) - float(pa)) / float(pu)) * 100, 1) if pu else 0
            except Exception:
                produit_data['marge'] = 0
            produit_data['tendance'] = 0  # À calculer avec historique
            produit_data['stock_actuel'] = _get_stock_val(produit)
        except:
            produit_data['marge'] = 0
            produit_data['tendance'] = 0
            produit_data['stock_actuel'] = 0
    
    context = {
        'ca_mois': float(ca_mois) / 1000000,  # Convertir en millions
        'nb_transactions': nb_transactions,
        'taux_conversion': taux_conversion,
        'satisfaction': satisfaction,
        'ventes_evolution': ventes_evolution,
        'top_produits': top_produits,
        'categories_data': categories_data,
    }
    
    return render(request, 'dashboard/analytics.html', context)


# Vue pour ajouter un produit (accès STOCK uniquement)
@login_required
def stock_add_product(request):
    # Vérifier que l'utilisateur a accès au module Stock
    if request.user.role != 'STOCK':
        messages.error(request, "Accès refusé. Vous n'avez pas les permissions pour gérer les produits.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        reference = request.POST.get('reference')
        categorie = request.POST.get('categorie')
        prix_achat = request.POST.get('prix_achat')
        prix_vente = request.POST.get('prix_vente')
        stock = request.POST.get('stock')
        fournisseur = request.POST.get('fournisseur', '')
        description = request.POST.get('description', '')
        
        # Vérifier que la référence n'existe pas déjà (champ `code` dans les nouveaux modèles)
        if Produit.objects.filter(idProduit=reference).exists():
            messages.error(request, f"La référence '{reference}' existe déjà. Veuillez en choisir une autre.")
            return render(request, 'dashboard/stock_add_product.html')

        try:
            # Créer le produit (champs alignés sur models_stock)
            produit = Produit.objects.create(
                nom=nom,
                categorie_id=categorie,
                prixAchat=Decimal(prix_achat),
                prixVente=Decimal(prix_vente),
                quantite=int(stock),
                description=description
            )

            # Créer l'objet Stock associé
            from .models_stock import Stock
            Stock.objects.create(
                idStock=f"STK-{produit.idProduit}",
                produit=produit,
                quantiteActuelle=int(stock),
                quantiteReservee=0,
                quantiteDisponible=int(stock),
                statut='EN_STOCK' if int(stock) > 0 else 'RUPTURE'
            )

            # Message utilisateur — s'assurer de l'indentation correcte
            messages.success(request, f"✅ Produit '{nom}' ajouté avec succès ! Stock initial: {stock} unités")
            return redirect('dashboard_stock')

        except Exception as e:
            messages.error(request, f"Erreur lors de la création du produit: {str(e)}")
            return render(request, 'dashboard/stock_add_product.html')
    
    return render(request, 'dashboard/stock_add_product.html')


# Vue pour créer un employé (accès RH uniquement)
@login_required
def rh_create_employee(request):
    # Vérifier que l'utilisateur est RH
    if request.user.role != 'RH':
        messages.error(request, "Accès non autorisé. Seul le RH peut créer des employés.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        
        # Vérifier que le nom d'utilisateur n'existe pas déjà
        if Employe.objects.filter(username=username).exists():
            messages.error(request, f"Le nom d'utilisateur '{username}' existe déjà. Veuillez en choisir un autre.")
            return render(request, 'dashboard/rh_create_employee.html')
        
        # Vérifier la longueur du mot de passe
        if len(password) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
            return render(request, 'dashboard/rh_create_employee.html')
        
        # Créer l'employé
        try:
            employe = Employe.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            
            # Configurer les horaires de travail (valeurs par défaut ou personnalisées)
            heure_debut = request.POST.get('heure_debut_travail', '08:00')
            heure_fin = request.POST.get('heure_fin_travail', '17:00')
            duree_pause = request.POST.get('duree_pause', '90')
            
            employe.heure_debut_travail = heure_debut
            employe.heure_fin_travail = heure_fin
            employe.duree_pause = int(duree_pause)
            
            # Le rôle détermine automatiquement les accès
            # Pas besoin de configurer des permissions supplémentaires
            employe.save()
            
            messages.success(request, f"✅ Employé créé avec succès ! Identifiant: {username} | Mot de passe: {password}")
            return redirect('dashboard_rh')
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la création de l'employé: {str(e)}")
            return render(request, 'dashboard/rh_create_employee.html')
    
    return render(request, 'dashboard/rh_create_employee.html')


# Vue liste des employés (RH)
@login_required
def rh_employees_list(request):
    if request.user.role != 'RH':
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    employes = Employe.objects.all().order_by('-date_embauche')
    context = {'employes': employes}
    return render(request, 'dashboard/rh_employees_list.html', context)


# Vue modifier un employé (RH)
@login_required
def rh_employee_edit(request, employee_id):
    if request.user.role != 'RH':
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    employe = get_object_or_404(Employe, id=employee_id)
    
    if request.method == 'POST':
        employe.first_name = request.POST.get('first_name')
        employe.last_name = request.POST.get('last_name')
        employe.email = request.POST.get('email')
        employe.telephone = request.POST.get('telephone')
        employe.departement = request.POST.get('departement')
        employe.role = request.POST.get('role')
        employe.est_actif = request.POST.get('est_actif') == 'on'
        
        # Gestion des horaires de travail
        heure_debut = request.POST.get('heure_debut_travail')
        heure_fin = request.POST.get('heure_fin_travail')
        duree_pause = request.POST.get('duree_pause')
        
        if heure_debut:
            employe.heure_debut_travail = heure_debut
        if heure_fin:
            employe.heure_fin_travail = heure_fin
        if duree_pause:
            employe.duree_pause = int(duree_pause)
        
        employe.save()
        
        messages.success(request, f"✅ Employé {employe.get_full_name()} modifié avec succès!")
        return redirect('rh_employees_list')
    
    context = {'employe': employe}
    return render(request, 'dashboard/rh_employee_edit.html', context)


# Vue supprimer un employé (RH)
@login_required
def rh_employee_delete(request, employee_id):
    if request.user.role != 'RH':
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    employe = get_object_or_404(Employe, id=employee_id)
    
    if request.method == 'POST':
        nom_complet = employe.get_full_name()
        employe.delete()
        messages.success(request, f"✅ Employé {nom_complet} supprimé avec succès!")
        return redirect('rh_employees_list')
    
    context = {'employe': employe}
    return render(request, 'dashboard/rh_employee_delete.html', context)


# Vue gestion des présences (RH)
@login_required
def rh_presences(request):
    if request.user.role != 'RH':
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    today = timezone.now().date()
    presences = Presence.objects.filter(date=today).select_related('employe')
    employes = Employe.objects.filter(est_actif=True)
    
    # Calculer les statistiques de présence
    total_presents = presences.filter(statut='PRESENT').count()
    total_retards = presences.filter(statut='RETARD').count()
    total_absents = employes.count() - presences.count()
    
    # Calculer les heures travaillées pour chaque présence
    presences_avec_heures = []
    for presence in presences:
        heures_travaillees = presence.calculer_heures_travaillees()
        pourcentage = presence.calculer_pourcentage_presence()
        presences_avec_heures.append({
            'presence': presence,
            'heures_travaillees': round(heures_travaillees, 2),
            'pourcentage': round(pourcentage, 1)
        })
    
    context = {
        'presences_data': presences_avec_heures,
        'employes': employes,
        'today': today,
        'total_presents': total_presents,
        'total_retards': total_retards,
        'total_absents': total_absents,
    }
    return render(request, 'dashboard/rh_presences.html', context)


# Vue gestion des congés (RH)
@login_required
def rh_conges(request):
    if request.user.role != 'RH':
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    conges_en_attente = Conge.objects.filter(statut='EN_ATTENTE').select_related('employe')
    tous_conges = Conge.objects.all().select_related('employe').order_by('-date_debut')
    
    context = {
        'conges_en_attente': conges_en_attente,
        'tous_conges': tous_conges
    }
    return render(request, 'dashboard/rh_conges.html', context)


# Vue approuver/refuser congé (RH)
@login_required
def rh_conge_action(request, conge_id, action):
    if request.user.role != 'RH':
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    conge = get_object_or_404(Conge, id=conge_id)
    
    if action == 'approve':
        conge.statut = 'APPROUVE'
        messages.success(request, f"✅ Congé de {conge.employe.get_full_name()} approuvé!")
    elif action == 'reject':
        conge.statut = 'REFUSE'
        messages.warning(request, f"❌ Congé de {conge.employe.get_full_name()} refusé!")
    
    conge.save()
    return redirect('rh_conges')


# Vue gestion des formations (RH)
@login_required
def rh_formations(request):
    if request.user.role != 'RH':
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    formations = Formation.objects.all().order_by('-date_debut')
    
    context = {'formations': formations}
    return render(request, 'dashboard/rh_formations.html', context)


# Vue planifications (RH)
@login_required
def rh_planifications(request):
    if request.user.role != 'RH':
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    employes = Employe.objects.filter(est_actif=True).order_by('departement', 'last_name')
    
    context = {'employes': employes}
    return render(request, 'dashboard/rh_planifications.html', context)


# Vue ajouter présence (RH)
@login_required
def rh_presence_add(request):
    if request.user.role != 'RH':
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        employe_id = request.POST.get('employe_id')
        date = request.POST.get('date')
        heure_premiere_arrivee = request.POST.get('heure_premiere_arrivee')
        heure_derniere_depart = request.POST.get('heure_derniere_depart')
        motif_absence = request.POST.get('motif_absence', '')
        tolerance_retard = request.POST.get('tolerance_retard', 60)
        
        try:
            employe = Employe.objects.get(id=employe_id)
            presence = Presence.objects.create(
                employe=employe,
                date=date,
                heure_premiere_arrivee=heure_premiere_arrivee if heure_premiere_arrivee else None,
                heure_derniere_depart=heure_derniere_depart if heure_derniere_depart else None,
                motif_absence=motif_absence,
                tolerance_retard=int(tolerance_retard)
            )
            messages.success(request, f"✅ Présence ajoutée pour {employe.get_full_name()}")
        except Exception as e:
            messages.error(request, f"❌ Erreur: {str(e)}")
        
        return redirect('rh_presences')
    
    employes = Employe.objects.filter(est_actif=True).order_by('last_name')
    context = {'employes': employes, 'today': timezone.now().date()}
    return render(request, 'dashboard/rh_presence_form.html', context)


# Vue modifier présence (RH)
@login_required
def rh_presence_edit(request, presence_id):
    if request.user.role != 'RH':
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    presence = get_object_or_404(Presence, id=presence_id)
    
    if request.method == 'POST':
        presence.date = request.POST.get('date')
        presence.heure_premiere_arrivee = request.POST.get('heure_premiere_arrivee') or None
        presence.heure_derniere_depart = request.POST.get('heure_derniere_depart') or None
        presence.motif_absence = request.POST.get('motif_absence', '')
        presence.tolerance_retard = int(request.POST.get('tolerance_retard', 60))
        
        try:
            presence.save()
            messages.success(request, f"✅ Présence mise à jour pour {presence.employe.get_full_name()}")
            return redirect('rh_presences')
        except Exception as e:
            messages.error(request, f"❌ Erreur: {str(e)}")
    
    context = {'presence': presence}
    return render(request, 'dashboard/rh_presence_form.html', context)


# Vue supprimer présence (RH)
@login_required
def rh_presence_delete(request, presence_id):
    if request.user.role != 'RH':
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    presence = get_object_or_404(Presence, id=presence_id)
    
    if request.method == 'POST':
        employe_name = presence.employe.get_full_name()
        presence.delete()
        messages.success(request, f"✅ Présence de {employe_name} supprimée")
        return redirect('rh_presences')
    
    context = {'presence': presence}
    return render(request, 'dashboard/rh_presence_delete.html', context)
