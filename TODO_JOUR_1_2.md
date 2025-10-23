# ✅ TODO LIST - Sprint 1 Jour 1 & 2

## 🎯 Objectif Aujourd'hui : Créer les Modèles de Données

---

## 📋 ÉTAPE 1 : Préparer l'environnement

- [ ] Ouvrir le fichier `CarrefourApp/models.py`
- [ ] Vérifier que le serveur est arrêté (CTRL+C dans le terminal)
- [ ] S'assurer d'avoir une sauvegarde de la base de données

---

## 📋 ÉTAPE 2 : Créer le Modèle Fournisseur

### Code à ajouter dans `models.py` :

```python
class Fournisseur(models.Model):
    """Modèle représentant un fournisseur du supermarché"""
    nom = models.CharField(max_length=200, verbose_name="Nom du fournisseur")
    contact = models.CharField(max_length=100, verbose_name="Nom du contact")
    email = models.EmailField(verbose_name="Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    adresse = models.TextField(verbose_name="Adresse complète")
    delai_livraison_moyen = models.IntegerField(
        verbose_name="Délai de livraison moyen (jours)"
    )
    conditions_paiement = models.TextField(
        verbose_name="Conditions de paiement"
    )
    est_actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
```

**Checklist** :
- [ ] Code copié dans models.py
- [ ] Vérifié qu'il n'y a pas d'erreurs de syntaxe
- [ ] Sauvegardé le fichier

---

## 📋 ÉTAPE 3 : Créer le Modèle CommandeFournisseur

### Code à ajouter :

```python
class CommandeFournisseur(models.Model):
    """Modèle représentant une commande passée à un fournisseur"""
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
        Employe,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Passée par"
    )
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Commande Fournisseur"
        verbose_name_plural = "Commandes Fournisseurs"
        ordering = ['-date_commande']
    
    def __str__(self):
        return f"{self.numero_commande} - {self.fournisseur.nom}"
    
    def save(self, *args, **kwargs):
        if not self.numero_commande:
            import datetime
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            dernier = CommandeFournisseur.objects.filter(
                numero_commande__startswith=f'CMD{date_str}'
            ).count()
            self.numero_commande = f'CMD{date_str}{dernier + 1:04d}'
        super().save(*args, **kwargs)
```

**Checklist** :
- [ ] Code copié
- [ ] Vérifié
- [ ] Sauvegardé

---

## 📋 ÉTAPE 4 : Créer le Modèle LigneCommandeFournisseur

### Code à ajouter :

```python
class LigneCommandeFournisseur(models.Model):
    """Ligne d'une commande fournisseur"""
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
```

**Checklist** :
- [ ] Code copié
- [ ] Vérifié
- [ ] Sauvegardé

---

## 📋 ÉTAPE 5 : Créer le Modèle MouvementStock

### Code à ajouter :

```python
class MouvementStock(models.Model):
    """Mouvement de stock (entrée/sortie)"""
    TYPE_MOUVEMENT_CHOICES = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
        ('AJUSTEMENT', 'Ajustement'),
        ('RETOUR', 'Retour'),
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
    quantite = models.IntegerField(verbose_name="Quantité")
    date_mouvement = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date"
    )
    raison = models.TextField(verbose_name="Raison")
    employe = models.ForeignKey(
        Employe,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Effectué par"
    )
    stock_avant = models.IntegerField(verbose_name="Stock avant")
    stock_apres = models.IntegerField(verbose_name="Stock après")
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

**Checklist** :
- [ ] Code copié
- [ ] Vérifié
- [ ] Sauvegardé

---

## 📋 ÉTAPE 6 : Créer le Modèle AlerteStock

### Code à ajouter :

```python
class AlerteStock(models.Model):
    """Alerte sur un produit en stock"""
    TYPE_ALERTE_CHOICES = [
        ('SEUIL_CRITIQUE', 'Seuil critique'),
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
        verbose_name="Date"
    )
    est_resolue = models.BooleanField(
        default=False,
        verbose_name="Résolue"
    )
    date_resolution = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de résolution"
    )
    message = models.TextField(verbose_name="Message")
    
    class Meta:
        verbose_name = "Alerte stock"
        verbose_name_plural = "Alertes stock"
        ordering = ['-date_alerte']
    
    def __str__(self):
        statut = "✅" if self.est_resolue else "🔔"
        return f"{statut} - {self.produit.nom} - {self.get_type_alerte_display()}"
```

**Checklist** :
- [ ] Code copié
- [ ] Vérifié
- [ ] Sauvegardé

---

## 📋 ÉTAPE 7 : Vérifier si Modèle Produit Existe

### Si le modèle Produit n'existe pas encore, le créer :

```python
class Produit(models.Model):
    """Modèle représentant un produit du supermarché"""
    CATEGORIE_CHOICES = [
        ('Alimentaire', 'Alimentaire'),
        ('Boissons', 'Boissons'),
        ('Hygiène', 'Hygiène'),
        ('Entretien', 'Entretien'),
        ('Électronique', 'Électronique'),
        ('Textile', 'Textile'),
        ('Fruits & Légumes', 'Fruits & Légumes'),
        ('Boulangerie', 'Boulangerie'),
        ('Surgelés', 'Surgelés'),
        ('Autres', 'Autres'),
    ]
    
    nom = models.CharField(max_length=200, verbose_name="Nom du produit")
    reference = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Référence"
    )
    categorie = models.CharField(
        max_length=50,
        choices=CATEGORIE_CHOICES,
        verbose_name="Catégorie"
    )
    prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix d'achat (FCFA)"
    )
    prix_vente = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix de vente (FCFA)"
    )
    stock = models.IntegerField(default=0, verbose_name="Stock actuel")
    seuil_reapprovisionnement = models.IntegerField(
        default=10,
        verbose_name="Seuil de réapprovisionnement"
    )
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Fournisseur"
    )
    description = models.TextField(blank=True, verbose_name="Description")
    est_actif = models.BooleanField(default=True, verbose_name="Actif")
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.reference})"
    
    def marge_beneficiaire(self):
        """Calcule la marge bénéficiaire"""
        if self.prix_achat > 0:
            return ((self.prix_vente - self.prix_achat) / self.prix_achat) * 100
        return 0
    
    def est_en_rupture(self):
        """Vérifie si le produit est en rupture"""
        return self.stock == 0
    
    def est_critique(self):
        """Vérifie si le stock est en dessous du seuil"""
        return self.stock <= self.seuil_reapprovisionnement and self.stock > 0
```

**Checklist** :
- [ ] Vérifié si Produit existe
- [ ] Si non, copié le code
- [ ] Sauvegardé

---

## 📋 ÉTAPE 8 : Créer les Migrations

### Commandes à exécuter dans le terminal :

```bash
# 1. Générer les migrations
python manage.py makemigrations

# 2. Vérifier les migrations créées
# Vous devriez voir quelque chose comme :
# Migrations for 'CarrefourApp':
#   CarrefourApp/migrations/0006_fournisseur_commandefournisseur_etc.py

# 3. Appliquer les migrations
python manage.py migrate
```

**Checklist** :
- [ ] `python manage.py makemigrations` exécuté
- [ ] Migrations créées sans erreur
- [ ] `python manage.py migrate` exécuté
- [ ] Migrations appliquées avec succès

---

## 📋 ÉTAPE 9 : Ajouter dans Django Admin

### Code à ajouter dans `CarrefourApp/admin.py` :

```python
from .models import (
    Fournisseur,
    CommandeFournisseur,
    LigneCommandeFournisseur,
    MouvementStock,
    AlerteStock,
    Produit
)

# Enregistrer les nouveaux modèles
admin.site.register(Fournisseur)
admin.site.register(CommandeFournisseur)
admin.site.register(LigneCommandeFournisseur)
admin.site.register(MouvementStock)
admin.site.register(AlerteStock)

# Si Produit n'est pas encore enregistré
# admin.site.register(Produit)
```

**Checklist** :
- [ ] Imports ajoutés
- [ ] Modèles enregistrés
- [ ] Sauvegardé

---

## 📋 ÉTAPE 10 : Tester dans Django Admin

### Actions :

1. **Démarrer le serveur** :
```bash
python manage.py runserver
```

2. **Se connecter à l'admin** :
- Aller sur http://127.0.0.1:8000/admin/
- Login avec compte DG (dg / DG2025@Admin)

3. **Vérifier que les nouveaux modèles apparaissent** :
- [ ] Fournisseur visible
- [ ] Commande Fournisseur visible
- [ ] Ligne Commande visible
- [ ] Mouvement Stock visible
- [ ] Alerte Stock visible
- [ ] Produit visible

4. **Créer des données de test** :
- [ ] Créer 2-3 fournisseurs
- [ ] Créer 5-10 produits
- [ ] Créer 1 commande de test

---

## ✅ RÉSULTAT ATTENDU À LA FIN DU JOUR 2

- ✅ 5 nouveaux modèles créés
- ✅ Modèle Produit créé ou amélioré
- ✅ Migrations générées et appliquées
- ✅ Modèles visibles dans Django Admin
- ✅ Données de test créées
- ✅ Aucune erreur

---

## 🎯 PROCHAINE ÉTAPE (Jour 3-4)

Une fois les modèles créés et testés :
- [ ] Améliorer le modèle Produit (ajouter champs si manquants)
- [ ] Créer les méthodes utiles
- [ ] Préparer les views pour CRUD Fournisseurs

---

## 🆘 En Cas de Problème

### Erreur de Migration
```bash
# Supprimer la dernière migration
python manage.py migrate CarrefourApp zero

# Supprimer le fichier de migration dans migrations/
# Puis refaire makemigrations et migrate
```

### Erreur d'Import
- Vérifier que tous les imports sont corrects en haut de `models.py`
- S'assurer que `from django.db import models` est présent

### Erreur de Syntaxe
- Vérifier les indentations (4 espaces)
- Vérifier les virgules
- Vérifier les parenthèses

---

**Date** : 17 octobre 2025  
**Sprint** : 1  
**Jour** : 1-2  
**Objectif** : ✅ Créer les modèles de données  

🚀 **BON COURAGE !**
