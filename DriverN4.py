from neo4j import GraphDatabase 

class Neo4j_C:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def create_nodes_and_relationships(self):
        with self._driver.session() as session:
            session.write_transaction(self._create_data)

    # Nodos y sus relaciones
    @staticmethod
    def _create_data(tx):
        # Definir las variables
        UserN = "Bran"
        ComidaN = "Lasagna"
        TempN = "Caliente"
        SaborN = "Salado"
        TexturaN = "Solido"
        LugarN = "Casa"
        TipoN = "Chatarra"
        RateN = "10"

        # Crear nodos de usuario y comida con parámetros
        tx.run("CREATE (:User {name: $UserN})", UserN=UserN)
        tx.run("CREATE (:Comida {name: $ComidaN})", ComidaN=ComidaN)

        # Crear nodos de características de comida con parámetros
        tx.run("CREATE (:Temperatura {name: $TempN})", TempN=TempN)
        tx.run("CREATE (:Sabor {name: $SaborN})", SaborN=SaborN)
        tx.run("CREATE (:Textura {name: $TexturaN})", TexturaN=TexturaN)
        tx.run("CREATE (:Lugar {name: $LugarN})", LugarN=LugarN)
        tx.run("CREATE (:Tipo {name: $TipoN})", TipoN=TipoN)
        tx.run("CREATE (:Rate {name: $RateN})", RateN=RateN)

        # Establecer relaciones entre usuario y comida
        tx.run("MATCH (u:User {name: $UserN}), (c:Comida {name: $ComidaN}) "
            "MERGE (u)-[:WATCH]->(c)", UserN=UserN, ComidaN=ComidaN)

        # Establecer relaciones entre comida y características
        tx.run("MATCH (c:Comida {name: $ComidaN}), "
            "(t:Temperatura {name: $TempN}), "
            "(s:Sabor {name: $SaborN}), "
            "(tx:Textura {name: $TexturaN}), "
            "(l:Lugar {name: $LugarN}), "
            "(tp:Tipo {name: $TipoN}) "
            "MERGE (c)-[:PERTENECE]->(t) "
            "MERGE (c)-[:PERTENECE]->(s) "
            "MERGE (c)-[:PERTENECE]->(tx) "
            "MERGE (c)-[:PERTENECE]->(l) "
            "MERGE (c)-[:PERTENECE]->(tp)",
            ComidaN=ComidaN, TempN=TempN, SaborN=SaborN, TexturaN=TexturaN, LugarN=LugarN, TipoN=TipoN)

        # Establecer relación entre comida y valoración (rating)
        tx.run("MATCH (c:Comida {name: $ComidaN}), (r:Rate {name: $RateN}) "
            "MERGE (c)-[:TIENE]->(r)", ComidaN=ComidaN, RateN=RateN)
