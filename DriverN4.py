from neo4j import GraphDatabase 
class Neo4j_C:
    global listName
    listName = []

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def create_nodes_and_relationships(self):
        with self._driver.session() as session:
            session.write_transaction(self._create_data)

    def mostrar_datos(self):
        with self._driver.session() as session:
            names = session.read_transaction(self._view_data)
            for i in range(len(names)):
                listName.append(names[i])
    
    menu = """Bienvenidos a Tinder de comida
1. ingresar preferencias
2. comida favorita
3. Encontrar comida
4. Salir

"""

    # Nodos y sus relaciones
    @staticmethod
    def _create_data(tx):
        # Definir las variables
        UserN = "David"
        ComidaN = "Pizza"
        TempN = "Caliente"
        SaborN = "Salado"
        TexturaN = "Solido"
        LugarN = "Restaurante"
        TipoN = "Chatarra"
        RateN = "7"

        global listName
        
        print(listName, "***")
        # Crear nodos de usuario y comida con parámetros
        tx.run("CREATE (:User {name: $UserN})", UserN=UserN)
        tx.run("CREATE (:Comida {name: $ComidaN})", ComidaN=ComidaN)

        # Crear nodos de características de comida con parámetros
        if TempN not in listName:
            tx.run("CREATE (:Temperatura {name: $TempN})", TempN=TempN)
        else:
            tx.run("MATCH (c:Comida {name: $ComidaN}), (t:Temperatura {name: $TempN}) "
            "MERGE (c)-[:PERTENECE]->(t)", ComidaN=ComidaN, TempN=TempN)
        if SaborN not in listName:
            tx.run("CREATE (:Sabor {name: $SaborN})", SaborN=SaborN)
        else:
            tx.run("MATCH (c:Comida {name: $ComidaN}), (s:Sabor {name: $SaborN}) "
            "MERGE (c)-[:PERTENECE]->(s)", ComidaN=ComidaN, SaborN=SaborN)
        if TexturaN not in listName:
            tx.run("CREATE (:Textura {name: $TexturaN})", TexturaN=TexturaN)
        else:
            tx.run("MATCH (c:Comida {name: $ComidaN}), (tx:Textura {name: $TexturaN}) "
            "MERGE (c)-[:PERTENECE]->(tx)", ComidaN=ComidaN, TexturaN=TexturaN)
        if LugarN not in listName:
            tx.run("CREATE (:Lugar {name: $LugarN})", LugarN=LugarN)
        else:
            tx.run("MATCH (c:Comida {name: $ComidaN}), (l:Lugar {name: $LugarN}) "
            "MERGE (c)-[:PERTENECE]->(l)", ComidaN=ComidaN, LugarN=LugarN)
        if TipoN not in listName:
            tx.run("CREATE (:Tipo {name: $TipoN})", LugarN=LugarN)
        else:
            tx.run("MATCH (c:Comida {name: $ComidaN}), (tp:Tipo {name: $TipoN}) "
            "MERGE (c)-[:PERTENECE]->(tp)", ComidaN=ComidaN, TipoN=TipoN)
        if RateN not in listName:
            tx.run("CREATE (:Rate {name: $RateN})", RateN=RateN)
        else:
            tx.run("MATCH (c:Comida {name: $ComidaN}), (r:Rate {name: $RateN}) "
            "MERGE (c)-[:TIENE]->(r)", ComidaN=ComidaN, RateN=RateN)

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
        
    @staticmethod
    def _view_data(tx):
        result = tx.run("MATCH (n) RETURN n.name AS name")
        names = [record["name"] for record in result]
        return names
        
# Configuración de conexión y ejecución de la creación de datos
uri = "neo4j+ssc://6ed9a403.databases.neo4j.io"
user = "neo4j"
password = "0iIoDYVv8wV4MZIcF_405l5muLHL3mMjuXN2tUevJ_w"

# Crear una instancia de la clase y ejecutar la creación de nodos y relaciones
example = Neo4j_C(uri, user, password)
example.mostrar_datos()
example.create_nodes_and_relationships()


# Cerrar la conexión al finalizar
example.close()

