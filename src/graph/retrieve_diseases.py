from neo4j_connection import get_neo4j_driver

def get_diseases_with_details(database="medgraph", limit=50):
    """
    Récupère les maladies avec leurs symptômes et traitements depuis Neo4j.
    """
    driver = get_neo4j_driver()
    
    query = """
    MATCH (d:Disease)
    OPTIONAL MATCH (d)-[:HAS_SYMPTOM]->(s:Symptom)
    OPTIONAL MATCH (d)-[:TREATED_BY]->(t:Treatment)
    RETURN d.name AS Disease, collect(DISTINCT s.name) AS Symptoms, collect(DISTINCT t.name) AS Treatments
    LIMIT $limit
    """
    
    with driver.session(database=database) as session:
        result = session.run(query, limit=limit)
        diseases_list = []
        for record in result:
            diseases_list.append({
                "Disease": record["Disease"],
                "Symptoms": record["Symptoms"],
                "Treatments": record["Treatments"]
            })
    return diseases_list

# Exemple
if __name__ == "__main__":
    diseases = get_diseases_with_details(limit=100)
    for d in diseases:
        print("Disease:", d["Disease"])
        print("Symptoms:", d["Symptoms"])
        print("Treatments:", d["Treatments"])
        print("------")
