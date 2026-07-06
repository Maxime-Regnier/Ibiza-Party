# 🎉 Ibiza Party 2027

## Description

Ibiza Party 2027 est une application web développée dans le cadre du Portfolio Project d'Holberton School.

L'objectif est de permettre à un utilisateur de réserver un billet pour un festival fictif de musique électronique.

Après la réservation :

- les informations sont enregistrées
- un billet PDF est généré automatiquement
- un email de confirmation est envoyé avec le billet en pièce jointe

Une interface d'administration sécurisée permet également de consulter les réservations.

---

# Technologies

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Python 3
- Flask
- Flask-CORS
- ReportLab
- SMTP Gmail

---

# Fonctionnalités

✅ Présentation du festival

✅ Compte à rebours

✅ Line-up interactif

✅ Informations pratiques

✅ Réservation d'un billet

✅ Validation des données

✅ Génération automatique d'un billet PDF

✅ Envoi automatique d'un email

✅ Sauvegarde des réservations

✅ Interface administrateur

✅ Authentification administrateur

✅ Recherche de réservations

---

# Architecture

```

Utilisateur

↓

Frontend
(HTML / CSS / JavaScript)

↓

Fetch API

↓

Flask

↓

Validation

↓

Création PDF

↓

Email SMTP

↓

data.json

```

---

# Structure du projet

```

Ibiza-Party/

│

├── frontend/

│ ├── index.html

│ ├── login.html

│ ├── admin.html

│ ├── style.css

│ ├── login.css

│ ├── admin.css

│ ├── script.js

│ ├── admin.js

│ └── image/

│

├── backend/

│ ├── app.py

│ ├── data.json

│ ├── requirements.txt

│ ├── logo.webp

│ └── README.md

│

└── README.md

```

---

# Installation

Cloner le projet

```bash
git clone <repository_url>
```

Installer les dépendances

```bash
pip install -r backend/requirements.txt
```

Lancer le serveur

```bash
cd backend

python app.py
```

Puis ouvrir :

```
http://127.0.0.1:5000
```

---

# Routes Flask

| Route | Méthode | Description |
|--------|----------|-------------|
| / | GET | Accueil |
| /tickets | POST | Nouvelle réservation |
| /tickets | GET | Liste des réservations |
| /login | POST | Connexion administrateur |
| /logout | POST | Déconnexion |
| /check-admin | GET | Vérification session |

---

# Génération du billet

Lors d'une réservation :

- validation des données
- enregistrement dans data.json
- génération du PDF
- envoi automatique par email

---

# Sécurité

Le panneau administrateur est protégé par une session Flask.

Les réservations ne peuvent être consultées qu'après authentification.

---

# Tests réalisés

- Réservation valide
- Champs obligatoires
- Adresse email invalide
- Génération du PDF
- Envoi du mail
- Connexion administrateur
- Accès protégé
- Recherche des réservations

---

# Améliorations futures

- Base de données MySQL
- QR Code sur le billet
- Paiement en ligne
- Tableau de bord administrateur avancé
- Export Excel

---

# Auteur

Maxime Régnier

Portfolio Project — Holberton School