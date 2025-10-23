# 🎯 GUIDE D'IMPLÉMENTATION - FONCTIONNALITÉS MANQUANTES

## FONCTIONNALITÉ 1 : Affichage Réductions/Fidélité AVANT Paiement

### Objectif
Afficher en temps réel dans l'interface caisse :
- Le niveau de fidélité du client
- Les remises applicables
- Le calcul détaillé avant/après remises

### Fichiers à modifier

#### 1. `templates/caisse/pos_interface.html`

**Ajout après la section du panier** :

```html
<!-- Section Réductions et Fidélité -->
<div id="section-reductions" class="card mb-3" style="display: none;">
    <div class="card-header bg-success text-white">
        <h5 class="mb-0">🎁 Réductions Applicables</h5>
    </div>
    <div class="card-body">
        <!-- Info Client -->
        <div class="alert alert-info mb-3">
            <h6>💳 CLIENT IDENTIFIÉ</h6>
            <p class="mb-1"><strong>Nom :</strong> <span id="client-nom">-</span></p>
            <p class="mb-1"><strong>Carte :</strong> <span id="client-niveau">-</span> #<span id="client-numero">-</span></p>
            <p class="mb-0"><strong>Points :</strong> <span id="client-points">0</span> pts</p>
        </div>

        <!-- Remises -->
        <div class="row">
            <div class="col-md-6">
                <div class="card bg-light">
                    <div class="card-body">
                        <h6>🏆 Remise Fidélité</h6>
                        <h3 class="text-success mb-0" id="remise-fidelite-pct">0%</h3>
                        <small class="text-muted" id="remise-fidelite-montant">0 FCFA</small>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card bg-light">
                    <div class="card-body">
                        <h6>🎉 Remise Promotion</h6>
                        <h3 class="text-warning mb-0" id="remise-promo-pct">0%</h3>
                        <small class="text-muted" id="remise-promo-montant">0 FCFA</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Calcul Détaillé -->
        <div class="mt-3 p-3" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px;">
            <div class="d-flex justify-content-between text-white mb-2">
                <span>Sous-total :</span>
                <strong id="calc-soustotal">0 FCFA</strong>
            </div>
            <div class="d-flex justify-content-between text-white mb-2">
                <span>Remise Fidélité :</span>
                <strong id="calc-remise-fidelite">-0 FCFA</strong>
            </div>
            <div class="d-flex justify-content-between text-white mb-2">
                <span>Remise Promotion :</span>
                <strong id="calc-remise-promo">-0 FCFA</strong>
            </div>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <div class="d-flex justify-content-between text-white">
                <h5>TOTAL À PAYER :</h5>
                <h4 id="calc-total-final">0 FCFA</h4>
            </div>
            <div class="text-center mt-2">
                <span class="badge bg-light text-dark">
                    💵 Vous économisez : <span id="calc-economie">0 FCFA</span>
                </span>
            </div>
        </div>
    </div>
</div>
```

#### 2. Ajouter JavaScript pour calcul en temps réel

**Dans le même fichier, section `<script>` :**

```javascript
// Fonction pour calculer les remises
function calculerRemises() {
    const clientId = document.getElementById('client_id').value;
    if (!clientId) {
        document.getElementById('section-reductions').style.display = 'none';
        return;
    }

    // Récupérer les infos du client via AJAX
    fetch(`/caisse/client-info/${clientId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                afficherReductions(data.client, data.remises);
            }
        })
        .catch(error => console.error('Erreur:', error));
}

function afficherReductions(client, remises) {
    // Afficher la section
    document.getElementById('section-reductions').style.display = 'block';

    // Info client
    document.getElementById('client-nom').textContent = client.nom_complet;
    document.getElementById('client-niveau').textContent = client.niveau_fidelite;
    document.getElementById('client-numero').textContent = client.numero_carte;
    document.getElementById('client-points').textContent = client.points;

    // Remises
    document.getElementById('remise-fidelite-pct').textContent = remises.fidelite_pct + '%';
    document.getElementById('remise-fidelite-montant').textContent = formatMontant(remises.fidelite_montant) + ' FCFA';
    document.getElementById('remise-promo-pct').textContent = remises.promo_pct + '%';
    document.getElementById('remise-promo-montant').textContent = formatMontant(remises.promo_montant) + ' FCFA';

    // Calcul détaillé
    document.getElementById('calc-soustotal').textContent = formatMontant(remises.sous_total) + ' FCFA';
    document.getElementById('calc-remise-fidelite').textContent = '-' + formatMontant(remises.fidelite_montant) + ' FCFA';
    document.getElementById('calc-remise-promo').textContent = '-' + formatMontant(remises.promo_montant) + ' FCFA';
    document.getElementById('calc-total-final').textContent = formatMontant(remises.total_final) + ' FCFA';
    document.getElementById('calc-economie').textContent = formatMontant(remises.economie_totale) + ' FCFA';
}

function formatMontant(montant) {
    return parseFloat(montant).toLocaleString('fr-FR', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    });
}

// Appeler calculerRemises() après identification client et après chaque ajout de produit
document.getElementById('client_id').addEventListener('change', calculerRemises);
```

#### 3. Créer nouvelle vue `CarrefourApp/views.py`

```python
@login_required
def caisse_client_info(request, client_id):
    """Retourne les infos client et calcul des remises"""
    try:
        client = Client.objects.get(id=client_id)
        
        # Transaction en cours
        transaction = Transaction.objects.filter(
            caissier=request.user,
            statut='EN_COURS'
        ).first()
        
        if not transaction:
            return JsonResponse({'success': False, 'error': 'Pas de transaction'})
        
        # Calculer sous-total
        sous_total = transaction.montant_total
        
        # Remise fidélité selon niveau
        remise_fidelite_pct = {
            'TOUS': 0,
            'SILVER': 3,
            'GOLD': 5,
            'VIP': 10
        }.get(client.niveau_fidelite, 0)
        
        remise_fidelite_montant = (sous_total * Decimal(remise_fidelite_pct) / 100)
        
        # Remise promotion (≥40,000 = -5%)
        remise_promo_pct = 5 if sous_total >= 40000 else 0
        remise_promo_montant = (sous_total * Decimal(remise_promo_pct) / 100)
        
        # Total après remises
        total_final = sous_total - remise_fidelite_montant - remise_promo_montant
        economie_totale = remise_fidelite_montant + remise_promo_montant
        
        return JsonResponse({
            'success': True,
            'client': {
                'nom_complet': client.get_nom_complet(),
                'niveau_fidelite': client.niveau_fidelite,
                'numero_carte': client.numero_carte,
                'points': client.points_fidelite
            },
            'remises': {
                'fidelite_pct': remise_fidelite_pct,
                'fidelite_montant': float(remise_fidelite_montant),
                'promo_pct': remise_promo_pct,
                'promo_montant': float(remise_promo_montant),
                'sous_total': float(sous_total),
                'total_final': float(total_final),
                'economie_totale': float(economie_totale)
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
```

#### 4. Ajouter route `CarrefourApp/urls.py`

```python
path('caisse/client-info/<int:client_id>/', views.caisse_client_info, name='caisse_client_info'),
```

---

## FONCTIONNALITÉ 2 : Génération Ticket PDF

### Étape 1 : Installer ReportLab

```bash
pip install reportlab
```

### Étape 2 : Créer `CarrefourApp/utils/ticket_pdf.py`

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, grey
from datetime import datetime
from django.conf import settings
import os

def generer_ticket_pdf(transaction):
    """
    Génère un ticket de caisse en PDF
    Args:
        transaction: Instance de Transaction
    Returns:
        str: Chemin du fichier PDF généré
    """
    
    # Créer dossier tickets si n'existe pas
    tickets_dir = os.path.join(settings.MEDIA_ROOT, 'tickets')
    os.makedirs(tickets_dir, exist_ok=True)
    
    # Nom du fichier
    filename = f"ticket_{transaction.numero_ticket}.pdf"
    filepath = os.path.join(tickets_dir, filename)
    
    # Créer le PDF (format ticket: 80mm x variable)
    width = 80 * mm
    height = 297 * mm  # A4 height
    c = canvas.Canvas(filepath, pagesize=(width, height))
    
    # Marges
    margin = 5 * mm
    y = height - margin
    line_height = 5 * mm
    
    # ========== EN-TÊTE ==========
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, y, "CARREFOUR ESATIC")
    y -= line_height
    
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, y, "Abidjan, Côte d'Ivoire")
    y -= line_height
    c.drawCentredString(width / 2, y, "Tel: +225 XX XX XX XX")
    y -= line_height * 1.5
    
    # Ligne de séparation
    c.line(margin, y, width - margin, y)
    y -= line_height
    
    # ========== INFOS TICKET ==========
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, f"TICKET N°: {transaction.numero_ticket}")
    y -= line_height
    
    c.setFont("Helvetica", 8)
    date_str = transaction.date_transaction.strftime("%d/%m/%Y")
    heure_str = transaction.date_transaction.strftime("%H:%M:%S")
    c.drawString(margin, y, f"Date: {date_str}  Heure: {heure_str}")
    y -= line_height
    
    c.drawString(margin, y, f"Caissier: {transaction.caissier.get_full_name()}")
    y -= line_height
    c.drawString(margin, y, f"Caisse: #{transaction.session.numero_caisse if transaction.session else 'N/A'}")
    y -= line_height * 1.5
    
    # ========== CLIENT ==========
    if transaction.client:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin, y, "CLIENT:")
        y -= line_height
        
        c.setFont("Helvetica", 8)
        c.drawString(margin, y, f"{transaction.client.get_nom_complet()}")
        y -= line_height
        c.drawString(margin, y, f"Carte: {transaction.client.niveau_fidelite} #{transaction.client.numero_carte}")
        y -= line_height
        c.drawString(margin, y, f"Points: {transaction.client.points_fidelite} pts")
        y -= line_height * 1.5
    
    # Ligne de séparation
    c.line(margin, y, width - margin, y)
    y -= line_height
    
    # ========== PRODUITS ==========
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, y, "PRODUITS")
    y -= line_height
    c.line(margin, y, width - margin, y)
    y -= line_height
    
    c.setFont("Helvetica", 7)
    for ligne in transaction.lignes.all():
        # Nom du produit
        c.drawString(margin, y, ligne.produit.nom[:30])  # Limiter à 30 car
        y -= line_height * 0.8
        
        # Prix unitaire x Quantité = Total
        detail = f"  {ligne.prix_unitaire:,.0f} x {ligne.quantite}"
        c.drawString(margin, y, detail)
        
        montant = f"{ligne.montant_ligne:,.0f} FCFA"
        c.drawRightString(width - margin, y, montant)
        y -= line_height * 1.2
    
    # Ligne de séparation
    c.line(margin, y, width - margin, y)
    y -= line_height
    
    # ========== TOTAUX ==========
    c.setFont("Helvetica", 8)
    
    # Sous-total
    c.drawString(margin, y, "SOUS-TOTAL:")
    c.drawRightString(width - margin, y, f"{transaction.montant_total:,.0f} FCFA")
    y -= line_height
    
    # Remises
    if transaction.remise > 0:
        c.drawString(margin, y, f"Remise (-{transaction.pourcentage_remise}%):")
        c.drawRightString(width - margin, y, f"-{transaction.remise:,.0f} FCFA")
        y -= line_height
    
    # TVA
    if hasattr(transaction, 'montant_tva'):
        c.drawString(margin, y, "TVA (18%):")
        c.drawRightString(width - margin, y, f"{transaction.montant_tva:,.0f} FCFA")
        y -= line_height
    
    # Ligne de séparation
    c.line(margin, y, width - margin, y)
    y -= line_height
    
    # TOTAL
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, "TOTAL À PAYER:")
    c.drawRightString(width - margin, y, f"{transaction.montant_final:,.0f} FCFA")
    y -= line_height * 1.5
    
    # ========== PAIEMENTS ==========
    for paiement in transaction.paiements.all():
        c.setFont("Helvetica", 8)
        c.drawString(margin, y, f"{paiement.type_paiement.nom.upper()}:")
        c.drawRightString(width - margin, y, f"{paiement.montant:,.0f} FCFA")
        y -= line_height
    
    # Monnaie rendue
    montant_paye = sum(p.montant for p in transaction.paiements.all())
    if montant_paye > transaction.montant_final:
        monnaie = montant_paye - transaction.montant_final
        c.drawString(margin, y, "MONNAIE RENDUE:")
        c.drawRightString(width - margin, y, f"{monnaie:,.0f} FCFA")
        y -= line_height * 1.5
    
    # Ligne de séparation
    c.line(margin, y, width - margin, y)
    y -= line_height
    
    # ========== POINTS FIDÉLITÉ ==========
    if transaction.client:
        points_gagnes = int(transaction.montant_final / 1000)  # 1pt = 1000 FCFA
        nouveau_solde = transaction.client.points_fidelite
        
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(width / 2, y, f"🎁 POINTS GAGNÉS: +{points_gagnes} pts")
        y -= line_height
        c.setFont("Helvetica", 8)
        c.drawCentredString(width / 2, y, f"Nouveau solde: {nouveau_solde} pts")
        y -= line_height * 1.5
    
    # ========== PIED DE PAGE ==========
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width / 2, y, "Merci de votre visite !")
    y -= line_height
    c.drawCentredString(width / 2, y, "À bientôt chez CARREFOUR")
    
    # Sauvegarder le PDF
    c.save()
    
    return filepath
```

### Étape 3 : Créer vue pour télécharger le PDF

**Dans `CarrefourApp/views.py` :**

```python
from django.http import FileResponse
from .utils.ticket_pdf import generer_ticket_pdf

@login_required
def telecharger_ticket_pdf(request, transaction_id):
    """Génère et télécharge le ticket PDF"""
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        
        # Vérifier autorisation
        if request.user != transaction.caissier and request.user.role not in ['MANAGER', 'ADMIN', 'DG']:
            messages.error(request, "Accès refusé")
            return redirect('pos_interface')
        
        # Générer le PDF
        filepath = generer_ticket_pdf(transaction)
        
        # Retourner le fichier
        response = FileResponse(open(filepath, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="ticket_{transaction.numero_ticket}.pdf"'
        
        return response
        
    except Transaction.DoesNotExist:
        messages.error(request, "Transaction introuvable")
        return redirect('pos_interface')
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('pos_interface')
```

### Étape 4 : Ajouter route

**Dans `CarrefourApp/urls.py` :**

```python
path('caisse/ticket/<int:transaction_id>/pdf/', views.telecharger_ticket_pdf, name='telecharger_ticket_pdf'),
```

### Étape 5 : Modifier `pos_valider_vente` pour retourner URL du PDF

**Dans la réponse JSON après validation :**

```python
return JsonResponse({
    'success': True,
    'numero_ticket': transaction.numero_ticket,
    'montant_final': float(transaction.montant_final),
    'montant_paye': float(montant_paye),
    'monnaie': float(monnaie),
    'pdf_url': f'/caisse/ticket/{transaction.id}/pdf/',  # AJOUT
    'message': 'Vente enregistrée avec succès!'
})
```

### Étape 6 : Ouvrir automatiquement le PDF après paiement

**Dans le JavaScript de `pos_interface.html` :**

```javascript
// Après validation réussie
if (data.success) {
    alert(data.message);
    
    // Ouvrir le PDF dans un nouvel onglet
    if (data.pdf_url) {
        window.open(data.pdf_url, '_blank');
    }
    
    // Réinitialiser l'interface
    location.reload();
}
```

---

## 🎯 RÉSUMÉ DE L'IMPLÉMENTATION

### Fonctionnalité 1 : Affichage Réductions
- ✅ Section HTML dans pos_interface.html
- ✅ JavaScript pour calcul en temps réel
- ✅ Vue `caisse_client_info` pour API
- ✅ Route `/caisse/client-info/<id>/`

### Fonctionnalité 2 : Ticket PDF
- ✅ Installation ReportLab
- ✅ Fonction `generer_ticket_pdf()`
- ✅ Vue `telecharger_ticket_pdf`
- ✅ Route `/caisse/ticket/<id>/pdf/`
- ✅ Ouverture automatique après paiement

---

## ⚠️ ATTENTION

Ces fonctionnalités nécessitent :
1. Les templates doivent être mis à jour
2. Les routes doivent être ajoutées
3. Le JavaScript doit être testé
4. ReportLab doit être installé

**Temps estimé total** : 3-5 heures
