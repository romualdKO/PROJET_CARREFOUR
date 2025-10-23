"""
Signals pour la gestion automatique du stock
Sprint 1 - Jour 7-8
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from decimal import Decimal
from .models import (
    MouvementStock, 
    AlerteStock, 
    Produit, 
    LigneCommandeFournisseur,
    CommandeFournisseur
)


@receiver(post_save, sender=MouvementStock)
def verifier_alertes_stock(sender, instance, created, **kwargs):
    """
    Vérifie et crée des alertes de stock après chaque mouvement
    Alertes déclenchées :
    - RUPTURE : stock = 0
    - SEUIL_CRITIQUE : stock <= stock_critique
    - SURSTOCK : stock >= stock_maximum
    """
    if created:
        produit = instance.produit
        stock_actuel = produit.stock_actuel
        
        # Alerte RUPTURE DE STOCK
        if stock_actuel == 0:
            # Vérifier si l'alerte existe déjà et n'est pas résolue
            alerte_existante = AlerteStock.objects.filter(
                produit=produit,
                type_alerte='RUPTURE',
                est_resolue=False
            ).first()
            
            if not alerte_existante:
                AlerteStock.objects.create(
                    produit=produit,
                    type_alerte='RUPTURE',
                    message=f"🔴 RUPTURE DE STOCK - Le produit '{produit.nom}' est en rupture de stock (0 unités)."
                )
        
        # Alerte SEUIL CRITIQUE
        elif produit.est_critique():
            alerte_existante = AlerteStock.objects.filter(
                produit=produit,
                type_alerte='SEUIL_CRITIQUE',
                est_resolue=False
            ).first()
            
            if not alerte_existante:
                AlerteStock.objects.create(
                    produit=produit,
                    type_alerte='SEUIL_CRITIQUE',
                    message=f"⚠️ STOCK CRITIQUE - Le produit '{produit.nom}' a atteint le seuil critique ({stock_actuel} unités restantes)."
                )
        
        # Alerte SURSTOCK
        elif stock_actuel >= produit.stock_maximum:
            alerte_existante = AlerteStock.objects.filter(
                produit=produit,
                type_alerte='SURSTOCK',
                est_resolue=False
            ).first()
            
            if not alerte_existante:
                AlerteStock.objects.create(
                    produit=produit,
                    type_alerte='SURSTOCK',
                    message=f"📦 SURSTOCK - Le produit '{produit.nom}' est en surstock ({stock_actuel}/{produit.stock_maximum} unités)."
                )
        
        # Résoudre les alertes si le stock revient à la normale
        else:
            # Résoudre les alertes de rupture et seuil critique si stock redevient normal
            AlerteStock.objects.filter(
                produit=produit,
                type_alerte__in=['RUPTURE', 'SEUIL_CRITIQUE'],
                est_resolue=False
            ).update(est_resolue=True)


@receiver(pre_save, sender=MouvementStock)
def enregistrer_stock_avant_mouvement(sender, instance, **kwargs):
    """
    Enregistre le stock avant et après le mouvement
    Met à jour automatiquement le stock du produit
    """
    if instance.pk is None:  # Nouveau mouvement uniquement
        produit = instance.produit
        instance.stock_avant = produit.stock_actuel
        
        # Calculer le nouveau stock selon le type de mouvement
        if instance.type_mouvement == 'ENTREE':
            nouveau_stock = produit.stock_actuel + instance.quantite
        elif instance.type_mouvement == 'SORTIE':
            nouveau_stock = max(0, produit.stock_actuel - instance.quantite)
        elif instance.type_mouvement == 'AJUSTEMENT':
            # Pour ajustement, la quantité peut être positive ou négative
            nouveau_stock = max(0, produit.stock_actuel + instance.quantite)
        elif instance.type_mouvement == 'RETOUR':
            nouveau_stock = produit.stock_actuel + instance.quantite
        else:
            nouveau_stock = produit.stock_actuel
        
        instance.stock_apres = nouveau_stock
        
        # Mettre à jour le stock du produit
        produit.stock_actuel = nouveau_stock
        produit.save()


@receiver(post_save, sender=LigneCommandeFournisseur)
def creer_mouvement_reception_commande(sender, instance, created, **kwargs):
    """
    Crée automatiquement un mouvement de stock lors de la réception d'une commande
    """
    if not created:
        # Vérifier si la quantité reçue a changé
        try:
            old_instance = LigneCommandeFournisseur.objects.get(pk=instance.pk)
            if old_instance.quantite_recue != instance.quantite_recue:
                quantite_ajoutee = instance.quantite_recue - old_instance.quantite_recue
                
                if quantite_ajoutee > 0:
                    # Créer un mouvement d'entrée
                    MouvementStock.objects.create(
                        produit=instance.produit,
                        type_mouvement='ENTREE',
                        quantite=quantite_ajoutee,
                        raison=f"Réception commande {instance.commande.numero_commande} - {quantite_ajoutee} unités reçues",
                        employe=instance.commande.employe,
                        commande_fournisseur=instance.commande
                    )
        except LigneCommandeFournisseur.DoesNotExist:
            pass


@receiver(post_save, sender=CommandeFournisseur)
def gerer_statut_commande(sender, instance, created, **kwargs):
    """
    Gère les actions automatiques selon le statut de la commande
    """
    if instance.statut == 'LIVREE':
        # Vérifier si tous les produits ont été reçus
        lignes_commande = instance.lignes.all()
        
        for ligne in lignes_commande:
            if ligne.quantite_recue > 0:
                # Créer un mouvement d'entrée si pas encore créé
                mouvement_existant = MouvementStock.objects.filter(
                    produit=ligne.produit,
                    commande_fournisseur=instance,
                    type_mouvement='ENTREE'
                ).exists()
                
                if not mouvement_existant:
                    MouvementStock.objects.create(
                        produit=ligne.produit,
                        type_mouvement='ENTREE',
                        quantite=ligne.quantite_recue,
                        raison=f"Livraison complète commande {instance.numero_commande}",
                        employe=instance.employe,
                        commande_fournisseur=instance
                    )


@receiver(post_save, sender=Produit)
def verifier_besoin_reapprovisionnement(sender, instance, created, **kwargs):
    """
    Vérifie si un produit nécessite un réapprovisionnement
    Envoie une alerte si le seuil est atteint
    """
    if not created:  # Uniquement pour les produits modifiés
        if instance.besoin_reapprovisionnement():
            # Vérifier si une alerte existe déjà
            alerte_existante = AlerteStock.objects.filter(
                produit=instance,
                type_alerte='SEUIL_CRITIQUE',
                est_resolue=False
            ).first()
            
            if not alerte_existante:
                quantite_recommandee = instance.quantite_a_commander()
                AlerteStock.objects.create(
                    produit=instance,
                    type_alerte='SEUIL_CRITIQUE',
                    message=f"🔔 RÉAPPROVISIONNEMENT NÉCESSAIRE - Le produit '{instance.nom}' nécessite un réapprovisionnement. "
                            f"Quantité recommandée : {quantite_recommandee} unités."
                )
