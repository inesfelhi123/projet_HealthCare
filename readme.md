# Projet HealthCare Knowledge Graph

## 1. Structure du projet

SMAI_Project/
│
├── data/
│ ├── medtext_2.csv # Dataset original
│ └── medtext_2clean.csv # Dataset nettoyé après exploration
│
├── src/
│ ├── graph/
│ │ ├── extract_entities.py # Extraction des entités médicales
│ │ ├── build_graph.py # Création du graphe Neo4j
│ │ ├── neo4j_connection.py # Connexion à Neo4j (fonction get_neo4j_driver)
│ │ └── test_neo4j_connection.py # Test de la connexion Neo4j
│ │
│ └── utils/ # (optionnel) fonctions utilitaires
│
├── notebook/
│ └── data_exploration.ipynb # Notebook pour l'exploration et nettoyage
│
└── README.md


---

## 2️⃣ Étapes réalisées

### 2.1 Exploration et nettoyage du dataset
**Dataset** : [`data/medtext_2.csv`](data/medtext_2.csv)
**Colonnes** : `Prompt` (cas clinique), `Completion` (réponse médicale)
**Actions réalisées :**
- Vérification du type de données et des valeurs manquantes.
- Nettoyage des textes : minuscules, suppression de ponctuation et caractères spéciaux.
- Standardisation des formats (ex : `50-year-old` → `50yearold`).
- Sauvegarde : [`data/medtext_2clean.csv`](data/medtext_2clean.csv).

---

### 2.2 Extraction des entités médicales
**Fichier** : [`src/graph/extract_entities.py`](src/graph/extract_entities.py)
**Objectif** : Identifier dans le dataset les entités médicales et relations :
**Entités :**
- Maladies (`Disease`)
- Symptômes (`Symptom`)
- Traitements (`Treatment`)
**Relations :**
- `HAS_SYMPTOM` (Disease → Symptom)
- `TREATED_BY` (Disease → Treatment)
**Résultat** : Fichiers CSV sauvegardés dans [`data/`](data/) :
- [`diseases.csv`](data/diseases.csv)
- [`symptoms.csv`](data/symptoms.csv)
- [`treatments.csv`](data/treatments.csv)
- [`relations.csv`](data/relations.csv)

---

### 2.3 Connexion à Neo4j
**Fichier** : [`src/graph/neo4j_connection.py`](src/graph/neo4j_connection.py)
**Fonction principale** : `get_neo4j_driver()`
**Informations de connexion :**
```python
uri = "neo4j://127.0.0.1:7687"
username = "neo4j"
password = "inesfelhi"
database = "medgraph"
```
Test de connexion via : [`src/graph/test_neo4j_connection.py`](src/graph/test_neo4j_connection.py)
Vérification que la base `medgraph` est accessible et prête à recevoir des nœuds et relations.

---

### 2.4 Test de connexion à Neo4j
Test de connexion via : [`src/graph/test_neo4j_connection.py`](src/graph/test_neo4j_connection.py)
Vérification que la base `medgraph` est accessible et prête à recevoir des nœuds et relations.

---

### 2.5 Construction du Knowledge Graph
**Fichier** : [`src/graph/build_graph.py`](src/graph/build_graph.py)
**Étapes :**
- Chargement des entités extraites :
  - [`diseases.csv`](data/diseases.csv)
  - [`symptoms.csv`](data/symptoms.csv)
  - [`treatments.csv`](data/treatments.csv)
- Création des nœuds dans Neo4j :
  - `Disease`
  - `Symptom`
  - `Treatment`
- Création des relations :
  - `HAS_SYMPTOM`
  - `TREATED_BY`
- Vérification du nombre de nœuds et relations insérés.

---

### 2.6 Interrogation du Graphe
Requêtes exemples pour récupérer maladies avec symptômes et traitements :
```cypher
MATCH (d\:Disease)-[\:HAS_SYMPTOM]->(s\:Symptom),
      (d)-[\:TREATED_BY]->(t\:Treatment)
RETURN d.name, collect(s.name) as symptoms, collect(t.name) as treatments

