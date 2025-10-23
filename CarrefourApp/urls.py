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
    path('dashboard/rh/conges/calendar/', views.rh_conges_calendar, name='rh_conges_calendar'),
    path('employee/request-leave/', views.employee_request_leave, name='employee_request_leave'),
    path('dashboard/rh/formations/', views.rh_formations, name='rh_formations'),
    path('dashboard/rh/planifications/', views.rh_planifications, name='rh_planifications'),
    path('dashboard/rh/historique/', views.rh_historique, name='rh_historique'),
    path('dashboard/rh/historique-presences/', views.rh_historique_presences, name='rh_historique_presences'),
    path('dashboard/stock/', views.dashboard_stock, name='dashboard_stock'),
    path('dashboard/stock/add-product/', views.stock_add_product, name='stock_add_product'),
    path('dashboard/stock/produit/<int:produit_id>/edit/', views.stock_produit_edit, name='stock_produit_edit'),
    
    # Gestion des fournisseurs
    path('dashboard/stock/fournisseurs/', views.stock_fournisseurs_list, name='stock_fournisseurs_list'),
    path('dashboard/stock/fournisseurs/create/', views.stock_fournisseur_create, name='stock_fournisseur_create'),
    path('dashboard/stock/fournisseurs/<int:fournisseur_id>/', views.stock_fournisseur_detail, name='stock_fournisseur_detail'),
    path('dashboard/stock/fournisseurs/<int:fournisseur_id>/edit/', views.stock_fournisseur_edit, name='stock_fournisseur_edit'),
    path('dashboard/stock/fournisseurs/<int:fournisseur_id>/delete/', views.stock_fournisseur_delete, name='stock_fournisseur_delete'),
    
    # Gestion des commandes fournisseurs
    path('dashboard/stock/commandes/', views.stock_commandes_list, name='stock_commandes_list'),
    path('dashboard/stock/commandes/create/', views.stock_commande_create, name='stock_commande_create'),
    path('dashboard/stock/commandes/<int:commande_id>/', views.stock_commande_detail, name='stock_commande_detail'),
    path('dashboard/stock/commandes/<int:commande_id>/valider/', views.stock_commande_valider, name='stock_commande_valider'),
    path('dashboard/stock/commandes/<int:commande_id>/recevoir/', views.stock_commande_recevoir, name='stock_commande_recevoir'),
    path('dashboard/stock/commandes/<int:commande_id>/annuler/', views.stock_commande_annuler, name='stock_commande_annuler'),
    
    # Nouvelles routes commandes fournisseurs (Scénario 8.1.1)
    path('commandes-fournisseurs/', views.commandes_fournisseurs, name='commandes_fournisseurs'),
    path('commandes-fournisseurs/creer/', views.creer_commande_fournisseur, name='creer_commande_fournisseur'),
    path('commandes-fournisseurs/<int:commande_id>/valider/', views.valider_commande_fournisseur, name='valider_commande_fournisseur'),
    path('commandes-fournisseurs/<int:commande_id>/recevoir/', views.recevoir_commande_fournisseur, name='recevoir_commande_fournisseur'),
    
    # Gestion caisse (Scénario 8.1.2)
    path('caisse/', views.caisse_vente, name='caisse_vente'),
    path('caisse/ajouter-produit/', views.caisse_ajouter_produit, name='caisse_ajouter_produit'),
    path('caisse/retirer-produit/<str:produit_id>/', views.caisse_retirer_produit, name='caisse_retirer_produit'),
    path('caisse/vider-panier/', views.caisse_vider_panier, name='caisse_vider_panier'),
    path('caisse/identifier-client/', views.caisse_identifier_client, name='caisse_identifier_client'),
    path('caisse/valider-vente/', views.caisse_valider_vente, name='caisse_valider_vente'),
    path('caisse/rapport/', views.caisse_rapport_journalier, name='caisse_rapport_journalier'),
    path('caisse/mes-ventes/', views.caissier_mes_ventes, name='caissier_mes_ventes'),
    
    # Gestion planning et congés (Scénario 8.1.3) - Espace Employé
    path('planning/mon-planning/', views.mon_planning, name='mon_planning'),
    path('planning/demander-conge/', views.demander_conge, name='demander_conge'),
    path('planning/mes-demandes/', views.mes_demandes_conges, name='mes_demandes_conges'),
    path('planning/changer-mot-de-passe/', views.changer_mot_de_passe, name='changer_mot_de_passe'),
    
    # Gestion planning et congés (Scénario 8.1.3) - Espace RH/Manager
    path('rh/demandes-conges/', views.rh_demandes_conges, name='rh_demandes_conges'),
    path('rh/traiter-demande/<int:demande_id>/', views.rh_traiter_demande, name='rh_traiter_demande'),
    path('rh/gestion-absences/', views.rh_gestion_absences, name='rh_gestion_absences'),
    path('rh/reinitialiser-mdp/', views.rh_reinitialiser_mdp, name='rh_reinitialiser_mdp'),
    
    # Gestion des alertes et mouvements de stock
    path('dashboard/stock/alertes/', views.stock_alertes_list, name='stock_alertes_list'),
    path('dashboard/stock/alertes/<int:alerte_id>/resoudre/', views.stock_alerte_resoudre, name='stock_alerte_resoudre'),
    path('dashboard/stock/mouvements/', views.stock_mouvements_list, name='stock_mouvements_list'),
    
    # Module Caisse/POS (Sprint 2)
    path('dashboard/caisse/', views.dashboard_caisse, name='dashboard_caisse'),
    path('pos/', views.pos_interface, name='pos_interface'),
    path('pos/nouvelle-transaction/', views.pos_nouvelle_transaction, name='pos_nouvelle_transaction'),
    path('pos/ajouter-produit/', views.pos_ajouter_produit, name='pos_ajouter_produit'),
    path('pos/retirer-produit/<int:ligne_id>/', views.pos_retirer_produit, name='pos_retirer_produit'),
    path('pos/annuler-transaction/', views.pos_annuler_transaction, name='pos_annuler_transaction'),
    path('pos/valider-vente/', views.pos_valider_vente, name='pos_valider_vente'),
    path('pos/ouvrir-session/', views.pos_ouvrir_session, name='pos_ouvrir_session'),
    path('pos/cloturer-session/', views.pos_cloturer_session, name='pos_cloturer_session'),
    
    # Module CRM & Fidélisation (Sprint 3)
    path('crm/clients/', views.clients_list, name='clients_list'),
    path('crm/clients/<int:client_id>/', views.client_detail, name='client_detail'),
    path('crm/clients/<int:client_id>/create-carte/', views.client_create_carte, name='client_create_carte'),
    path('crm/clients/<int:client_id>/crediter-points/', views.client_crediter_points, name='client_crediter_points'),
    path('crm/segments/', views.segments_list, name='segments_list'),
    path('crm/segments/create/', views.segment_create, name='segment_create'),
    path('crm/segments/<int:segment_id>/clients/', views.segment_clients, name='segment_clients'),
    path('crm/campagnes/', views.campagnes_list, name='campagnes_list'),
    path('crm/campagnes/create/', views.campagne_create, name='campagne_create'),
    path('crm/campagnes/<int:campagne_id>/', views.campagne_detail, name='campagne_detail'),
    path('crm/campagnes/<int:campagne_id>/send/', views.campagne_send, name='campagne_send'),
    
    # Module Analytics & Reporting (Sprint 4)
    path('dashboard/analytics/', views.dashboard_analytics, name='dashboard_analytics'),
    path('analytics/export/ventes/', views.export_ventes_excel, name='export_ventes_excel'),
    path('analytics/rapport-mensuel/', views.rapport_mensuel, name='rapport_mensuel'),
    
    # Gestion des Coupons (Marketing)
    path('marketing/coupons/', views.marketing_coupons_list, name='marketing_coupons_list'),
    path('marketing/coupons/create/', views.marketing_coupon_create, name='marketing_coupon_create'),
    path('marketing/coupons/generer-speciaux/', views.marketing_coupon_generer_speciaux, name='marketing_coupon_generer_speciaux'),
    path('marketing/coupons/<int:coupon_id>/desactiver/', views.marketing_coupon_desactiver, name='marketing_coupon_desactiver'),
    path('caisse/valider-coupon/', views.caisse_valider_coupon, name='caisse_valider_coupon'),
    
    # Algorithme Intelligent de Fidélité (Marketing)
    path('marketing/analyser-fidelite/', views.marketing_analyser_fidelite, name='marketing_analyser_fidelite'),
    path('marketing/fidelite-stats/', views.marketing_fidelite_stats, name='marketing_fidelite_stats'),
    
    # Dashboard KPIs CRM
    path('marketing/kpis/', views.marketing_dashboard_kpis, name='marketing_dashboard_kpis'),
    
    path('dashboard/marketing/', views.dashboard_marketing, name='dashboard_marketing'),
]
