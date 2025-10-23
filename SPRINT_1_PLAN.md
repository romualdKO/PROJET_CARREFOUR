# 🚀 SPRINT 1 - Gestion Stocks Avancée

## 📅 Durée : 2 semaines (17 oct - 31 oct 2025)

## 🎯 Objectifs du Sprint

1. ✅ Créer les modèles de base pour la gestion avancée des stocks
2. ✅ Implémenter le CRUD des fournisseurs
3. ✅ Développer le système d'alertes automatiques
4. ✅ Enrichir le dashboard Stock avec KPIs et graphiques

---

## 📋 Checklist des Tâches

### Jour 1-2 : Modèles de Données

- [ ] **Modèle Fournisseur**
  - [ ] Créer le modèle avec tous les champs
  - [ ] Ajouter les validations
  - [ ] Créer la migration
  - [ ] Appliquer la migration
  - [ ] Tester dans Django Admin

- [ ] **Modèle CommandeFournisseur**
  - [ ] Créer le modèle avec relation vers Fournisseur
  - [ ] Ajouter les champs de statut
  - [ ] Générer numéro de commande automatique
  - [ ] Migration + test

- [ ] **Modèle LigneCommandeFournisseur**
  - [ ] Créer le modèle
  - [ ] Relation avec CommandeFournisseur et Produit
  - [ ] Calculs automatiques
  - [ ] Migration + test

- [ ] **Modèle MouvementStock**
  - [ ] Créer le modèle
  - [ ] Types de mouvements (ENTREE, SORTIE, AJUSTEMENT, RETOUR)
  - [ ] Traçabilité complète
  - [ ] Migration + test

- [ ] **Modèle AlerteStock**
  - [ ] Créer le modèle
  - [ ] Types d'alertes
  - [ ] Système de résolution
  - [ ] Migration + test

### Jour 3-4 : Amélioration du Modèle Produit

- [ ] **Enrichir le modèle Produit existant**
  - [ ] Ajouter champ `seuil_reapprovisionnement`
  - [ ] Ajouter champ `stock_minimum`
  - [ ] Ajouter champ `stock_maximum`
  - [ ] Ajouter champ `marge_beneficiaire` (calculé)
  - [ ] Ajouter relation vers Fournisseur
  - [ ] Créer migration
  - [ ] Mettre à jour les produits existants

- [ ] **Méthodes du modèle Produit**
  - [ ] `est_en_rupture()` → bool
  - [ ] `est_critique()` → bool
  - [ ] `calculer_marge()` → Decimal
  - [ ] `besoin_reapprovisionnement()` → bool
  - [ ] `quantite_a_commander()` → int

### Jour 5-6 : CRUD Fournisseurs

- [ ] **Views Fournisseurs**
  - [ ] `stock_fournisseurs_list()` - Liste des fournisseurs
  - [ ] `stock_fournisseur_create()` - Créer un fournisseur
  - [ ] `stock_fournisseur_edit()` - Modifier un fournisseur
  - [ ] `stock_fournisseur_delete()` - Supprimer un fournisseur
  - [ ] `stock_fournisseur_detail()` - Détails + historique

- [ ] **Templates Fournisseurs**
  - [ ] `stock_fournisseurs_list.html`
  - [ ] `stock_fournisseur_form.html` (create/edit)
  - [ ] `stock_fournisseur_detail.html`
  - [ ] `stock_fournisseur_delete.html`

- [ ] **URLs**
  - [ ] `/dashboard/stock/fournisseurs/`
  - [ ] `/dashboard/stock/fournisseurs/create/`
  - [ ] `/dashboard/stock/fournisseurs/<id>/edit/`
  - [ ] `/dashboard/stock/fournisseurs/<id>/delete/`
  - [ ] `/dashboard/stock/fournisseurs/<id>/`

### Jour 7-8 : Système d'Alertes Automatiques

- [ ] **Signal pour détecter seuils critiques**
  - [ ] Créer signal `post_save` sur MouvementStock
  - [ ] Vérifier le stock après chaque mouvement
  - [ ] Créer alerte si seuil atteint
  - [ ] Envoyer notification (dans l'app pour l'instant)

- [ ] **Views Alertes**
  - [ ] `stock_alertes_list()` - Liste des alertes actives
  - [ ] `stock_alerte_resolve()` - Marquer comme résolue
  - [ ] `stock_alertes_dashboard()` - Widget dashboard

- [ ] **Templates Alertes**
  - [ ] `stock_alertes_list.html`
  - [ ] Widget d'alertes pour sidebar (composant réutilisable)

### Jour 9-10 : Gestion des Commandes Fournisseurs

- [ ] **Views Commandes**
  - [ ] `stock_commandes_list()` - Liste des commandes
  - [ ] `stock_commande_create()` - Créer une commande
  - [ ] `stock_commande_detail()` - Détails de la commande
  - [ ] `stock_commande_validate()` - Valider une commande
  - [ ] `stock_commande_receive()` - Réception marchandises
  - [ ] `stock_commande_cancel()` - Annuler une commande

- [ ] **Templates Commandes**
  - [ ] `stock_commandes_list.html`
  - [ ] `stock_commande_form.html`
  - [ ] `stock_commande_detail.html`
  - [ ] `stock_commande_reception.html`

- [ ] **Logique Métier**
  - [ ] Génération auto numéro de commande
  - [ ] Calcul du montant total
  - [ ] Mise à jour du stock à la réception
  - [ ] Création automatique de MouvementStock

### Jour 11-12 : Dashboard Stock Enrichi

- [ ] **KPIs à Afficher**
  - [ ] Nombre total de produits
  - [ ] Valeur du stock (en FCFA)
  - [ ] Nombre d'alertes actives
  - [ ] Nombre de produits en rupture
  - [ ] Nombre de commandes en attente
  - [ ] Taux de rotation du stock

- [ ] **Graphiques**
  - [ ] Évolution du stock (7 derniers jours)
  - [ ] Top 10 produits les plus en stock
  - [ ] Top 10 produits en rupture/critique
  - [ ] Répartition par catégorie
  - [ ] Valeur du stock par catégorie

- [ ] **Widgets**
  - [ ] Liste des derniers mouvements
  - [ ] Alertes en temps réel
  - [ ] Commandes à traiter
  - [ ] Produits à réapprovisionner (suggestions)

- [ ] **Template**
  - [ ] Mettre à jour `stock.html`
  - [ ] Ajouter Chart.js pour les graphiques
  - [ ] Design responsive

### Jour 13-14 : Tests et Documentation

- [ ] **Tests**
  - [ ] Tester tous les modèles
  - [ ] Tester toutes les views
  - [ ] Tester le système d'alertes
  - [ ] Tester la génération de commandes

- [ ] **Documentation**
  - [ ] Documenter les modèles
  - [ ] Documenter les views
  - [ ] Créer un guide utilisateur pour le module Stock
  - [ ] Documenter les signaux et alertes

- [ ] **Optimisation**
  - [ ] Optimiser les requêtes SQL (select_related, prefetch_related)
  - [ ] Ajouter des index sur les champs critiques
  - [ ] Vérifier les performances

---

## 📊 Modèles de Données Détaillés

### 1. Modèle Fournisseur

```python
class Fournisseur(models.Model):
    """
    Modèle représentant un fournisseur du supermarché
    """
    nom = models.CharField(max_length=200, verbose_name="Nom du fournisseur")
    contact = models.CharField(max_length=100, verbose_name="Nom du contact")
    email = models.EmailField(verbose_name="Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    adresse = models.TextField(verbose_name="Adresse complète")
    
    delai_livraison_moyen = models.IntegerField(
        verbose_name="Délai de livraison moyen (jours)",
        help_text="Nombre de jours en moyenne pour une livraison"
    )
    
    conditions_paiement = models.TextField(
        verbose_name="Conditions de paiement",
        help_text="Ex: Paiement à 30 jours, 50% à la commande"
    )
    
    est_actif = models.BooleanField(
        default=True,
        verbose_name="Fournisseur actif",
        help_text="Décocher pour désactiver le fournisseur"
    )
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
    
    def nombre_produits(self):
        """Retourne le nombre de produits fournis"""
        return self.produit_set.count()
    
    def nombre_commandes(self):
        """Retourne le nombre total de commandes"""
        return self.commandefournisseur_set.count()
    
    def montant_total_commandes(self):
        """Retourne le montant total de toutes les commandes"""
        from django.db.models import Sum
        total = self.commandefournisseur_set.aggregate(
            total=Sum('montant_total')
        )['total']
        return total or 0
```

### 2. Modèle CommandeFournisseur

```python
class CommandeFournisseur(models.Model):
    """
    Modèle représentant une commande passée à un fournisseur
    """
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDEE', 'Validée'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    numero_commande = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Numéro de commande"
    )
    
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        verbose_name="Fournisseur"
    )
    
    date_commande = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de commande"
    )
    
    date_livraison_prevue = models.DateTimeField(
        verbose_name="Date de livraison prévue"
    )
    
    date_livraison_reelle = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de livraison réelle"
    )
    
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE',
        verbose_name="Statut"
    )
    
    montant_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Montant total (FCFA)"
    )
    
    employe = models.ForeignKey(
        'Employe',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Passée par"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="Notes / Remarques"
    )
    
    class Meta:
        verbose_name = "Commande Fournisseur"
        verbose_name_plural = "Commandes Fournisseurs"
        ordering = ['-date_commande']
    
    def __str__(self):
        return f"{self.numero_commande} - {self.fournisseur.nom}"
    
    def save(self, *args, **kwargs):
        if not self.numero_commande:
            # Générer un numéro de commande automatique
            import datetime
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            dernier = CommandeFournisseur.objects.filter(
                numero_commande__startswith=f'CMD{date_str}'
            ).count()
            self.numero_commande = f'CMD{date_str}{dernier + 1:04d}'
        super().save(*args, **kwargs)
    
    def calculer_montant_total(self):
        """Calcule le montant total de la commande"""
        from django.db.models import Sum, F
        total = self.lignecommandefournisseur_set.aggregate(
            total=Sum(F('quantite_commandee') * F('prix_unitaire'))
        )['total']
        return total or 0
    
    def nombre_produits(self):
        """Retourne le nombre de produits différents dans la commande"""
        return self.lignecommandefournisseur_set.count()
```

### 3. Modèle LigneCommandeFournisseur

```python
class LigneCommandeFournisseur(models.Model):
    """
    Modèle représentant une ligne d'une commande fournisseur
    """
    commande = models.ForeignKey(
        CommandeFournisseur,
        on_delete=models.CASCADE,
        verbose_name="Commande"
    )
    
    produit = models.ForeignKey(
        'Produit',
        on_delete=models.PROTECT,
        verbose_name="Produit"
    )
    
    quantite_commandee = models.IntegerField(
        verbose_name="Quantité commandée"
    )
    
    quantite_recue = models.IntegerField(
        default=0,
        verbose_name="Quantité reçue"
    )
    
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix unitaire (FCFA)"
    )
    
    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"
    
    def __str__(self):
        return f"{self.produit.nom} x {self.quantite_commandee}"
    
    def montant_ligne(self):
        """Calcule le montant de la ligne"""
        return self.quantite_commandee * self.prix_unitaire
    
    def ecart_quantite(self):
        """Calcule l'écart entre commandé et reçu"""
        return self.quantite_recue - self.quantite_commandee
```

### 4. Modèle MouvementStock

```python
class MouvementStock(models.Model):
    """
    Modèle représentant un mouvement de stock (entrée/sortie)
    """
    TYPE_MOUVEMENT_CHOICES = [
        ('ENTREE', 'Entrée (Achat/Livraison)'),
        ('SORTIE', 'Sortie (Vente)'),
        ('AJUSTEMENT', 'Ajustement (Inventaire)'),
        ('RETOUR', 'Retour (Client/Fournisseur)'),
    ]
    
    produit = models.ForeignKey(
        'Produit',
        on_delete=models.PROTECT,
        verbose_name="Produit"
    )
    
    type_mouvement = models.CharField(
        max_length=20,
        choices=TYPE_MOUVEMENT_CHOICES,
        verbose_name="Type de mouvement"
    )
    
    quantite = models.IntegerField(
        verbose_name="Quantité",
        help_text="Nombre positif pour entrée, négatif pour sortie"
    )
    
    date_mouvement = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date du mouvement"
    )
    
    raison = models.TextField(
        verbose_name="Raison / Commentaire"
    )
    
    employe = models.ForeignKey(
        'Employe',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Effectué par"
    )
    
    stock_avant = models.IntegerField(
        verbose_name="Stock avant mouvement"
    )
    
    stock_apres = models.IntegerField(
        verbose_name="Stock après mouvement"
    )
    
    commande_fournisseur = models.ForeignKey(
        CommandeFournisseur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Commande liée"
    )
    
    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ['-date_mouvement']
    
    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom} ({self.quantite})"
```

### 5. Modèle AlerteStock

```python
class AlerteStock(models.Model):
    """
    Modèle représentant une alerte sur un produit en stock
    """
    TYPE_ALERTE_CHOICES = [
        ('SEUIL_CRITIQUE', 'Seuil critique atteint'),
        ('RUPTURE', 'Rupture de stock'),
        ('SURSTOCK', 'Surstock'),
    ]
    
    produit = models.ForeignKey(
        'Produit',
        on_delete=models.CASCADE,
        verbose_name="Produit"
    )
    
    type_alerte = models.CharField(
        max_length=20,
        choices=TYPE_ALERTE_CHOICES,
        verbose_name="Type d'alerte"
    )
    
    date_alerte = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de l'alerte"
    )
    
    est_resolue = models.BooleanField(
        default=False,
        verbose_name="Alerte résolue"
    )
    
    date_resolution = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de résolution"
    )
    
    message = models.TextField(
        verbose_name="Message de l'alerte"
    )
    
    class Meta:
        verbose_name = "Alerte stock"
        verbose_name_plural = "Alertes stock"
        ordering = ['-date_alerte']
    
    def __str__(self):
        statut = "✅ Résolue" if self.est_resolue else "🔔 Active"
        return f"{statut} - {self.produit.nom} - {self.get_type_alerte_display()}"
```

---

## 🎨 Exemple de Dashboard Stock Enrichi

### KPIs à Afficher

```
┌─────────────────────────────────────────────────────────────┐
│                    GESTION DES STOCKS                        │
└─────────────────────────────────────────────────────────────┘

┌──────────┬──────────┬──────────┬──────────┬──────────────┐
│  Total   │  Valeur  │  Alertes │ Ruptures │  Commandes   │
│ Produits │  Stock   │  Actives │          │  En attente  │
├──────────┼──────────┼──────────┼──────────┼──────────────┤
│   1,245  │ 45.5M F  │    12    │    3     │      5       │
└──────────┴──────────┴──────────┴──────────┴──────────────┘

┌─────────────────────────────────────────────────────────────┐
│               📊 ÉVOLUTION DU STOCK (7 jours)               │
│  [Graphique en ligne montrant l'évolution]                  │
└─────────────────────────────────────────────────────────────┘

┌────────────────────────┬────────────────────────────────────┐
│  🔔 ALERTES ACTIVES    │  📦 PRODUITS À RÉAPPROVISIONNER   │
│  (12 alertes)          │  (Suggestions automatiques)        │
│                        │                                    │
│  • Lait 1L (Rupture)   │  • Farine T45 (Commander 500u)    │
│  • Pain (Critique)     │  • Sucre 1kg (Commander 200u)     │
│  • Œufs (Critique)     │  • Riz 5kg (Commander 100u)       │
└────────────────────────┴────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│            📋 DERNIERS MOUVEMENTS DE STOCK                  │
│                                                             │
│  17/10 14:30 | ENTREE | Lait 1L (+100) | CMD20251017001   │
│  17/10 12:15 | SORTIE | Pain (-50)     | Vente #1234      │
│  17/10 10:00 | ENTREE | Sucre (+200)   | CMD20251017002   │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ Critères de Validation du Sprint

- [ ] Tous les modèles créés et migrés
- [ ] CRUD Fournisseurs fonctionnel
- [ ] Système d'alertes automatiques opérationnel
- [ ] Dashboard Stock enrichi avec KPIs et graphiques
- [ ] Gestion des commandes fournisseurs fonctionnelle
- [ ] Tests unitaires pour tous les modèles
- [ ] Documentation complète du module
- [ ] Code reviewé et optimisé
- [ ] Démo fonctionnelle du module Stock

---

## 📝 Notes de Développement

### Bonnes Pratiques

1. **Modèles** :
   - Toujours ajouter `__str__()`
   - Utiliser `verbose_name` pour tous les champs
   - Ajouter `help_text` quand nécessaire
   - Créer des méthodes utiles (calculs, vérifications)

2. **Views** :
   - Utiliser `@login_required`
   - Vérifier les permissions
   - Ajouter des messages de succès/erreur
   - Optimiser les requêtes (select_related, prefetch_related)

3. **Templates** :
   - Utiliser le système de templates Django (extends, include)
   - Rendre responsive
   - Ajouter des icônes pour une meilleure UX
   - Gérer les messages d'erreur

4. **Sécurité** :
   - CSRF tokens dans tous les formulaires
   - Validation des données côté serveur
   - Protection contre les injections SQL (ORM Django)
   - Logging des actions critiques

---

## 🚀 Démarrage du Sprint

**Commande pour créer les migrations** :
```bash
python manage.py makemigrations
python manage.py migrate
```

**Ordre de développement recommandé** :
1. Modèles → 2. Migrations → 3. Admin → 4. Views → 5. Templates → 6. URLs → 7. Tests

---

**Date de début** : 17 octobre 2025  
**Date de fin prévue** : 31 octobre 2025  
**Équipe** : Developer + Product Owner  
**Statut** : 🟢 PRÊT À DÉMARRER
