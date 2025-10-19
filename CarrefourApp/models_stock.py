from django.db import models

class Categorie(models.Model):
    idCategorie = models.CharField(primary_key=True, max_length=50)
    nom = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Produit(models.Model):
    idProduit = models.CharField(primary_key=True, max_length=50)
    nom = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    prixAchat = models.DecimalField(max_digits=10, decimal_places=2)
    prixVente = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.IntegerField()
    dateCreation = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='produits/', null=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="produits")

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Fournisseur(models.Model):
    idFournisseur = models.CharField(primary_key=True, max_length=50)
    nom = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=255)
    delaiLivraison = models.IntegerField()
    evaluationQualite = models.FloatField()

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class CommandeApprovisionnement(models.Model):
    idCommande = models.CharField(primary_key=True, max_length=50)
    dateCommande = models.DateField(auto_now_add=True)
    statutCommande = models.CharField(max_length=50)
    dateLivraisonPrevue = models.DateField(null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name="commandes")

    class Meta:
        verbose_name = "Commande d'approvisionnement"
        verbose_name_plural = "Commandes d'approvisionnement"
        ordering = ["-dateCommande"]

    def __str__(self):
        return f"Commande {self.idCommande}"


class LigneDeCommande(models.Model):
    idLigneCommande = models.CharField(primary_key=True, max_length=50)
    commande = models.ForeignKey(CommandeApprovisionnement, on_delete=models.CASCADE, related_name="lignes")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantiteCommandee = models.IntegerField()
    quantiteRecue = models.IntegerField(default=0)
    prixUnitaire = models.DecimalField(max_digits=10, decimal_places=2)
    dateReception = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"
        ordering = ["idLigneCommande"]

    def __str__(self):
        return f"Ligne {self.idLigneCommande} - {self.produit.nom}"


class Stock(models.Model):
    idStock = models.CharField(primary_key=True, max_length=50)
    produit = models.OneToOneField(Produit, on_delete=models.CASCADE, related_name="stock")
    quantiteActuelle = models.IntegerField(default=0)
    quantiteReservee = models.IntegerField(default=0)
    quantiteDisponible = models.IntegerField(default=0)
    statut = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stock"
        ordering = ["produit__nom"]

    def __str__(self):
        return f"Stock {self.produit.nom}"


class HistoriqueStock(models.Model):
    idInventaire = models.CharField(primary_key=True, max_length=50)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="historique")
    dateInventaire = models.DateField(auto_now_add=True)
    responsable = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Historique stock"
        verbose_name_plural = "Historique des stocks"
        ordering = ["-dateInventaire"]

    def __str__(self):
        return f"Inventaire {self.idInventaire}"


class AlerteStock(models.Model):
    idAlerte = models.CharField(primary_key=True, max_length=50)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="alertes")
    typeAlerte = models.CharField(max_length=100)
    dateTraitement = models.DateTimeField(null=True, blank=True)
    dateCreation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Alerte stock"
        verbose_name_plural = "Alertes stock"
        ordering = ["-dateCreation"]

    def __str__(self):
        return f"Alerte {self.typeAlerte} - {self.produit.nom}"
