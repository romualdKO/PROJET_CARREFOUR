from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Employe, Produit, Vente, LigneVente, Client, 
    Promotion, Presence, SessionPresence, Conge, Formation, Reclamation,
    Fournisseur, CommandeFournisseur, LigneCommandeFournisseur, 
    MouvementStock, AlerteStock,
    # Sprint 2 - Caisse/POS
    Transaction, LigneTransaction, Paiement, TypePaiement, SessionCaisse,
    # Sprint 3 - CRM & Fidélisation
    CarteFidelite, OperationFidelite, Campagne, SegmentClient,
    # Scénario 8.1.3 - Planning & Congés
    Planning, DemandeConge, Pointage, Notification
)

@admin.register(Employe)
class EmployeAdmin(UserAdmin):
    list_display = ['username', 'employee_id', 'get_full_name', 'role', 'departement', 'est_actif']
    list_filter = ['role', 'departement', 'est_actif']
    search_fields = ['username', 'employee_id', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Employé', {
            'fields': ('employee_id', 'role', 'departement', 'telephone', 'photo', 
                      'date_embauche', 'est_actif')
        }),
        ('Autorisations Module', {
            'fields': ('acces_stocks', 'acces_caisse', 'acces_fidelisation', 'acces_rapports')
        }),
    )

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['reference', 'nom', 'categorie', 'prix_unitaire', 'stock_actuel', 'statut']
    list_filter = ['categorie', 'statut']
    search_fields = ['reference', 'nom', 'code_barre']

@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ['numero_transaction', 'caissier', 'montant_final', 'moyen_paiement', 'date_vente']
    list_filter = ['moyen_paiement', 'date_vente']
    search_fields = ['numero_transaction']
    date_hierarchy = 'date_vente'

@admin.register(LigneVente)
class LigneVenteAdmin(admin.ModelAdmin):
    list_display = ['vente', 'produit', 'quantite', 'prix_unitaire', 'montant_ligne']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'telephone', 'points_fidelite', 'niveau_fidelite', 'date_inscription']
    list_filter = ['niveau_fidelite']
    search_fields = ['nom', 'prenom', 'telephone']

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['titre', 'reduction', 'date_debut', 'date_fin', 'est_active']
    list_filter = ['est_active', 'date_debut']

@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ['employe', 'date', 'heure_premiere_arrivee', 'heure_derniere_depart', 'temps_actif_total', 'statut']
    list_filter = ['statut', 'date']
    date_hierarchy = 'date'

@admin.register(SessionPresence)
class SessionPresenceAdmin(admin.ModelAdmin):
    list_display = ['employe', 'date', 'heure_connexion', 'heure_deconnexion', 'duree_active']
    list_filter = ['date']
    date_hierarchy = 'date'

@admin.register(Conge)
class CongeAdmin(admin.ModelAdmin):
    list_display = ['employe', 'type_conge', 'date_debut', 'date_fin', 'statut']
    list_filter = ['type_conge', 'statut']

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'date_debut', 'date_fin', 'nombre_participants', 'est_terminee']
    list_filter = ['est_terminee']

@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ['client', 'sujet', 'statut', 'date_creation']


# ========================================
# ADMIN GESTION DES STOCKS (Sprint 1)
# ========================================

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'contact', 'telephone', 'email', 'delai_livraison_moyen', 'est_actif']
    list_filter = ['est_actif']
    search_fields = ['nom', 'contact', 'email']
    readonly_fields = ['date_creation', 'date_modification']


@admin.register(CommandeFournisseur)
class CommandeFournisseurAdmin(admin.ModelAdmin):
    list_display = ['numero_commande', 'fournisseur', 'statut', 'montant_total', 'date_commande', 'date_livraison_prevue']
    list_filter = ['statut', 'date_commande']
    search_fields = ['numero_commande', 'fournisseur__nom']
    readonly_fields = ['numero_commande', 'date_commande']
    date_hierarchy = 'date_commande'


@admin.register(LigneCommandeFournisseur)
class LigneCommandeFournisseurAdmin(admin.ModelAdmin):
    list_display = ['commande', 'produit', 'quantite_commandee', 'quantite_recue', 'prix_unitaire', 'montant_ligne']
    list_filter = ['commande__statut']
    search_fields = ['commande__numero_commande', 'produit__nom']


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ['produit', 'type_mouvement', 'quantite', 'stock_avant', 'stock_apres', 'date_mouvement', 'employe']
    list_filter = ['type_mouvement', 'date_mouvement']
    search_fields = ['produit__nom', 'employe__username']
    readonly_fields = ['date_mouvement']
    date_hierarchy = 'date_mouvement'


@admin.register(AlerteStock)
class AlerteStockAdmin(admin.ModelAdmin):
    list_display = ['produit', 'type_alerte', 'est_resolue', 'date_alerte', 'date_resolution']
    list_filter = ['type_alerte', 'est_resolue', 'date_alerte']
    search_fields = ['produit__nom', 'message']
    readonly_fields = ['date_alerte']


# =====================================================
# SPRINT 2 - ADMIN CAISSE/POS
# =====================================================

@admin.register(TypePaiement)
class TypePaiementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'est_actif', 'icone']
    list_filter = ['est_actif']
    search_fields = ['nom', 'code']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['numero_ticket', 'caissier', 'client', 'montant_final', 'statut', 'date_transaction']
    list_filter = ['statut', 'date_transaction', 'caissier']
    search_fields = ['numero_ticket', 'client__nom', 'client__telephone']
    readonly_fields = ['numero_ticket', 'date_transaction', 'date_modification']
    date_hierarchy = 'date_transaction'


@admin.register(LigneTransaction)
class LigneTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'produit', 'quantite', 'prix_unitaire', 'sous_total']
    list_filter = ['transaction__date_transaction']
    search_fields = ['transaction__numero_ticket', 'produit__nom']


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'type_paiement', 'montant', 'reference', 'valide', 'date_paiement']
    list_filter = ['type_paiement', 'valide', 'date_paiement']
    search_fields = ['transaction__numero_ticket', 'reference']
    readonly_fields = ['date_paiement']


@admin.register(SessionCaisse)
class SessionCaisseAdmin(admin.ModelAdmin):
    list_display = ['caissier', 'date_ouverture', 'date_cloture', 'fonds_ouverture', 'fonds_cloture_reel', 'ecart', 'est_cloturee']
    list_filter = ['est_cloturee', 'date_ouverture', 'caissier']
    search_fields = ['caissier__username', 'caissier__first_name', 'caissier__last_name']
    readonly_fields = ['date_ouverture', 'fonds_cloture_theorique', 'ecart']
    date_hierarchy = 'date_ouverture'


# =====================================================
# SPRINT 3 - MODULE CRM & FIDÉLISATION
# =====================================================

@admin.register(CarteFidelite)
class CarteFideliteAdmin(admin.ModelAdmin):
    list_display = ['numero_carte', 'client', 'date_emission', 'solde_points', 'statut']
    list_filter = ['statut', 'date_emission']
    search_fields = ['numero_carte', 'client__nom', 'client__prenom']
    readonly_fields = ['numero_carte', 'date_emission']
    date_hierarchy = 'date_emission'


@admin.register(OperationFidelite)
class OperationFideliteAdmin(admin.ModelAdmin):
    list_display = ['carte', 'type_operation', 'points', 'solde_avant', 'solde_apres', 'motif', 'date_operation']
    list_filter = ['type_operation', 'date_operation']
    search_fields = ['carte__numero_carte', 'carte__client__nom', 'motif']
    readonly_fields = ['date_operation', 'solde_avant', 'solde_apres']
    date_hierarchy = 'date_operation'


@admin.register(Campagne)
class CampagneAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_campagne', 'statut', 'date_debut', 'date_fin', 'nb_destinataires', 'nb_envoyes', 'nb_ouverts']
    list_filter = ['type_campagne', 'statut', 'date_debut']
    search_fields = ['titre', 'description']
    readonly_fields = ['date_creation', 'nb_destinataires', 'nb_envoyes', 'nb_ouverts']
    date_hierarchy = 'date_creation'


@admin.register(SegmentClient)
class SegmentClientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'niveau_fidelite', 'montant_achats_min', 'montant_achats_max', 'est_actif', 'date_creation']
    list_filter = ['niveau_fidelite', 'est_actif', 'date_creation']
    search_fields = ['nom', 'description']
    readonly_fields = ['date_creation']


# ==================== SCÉNARIO 8.1.3 : PLANNING & CONGÉS ====================

@admin.register(Planning)
class PlanningAdmin(admin.ModelAdmin):
    list_display = ['employe', 'date', 'poste', 'creneau', 'statut', 'heures_prevues', 'heures_reelles']
    list_filter = ['poste', 'creneau', 'statut', 'date']
    search_fields = ['employe__username', 'employe__first_name', 'employe__last_name']
    date_hierarchy = 'date'
    readonly_fields = ['cree_le', 'modifie_le']


@admin.register(DemandeConge)
class DemandeCongeAdmin(admin.ModelAdmin):
    list_display = ['employe', 'type_conge', 'date_debut', 'date_fin', 'nb_jours', 'statut', 'approuve_par', 'cree_le']
    list_filter = ['type_conge', 'statut', 'date_debut']
    search_fields = ['employe__username', 'employe__first_name', 'employe__last_name', 'motif']
    date_hierarchy = 'cree_le'
    readonly_fields = ['nb_jours', 'cree_le', 'modifie_le', 'date_reponse']


@admin.register(Pointage)
class PointageAdmin(admin.ModelAdmin):
    list_display = ['employe', 'date', 'heure_entree', 'heure_sortie', 'heures_travaillees', 'retard_minutes', 'type_journee', 'validee']
    list_filter = ['type_journee', 'validee', 'date']
    search_fields = ['employe__username', 'employe__first_name', 'employe__last_name']
    date_hierarchy = 'date'
    readonly_fields = ['heures_travaillees', 'retard_minutes', 'cree_le', 'modifie_le']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['destinataire', 'titre', 'type_notif', 'lue', 'cree_le']
    list_filter = ['type_notif', 'lue', 'cree_le']
    search_fields = ['destinataire__username', 'titre', 'message']
    date_hierarchy = 'cree_le'
    readonly_fields = ['cree_le', 'lue_le']

