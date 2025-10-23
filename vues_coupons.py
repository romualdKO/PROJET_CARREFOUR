# Vues de gestion des coupons

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
from datetime import date, datetime, timedelta
from CarrefourApp.models import Coupon, Client, UtilisationCoupon


@login_required
def marketing_coupons_list(request):
    """Liste des coupons (Marketing)"""
    if request.user.role not in ['MARKETING', 'DG', 'ADMIN']:
        messages.error(request, "Accès refusé.")
        return redirect('dashboard_' + request.user.role.lower())
    
    # Filtres
    type_coupon = request.GET.get('type', 'all')
    statut = request.GET.get('statut', 'all')
    
    coupons = Coupon.objects.all()
    
    if type_coupon != 'all':
        coupons = coupons.filter(type_coupon=type_coupon)
    
    if statut != 'all':
        coupons = coupons.filter(statut=statut)
    
    # Statistiques
    stats = {
        'total': Coupon.objects.count(),
        'actifs': Coupon.objects.filter(statut='ACTIF').count(),
        'generiques': Coupon.objects.filter(type_coupon='GENERIC').count(),
        'speciaux': Coupon.objects.filter(type_coupon='SPECIAL').count(),
        'utilisations': UtilisationCoupon.objects.count(),
        'remise_totale': UtilisationCoupon.objects.aggregate(total=Sum('montant_remise'))['total'] or 0
    }
    
    context = {
        'coupons': coupons,
        'stats': stats,
        'type_filter': type_coupon,
        'statut_filter': statut,
    }
    
    return render(request, 'marketing/coupons_list.html', context)


@login_required
def marketing_coupon_create(request):
    """Créer un nouveau coupon"""
    if request.user.role not in ['MARKETING', 'DG', 'ADMIN']:
        messages.error(request, "Accès refusé.")
        return redirect('dashboard_' + request.user.role.lower())
    
    if request.method == 'POST':
        type_coupon = request.POST.get('type_coupon')
        type_remise = request.POST.get('type_remise')
        valeur = request.POST.get('valeur')
        description = request.POST.get('description')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        montant_minimum = request.POST.get('montant_minimum', 0)
        niveau_requis = request.POST.get('niveau_fidelite_requis', None)
        limite_globale = request.POST.get('limite_globale', None)
        
        try:
            coupon = Coupon.objects.create(
                type_coupon=type_coupon,
                type_remise=type_remise,
                valeur=valeur,
                description=description,
                date_debut=datetime.strptime(date_debut, '%Y-%m-%d').date(),
                date_fin=datetime.strptime(date_fin, '%Y-%m-%d').date(),
                montant_minimum=montant_minimum or 0,
                niveau_fidelite_requis=niveau_requis if niveau_requis else None,
                limite_globale=int(limite_globale) if limite_globale else None,
                cree_par=request.user,
                statut='ACTIF'
            )
            
            messages.success(request, f'Coupon {coupon.code} créé avec succès!')
            return redirect('marketing_coupons_list')
            
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
    
    context = {
        'niveaux_fidelite': Client.NIVEAUX_FIDELITE,
    }
    
    return render(request, 'marketing/coupon_create.html', context)


@login_required
def marketing_coupon_generer_speciaux(request):
    """Générer des coupons spéciaux pour les clients fidèles"""
    if request.user.role not in ['MARKETING', 'DG', 'ADMIN']:
        messages.error(request, "Accès refusé.")
        return redirect('dashboard_' + request.user.role.lower())
    
    if request.method == 'POST':
        niveau_min = request.POST.get('niveau_minimum', 'SILVER')
        type_remise = request.POST.get('type_remise', 'POURCENTAGE')
        valeur = float(request.POST.get('valeur', 0))
        description = request.POST.get('description')
        duree_jours = int(request.POST.get('duree_jours', 30))
        
        # Sélectionner les clients éligibles
        niveaux_eligibles = {
            'SILVER': ['SILVER', 'GOLD', 'VIP'],
            'GOLD': ['GOLD', 'VIP'],
            'VIP': ['VIP']
        }
        
        clients = Client.objects.filter(
            niveau_fidelite__in=niveaux_eligibles.get(niveau_min, ['VIP']),
            est_actif=True
        )
        
        nb_coupons = 0
        date_debut = date.today()
        date_fin = date_debut + timedelta(days=duree_jours)
        
        for client in clients:
            # Vérifier si le client n'a pas déjà un coupon similaire actif
            coupon_existant = Coupon.objects.filter(
                client=client,
                type_coupon='SPECIAL',
                statut='ACTIF',
                est_utilise=False,
                date_fin__gte=date.today()
            ).exists()
            
            if not coupon_existant:
                Coupon.objects.create(
                    type_coupon='SPECIAL',
                    type_remise=type_remise,
                    valeur=valeur,
                    description=description,
                    date_debut=date_debut,
                    date_fin=date_fin,
                    client=client,
                    cree_par=request.user,
                    statut='ACTIF'
                )
                nb_coupons += 1
        
        messages.success(request, f'{nb_coupons} coupons spéciaux générés avec succès!')
        return redirect('marketing_coupons_list')
    
    context = {
        'niveaux': ['SILVER', 'GOLD', 'VIP']
    }
    
    return render(request, 'marketing/coupon_generer_speciaux.html', context)


@login_required
def marketing_coupon_desactiver(request, coupon_id):
    """Désactiver un coupon"""
    if request.user.role not in ['MARKETING', 'DG', 'ADMIN']:
        return JsonResponse({'success': False, 'error': 'Accès refusé'})
    
    coupon = get_object_or_404(Coupon, id=coupon_id)
    coupon.statut = 'DESACTIVE'
    coupon.save()
    
    messages.success(request, f'Coupon {coupon.code} désactivé.')
    return redirect('marketing_coupons_list')


@login_required
def caisse_valider_coupon(request):
    """AJAX - Valider un coupon au POS"""
    if request.method == 'POST':
        code_coupon = request.POST.get('code', '').strip().upper()
        client_id = request.POST.get('client_id')
        montant_achat = float(request.POST.get('montant', 0))
        
        try:
            coupon = Coupon.objects.get(code=code_coupon)
            
            # Récupérer le client si fourni
            client = None
            if client_id:
                client = Client.objects.get(id=client_id)
            
            # Valider le coupon
            valide, message = coupon.est_valide(client, montant_achat)
            
            if not valide:
                return JsonResponse({
                    'success': False,
                    'error': message
                })
            
            # Calculer la remise
            remise = coupon.calculer_remise(montant_achat)
            
            return JsonResponse({
                'success': True,
                'coupon': {
                    'id': coupon.id,
                    'code': coupon.code,
                    'description': coupon.description,
                    'type_remise': coupon.type_remise,
                    'valeur': float(coupon.valeur),
                    'remise': float(remise)
                }
            })
            
        except Coupon.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Coupon invalide'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


@login_required
def marketing_coupons_stats(request):
    """Statistiques d'utilisation des coupons"""
    if request.user.role not in ['MARKETING', 'DG', 'ADMIN']:
        messages.error(request, "Accès refusé.")
        return redirect('dashboard_' + request.user.role.lower())
    
    # Stats globales
    today = date.today()
    
    stats = {
        'coupons_actifs': Coupon.objects.filter(statut='ACTIF', date_fin__gte=today).count(),
        'utilisations_mois': UtilisationCoupon.objects.filter(
            date_utilisation__month=today.month,
            date_utilisation__year=today.year
        ).count(),
        'remise_mois': UtilisationCoupon.objects.filter(
            date_utilisation__month=today.month,
            date_utilisation__year=today.year
        ).aggregate(total=Sum('montant_remise'))['total'] or 0,
    }
    
    # Top 10 coupons les plus utilisés
    top_coupons = UtilisationCoupon.objects.values(
        'coupon__code', 'coupon__description'
    ).annotate(
        nb_utilisations=Count('id'),
        remise_totale=Sum('montant_remise')
    ).order_by('-nb_utilisations')[:10]
    
    # Utilisation par type
    par_type = UtilisationCoupon.objects.values(
        'coupon__type_coupon'
    ).annotate(
        nb=Count('id'),
        remise=Sum('montant_remise')
    )
    
    context = {
        'stats': stats,
        'top_coupons': top_coupons,
        'par_type': par_type,
    }
    
    return render(request, 'marketing/coupons_stats.html', context)
