# Script d'installation automatique après clonage
# Usage: .\quick_install.ps1

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  INSTALLATION AUTOMATIQUE - PROJET CARREFOUR" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Vérifier si manage.py existe
if (-Not (Test-Path "manage.py")) {
    Write-Host "❌ ERREUR: manage.py non trouvé!" -ForegroundColor Red
    Write-Host "Veuillez exécuter ce script depuis le dossier racine du projet.`n" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dossier du projet détecté`n" -ForegroundColor Green

# Étape 1: Installer les dépendances (optionnel)
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  ÉTAPE 1/4 : Installation des dépendances" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
$installDeps = Read-Host "Installer les dépendances Python ? (o/n) [n]"
if ($installDeps -eq "o" -or $installDeps -eq "O") {
    Write-Host "📦 Installation des dépendances..." -ForegroundColor Cyan
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Erreur lors de l'installation des dépendances" -ForegroundColor Yellow
    }
}

# Étape 2: Migrations
Write-Host "`n============================================================" -ForegroundColor Yellow
Write-Host "  ÉTAPE 2/4 : Création de la base de données" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "🔧 Application des migrations..." -ForegroundColor Cyan
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors des migrations!" -ForegroundColor Red
    exit 1
}

# Étape 3: Création des comptes
Write-Host "`n============================================================" -ForegroundColor Yellow
Write-Host "  ÉTAPE 3/4 : Création des comptes par défaut" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "👥 Création des comptes..." -ForegroundColor Cyan
python setup_after_clone.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de la création des comptes!" -ForegroundColor Red
    exit 1
}

# Étape 4: Test
Write-Host "`n============================================================" -ForegroundColor Yellow
Write-Host "  ÉTAPE 4/4 : Test des connexions" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "🧪 Vérification des comptes..." -ForegroundColor Cyan
python test_connexion.py

# Résumé
Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "  ✅ INSTALLATION TERMINÉE AVEC SUCCÈS!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green

Write-Host "`n📋 Prochaines étapes:`n" -ForegroundColor Cyan
Write-Host "1️⃣  Lancer le serveur:" -ForegroundColor White
Write-Host "   python manage.py runserver`n" -ForegroundColor Yellow

Write-Host "2️⃣  Accéder à l'application:" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000/login/`n" -ForegroundColor Yellow

Write-Host "3️⃣  Se connecter avec:" -ForegroundColor White
Write-Host "   • DG       : dg / DG2025@Admin" -ForegroundColor Yellow
Write-Host "   • DAF      : daf / DAF2025@Admin" -ForegroundColor Yellow
Write-Host "   • RH       : rh / RH2025@Admin" -ForegroundColor Yellow
Write-Host "   • Stock    : stock / Stock2025" -ForegroundColor Yellow
Write-Host "   • Caissier : caissier / Caissier2025" -ForegroundColor Yellow
Write-Host "   • Marketing: marketing / Marketing2025" -ForegroundColor Yellow

Write-Host "`n============================================================`n" -ForegroundColor Green

# Proposer de lancer le serveur
$launchServer = Read-Host "Voulez-vous lancer le serveur maintenant ? (o/n) [o]"
if ($launchServer -eq "" -or $launchServer -eq "o" -or $launchServer -eq "O") {
    Write-Host "`n🚀 Lancement du serveur...`n" -ForegroundColor Cyan
    python manage.py runserver
}
