from django.urls import path
from . import views

urlpatterns = [
    # Pages publiques
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentification
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Tableaux de bord
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/dg/', views.dashboard_dg, name='dashboard_dg'),
    path('dashboard/daf/', views.dashboard_daf, name='dashboard_daf'),
    path('dashboard/rh/', views.dashboard_rh, name='dashboard_rh'),
    path('dashboard/rh/create-employee/', views.rh_create_employee, name='rh_create_employee'),
    path('dashboard/rh/employees/', views.rh_employees_list, name='rh_employees_list'),
    path('dashboard/rh/employee/<int:employee_id>/edit/', views.rh_employee_edit, name='rh_employee_edit'),
    path('dashboard/rh/employee/<int:employee_id>/delete/', views.rh_employee_delete, name='rh_employee_delete'),
    path('dashboard/rh/presences/', views.rh_presences, name='rh_presences'),
    path('dashboard/rh/presence/add/', views.rh_presence_add, name='rh_presence_add'),
    path('dashboard/rh/presence/<int:presence_id>/edit/', views.rh_presence_edit, name='rh_presence_edit'),
    path('dashboard/rh/presence/<int:presence_id>/delete/', views.rh_presence_delete, name='rh_presence_delete'),
    path('dashboard/rh/conges/', views.rh_conges, name='rh_conges'),
    path('dashboard/rh/conge/<int:conge_id>/<str:action>/', views.rh_conge_action, name='rh_conge_action'),
    path('dashboard/rh/formations/', views.rh_formations, name='rh_formations'),
    path('dashboard/rh/planifications/', views.rh_planifications, name='rh_planifications'),
    path('dashboard/stock/', views.dashboard_stock, name='dashboard_stock'),
    path('dashboard/stock/add-product/', views.stock_add_product, name='stock_add_product'),
    path('dashboard/caisse/', views.dashboard_caisse, name='dashboard_caisse'),
    path('dashboard/marketing/', views.dashboard_marketing, name='dashboard_marketing'),
    path('dashboard/analytics/', views.dashboard_analytics, name='dashboard_analytics'),
    # New route for adding product
    path('dashboard/stock/ajout-product/', views.ajouter_produit, name='add_product'),
    #dashboard fournisseur
    path('dashboard/fournisseurs/', views.fournisseur, name='page_fournisseurs'),
    #dashboard reaprovisionnement
    path('dashboard/approvisionnement/', views.reaprovisionnement, name='page_approvisionnement'),
    # Formulaires fournisseur
    path('dashboard/fournisseurs/form/', views.formFournisseur, name='form_fournisseur'),
    # Formulaires commande approvisionnement
    path('dashboard/approvisionnement/form/', views.formApprovisionnement, name='form_commande'),
    # Ajout fournisseur
    path('dashboard/fournisseurs/ajout/', views.AjoutFournisseur, name='ajout_fournisseur'),
    # suppression fournisseur
    path('dashboard/fournisseurs/suppression/<str:idFournisseur>/', views.supprimerFournisseur, name='suppression_fournisseur'),
    #page Modifier fournisseur
    path('dashboard/fournisseurs/modifier/<str:idFournisseur>/', views.ModifierFournisseur, name='modifier_fournisseur'),
    #total fournisseurs
    
]
