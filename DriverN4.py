from neo4j import GraphDatabase 

class Neo4j_C:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def create_nodes_and_relationships(self):
        with self._driver.session() as session:
            session.write_transaction(self._create_data)

