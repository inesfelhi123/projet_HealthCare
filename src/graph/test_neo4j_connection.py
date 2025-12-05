# test_connection.py
from neo4j_connection import get_neo4j_driver


driver = get_neo4j_driver()

# Fonction pour tester la connexion
def test_connection(tx):
    result = tx.run("RETURN 1 AS connected")
    for record in result:
        print("Connection test result:", record["connected"])

# Vérifier la connexion à la base de données 'medgraph'
try:
    with driver.session(database="medgraph") as session:
        session.execute_read(test_connection)
    print("✅ Connexion à Neo4j (medgraph) réussie !")
except Exception as e:
    print("❌ Erreur de connexion :", e)
finally:
    driver.close()
