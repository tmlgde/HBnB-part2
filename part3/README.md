# HBnB API RESTful – Partie 3 : Backend Sécurisé et Intégration Base de Données

## 🚀 Présentation

Cette troisième étape du projet HBnB consiste à renforcer le backend en y intégrant :

- Une authentification sécurisée basée sur JWT,
- Une gestion fine des autorisations (utilisateurs et administrateurs),
- Une persistance des données avec une base relationnelle (SQLite en dev, MySQL en production),
- Une migration des opérations CRUD vers une vraie base,
- La conception et la visualisation du schéma de base avec Mermaid.js.

L’objectif est d’obtenir un backend sécurisé, robuste et prêt pour un usage réel en production.

---

## 🎯 Objectifs clés

- **Authentification & Contrôle d’accès :**  
  Mise en place d’un système JWT pour gérer l’accès sécurisé, avec des rôles utilisateur (admin vs utilisateur standard).

- **Persistance en base relationnelle :**  
  Transition d’un stockage temporaire en mémoire vers une base SQL via SQLAlchemy (SQLite local, MySQL prod).

- **CRUD permanent :**  
  Adaptation de toutes les opérations pour qu’elles interagissent avec la base de données.

- **Modélisation & Visualisation :**  
  Schéma relationnel modélisé et visualisé avec Mermaid.js pour une meilleure compréhension des relations.

- **Validation des données :**  
  Mise en place de validations et contraintes strictes pour garantir la cohérence des données.

---

## 🌍 Contexte

Les premières phases utilisaient un stockage volatile en mémoire, idéal pour du prototypage mais insuffisant pour un déploiement. Cette phase vous permettra de maîtriser :

- L’intégration d’une base de données relationnelle dans un projet Flask,
- La sécurisation d’une API via des tokens JWT,
- La gestion des rôles et des droits d’accès.

Ainsi, vous serez en mesure de déployer une API REST robuste et professionnelle.

---

## 📚 Ressources recommandées

- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/en/stable/)  
- [SQLAlchemy ORM Documentation](https://docs.sqlalchemy.org/en/20/)  
- [SQLite Documentation](https://www.sqlite.org/docs.html)  
- [Flask Official Docs](https://flask.palletsprojects.com/en/latest/)  
- [Mermaid.js Guide](https://mermaid-js.github.io/mermaid/#/)  
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

---

## 🗂 Organisation du projet et étapes

### Plan de travail

| Étape | Description                                                       | Points |
|-------|------------------------------------------------------------------|--------|
| 0     | Intégrer la configuration dans la factory Flask                  | 5      |
| 1     | Ajouter le hashage des mots de passe dans le modèle User         | 10     |
| 2     | Mettre en place l’authentification JWT                           | 10     |
| 3     | Sécuriser les endpoints pour accès utilisateur authentifié       | 10     |
| 4     | Restreindre certains accès aux administrateurs                   | 10     |
| 5     | Implémenter le repository SQLAlchemy                              | 10     |
| 6     | Mapper l’entité User avec SQLAlchemy                              | 10     |
| 7     | Mapper Place, Review, Amenity                                     | 10     |
| 8     | Définir les relations entre les entités                          | 10     |
| 9     | Créer scripts SQL pour créer tables et données initiales         | 10     |
| 10    | Générer les diagrammes ER avec Mermaid.js                        | 10     |

---

## 🛠 Installation et lancement

1. Cloner le dépôt et accéder au dossier part3 :

```bash
git clone https://github.com/tmlgde/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3
