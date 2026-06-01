# Smart Complaints Management

## 📌 Description

Smart Complaints Management est une plateforme web de gestion des réclamations citoyennes développée avec Flask et MySQL.

L'application permet aux citoyens de déposer des réclamations en ligne, de suivre leur état d'avancement et de recevoir les réponses des services communaux. Elle offre également aux responsables des divisions communales des outils de gestion, de traitement et d'export des données.

Le système intègre une classification automatique des réclamations grâce à l'intelligence artificielle afin d'orienter chaque demande vers la division compétente.

---

## 🚀 Fonctionnalités

### 👥 Citoyens

* Dépôt de réclamations en ligne
* Téléversement de pièces jointes (images ou documents)
* Génération automatique d'un code de suivi
* Suivi de l'état de traitement
* Consultation des réponses communales
* Interface bilingue Français / Arabe

### 🏢 Chefs de division

* Tableau de bord personnalisé
* Consultation des réclamations affectées
* Filtres par statut et priorité
* Réponse aux citoyens
* Clôture des réclamations
* Transfert vers une autre division
* Historique des actions

### 👨‍💼 Administration

* Gestion des utilisateurs
* Gestion des divisions
* Consultation globale des réclamations
* Statistiques générales
* Exports administratifs

### 🤖 Intelligence Artificielle

* Classification automatique des réclamations
* Détection de la catégorie concernée
* Attribution automatique de la division responsable
* Support des réclamations rédigées en français et en arabe

---

## 🛠️ Technologies utilisées

### Backend

* Python
* Flask
* MySQL
* mysql-connector-python

### Frontend

* HTML5
* CSS3
* JavaScript
* Chart.js

### Intelligence Artificielle

* Scikit-learn
* Gemini API
* Machine Learning (classification automatique)

### Génération de documents

* Pandas
* OpenPyXL
* ReportLab

---

## 🗄️ Structure du projet

```text
smart-complaints-management/
│
├── app.py
├── config.py
├── requirements.txt
│
├── database/
│   └── database.sql
│
├── ml/
│   ├── train_model.py
│   ├── modele_reclamations.pkl
│   └── vectorizer.pkl
│
├── static/
│   ├── css/
│   ├── images/
│   └── uploads/
│
└── templates/
    ├── index.html
    ├── deposer_reclamation.html
    ├── suivi.html
    ├── resultat_suivi.html
    ├── dashboard_division.html
    ├── detail_reclamation.html
    ├── exports.html
    └── ...
```

---

## 📸 Captures d'écran

### Accueil

<img width="1355" height="611" alt="image" src="https://github.com/user-attachments/assets/afbf60ba-9739-4a6c-b26c-f5adec4f7742" />

### Dépôt d'une réclamation

<img width="1364" height="608" alt="image" src="https://github.com/user-attachments/assets/0f08cf73-a1c1-4142-9d73-1abce31f70f3" />
<img width="1363" height="611" alt="image" src="https://github.com/user-attachments/assets/4af6acd8-2d8b-4202-b4a4-301f13b7f1c8" />


### Suivi d'une réclamation

*(Ajouter une capture d'écran ici)*
<img width="1366" height="611" alt="image" src="https://github.com/user-attachments/assets/84c094c4-5267-4f3d-a804-956cde0c5806" />
<img width="1366" height="602" alt="image" src="https://github.com/user-attachments/assets/48d4c72d-cb0b-4b9a-8381-81b815f638fc" />


### Tableau de bord Division

<img width="1364" height="604" alt="image" src="https://github.com/user-attachments/assets/5debb588-ed98-4098-b5e5-f503670949c2" />


### Détail d'une réclamation


<img width="1364" height="599" alt="image" src="https://github.com/user-attachments/assets/ac58a775-bddd-4680-83a2-108a01d35571" />

### Exports administratifs

<img width="1366" height="607" alt="image" src="https://github.com/user-attachments/assets/7c4e69a8-ff6a-4407-b8f3-3444a87d8d0d" />
<img width="1366" height="605" alt="image" src="https://github.com/user-attachments/assets/e93dfe51-5277-4e36-9bae-0975d8269051" />


## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/OUMAIMA774/smart-complaints-management.git
cd smart-complaints-management
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer MySQL

Créer une base de données puis importer :

```text
database/database.sql
```

### 4. Configurer les paramètres

Modifier le fichier :

```text
config.py
```

avec les informations de connexion à votre base de données.

### 5. Lancer l'application

```bash
python app.py
```

Puis ouvrir :

```text
http://127.0.0.1:5001
```

---

## 📊 Fonctionnalités d'export

* Export Excel
* Export CSV
* Export PDF
* Export des réclamations urgentes

---

## 🔐 Sécurité

* Authentification des utilisateurs
* Contrôle des accès par rôle
* Protection des espaces administratifs
* Gestion sécurisée des sessions

---

## 👩‍🎓 Projet académique

Projet réalisé dans le cadre d'un Projet de Fin d'Année (PFA) en cycle ingénieur.

**Filière :** Ingénierie Data Sciences et Informatique (IDSI)

**Établissement :** Faculté des Sciences et Techniques de Mohammedia

---

## 👤 Auteur

**Oumaima El Yamani**

GitHub : https://github.com/OUMAIMA774
