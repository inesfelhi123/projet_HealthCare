from neo4j import GraphDatabase

uri = "neo4j://127.0.0.1:7687"
username = "neo4j"
password = "inesfelhi"

def get_neo4j_driver():
    """
    Crée et retourne un driver Neo4j.
    """
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver
