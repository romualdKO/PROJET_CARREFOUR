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
    est_compte_systeme = models.BooleanField(default=False, help_text="Compte système protégé (DG, DAF, RH) - Ne peut pas être supprimé")
    
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
    
    def is_system_account(self):
        """Vérifie si c'est un compte système protégé (DG, DAF, RH)"""
        return self.est_compte_systeme or self.username in ['dg', 'daf', 'rh']
    
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
    
    reference = models.CharField(max_length=20, unique=True, verbose_name="Référence")
    nom = models.CharField(max_length=200, verbose_name="Nom du produit")
    categorie = models.CharField(max_length=50, choices=CATEGORIES, verbose_name="Catégorie")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix de vente (FCFA)")
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix d'achat (FCFA)")
    stock_actuel = models.IntegerField(default=0, verbose_name="Stock actuel")
    stock_critique = models.IntegerField(default=10, verbose_name="Seuil critique")
    
    # Nouveaux champs pour gestion avancée
    seuil_reapprovisionnement = models.IntegerField(
        default=20,
        verbose_name="Seuil de réapprovisionnement",
        help_text="Quantité en dessous de laquelle il faut réapprovisionner"
    )
    stock_minimum = models.IntegerField(
        default=5,
        verbose_name="Stock minimum",
        help_text="Stock minimum à maintenir"
    )
    stock_maximum = models.IntegerField(
        default=1000,
        verbose_name="Stock maximum",
        help_text="Stock maximum autorisé"
    )
    
    # Relation vers Fournisseur (ForeignKey au lieu de CharField)
    fournisseur_principal = models.ForeignKey(
        'Fournisseur',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Fournisseur principal",
        related_name='produits'
    )
    fournisseur = models.CharField(max_length=200, blank=True, verbose_name="Fournisseur (ancien)")
    
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    code_barre = models.CharField(max_length=50, blank=True, verbose_name="Code-barres")
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN_STOCK')
    est_actif = models.BooleanField(default=True, verbose_name="Produit actif")
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def get_statut(self):
        """Détermine le statut du produit selon son stock"""
        if self.stock_actuel == 0:
            return 'RUPTURE'
        elif self.stock_actuel <= self.stock_critique:
            return 'CRITIQUE'
        return 'EN_STOCK'
    
    def est_en_rupture(self):
        """Vérifie si le produit est en rupture de stock"""
        return self.stock_actuel == 0
    
    def est_critique(self):
        """Vérifie si le stock est critique"""
        return 0 < self.stock_actuel <= self.stock_critique
    
    def calculer_marge(self):
        """Calcule la marge bénéficiaire en pourcentage"""
        if self.prix_achat > 0:
            return ((self.prix_vente - self.prix_achat) / self.prix_achat) * 100
        return 0
    
    @property
    def prix_vente(self):
        """Alias pour prix_unitaire"""
        return self.prix_unitaire
    
    @property
    def marge_beneficiaire(self):
        """Retourne la marge bénéficiaire"""
        return self.calculer_marge()
    
    def besoin_reapprovisionnement(self):
        """Vérifie si le produit a besoin d'être réapprovisionné"""
        return self.stock_actuel <= self.seuil_reapprovisionnement
    
    def quantite_a_commander(self):
        """Calcule la quantité optimale à commander"""
        if self.besoin_reapprovisionnement():
            # Commander jusqu'au stock maximum
            return self.stock_maximum - self.stock_actuel
        return 0
    
    def valeur_stock(self):
        """Calcule la valeur totale du stock (prix d'achat × quantité)"""
        return self.prix_achat * self.stock_actuel
    
    def valeur_stock_vente(self):
        """Calcule la valeur du stock au prix de vente"""
        return self.prix_unitaire * self.stock_actuel
    
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
    
    # Champs de base
    numero_client = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Numéro client")
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True, verbose_name="Adresse")
    ville = models.CharField(max_length=100, default="Abidjan", blank=True)
    date_naissance = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    
    # Champs fidélité
    points_fidelite = models.IntegerField(default=0)
    niveau_fidelite = models.CharField(max_length=20, choices=NIVEAUX_FIDELITE, default='TOUS')
    date_inscription = models.DateTimeField(auto_now_add=True)
    derniere_visite = models.DateTimeField(null=True, blank=True)
    total_achats = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    est_actif = models.BooleanField(default=True, verbose_name="Client actif")
    
    def calculer_niveau(self):
        if self.points_fidelite >= 2000:
            return 'VIP'
        elif self.points_fidelite >= 1000:
            return 'GOLD'
        elif self.points_fidelite >= 500:
            return 'SILVER'
        return 'TOUS'
    
    def save(self, *args, **kwargs):
        # Générer numéro client si vide
        if not self.numero_client:
            last_client = Client.objects.all().order_by('-id').last()
            if last_client and last_client.numero_client:
                try:
                    last_num = int(last_client.numero_client.replace('CLT', ''))
                    self.numero_client = f'CLT{str(last_num + 1).zfill(3)}'
                except:
                    self.numero_client = 'CLT001'
            else:
                self.numero_client = 'CLT001'
        
        self.niveau_fidelite = self.calculer_niveau()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.telephone}"
    
    def get_full_name(self):
        return f"{self.nom} {self.prenom}"
    
    def nombre_achats(self):
        """Retourne le nombre total d'achats validés"""
        return self.transactions.filter(statut='VALIDEE').count()
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


# Modèle Coupon
class Coupon(models.Model):
    TYPE_COUPON = [
        ('GENERIC', 'Générique'),  # Pour tous les clients pendant période promo
        ('SPECIAL', 'Spécial'),    # Généré par CRM pour clients fidèles uniquement
    ]
    
    TYPE_REMISE = [
        ('POURCENTAGE', 'Pourcentage'),
        ('MONTANT', 'Montant fixe'),
    ]
    
    STATUTS = [
        ('ACTIF', 'Actif'),
        ('EXPIRE', 'Expiré'),
        ('DESACTIVE', 'Désactivé'),
    ]
    
    # Informations de base
    code = models.CharField(max_length=20, unique=True, verbose_name="Code coupon")
    type_coupon = models.CharField(max_length=10, choices=TYPE_COUPON, default='GENERIC', verbose_name="Type de coupon")
    type_remise = models.CharField(max_length=12, choices=TYPE_REMISE, default='POURCENTAGE', verbose_name="Type de remise")
    valeur = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valeur")
    description = models.CharField(max_length=200, verbose_name="Description")
    
    # Dates de validité
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    # Limites d'usage
    limite_utilisation = models.IntegerField(default=1, verbose_name="Nombre max d'utilisations par client")
    limite_globale = models.IntegerField(null=True, blank=True, verbose_name="Limite globale d'utilisations")
    nb_utilisations = models.IntegerField(default=0, verbose_name="Nombre d'utilisations actuelles")
    
    # Conditions
    montant_minimum = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Montant minimum d'achat")
    niveau_fidelite_requis = models.CharField(
        max_length=20, 
        choices=Client.NIVEAUX_FIDELITE, 
        blank=True, 
        null=True,
        verbose_name="Niveau de fidélité requis"
    )
    
    # Relations
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='coupons',
        verbose_name="Client (pour coupons spéciaux)"
    )
    cree_par = models.ForeignKey(
        Employe, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='coupons_crees',
        verbose_name="Créé par"
    )
    
    # Statut
    statut = models.CharField(max_length=10, choices=STATUTS, default='ACTIF')
    est_utilise = models.BooleanField(default=False, verbose_name="Utilisé")
    
    def save(self, *args, **kwargs):
        # Générer code si vide
        if not self.code:
            import random
            import string
            if self.type_coupon == 'GENERIC':
                prefix = 'GEN'
            else:
                prefix = 'SPE'
            
            # Générer code unique
            while True:
                random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                code = f'{prefix}{random_part}'
                if not Coupon.objects.filter(code=code).exists():
                    self.code = code
                    break
        
        super().save(*args, **kwargs)
    
    def est_valide(self, client=None, montant_achat=0):
        """Vérifie si le coupon est valide"""
        from datetime import date
        
        # Vérifier dates
        today = date.today()
        if not (self.date_debut <= today <= self.date_fin):
            return False, "Coupon expiré ou pas encore actif"
        
        # Vérifier statut
        if self.statut != 'ACTIF':
            return False, "Coupon désactivé"
        
        # Vérifier si déjà utilisé (pour coupons spéciaux à usage unique)
        if self.type_coupon == 'SPECIAL' and self.est_utilise:
            return False, "Coupon déjà utilisé"
        
        # Vérifier limite globale
        if self.limite_globale and self.nb_utilisations >= self.limite_globale:
            return False, "Limite globale d'utilisations atteinte"
        
        # Vérifier montant minimum
        if montant_achat < self.montant_minimum:
            return False, f"Montant minimum requis: {self.montant_minimum} FCFA"
        
        # Pour coupons spéciaux, vérifier le client
        if self.type_coupon == 'SPECIAL':
            if not client:
                return False, "Client requis pour ce coupon"
            if self.client and self.client != client:
                return False, "Ce coupon n'est pas assigné à ce client"
        
        # Vérifier niveau de fidélité requis
        if self.niveau_fidelite_requis and client:
            niveaux_ordre = ['TOUS', 'SILVER', 'GOLD', 'VIP']
            niveau_client_idx = niveaux_ordre.index(client.niveau_fidelite)
            niveau_requis_idx = niveaux_ordre.index(self.niveau_fidelite_requis)
            
            if niveau_client_idx < niveau_requis_idx:
                return False, f"Niveau {self.niveau_fidelite_requis} requis"
        
        return True, "Coupon valide"
    
    def calculer_remise(self, montant):
        """Calcule le montant de la remise"""
        if self.type_remise == 'POURCENTAGE':
            return montant * (self.valeur / 100)
        else:
            return min(self.valeur, montant)  # Ne pas dépasser le montant total
    
    def marquer_utilise(self):
        """Marque le coupon comme utilisé"""
        self.nb_utilisations += 1
        if self.type_coupon == 'SPECIAL':
            self.est_utilise = True
        
        # Vérifier si limite globale atteinte
        if self.limite_globale and self.nb_utilisations >= self.limite_globale:
            self.statut = 'DESACTIVE'
        
        self.save()
    
    def __str__(self):
        return f"{self.code} - {self.description}"
    
    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        ordering = ['-date_creation']


# Modèle Utilisation Coupon (pour tracking)
class UtilisationCoupon(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='utilisations')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name='coupons_utilises')
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, null=True, blank=True)
    vente = models.ForeignKey('Vente', on_delete=models.CASCADE, null=True, blank=True)
    montant_remise = models.DecimalField(max_digits=10, decimal_places=2)
    date_utilisation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.coupon.code} utilisé le {self.date_utilisation.strftime('%d/%m/%Y')}"
    
    class Meta:
        verbose_name = 'Utilisation de coupon'
        verbose_name_plural = 'Utilisations de coupons'


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
class SessionPresence(models.Model):
    """Enregistre chaque session de connexion/déconnexion d'un employé"""
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField(default=timezone.now)
    heure_connexion = models.TimeField()
    heure_deconnexion = models.TimeField(null=True, blank=True)
    duree_active = models.FloatField(default=0, help_text="Durée en heures")
    
    def calculer_duree_active(self):
        """Calcule la durée active de cette session"""
        if not self.heure_connexion or not self.heure_deconnexion:
            return 0
        
        from datetime import datetime
        connexion = datetime.combine(self.date, self.heure_connexion)
        deconnexion = datetime.combine(self.date, self.heure_deconnexion)
        
        duree_secondes = (deconnexion - connexion).total_seconds()
        return duree_secondes / 3600  # Convertir en heures
    
    def save(self, *args, **kwargs):
        # Calculer automatiquement la durée avant sauvegarde
        if self.heure_deconnexion:
            self.duree_active = self.calculer_duree_active()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.date} ({self.heure_connexion} - {self.heure_deconnexion or 'En cours'})"
    
    class Meta:
        verbose_name = 'Session de Présence'
        verbose_name_plural = 'Sessions de Présence'
        ordering = ['-date', '-heure_connexion']


class Presence(models.Model):
    STATUTS = [
        ('PRESENT', 'Présent'),
        ('RETARD', 'En retard'),
        ('ABSENT', 'Absent'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='presences')
    date = models.DateField(default=timezone.now)
    heure_premiere_arrivee = models.TimeField(null=True, blank=True, help_text="Première connexion de la journée")
    heure_derniere_depart = models.TimeField(null=True, blank=True, help_text="Dernière déconnexion de la journée")
    temps_actif_total = models.FloatField(default=0, help_text="Temps total actif en heures (somme de toutes les sessions)")
    statut = models.CharField(max_length=20, choices=STATUTS, default='ABSENT')
    motif_absence = models.CharField(max_length=200, blank=True)
    tolerance_retard = models.IntegerField(default=60, help_text="Tolérance en minutes avant d'être marqué absent (défaut: 60min)")
    
    def calculer_temps_actif_total(self):
        """Calcule le temps total actif à partir de toutes les sessions de la journée"""
        sessions = SessionPresence.objects.filter(employe=self.employe, date=self.date)
        total = sum(session.duree_active for session in sessions if session.duree_active > 0)
        return total
    
    def calculer_statut(self):
        """
        Calcule le statut basé sur la première arrivée et le temps actif total:
        - ABSENT: Si pas d'arrivée OU arrivée > tolerance_retard (défaut 1h) OU temps actif < 60% des heures requises
        - RETARD: Si arrivée en retard mais temps actif ≥ 60%
        - PRESENT: Si arrivée à l'heure et temps actif ≥ 60%
        """
        if not self.heure_premiere_arrivee:
            return 'ABSENT'
        
        from datetime import datetime, timedelta
        heure_debut = datetime.combine(self.date, self.employe.heure_debut_travail)
        heure_arrivee_dt = datetime.combine(self.date, self.heure_premiere_arrivee)
        
        # Règle 1: Si première arrivée > tolérance (défaut 60 min), c'est ABSENT
        tolerance_absence = timedelta(minutes=self.tolerance_retard)
        if heure_arrivee_dt > heure_debut + tolerance_absence:
            return 'ABSENT'
        
        # Recalculer le temps actif total depuis toutes les sessions
        temps_actif = self.calculer_temps_actif_total()
        
        # Calculer les heures requises et soustraire la pause
        heures_requises = self.calculer_heures_requises()
        temps_actif_net = temps_actif - (self.employe.duree_pause / 60)
        
        # Règle 2: Si temps actif net < 60% des heures requises, c'est ABSENT
        if heures_requises > 0:
            pourcentage = (max(0, temps_actif_net) / heures_requises) * 100
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
        """Calcule les heures effectivement travaillées (temps actif moins la pause)"""
        temps_actif = self.calculer_temps_actif_total()
        pause_heures = self.employe.duree_pause / 60
        
        heures_travaillees = temps_actif - pause_heures
        return max(0, heures_travaillees)  # Ne pas retourner de valeur négative
    
    def calculer_pourcentage_presence(self):
        """Calcule le pourcentage de présence effectif"""
        heures_travaillees = self.calculer_heures_travaillees()
        heures_requises = self.calculer_heures_requises()
        
        if heures_requises > 0:
            return (heures_travaillees / heures_requises) * 100
        return 0
    
    def save(self, *args, **kwargs):
        # Mettre à jour le temps actif total depuis les sessions
        self.temps_actif_total = self.calculer_temps_actif_total()
        
        # Calculer automatiquement le statut avant de sauvegarder
        if self.heure_premiere_arrivee:
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


# ========================================
# MODÈLES GESTION DES STOCKS (Sprint 1)
# ========================================

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
        Employe,
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
        total = self.lignes.aggregate(  # ✅ Utiliser related_name
            total=Sum(F('quantite_commandee') * F('prix_unitaire'))
        )['total']
        return total or 0
    
    def nombre_produits(self):
        """Retourne le nombre de produits différents dans la commande"""
        return self.lignes.count()  # ✅ Utiliser related_name
    
    def delai_restant(self):
        """Calcule le délai restant jusqu'à la livraison prévue"""
        if not self.date_livraison_prevue:
            return None
        from datetime import date
        delta = self.date_livraison_prevue - date.today()
        return delta.days if delta.days >= 0 else 0
    
    def est_en_retard(self):
        """Vérifie si la commande est en retard"""
        if not self.date_livraison_prevue or self.statut == 'LIVREE':
            return False
        from datetime import date
        return date.today() > self.date_livraison_prevue
    
    def liste_produits(self):
        """Retourne la liste des noms de produits commandés"""
        return ', '.join([ligne.produit.nom for ligne in self.lignes.all()[:3]]) + \
               (f' (+{self.lignes.count() - 3} autres)' if self.lignes.count() > 3 else '')


class LigneCommandeFournisseur(models.Model):
    """
    Modèle représentant une ligne d'une commande fournisseur
    """
    commande = models.ForeignKey(
        CommandeFournisseur,
        on_delete=models.CASCADE,
        related_name='lignes',  # ✅ CORRECTION: Permet d'utiliser commande.lignes.all()
        verbose_name="Commande"
    )
    
    produit = models.ForeignKey(
        Produit,
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
        Produit,
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
        Employe,
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
        Produit,
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


# =====================================================
# SPRINT 2 - MODULE CAISSE (POS)
# =====================================================

class Transaction(models.Model):
    """
    Modèle représentant une transaction de vente à la caisse
    """
    STATUT_CHOICES = [
        ('EN_COURS', 'En cours'),
        ('VALIDEE', 'Validée'),
        ('ANNULEE', 'Annulée'),
        ('REMBOURSEE', 'Remboursée'),
    ]
    
    numero_ticket = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Numéro de ticket",
        blank=True
    )
    
    caissier = models.ForeignKey(
        Employe,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name="Caissier",
        limit_choices_to={'role': 'CAISSIER'}
    )
    
    client = models.ForeignKey(
        'Client',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name="Client (fidélité)"
    )
    
    date_transaction = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date et heure"
    )
    
    montant_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Montant total (FCFA)"
    )
    
    montant_remise = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Remise appliquée (FCFA)"
    )
    
    montant_final = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Montant final (FCFA)"
    )
    
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_COURS',
        verbose_name="Statut"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="Notes"
    )
    
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-date_transaction']
    
    def save(self, *args, **kwargs):
        if not self.numero_ticket:
            # Générer numéro de ticket: TKT20251019001
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_ticket = Transaction.objects.filter(
                numero_ticket__startswith=f'TKT{date_str}'
            ).order_by('-numero_ticket').first()
            
            if last_ticket:
                last_num = int(last_ticket.numero_ticket[-3:])
                new_num = f'{last_num + 1:03d}'
            else:
                new_num = '001'
            
            self.numero_ticket = f'TKT{date_str}{new_num}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero_ticket} - {self.caissier.get_full_name()} - {self.montant_final} FCFA"
    
    def calculer_montant_total(self):
        """Calcule le montant total de la transaction"""
        total = sum(ligne.sous_total() for ligne in self.lignes.all())
        self.montant_total = total
        self.montant_final = total - self.montant_remise
        self.save()
    
    def nombre_articles(self):
        """Retourne le nombre total d'articles"""
        return sum(ligne.quantite for ligne in self.lignes.all())
    
    def annuler(self, motif=""):
        """Annule la transaction et restaure le stock"""
        if self.statut == 'VALIDEE':
            # Restaurer le stock pour chaque ligne
            for ligne in self.lignes.all():
                ligne.produit.stock_actuel += ligne.quantite
                ligne.produit.save()
                
                # Créer un mouvement de stock
                MouvementStock.objects.create(
                    produit=ligne.produit,
                    type_mouvement='ENTREE',
                    quantite=ligne.quantite,
                    stock_avant=ligne.produit.stock_actuel - ligne.quantite,
                    stock_apres=ligne.produit.stock_actuel,
                    motif=f"Annulation transaction {self.numero_ticket}",
                    employe=self.caissier
                )
        
        self.statut = 'ANNULEE'
        self.notes = f"{self.notes}\nAnnulée: {motif}" if motif else self.notes
        self.save()


class LigneTransaction(models.Model):
    """
    Modèle représentant une ligne d'article dans une transaction
    """
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='lignes',
        verbose_name="Transaction"
    )
    
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
        verbose_name="Produit"
    )
    
    quantite = models.IntegerField(
        default=1,
        verbose_name="Quantité"
    )
    
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix unitaire (FCFA)"
    )
    
    remise_ligne = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Remise sur la ligne (FCFA)"
    )
    
    class Meta:
        verbose_name = "Ligne de transaction"
        verbose_name_plural = "Lignes de transaction"
    
    def __str__(self):
        return f"{self.produit.nom} x{self.quantite}"
    
    def sous_total(self):
        """Calcule le sous-total de la ligne"""
        return (self.prix_unitaire * self.quantite) - self.remise_ligne
    
    def save(self, *args, **kwargs):
        # Enregistrer le prix actuel du produit si pas déjà défini
        if not self.prix_unitaire:
            self.prix_unitaire = self.produit.prix_unitaire
        super().save(*args, **kwargs)


class TypePaiement(models.Model):
    """
    Modèle représentant un type de paiement accepté
    """
    nom = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nom du type de paiement"
    )
    
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code"
    )
    
    est_actif = models.BooleanField(
        default=True,
        verbose_name="Type actif"
    )
    
    icone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Icône FontAwesome",
        help_text="Ex: fa-money-bill-wave, fa-credit-card"
    )
    
    class Meta:
        verbose_name = "Type de paiement"
        verbose_name_plural = "Types de paiement"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Paiement(models.Model):
    """
    Modèle représentant un paiement effectué pour une transaction
    Une transaction peut avoir plusieurs paiements (paiement mixte)
    """
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='paiements',
        verbose_name="Transaction"
    )
    
    type_paiement = models.ForeignKey(
        TypePaiement,
        on_delete=models.PROTECT,
        verbose_name="Type de paiement"
    )
    
    montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Montant payé (FCFA)"
    )
    
    reference = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Référence",
        help_text="Numéro de transaction CB, Mobile Money, etc."
    )
    
    date_paiement = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date et heure du paiement"
    )
    
    valide = models.BooleanField(
        default=True,
        verbose_name="Paiement validé"
    )
    
    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-date_paiement']
    
    def __str__(self):
        return f"{self.type_paiement.nom} - {self.montant} FCFA"


class SessionCaisse(models.Model):
    """
    Modèle représentant une session de caisse (ouverture/clôture)
    """
    numero_caisse = models.PositiveIntegerField(
        default=1,
        verbose_name="Numéro de caisse",
        help_text="Numéro de la caisse physique (1-10)"
    )
    
    caissier = models.ForeignKey(
        Employe,
        on_delete=models.PROTECT,
        related_name='sessions_caisse',
        verbose_name="Caissier"
    )
    
    date_ouverture = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date et heure d'ouverture"
    )
    
    date_cloture = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date et heure de clôture"
    )
    
    fonds_ouverture = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Fonds d'ouverture (FCFA)"
    )
    
    fonds_cloture_theorique = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Fonds théorique de clôture (FCFA)"
    )
    
    fonds_cloture_reel = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Fonds réel de clôture (FCFA)"
    )
    
    ecart = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Écart (FCFA)"
    )
    
    est_cloturee = models.BooleanField(
        default=False,
        verbose_name="Session clôturée"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="Notes"
    )
    
    class Meta:
        verbose_name = "Session de caisse"
        verbose_name_plural = "Sessions de caisse"
        ordering = ['-date_ouverture']
    
    def __str__(self):
        statut = "Clôturée" if self.est_cloturee else "Ouverte"
        return f"{statut} - {self.caissier.get_full_name()} - {self.date_ouverture.strftime('%d/%m/%Y %H:%M')}"
    
    def calculer_fonds_theorique(self):
        """Calcule le fonds théorique = fonds ouverture + total ventes"""
        total_ventes = sum(
            t.montant_final for t in Transaction.objects.filter(
                caissier=self.caissier,
                date_transaction__gte=self.date_ouverture,
                date_transaction__lte=self.date_cloture if self.date_cloture else timezone.now(),
                statut='VALIDEE'
            )
        )
        return self.fonds_ouverture + total_ventes
    
    def nombre_transactions(self):
        """Retourne le nombre de transactions de la session"""
        return Transaction.objects.filter(
            caissier=self.caissier,
            date_transaction__gte=self.date_ouverture,
            date_transaction__lte=self.date_cloture if self.date_cloture else timezone.now()
        ).count()
    
    def cloturer(self, fonds_reel):
        """Clôture la session de caisse"""
        from django.utils import timezone
        
        self.date_cloture = timezone.now()
        self.fonds_cloture_theorique = self.calculer_fonds_theorique()
        self.fonds_cloture_reel = fonds_reel
        self.ecart = fonds_reel - self.fonds_cloture_theorique
        self.est_cloturee = True
        self.save()


# =====================================================
# SPRINT 3 - MODULE CRM & FIDÉLISATION
# =====================================================

class CarteFidelite(models.Model):
    """
    Carte de fidélité d'un client
    """
    STATUT_CHOICES = [
        ('ACTIVE', 'Active'),
        ('SUSPENDUE', 'Suspendue'),
        ('EXPIREE', 'Expirée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    numero_carte = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Numéro de carte"
    )
    
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name='carte_fidelite',
        verbose_name="Client"
    )
    
    date_emission = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'émission"
    )
    
    date_expiration = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date d'expiration"
    )
    
    solde_points = models.IntegerField(
        default=0,
        verbose_name="Solde de points"
    )
    
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='ACTIVE',
        verbose_name="Statut"
    )
    
    class Meta:
        verbose_name = "Carte de fidélité"
        verbose_name_plural = "Cartes de fidélité"
        ordering = ['-date_emission']
    
    def save(self, *args, **kwargs):
        if not self.numero_carte:
            # Générer numéro: CARD20251019001
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_card = CarteFidelite.objects.filter(
                numero_carte__startswith=f'CARD{date_str}'
            ).order_by('-numero_carte').first()
            
            if last_card:
                last_num = int(last_card.numero_carte[-3:])
                new_num = f'{last_num + 1:03d}'
            else:
                new_num = '001'
            
            self.numero_carte = f'CARD{date_str}{new_num}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero_carte} - {self.client.get_full_name()} ({self.solde_points} pts)"
    
    def crediter_points(self, points, motif="", transaction=None):
        """Crédite des points sur la carte"""
        self.solde_points += points
        self.save()
        
        OperationFidelite.objects.create(
            carte=self,
            type_operation='CREDIT',
            points=points,
            motif=motif,
            transaction=transaction
        )
    
    def debiter_points(self, points, motif=""):
        """Débite des points de la carte"""
        if self.solde_points >= points:
            self.solde_points -= points
            self.save()
            
            OperationFidelite.objects.create(
                carte=self,
                type_operation='DEBIT',
                points=points,
                motif=motif
            )
            return True
        return False


class OperationFidelite(models.Model):
    """
    Historique des opérations de points de fidélité
    """
    TYPE_CHOICES = [
        ('CREDIT', 'Crédit'),
        ('DEBIT', 'Débit'),
        ('AJUSTEMENT', 'Ajustement'),
        ('EXPIRATION', 'Expiration'),
    ]
    
    carte = models.ForeignKey(
        CarteFidelite,
        on_delete=models.CASCADE,
        related_name='operations',
        verbose_name="Carte"
    )
    
    type_operation = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Type d'opération"
    )
    
    points = models.IntegerField(
        verbose_name="Points"
    )
    
    solde_avant = models.IntegerField(
        verbose_name="Solde avant",
        default=0
    )
    
    solde_apres = models.IntegerField(
        verbose_name="Solde après",
        default=0
    )
    
    motif = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Motif"
    )
    
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Transaction associée"
    )
    
    date_operation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de l'opération"
    )
    
    class Meta:
        verbose_name = "Opération fidélité"
        verbose_name_plural = "Opérations fidélité"
        ordering = ['-date_operation']
    
    def __str__(self):
        return f"{self.get_type_operation_display()} - {self.points} pts - {self.carte.numero_carte}"


class Campagne(models.Model):
    """
    Campagne marketing/promotionnelle
    """
    TYPE_CHOICES = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('NOTIFICATION', 'Notification Push'),
        ('PROMOTION', 'Promotion'),
    ]
    
    STATUT_CHOICES = [
        ('BROUILLON', 'Brouillon'),
        ('PROGRAMMEE', 'Programmée'),
        ('EN_COURS', 'En cours'),
        ('TERMINEE', 'Terminée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    titre = models.CharField(
        max_length=200,
        verbose_name="Titre"
    )
    
    description = models.TextField(
        verbose_name="Description"
    )
    
    type_campagne = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Type"
    )
    
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='BROUILLON',
        verbose_name="Statut"
    )
    
    date_debut = models.DateTimeField(
        verbose_name="Date de début"
    )
    
    date_fin = models.DateTimeField(
        verbose_name="Date de fin"
    )
    
    segment_cible = models.ForeignKey(
        'SegmentClient',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Segment cible"
    )
    
    message = models.TextField(
        verbose_name="Message"
    )
    
    nb_destinataires = models.IntegerField(
        default=0,
        verbose_name="Nombre de destinataires"
    )
    
    nb_envoyes = models.IntegerField(
        default=0,
        verbose_name="Nombre envoyés"
    )
    
    nb_ouverts = models.IntegerField(
        default=0,
        verbose_name="Nombre ouverts"
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True
    )
    
    creee_par = models.ForeignKey(
        Employe,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Créée par"
    )
    
    class Meta:
        verbose_name = "Campagne"
        verbose_name_plural = "Campagnes"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.titre} ({self.get_type_campagne_display()})"
    
    def taux_ouverture(self):
        """Calcule le taux d'ouverture"""
        if self.nb_envoyes > 0:
            return (self.nb_ouverts / self.nb_envoyes) * 100
        return 0


class SegmentClient(models.Model):
    """
    Segment de clientèle pour le ciblage marketing
    """
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom du segment"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    
    # Critères de segmentation
    niveau_fidelite = models.CharField(
        max_length=20,
        choices=Client.NIVEAUX_FIDELITE,
        blank=True,
        verbose_name="Niveau de fidélité"
    )
    
    montant_achats_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Montant achats minimum"
    )
    
    montant_achats_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Montant achats maximum"
    )
    
    date_derniere_visite_avant = models.DateField(
        null=True,
        blank=True,
        verbose_name="Dernière visite avant le"
    )
    
    est_actif = models.BooleanField(
        default=True,
        verbose_name="Segment actif"
    )
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Segment client"
        verbose_name_plural = "Segments clients"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
    
    def get_clients(self):
        """Retourne les clients correspondant au segment"""
        queryset = Client.objects.filter(est_actif=True)
        
        if self.niveau_fidelite:
            queryset = queryset.filter(niveau_fidelite=self.niveau_fidelite)
        
        if self.montant_achats_min:
            queryset = queryset.filter(total_achats__gte=self.montant_achats_min)
        
        if self.montant_achats_max:
            queryset = queryset.filter(total_achats__lte=self.montant_achats_max)
        
        if self.date_derniere_visite_avant:
            queryset = queryset.filter(derniere_visite__lt=self.date_derniere_visite_avant)
        
        return queryset
    
    def nombre_clients(self):
        """Compte le nombre de clients dans ce segment"""
        return self.get_clients().count()


# ==================== SCÉNARIO 8.1.3 : PLANNING & CONGÉS ====================

class Planning(models.Model):
    """Planning de travail des employés"""
    
    POSTES = [
        ('CAISSE', 'Caisse'),
        ('RAYON', 'Rayon'),
        ('MAGASIN', 'Magasin'),
        ('SECURITE', 'Sécurité'),
        ('RECEPTION', 'Réception Marchandises'),
        ('SERVICE_CLIENT', 'Service Client'),
    ]
    
    CRENEAUX = [
        ('MATIN', 'Matin (6h-14h)'),
        ('APRES_MIDI', 'Après-midi (14h-22h)'),
        ('NUIT', 'Nuit (22h-6h)'),
    ]
    
    STATUTS = [
        ('PRESENT', 'Présent'),
        ('CONGE', 'En congé'),
        ('ARRET_MALADIE', 'Arrêt maladie'),
        ('ABSENT', 'Absent'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='plannings')
    date = models.DateField()
    poste = models.CharField(max_length=20, choices=POSTES, default='CAISSE')
    creneau = models.CharField(max_length=20, choices=CRENEAUX, default='MATIN')
    statut = models.CharField(max_length=20, choices=STATUTS, default='PRESENT')
    heures_prevues = models.DecimalField(max_digits=4, decimal_places=2, default=8.0)
    heures_reelles = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, help_text="Notes ou remarques")
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Planning"
        verbose_name_plural = "Plannings"
        ordering = ['-date', 'employe']
        unique_together = ['employe', 'date', 'creneau']
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.date} ({self.get_creneau_display()})"
    
    def get_horaires(self):
        """Retourne les horaires du créneau"""
        horaires = {
            'MATIN': '06:00 - 14:00',
            'APRES_MIDI': '14:00 - 22:00',
            'NUIT': '22:00 - 06:00',
        }
        return horaires.get(self.creneau, '')


class DemandeConge(models.Model):
    """Demandes de congé des employés"""
    
    TYPES_CONGE = [
        ('CONGE_PAYE', 'Congé payé'),
        ('CONGE_MALADIE', 'Congé maladie'),
        ('RTT', 'RTT (Récupération)'),
        ('CONGE_MATERNITE', 'Congé maternité'),
        ('CONGE_PATERNITE', 'Congé paternité'),
        ('ABSENCE_AUTORISEE', 'Absence autorisée'),
    ]
    
    STATUTS = [
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVE', 'Approuvé'),
        ('REFUSE', 'Refusé'),
        ('ANNULE', 'Annulé'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='demandes_conge')
    type_conge = models.CharField(max_length=20, choices=TYPES_CONGE, default='CONGE_PAYE')
    date_debut = models.DateField()
    date_fin = models.DateField()
    nb_jours = models.IntegerField(default=1)
    motif = models.TextField(help_text="Raison de la demande")
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN_ATTENTE')
    reponse_manager = models.TextField(blank=True, help_text="Commentaire du manager")
    approuve_par = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=True, related_name='demandes_conge_approuvees')
    date_reponse = models.DateTimeField(null=True, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Demande de congé"
        verbose_name_plural = "Demandes de congé"
        ordering = ['-cree_le']
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.get_type_conge_display()} ({self.date_debut} au {self.date_fin})"
    
    def save(self, *args, **kwargs):
        # Calculer automatiquement le nombre de jours ouvrés
        if self.date_debut and self.date_fin:
            from datetime import timedelta
            nb_jours = 0
            date_courante = self.date_debut
            while date_courante <= self.date_fin:
                if date_courante.weekday() < 5:  # Lundi à Vendredi
                    nb_jours += 1
                date_courante += timedelta(days=1)
            self.nb_jours = nb_jours
        
        super().save(*args, **kwargs)
    
    def get_statut_badge_class(self):
        """Retourne la classe CSS pour le badge de statut"""
        classes = {
            'EN_ATTENTE': 'warning',
            'APPROUVE': 'success',
            'REFUSE': 'danger',
            'ANNULE': 'secondary',
        }
        return classes.get(self.statut, 'secondary')


class Pointage(models.Model):
    """Pointages entrée/sortie des employés"""
    
    TYPES_JOURNEE = [
        ('NORMAL', 'Journée normale'),
        ('SUPPLEMENTAIRE', 'Heures supplémentaires'),
        ('NUIT', 'Travail de nuit'),
        ('FERIE', 'Jour férié'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='pointages')
    date = models.DateField(default=timezone.now)
    heure_entree = models.TimeField(null=True, blank=True)
    heure_sortie = models.TimeField(null=True, blank=True)
    heures_travaillees = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    type_journee = models.CharField(max_length=20, choices=TYPES_JOURNEE, default='NORMAL')
    retard_minutes = models.IntegerField(default=0, help_text="Retard en minutes")
    validee = models.BooleanField(default=False, help_text="Validé par le responsable")
    notes = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pointage"
        verbose_name_plural = "Pointages"
        ordering = ['-date', '-heure_entree']
        unique_together = ['employe', 'date']
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.date}"
    
    def calculer_heures_travaillees(self):
        """Calcule les heures travaillées"""
        if self.heure_entree and self.heure_sortie:
            from datetime import datetime, date
            entree = datetime.combine(date.today(), self.heure_entree)
            sortie = datetime.combine(date.today(), self.heure_sortie)
            
            # Si sortie < entrée, c'est le lendemain
            if sortie < entree:
                from datetime import timedelta
                sortie += timedelta(days=1)
            
            delta = sortie - entree
            self.heures_travaillees = round(delta.total_seconds() / 3600, 2)
        return self.heures_travaillees
    
    def calculer_retard(self):
        """Calcule le retard en minutes"""
        if self.heure_entree:
            from datetime import datetime, date
            heure_prevue = self.employe.heure_debut_travail
            entree_dt = datetime.combine(date.today(), self.heure_entree)
            prevue_dt = datetime.combine(date.today(), heure_prevue)
            
            if entree_dt > prevue_dt:
                delta = entree_dt - prevue_dt
                self.retard_minutes = int(delta.total_seconds() / 60)
            else:
                self.retard_minutes = 0
        return self.retard_minutes
    
    def save(self, *args, **kwargs):
        # Calculer automatiquement heures et retard
        if self.heure_sortie:
            self.calculer_heures_travaillees()
        if self.heure_entree:
            self.calculer_retard()
        super().save(*args, **kwargs)


class Notification(models.Model):
    """Notifications pour les employés"""
    
    TYPES_NOTIFICATION = [
        ('DEMANDE_CONGE', 'Demande de congé'),
        ('REPONSE_CONGE', 'Réponse à demande de congé'),
        ('PLANNING_MAJ', 'Mise à jour du planning'),
        ('POINTAGE', 'Pointage'),
        ('ALERTE_STOCK', 'Alerte stock'),
        ('VENTE', 'Vente'),
        ('AUTRE', 'Autre'),
    ]
    
    destinataire = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    type_notif = models.CharField(max_length=20, choices=TYPES_NOTIFICATION, default='AUTRE')
    lue = models.BooleanField(default=False)
    lien = models.CharField(max_length=500, blank=True, help_text="Lien vers la page concernée")
    cree_le = models.DateTimeField(auto_now_add=True)
    lue_le = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-cree_le']
    
    def __str__(self):
        return f"{self.destinataire.get_full_name()} - {self.titre}"
    
    def marquer_comme_lue(self):
        """Marque la notification comme lue"""
        if not self.lue:
            self.lue = True
            self.lue_le = timezone.now()
            self.save()
    
    def get_icone(self):
        """Retourne l'icône correspondant au type"""
        icones = {
            'DEMANDE_CONGE': '🏖️',
            'REPONSE_CONGE': '✅',
            'PLANNING_MAJ': '📅',
            'POINTAGE': '⏰',
            'ALERTE_STOCK': '⚠️',
            'VENTE': '🛒',
            'AUTRE': '📌',
        }
        return icones.get(self.type_notif, '📌')


class Absence(models.Model):
    """Enregistrement des absences des employés"""
    
    TYPE_ABSENCE_CHOICES = [
        ('MALADIE', 'Maladie'),
        ('CONGE', 'Congé'),
        ('ABSENCE_INJUSTIFIEE', 'Absence injustifiée'),
        ('RETARD', 'Retard'),
        ('AUTRE', 'Autre'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='absences')
    date = models.DateField()
    type_absence = models.CharField(max_length=50, choices=TYPE_ABSENCE_CHOICES, default='AUTRE')
    justifiee = models.BooleanField(default=False)
    commentaire = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Absence"
        verbose_name_plural = "Absences"
        ordering = ['-date']
        unique_together = ['employe', 'date']
    
    def __str__(self):
        return f"{self.employe.nom} - {self.date} - {self.get_type_absence_display()}"

