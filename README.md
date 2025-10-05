#  Système de Gestion de Livraison par Drone

Un système de gestion complet pour la livraison de produits pharmaceutiques par drone, développé en Python avec une architecture orientée objet et des contrats de programmation.

##  Description du Projet

Ce projet simule un système de livraison par drone pour des services d'état (comme les SDIS) permettant :
- La gestion de bases opérationnelles
- L'affectation intelligente de commandes
- L'exécution de livraisons par des opérateurs de drones
- Le suivi en temps réel des missions
- La génération de rapports de performance

##  Architecture du Système

### Composants Principaux

- **`Administrateur`** : Point central de coordination du système
- **`Services_etat`** : Services publics bénéficiaires (SDIS-38, SDIS-73)
- **`Base`** : Bases opérationnelles hébergeant les opérateurs
- **`Operateur`** : Sociétés de livraison par drone
- **`Drone`** : Unités de livraison avec capacités spécifiques
- **`Commande`** : Demandes de livraison avec priorités
- **`Livraison`** : Missions regroupant plusieurs commandes
- **`Zone`** : Zones géographiques de destination

##  Fonctionnalités

###  Gestion des Ressources
- Création et gestion des bases opérationnelles
- Attribution d'opérateurs et de drones
- Contrôle de capacité et d'autonomie

###  Affectation Intelligente
- Algorithmes d'affectation basés sur :
  - Priorité des zones (nombre de personnes)
  - Capacité des drones (charge utile, autonomie)
  - Optimisation des trajets

###  Exécution des Livraisons
- Simulation réaliste des vols
- Gestion d'état des commandes (À faire → En cours → Terminée)
- Calcul des distances avec formule de Haversine

###  Reporting Avancé
- Statistiques de performance
- Taux de réussite par service
- Performance individuelle des drones
- Distances parcourues et charges transportées

##  Installation et Utilisation

### Prérequis
- Python 3.8+
- Bibliothèques requises :

```bash
pip install pint icontract

### Exécution
python main.py

### Structure des Fichiers

drone-delivery-system/
├── administrateur.py     # Gestionnaire principal
├── base.py               # Bases opérationnelles
├── commande.py           # Commandes de livraison
├── drone.py              # Unités drones
├── etat.py               # États des commandes
├── livraison.py          # Missions de livraison
├── operateur.py          # Opérateurs de drones
├── services_etat.py      # Services bénéficiaires
├── tools.py              # Utilitaires (calcul de distance)
├── zone.py               # Zones géographiques
└── main.py               # Point d'entrée

###  Exemple de Scénario

Le système gère actuellement :
2 services d'état : SDIS-38 (Isère) et SDIS-73 (Savoie)
2 bases opérationnelles : Base Alpes Nord et Base Savoie Sud
2 opérateurs avec 5 drones au total
8 zones de livraison avec différentes priorités
8 commandes réparties selon les besoins

 Contrats et Vérifications
Le projet utilise icontract pour assurer la robustesse :
-Vérification des préconditions
-Validation des postconditions
-Contrôle des invariants

Métriques et Performance
Le système génère des rapports détaillés incluant :
-Taux de livraison réussie
-Distance totale parcourue
-Charge utile utilisée
-Performance par drone et par service

Objectifs Pédagogiques
Ce projet démontre :
-Conception OO avancée avec relations complexes
-Gestion d'états avec pattern State
-Calculs géospatiaux précis
-Gestion d\'unités avec Pint
-Programmation par contrat

Auteur
Développé dans le cadre d'un projet de programmation orientée objet avancée.

Licence
Projet éducatif - Libre pour usage académique.





