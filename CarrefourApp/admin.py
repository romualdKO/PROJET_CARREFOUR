from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Employe, Produit, Vente, LigneVente, Client, 
    Promotion, Presence, SessionPresence, Conge, Formation, Reclamation
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
    list_filter = ['statut', 'date_creation']
