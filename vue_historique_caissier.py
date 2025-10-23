@login_required
def caissier_mes_ventes(request):
    """Historique des ventes du caissier connecté"""
    if request.user.role not in ['CAISSIER', 'MANAGER', 'ADMIN']:
        messages.error(request, "Accès refusé.")
        dashboard_url = get_dashboard_by_role(request.user)
        return redirect(dashboard_url)
    
    from datetime import datetime, timedelta
    
    # Paramètres de filtrage
    date_debut_param = request.GET.get('date_debut', '')
    date_fin_param = request.GET.get('date_fin', '')
    periode = request.GET.get('periode', 'aujourd_hui')
    
    # Définir les dates selon la période
    now = timezone.now()
    
    if date_debut_param and date_fin_param:
        date_debut = datetime.strptime(date_debut_param, '%Y-%m-%d').date()
        date_fin = datetime.strptime(date_fin_param, '%Y-%m-%d').date()
    elif periode == 'aujourd_hui':
        date_debut = now.date()
        date_fin = now.date()
    elif periode == 'semaine':
        date_debut = now.date() - timedelta(days=now.weekday())
        date_fin = date_debut + timedelta(days=6)
    elif periode == 'mois':
        date_debut = now.date().replace(day=1)
        import calendar
        _, last_day = calendar.monthrange(now.year, now.month)
        date_fin = now.date().replace(day=last_day)
    else:
        date_debut = now.date()
        date_fin = now.date()
    
    # Récupérer les transactions du caissier
    transactions = Transaction.objects.filter(
        caissier=request.user,
        date_transaction__date__gte=date_debut,
        date_transaction__date__lte=date_fin,
        statut='VALIDEE'
    ).select_related('client', 'session').prefetch_related('lignes__produit', 'paiements__type_paiement').order_by('-date_transaction')
    
    # Statistiques
    nb_transactions = transactions.count()
    ca_total = transactions.aggregate(total=Sum('montant_final'))['total'] or 0
    remises_total = transactions.aggregate(total=Sum('remise'))['total'] or 0
    panier_moyen = ca_total / nb_transactions if nb_transactions > 0 else 0
    
    # Répartition moyens de paiement
    moyens_paiement = transactions.values('paiements__type_paiement__nom').annotate(
        total=Sum('paiements__montant'),
        nb=Count('id', distinct=True)
    ).order_by('-total')
    
    # Top 10 produits vendus
    from django.db.models import F
    top_produits = LigneTransaction.objects.filter(
        transaction__caissier=request.user,
        transaction__date_transaction__date__gte=date_debut,
        transaction__date_transaction__date__lte=date_fin,
        transaction__statut='VALIDEE'
    ).values('produit__nom', 'produit__reference').annotate(
        quantite_totale=Sum('quantite'),
        ca=Sum(F('quantite') * F('prix_unitaire'))
    ).order_by('-quantite_totale')[:10]
    
    # CA par jour (pour graphique)
    ca_par_jour = transactions.extra(
        select={'jour': 'DATE(date_transaction)'}
    ).values('jour').annotate(
        ca=Sum('montant_final'),
        nb_ventes=Count('id')
    ).order_by('jour')
    
    context = {
        'transactions': transactions,
        'date_debut': date_debut,
        'date_fin': date_fin,
        'periode': periode,
        'nb_transactions': nb_transactions,
        'ca_total': ca_total,
        'remises_total': remises_total,
        'panier_moyen': panier_moyen,
        'moyens_paiement': moyens_paiement,
        'top_produits': top_produits,
        'ca_par_jour': list(ca_par_jour),
    }
    
    return render(request, 'caisse/mes_ventes.html', context)
