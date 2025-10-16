# 🤝 Guide de Contribution - SuperMarché Plus

Merci de votre intérêt pour contribuer au projet SuperMarché Plus ! Ce guide vous aidera à contribuer efficacement.

## 📋 Table des Matières

- [Code de Conduite](#code-de-conduite)
- [Comment Contribuer](#comment-contribuer)
- [Processus de Développement](#processus-de-développement)
- [Standards de Code](#standards-de-code)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)
- [Signaler des Bugs](#signaler-des-bugs)
- [Proposer des Fonctionnalités](#proposer-des-fonctionnalités)

## 📜 Code de Conduite

En participant à ce projet, vous acceptez de :
- Être respectueux et professionnel
- Accepter les critiques constructives
- Collaborer de bonne foi
- Respecter les décisions des mainteneurs

## 🚀 Comment Contribuer

### 1. Fork et Clone

```bash
# Fork le projet sur GitHub, puis :
git clone https://github.com/VOTRE-USERNAME/PROJET_CARREFOUR.git
cd PROJET_CARREFOUR
```

### 2. Configurer l'Environnement

```bash
# Créer l'environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données
python manage.py migrate
python init_default_accounts.py
```

### 3. Créer une Branche

```bash
# Toujours partir de main à jour
git checkout main
git pull origin main

# Créer votre branche
git checkout -b feature/ma-fonctionnalite
# ou
git checkout -b fix/mon-correctif
```

### 4. Faire vos Modifications

- Écrire du code propre et documenté
- Suivre les standards de code Python (PEP 8)
- Ajouter des tests si possible
- Mettre à jour la documentation si nécessaire

### 5. Commit et Push

```bash
# Ajouter les fichiers modifiés
git add .

# Commit avec un message descriptif
git commit -m "✨ Add nouvelle fonctionnalité"

# Pousser vers votre fork
git push origin feature/ma-fonctionnalite
```

### 6. Créer une Pull Request

1. Aller sur GitHub
2. Cliquer sur "New Pull Request"
3. Sélectionner votre branche
4. Remplir le template de PR
5. Soumettre pour review

## 🔄 Processus de Développement

### Workflow Git

```
main (production)
  ↓
develop (développement)
  ↓
feature/* (nouvelles fonctionnalités)
fix/* (corrections de bugs)
hotfix/* (corrections urgentes)
```

### Branches

| Type | Nom | Description | Exemple |
|------|-----|-------------|---------|
| **Feature** | `feature/*` | Nouvelle fonctionnalité | `feature/export-excel` |
| **Fix** | `fix/*` | Correction de bug | `fix/presence-calculation` |
| **Hotfix** | `hotfix/*` | Correction urgente | `hotfix/security-patch` |
| **Docs** | `docs/*` | Documentation | `docs/update-readme` |
| **Test** | `test/*` | Ajout de tests | `test/presence-tests` |
| **Refactor** | `refactor/*` | Refactoring | `refactor/views-cleanup` |

## 📝 Standards de Code

### Python / Django

Suivre **PEP 8** pour Python :

```python
# ✅ BON
def calculer_heures_travaillees(self):
    """Calcule le nombre d'heures travaillées."""
    if not self.heure_arrivee or not self.heure_depart:
        return 0
    
    total = (datetime.combine(date.today(), self.heure_depart) - 
             datetime.combine(date.today(), self.heure_arrivee))
    return (total.seconds / 3600) - (self.employe.duree_pause / 60)

# ❌ MAUVAIS
def calc_hrs(self):
    if not self.heure_arrivee or not self.heure_depart:return 0
    total=(datetime.combine(date.today(),self.heure_depart)-datetime.combine(date.today(),self.heure_arrivee))
    return(total.seconds/3600)-(self.employe.duree_pause/60)
```

### HTML / Templates Django

```html
<!-- ✅ BON -->
<div class="card">
    <div class="card-header">
        <h2>{{ titre }}</h2>
    </div>
    <div class="card-body">
        {% for item in items %}
            <p>{{ item.nom }}</p>
        {% empty %}
            <p>Aucun élément trouvé.</p>
        {% endfor %}
    </div>
</div>

<!-- ❌ MAUVAIS -->
<div class="card"><div class="card-header"><h2>{{ titre }}</h2></div><div class="card-body">{% for item in items %}<p>{{ item.nom }}</p>{% endfor %}</div></div>
```

### CSS

```css
/* ✅ BON */
.stat-card {
    padding: 20px;
    border-radius: 12px;
    background: linear-gradient(135deg, #2563EB, #1E40AF);
    color: white;
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
}

/* ❌ MAUVAIS */
.stat-card{padding:20px;border-radius:12px;background:linear-gradient(135deg,#2563EB,#1E40AF);color:white;}
```

## 💬 Commit Messages

### Format

Utiliser les **Conventional Commits** avec emojis :

```
<type>(<scope>): <description>

[corps optionnel]

[footer optionnel]
```

### Types de Commits

| Emoji | Type | Description |
|-------|------|-------------|
| ✨ | `feat` | Nouvelle fonctionnalité |
| 🐛 | `fix` | Correction de bug |
| 📚 | `docs` | Documentation |
| 💄 | `style` | Formatage, style CSS |
| ♻️ | `refactor` | Refactoring de code |
| 🚀 | `perf` | Amélioration de performance |
| ✅ | `test` | Ajout de tests |
| 🔧 | `chore` | Tâches de maintenance |
| 🔒 | `security` | Sécurité |

### Exemples

```bash
# ✅ BON
git commit -m "✨ feat(rh): Add export Excel des présences mensuelles"
git commit -m "🐛 fix(presence): Correct calcul pourcentage avec pause"
git commit -m "📚 docs: Update README with new features"
git commit -m "♻️ refactor(views): Clean up rh_presences view"

# ❌ MAUVAIS
git commit -m "update"
git commit -m "fix bug"
git commit -m "work in progress"
```

## 🔍 Pull Requests

### Template de PR

Lors de la création d'une PR, remplir ce template :

```markdown
## 📝 Description
[Décrivez les changements effectués]

## 🎯 Type de Changement
- [ ] ✨ Nouvelle fonctionnalité
- [ ] 🐛 Correction de bug
- [ ] ♻️ Refactoring
- [ ] 📚 Documentation
- [ ] 🔒 Sécurité

## 🧪 Tests Effectués
- [ ] Tests manuels
- [ ] Tests unitaires
- [ ] Tests d'intégration

## 📸 Screenshots (si applicable)
[Ajouter des captures d'écran]

## ✅ Checklist
- [ ] Code suit les standards PEP 8
- [ ] Documentation mise à jour
- [ ] Tests ajoutés/mis à jour
- [ ] Pas de conflits avec main
- [ ] Commit messages clairs

## 🔗 Issues Liées
Closes #[numéro]
```

### Review Process

1. **Soumission** : Créer la PR
2. **CI/CD** : Vérification automatique (si configuré)
3. **Review** : Au moins 1 approbation requise
4. **Tests** : Vérifier que tout passe
5. **Merge** : Fusion par un mainteneur

## 🐛 Signaler des Bugs

### Template d'Issue pour Bug

```markdown
## 🐛 Description du Bug
[Décrivez le bug clairement]

## 🔄 Étapes pour Reproduire
1. Aller sur '...'
2. Cliquer sur '...'
3. Voir l'erreur

## ✅ Comportement Attendu
[Ce qui devrait se passer]

## ❌ Comportement Actuel
[Ce qui se passe réellement]

## 📸 Screenshots
[Si applicable]

## 🖥️ Environnement
- **OS** : Windows 11 / Ubuntu 22.04
- **Navigateur** : Chrome 120
- **Django Version** : 5.2
- **Python Version** : 3.13.5

## 📝 Informations Supplémentaires
[Contexte additionnel, logs, etc.]
```

## 💡 Proposer des Fonctionnalités

### Template d'Issue pour Feature

```markdown
## ✨ Fonctionnalité Proposée
[Décrivez la fonctionnalité]

## 🎯 Problème à Résoudre
[Pourquoi cette fonctionnalité est nécessaire]

## 💡 Solution Proposée
[Comment implémenter cette fonctionnalité]

## 🔄 Alternatives Considérées
[Autres solutions envisagées]

## 📊 Impact
- [ ] Performance
- [ ] Sécurité
- [ ] UX/UI
- [ ] Base de données

## 📝 Contexte Additionnel
[Maquettes, liens, etc.]
```

## 🧪 Tests

### Écrire des Tests

```python
# tests/test_presence.py
from django.test import TestCase
from CarrefourApp.models import Employe, Presence
from datetime import time, date

class PresenceTestCase(TestCase):
    def setUp(self):
        self.employe = Employe.objects.create_user(
            username='test',
            password='Test1234!',
            role='CAISSIER'
        )
    
    def test_calcul_statut_present(self):
        """Test du statut PRÉSENT"""
        presence = Presence.objects.create(
            employe=self.employe,
            date=date.today(),
            heure_arrivee=time(8, 10),
            heure_depart=time(17, 0)
        )
        self.assertEqual(presence.statut, 'PRESENT')
    
    def test_calcul_statut_retard(self):
        """Test du statut RETARD"""
        presence = Presence.objects.create(
            employe=self.employe,
            date=date.today(),
            heure_arrivee=time(8, 45),
            heure_depart=time(17, 0)
        )
        self.assertEqual(presence.statut, 'RETARD')
```

### Lancer les Tests

```bash
# Tous les tests
python manage.py test

# Tests spécifiques
python manage.py test CarrefourApp.tests.test_presence

# Avec coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📚 Documentation

### Documenter le Code

```python
def calculer_pourcentage_presence(self):
    """
    Calcule le pourcentage de présence par rapport aux heures requises.
    
    Returns:
        float: Pourcentage entre 0 et 100
        
    Example:
        >>> presence = Presence(...)
        >>> presence.calculer_pourcentage_presence()
        97.8
    """
    heures_requises = self.calculer_heures_requises()
    heures_travaillees = self.calculer_heures_travaillees()
    
    if heures_requises == 0:
        return 0
    
    return (heures_travaillees / heures_requises) * 100
```

## 🏆 Bonnes Pratiques

### ✅ À Faire

- Écrire du code lisible et maintenable
- Commenter le code complexe
- Ajouter des docstrings
- Tester avant de commit
- Garder les commits petits et focalisés
- Mettre à jour la documentation
- Respecter la structure du projet

### ❌ À Éviter

- Commit de fichiers sensibles (.env, db.sqlite3)
- Code non testé
- Commits massifs sans description
- Ignorer les warnings
- Hard-coder des valeurs
- Dupliquer du code

## 📞 Support

Besoin d'aide pour contribuer ?

- **GitHub Discussions** : https://github.com/romualdKO/PROJET_CARREFOUR/discussions
- **Issues** : https://github.com/romualdKO/PROJET_CARREFOUR/issues
- **Email** : dev@supermarche-plus.com

## 🙏 Remerciements

Merci à tous les contributeurs qui aident à améliorer SuperMarché Plus !

### Contributeurs

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- Sera mis à jour automatiquement -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

---

**Développé avec ❤️ par l'équipe ESATIC**  
**Licence** : MIT
