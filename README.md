# Système d'Analyse de Défauts Électriques

## Auteur
**Aouf Nihed**  
**Projet** : Système intelligent de classification et prédiction de défauts dans les réseaux triphasés.

## Table des Matières
- [Présentation](#présentation)
- [Fonctionnalités](#fonctionnalités)
- [Structure du Projet](#structure-du-projet)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Contribution](#contribution)
- [Licence](#licence)

## Présentation
Ce projet vise à développer un système capable de détecter et de classer les défauts électriques dans un réseau triphasé en utilisant des techniques basées sur les normes IEEE. Il intègre également un modèle prédictif pour anticiper les futures anomalies.

## Fonctionnalités
✅ **Classification de Défauts** : Monophasé, Biphasé (Simple & Grounded), Triphasé, et Open Circuit.  
✅ **Prédiction** : Utilisation de techniques de machine learning pour prédire les défauts futurs.  
✅ **Génération de Rapports** : Sauvegarde automatique des résultats dans des fichiers CSV.

## Structure du Projet
```bash
power_fault_analysis/
├── src/
│   ├── system.py
│   ├── analyzers/
│   │   ├── fault_analyzer.py
│   │   └── predictive_model.py
├── data/
│   ├── grte_data.csv
│   ├── fault_classified.csv
│   └── fault_predictions.csv
├── docs/
└── venv/
```

## Installation
1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-repo/power_fault_analysis.git
   ```
2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Activer l'environnement virtuel** :
   ```bash
   source venv/bin/activate  # Sur macOS/Linux
   venv\Scripts\activate     # Sur Windows
   ```

## Utilisation
1. **Exécuter le système** :
   ```bash
   python src/system.py
   ```
2. **Vérifier les résultats** :
   - Fichier `data/fault_classified.csv` pour les défauts classifiés.
   - Fichier `data/fault_predictions.csv` pour les prédictions.

## Contribution
Les contributions sont les bienvenues ! Pour participer, veuillez suivre ces étapes :
1. **Forker** le dépôt.
2. **Créer** une branche pour vos modifications.
3. **Soumettre** une pull request avec une description détaillée.

---
**"Un système innovant pour la stabilité des réseaux électriques"** - *Aouf Nihed*
