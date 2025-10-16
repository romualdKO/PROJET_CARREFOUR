from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Modèle Utilisateur personnalisé
class Employe(AbstractUser):
    ROLES = [
        ('DG', 'Directeur Général'),
        ('DAF', 'Directeur Administratif et Financier'),
        ('RH', 'Responsable RH'),
        ('STOCK', 'Gestionnaire Stock'),
        ('CAISSIER', 'Caissier'),
        ('MARKETING', 'Marketing'),
        ('ANALYSTE', 'Analyste'),
    ]
    
    DEPARTEMENTS = [
        ('DIRECTION', 'Direction Générale'),
        ('FINANCE', 'Finance'),
        ('RH', 'Ressources Humaines'),
        ('LOGISTIQUE', 'Logistique'),
        ('VENTES', 'Ventes'),
        ('MARKETING', 'Marketing'),
        ('ALIMENTAIRE', 'Alimentaire'),
        ('HYGIENE', 'Hygiène'),
    ]
    
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLES, default='CAISSIER')
    departement = models.CharField(max_length=50, choices=DEPARTEMENTS, default='VENTES')
    telephone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='employees/', blank=True, null=True)
    date_embauche = models.DateField(default=timezone.now)
    est_actif = models.BooleanField(default=True)
    
    # Autorisations d'accès aux modules
    acces_stocks = models.BooleanField(default=False)
    acces_caisse = models.BooleanField(default=False)
    acces_fidelisation = models.BooleanField(default=False)
    acces_rapports = models.BooleanField(default=False)
    
    # Horaires de travail (définis par RH)
    heure_debut_travail = models.TimeField(default='08:00', help_text="Heure de début de travail")
    heure_fin_travail = models.TimeField(default='17:00', help_text="Heure de fin de travail")
    duree_pause = models.IntegerField(default=90, help_text="Durée de la pause en minutes (par défaut 1h30)")
    
    derniere_connexion_custom = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.employee_id:
            # Générer un ID employé automatique
            last_emp = Employe.objects.all().order_by('id').last()
            if last_emp and last_emp.employee_id:
                try:
                    last_num = int(last_emp.employee_id.replace('EMP', ''))
                    self.employee_id = f'EMP{str(last_num + 1).zfill(3)}'
                except:
                    self.employee_id = 'EMP001'
            else:
                self.employee_id = 'EMP001'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.employee_id})"
    
    class Meta:
        verbose_name = 'Employé'
        verbose_name_plural = 'Employés'


# Modèle Produit
class Produit(models.Model):
    CATEGORIES = [
        ('ALIMENTAIRE', 'Alimentaire'),
        ('BOISSONS', 'Boissons'),
        ('HYGIENE', 'Hygiène'),
        ('VETEMENTS', 'Vêtements'),
        ('ELECTRONIQUE', 'Électronique'),
        ('MAISON', 'Maison & Jardin'),
    ]
    
    STATUTS = [
        ('EN_STOCK', 'En stock'),
        ('CRITIQUE', 'Stock critique'),
        ('RUPTURE', 'Rupture'),
    ]
    
    reference = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=200)
    categorie = models.CharField(max_length=50, choices=CATEGORIES)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actuel = models.IntegerField(default=0)
    stock_critique = models.IntegerField(default=10)
    fournisseur = models.CharField(max_length=200)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    code_barre = models.CharField(max_length=50, blank=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN_STOCK')
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def get_statut(self):
        if self.stock_actuel == 0:
            return 'RUPTURE'
        elif self.stock_actuel <= self.stock_critique:
            return 'CRITIQUE'
        return 'EN_STOCK'
    
    def save(self, *args, **kwargs):
        self.statut = self.get_statut()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nom} ({self.reference})"
    
    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'


# Modèle Vente
class Vente(models.Model):
    MOYENS_PAIEMENT = [
        ('ESPECES', 'Espèces'),
        ('CARTE', 'Carte bancaire'),
        ('MOBILE', 'Mobile Money'),
    ]
    
    numero_transaction = models.CharField(max_length=20, unique=True)
    caissier = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, related_name='ventes')
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, blank=True)
    montant_total = models.DecimalField(max_digits=12, decimal_places=2)
    montant_tva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remise = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_final = models.DecimalField(max_digits=12, decimal_places=2)
    moyen_paiement = models.CharField(max_length=20, choices=MOYENS_PAIEMENT)
    date_vente = models.DateTimeField(auto_now_add=True)
    caisse_numero = models.CharField(max_length=10, default='#01')
    
    def save(self, *args, **kwargs):
        if not self.numero_transaction:
            # Générer numéro de transaction
            today = timezone.now().strftime('%y%m%d')
            last_vente = Vente.objects.filter(numero_transaction__startswith=f'T{today}').order_by('id').last()
            if last_vente:
                try:
                    last_num = int(last_vente.numero_transaction[-3:])
                    self.numero_transaction = f'T{today}{str(last_num + 1).zfill(3)}'
                except:
                    self.numero_transaction = f'T{today}001'
            else:
                self.numero_transaction = f'T{today}001'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Vente {self.numero_transaction} - {self.montant_final} FCFA"
    
    class Meta:
        verbose_name = 'Vente'
        verbose_name_plural = 'Ventes'
        ordering = ['-date_vente']


# Modèle Ligne de Vente
class LigneVente(models.Model):
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    montant_ligne = models.DecimalField(max_digits=12, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.montant_ligne = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"


# Modèle Client
class Client(models.Model):
    NIVEAUX_FIDELITE = [
        ('TOUS', 'Tous'),
        ('VIP', 'VIP'),
        ('GOLD', 'Gold'),
        ('SILVER', 'Silver'),
    ]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    points_fidelite = models.IntegerField(default=0)
    niveau_fidelite = models.CharField(max_length=20, choices=NIVEAUX_FIDELITE, default='TOUS')
    date_inscription = models.DateTimeField(auto_now_add=True)
    derniere_visite = models.DateTimeField(null=True, blank=True)
    total_achats = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def calculer_niveau(self):
        if self.points_fidelite >= 2000:
            return 'VIP'
        elif self.points_fidelite >= 1000:
            return 'GOLD'
        elif self.points_fidelite >= 500:
            return 'SILVER'
        return 'TOUS'
    
    def save(self, *args, **kwargs):
        self.niveau_fidelite = self.calculer_niveau()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.telephone}"
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


# Modèle Promotion
class Promotion(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    reduction = models.DecimalField(max_digits=5, decimal_places=2)  # en pourcentage
    date_debut = models.DateField()
    date_fin = models.DateField()
    est_active = models.BooleanField(default=True)
    produits = models.ManyToManyField(Produit, related_name='promotions', blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titre
    
    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'


# Modèle Présence
class Presence(models.Model):
    STATUTS = [
        ('PRESENT', 'Présent'),
        ('RETARD', 'En retard'),
        ('ABSENT', 'Absent'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='presences')
    date = models.DateField(default=timezone.now)
    heure_arrivee = models.TimeField(null=True, blank=True)
    heure_depart = models.TimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='ABSENT')
    motif_absence = models.CharField(max_length=200, blank=True)
    tolerance_retard = models.IntegerField(default=60, help_text="Tolérance en minutes avant d'être marqué absent (défaut: 60min)")
    
    def calculer_statut(self):
        """
        Calcule le statut basé sur l'heure d'arrivée et les heures travaillées:
        - ABSENT: Si pas d'arrivée OU arrivée > tolerance_retard (défaut 1h) OU heures travaillées < 60%
        - RETARD: Si arrivée en retard mais heures travaillées ≥ 60%
        - PRESENT: Si arrivée à l'heure et heures travaillées ≥ 60%
        """
        if not self.heure_arrivee:
            return 'ABSENT'
        
        from datetime import datetime, timedelta
        heure_debut = datetime.combine(self.date, self.employe.heure_debut_travail)
        heure_arrivee_dt = datetime.combine(self.date, self.heure_arrivee)
        
        # Règle 1: Si arrivée > tolérance (défaut 60 min), c'est ABSENT
        tolerance_absence = timedelta(minutes=self.tolerance_retard)
        if heure_arrivee_dt > heure_debut + tolerance_absence:
            return 'ABSENT'
        
        # Si heure de départ existe, vérifier le pourcentage d'heures travaillées
        if self.heure_depart:
            heures_travaillees = self.calculer_heures_travaillees()
            heures_requises = self.calculer_heures_requises()
            
            # Règle 2: Si < 60% des heures requises, c'est ABSENT
            if heures_requises > 0:
                pourcentage = (heures_travaillees / heures_requises) * 100
                if pourcentage < 60:
                    return 'ABSENT'
        
        # Règle 3: Vérifier le retard (15 minutes de tolérance pour le retard)
        tolerance_retard_simple = timedelta(minutes=15)
        if heure_arrivee_dt > heure_debut + tolerance_retard_simple:
            return 'RETARD'
        
        return 'PRESENT'
    
    def calculer_heures_requises(self):
        """Calcule les heures de travail requises pour la journée"""
        from datetime import datetime
        debut = datetime.combine(self.date, self.employe.heure_debut_travail)
        fin = datetime.combine(self.date, self.employe.heure_fin_travail)
        
        duree_totale = (fin - debut).total_seconds() / 3600
        pause_heures = self.employe.duree_pause / 60
        
        return duree_totale - pause_heures
    
    def calculer_heures_travaillees(self):
        """Calcule les heures effectivement travaillées (excluant la pause)"""
        if not self.heure_arrivee or not self.heure_depart:
            return 0
        
        from datetime import datetime, timedelta
        arrivee = datetime.combine(self.date, self.heure_arrivee)
        depart = datetime.combine(self.date, self.heure_depart)
        
        # Calculer la durée totale
        duree_totale = (depart - arrivee).total_seconds() / 3600  # en heures
        
        # Soustraire la pause (convertir minutes en heures)
        pause_heures = self.employe.duree_pause / 60
        
        heures_travaillees = duree_totale - pause_heures
        return max(0, heures_travaillees)  # Ne pas retourner de valeur négative
    
    def calculer_pourcentage_presence(self):
        """Calcule le pourcentage de présence effectif"""
        heures_travaillees = self.calculer_heures_travaillees()
        heures_requises = self.calculer_heures_requises()
        
        if heures_requises > 0:
            return (heures_travaillees / heures_requises) * 100
        return 0
    
    def save(self, *args, **kwargs):
        # Calculer automatiquement le statut avant de sauvegarder
        if self.heure_arrivee:
            self.statut = self.calculer_statut()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.date} ({self.statut})"
    
    class Meta:
        verbose_name = 'Présence'
        verbose_name_plural = 'Présences'
        unique_together = ['employe', 'date']


# Modèle Congé
class Conge(models.Model):
    TYPES = [
        ('ANNUEL', 'Congé annuel'),
        ('MALADIE', 'Congé maladie'),
        ('MATERNITE', 'Congé maternité'),
        ('SANS_SOLDE', 'Congé sans solde'),
    ]
    
    STATUTS = [
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVE', 'Approuvé'),
        ('REFUSE', 'Refusé'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='conges')
    type_conge = models.CharField(max_length=20, choices=TYPES)
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN_ATTENTE')
    date_demande = models.DateTimeField(auto_now_add=True)
    approuve_par = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=True, related_name='conges_approuves')
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.type_conge}"
    
    class Meta:
        verbose_name = 'Congé'
        verbose_name_plural = 'Congés'


# Modèle Formation
class Formation(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    nombre_participants = models.IntegerField(default=0)
    participants = models.ManyToManyField(Employe, related_name='formations', blank=True)
    est_terminee = models.BooleanField(default=False)
    
    def __str__(self):
        return self.titre
    
    class Meta:
        verbose_name = 'Formation'
        verbose_name_plural = 'Formations'


# Modèle Réclamation
class Reclamation(models.Model):
    STATUTS = [
        ('EN_COURS', 'En cours'),
        ('RESOLUE', 'Résolue'),
        ('FERMEE', 'Fermée'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reclamations')
    sujet = models.CharField(max_length=200)
    description = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN_COURS')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_resolution = models.DateTimeField(null=True, blank=True)
    traite_par = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.sujet} - {self.client.nom}"
    
    class Meta:
        verbose_name = 'Réclamation'
        verbose_name_plural = 'Réclamations'
