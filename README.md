# Smart Complaints Management
### Plateforme intelligente de gestion des réclamations citoyennes
**Commune de Kénitra — Projet de Fin d'Année 2025–2026**

---

## Description

Smart Complaints Management est une plateforme web intelligente dédiée à la gestion, au suivi et à l'analyse des réclamations citoyennes au sein de la Commune de Kénitra. Elle permet aux citoyens de déposer des réclamations en ligne, de les suivre grâce à un code unique, et aux responsables communaux de les traiter, répondre et exporter les données.

Le système intègre un module de Machine Learning basé sur TF-IDF et Régression Logistique pour la classification automatique des réclamations, ainsi que l'API Google Gemini AI pour la traduction automatique français–arabe.

---

## Fonctionnalités

### Citoyens
- Dépôt de réclamations en ligne avec pièce jointe
- Génération automatique d'un code de suivi unique
- Suivi de l'état d'avancement par CIN + code
- Consultation des réponses de la commune
- Interface bilingue Français / Arabe

### Chefs de division
- Tableau de bord personnalisé par division
- Consultation, filtrage et tri des réclamations affectées
- Réponse aux citoyens avec pièce jointe
- Transfert d'une réclamation vers une autre division
- Clôture administrative des dossiers
- Historique complet des actions
- Export des données (Excel, CSV, PDF avec graphiques)

### Administration
- Gestion des utilisateurs (création, activation, désactivation)
- Gestion des divisions et des chefs responsables
- Supervision globale de toutes les réclamations
- Tableaux de bord statistiques avec graphiques
- Export global des données (Excel, PDF)

### Intelligence Artificielle
- Classification automatique par catégorie (voirie, eau, éclairage, assainissement, propreté)
- Détection automatique du niveau de priorité (faible, moyenne, élevée, urgente)
- Affectation automatique à la division compétente
- Traduction automatique arabe → français via Gemini AI
- Traduction des réponses français → arabe pour les citoyens arabophones

---

## Technologies utilisées

| Couche | Technologies |
|--------|-------------|
| Backend | Python 3.11, Flask, MySQL |
| Frontend | HTML5, CSS3, JavaScript, Chart.js |
| Machine Learning | Scikit-learn, NLTK, TF-IDF, Régression Logistique |
| Traduction IA | Google Gemini API |
| Export documents | Pandas, OpenPyXL, ReportLab, Matplotlib |
| Texte arabe PDF | arabic-reshaper, python-bidi |
| Sécurité | Werkzeug (hachage des mots de passe), Sessions Flask |

---

## Prérequis à installer

Avant de commencer, installer les logiciels suivants :

- **Python 3.11+** → https://www.python.org/downloads/
- **XAMPP** (inclut MySQL + phpMyAdmin) → https://www.apachefriends.org/

---

## Installation étape par étape

### Étape 1 — Télécharger le projet

Télécharger et décompresser le dossier du projet, ou cloner depuis GitHub :

```bash
git clone https://github.com/OUMAIMA774/smart-complaints-management.git
cd smart-complaints-management
```

### Étape 2 — Installer les dépendances Python

Ouvrir un terminal dans le dossier du projet et exécuter :

```bash
pip install -r requirements.txt
```

> Si une erreur apparaît sur un package, installer manuellement :
> `pip install flask mysql-connector-python scikit-learn nltk pandas openpyxl reportlab google-generativeai arabic-reshaper python-bidi matplotlib Werkzeug`

### Étape 3 — Démarrer XAMPP

1. Ouvrir XAMPP Control Panel
2. Démarrer **Apache** et **MySQL**
3. Ouvrir phpMyAdmin via http://localhost/phpmyadmin

### Étape 4 — Importer les bases de données

Deux bases de données sont nécessaires :

#### Base principale (application Flask)
1. Dans phpMyAdmin, cliquer sur **Nouvelle base de données**
2. Nommer la base : `gestion_reclamations`
3. Cliquer sur **Créer**
4. Aller dans l'onglet **Importer**
5. Sélectionner le fichier : `database/gestion_reclamations.sql`
6. Cliquer sur **Exécuter**

#### Base d'entraînement ML (optionnelle)
> Cette base est nécessaire **uniquement** si vous souhaitez réentraîner le modèle ML.
> Le modèle est déjà entraîné et prêt à l'emploi dans le dossier `ml/`.

1. Créer une nouvelle base nommée : `data_citoyen`
2. Importer le fichier : `database/data_citoyen.sql`

### Étape 5 — Configurer la connexion à la base de données

Ouvrir le fichier `config.py` et vérifier les paramètres :

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",        # Mettre le mot de passe MySQL si défini
    "database": "gestion_reclamations"
}
```

> Ne pas changer le nom de la base (`gestion_reclamations`). C'est la base utilisée par l'application.

### Étape 6 — Lancer l'application

```bash
python app.py
```

Puis ouvrir dans le navigateur :

```
http://127.0.0.1:5001
```

---

## Comptes de connexion par défaut

Après import de la base, les comptes suivants sont disponibles :

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Administrateur | admin@commune.ma | (défini dans la base) |
| Chef de division | (selon division) | (à changer à la première connexion) |

> Les chefs de division sont invités à changer leur mot de passe lors de la première connexion.

---

## Structure du projet

```
smart-complaints-management/
│
├── app.py                        ← Application principale Flask
├── config.py                     ← Configuration BDD + clés API
├── create_users.py               ← Script de création des utilisateurs
├── requirements.txt              ← Dépendances Python
│
├── database/
│   ├── gestion_reclamations.sql  ← Base principale (obligatoire)
│   └── data_citoyen.sql          ← Base d'entraînement ML (optionnelle)
│
├── ml/
│   ├── train_model.py            ← Script d'entraînement du modèle
│   ├── modele_reclamations.pkl   ← Modèle ML déjà entraîné (NE PAS SUPPRIMER)
│   └── vectorizer.pkl            ← Vectoriseur TF-IDF (NE PAS SUPPRIMER)
│
├── static/
│   ├── css/style.css
│   ├── images/logo.png
│   └── uploads/                  ← Pièces jointes des réclamations
│
└── templates/                    ← Pages HTML
    ├── index.html
    ├── deposer_reclamation.html
    ├── suivi.html
    ├── resultat_suivi.html
    ├── confirmation.html
    ├── login.html
    ├── changer_mot_de_passe.html
    ├── dashboard_division.html
    ├── detail_reclamation.html
    ├── exports.html
    ├── admin_dashboard.html
    ├── admin_reclamations.html
    ├── admin_utilisateurs.html
    ├── admin_divisions.html
    └── admin_exports.html
```

---

## Module ML — Informations importantes

> **Ne pas relancer `train_model.py`** sauf si vous souhaitez réentraîner le modèle.
> Les fichiers `.pkl` dans le dossier `ml/` sont déjà prêts et utilisés automatiquement par `app.py`.

Si vous souhaitez réentraîner le modèle :
1. Vérifier que la base `data_citoyen` est importée
2. Exécuter :
```bash
python ml/train_model.py
```
Le modèle sera remplacé automatiquement.

**Performances du modèle actuel :**
- Accuracy : 98.66%
- Validation croisée moyenne : 98.2%
- Nombre de catégories : 5 (voirie, eau, éclairage, assainissement, propreté)

---

## Fonctionnalités d'export PDF

Les rapports PDF générés contiennent :
- Synthèse globale avec indicateurs chiffrés
- Graphiques statistiques (répartition par priorité et par statut)
- Commentaire analytique automatique
- Liste détaillée des réclamations avec mise en évidence des urgences

---

## Sécurité

- Mots de passe hachés avec Werkzeug (bcrypt)
- Sessions sécurisées Flask
- Contrôle d'accès par rôle (citoyen / chef de division / administrateur)
- Protection des routes sensibles
- Désactivation possible des comptes utilisateurs

---

## Problèmes fréquents

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError` | Relancer `pip install -r requirements.txt` |
| Erreur de connexion MySQL | Vérifier que XAMPP est démarré et que `config.py` est correct |
| Page blanche au lancement | Vérifier la console Python pour l'erreur exacte |
| Texte arabe en carrés dans le PDF | Vérifier que la police `arial.ttf` existe dans `C:\Windows\Fonts\` |
| Erreur Gemini API | Vérifier la clé API dans `config.py` |

---

## Projet académique

**Intitulé :** Smart Complaints Management — Plateforme intelligente de gestion des réclamations citoyennes

**Filière :** Ingénierie Data Science et Informatique (IDSI)

**Établissement :** Faculté des Sciences et Techniques de Mohammedia — Université Hassan II de Casablanca

**Encadrante académique :** Pr. Hanae SBAI

**Année universitaire :** 2025–2026

---

## Auteur

**Oumaima El Yamani**

GitHub : https://github.com/OUMAIMA774