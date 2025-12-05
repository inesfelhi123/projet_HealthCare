import pandas as pd
from neo4j import GraphDatabase

# Connexion Neo4j
uri = "neo4j://127.0.0.1:7687"
username = "neo4j"
password = "inesfelhi"
database = "medgraph"

driver = GraphDatabase.driver(uri, auth=(username, password))

def create_nodes(tx, label, col_name, df):
    for value in df[col_name].dropna().unique():
        tx.run(f"MERGE (n:{label} {{name: $value}})", value=value)

def create_relationships(tx, rel_type, df, start_label, end_label, start_col, end_col):
    for _, row in df.iterrows():
        start = row[start_col]
        end = row[end_col]
        if pd.notna(start) and pd.notna(end):
            tx.run(
                f"""
                MATCH (a:{start_label} {{name: $start}})
                MATCH (b:{end_label} {{name: $end}})
                MERGE (a)-[r:{rel_type}]->(b)
                """,
                start=start,
                end=end
            )

with driver.session(database=database) as session:
    # Lecture des fichiers CSV
    diseases_df = pd.read_csv("../../data/diseases.csv")
    symptoms_df = pd.read_csv("../../data/symptoms.csv")
    treatments_df = pd.read_csv("../../data/treatments.csv")
    has_symptom_df = pd.read_csv("../../data/has_symptom.csv")
    treated_by_df = pd.read_csv("../../data/treated_by.csv")

    # Création des noeuds
    session.execute_write(create_nodes, "Disease", "Disease", diseases_df)
    session.execute_write(create_nodes, "Symptom", "Symptom", symptoms_df)
    session.execute_write(create_nodes, "Treatment", "Treatment", treatments_df)

    # Création des relations
    session.execute_write(create_relationships, "HAS_SYMPTOM", has_symptom_df, "Disease", "Symptom", "Disease", "Symptom")
    session.execute_write(create_relationships, "TREATED_BY", treated_by_df, "Disease", "Treatment", "Disease", "Treatment")

driver.close()
print("✅ Graphe créé et relations insérées avec succès !")
