def dashboard_url(request):
    """Context processor pour ajouter l'URL du dashboard approprié selon le rôle"""
    if request.user.is_authenticated:
        dashboard_map = {
            'DG': 'dashboard_dg',
            'DAF': 'dashboard_daf',
            'RH': 'dashboard_rh',
            'STOCK': 'dashboard_stock',
            'CAISSIER': 'dashboard_caisse',
            'MARKETING': 'dashboard_marketing',
        }
        return {
            'user_dashboard_url': dashboard_map.get(request.user.role, 'home')
        }
    return {
        'user_dashboard_url': 'home'
    }
