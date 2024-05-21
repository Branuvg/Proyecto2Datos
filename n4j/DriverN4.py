from neo4j import GraphDatabase 

class Neo4j_C:
    global listName
    listName = []
    global reclist
    reclist = []

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
    def recomendation_comida(usuario_activo):
        if usuario_activo:
            example.recomendar_comida(usuario_activo)
        else:
            print("Por favor, ingrese sus preferencias primero.")

    def recomendar_comida(self, user_name):
        with self._driver.session() as session:
            recommendations = session.read_transaction(self._view_food)
            print(f"Recomendaciones para {user_name}:")
            for nodo in recommendations:
                reclist.append(nodo)

        print(reclist)


    # Nodos y sus relaciones
    @staticmethod
    def _create_data(tx):
        # Definir las variables
        UserN = "David"
        ComidaN = "Lasagna"
        TempN = "Templada"
        SaborN = "Salado"
        TexturaN = "Solido"
        LugarN = "Casa"
        TipoN = "Chatarra"
        RateN = "9"

        global listName

        print(listName, "***")
        # Crear nodos de usuario y comida con parámetros
        tx.run("CREATE (:User {name: $UserN})", UserN=UserN)

        # Crear nodos de características de comida con parámetros
        if TempN not in listName:
            tx.run("CREATE (:Comida {name: $ComidaN})", ComidaN=ComidaN)
        else:
            tx.run("MATCH (c:User {name: $UserN}), (t:Comida {name: $ComidaN}) "
            "MERGE (c)-[:PERTENECE]->(t)", UserN=UserN, ComidaN=ComidaN)
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
            tx.run("CREATE (:Tipo {name: $TipoN})", TipoN=TipoN)
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
    
    @staticmethod
    def _view_food(tx):
        result = tx.run("MATCH (n:Comida) RETURN n.name AS name")
        names = [record["name"] for record in result]
        return names
    


@staticmethod
def _recommend_food(tx, user_name):
    query = """
    MATCH (u:User {name: $user_name})-[:WATCH]->(f:Comida)
    MATCH (f)-[:PERTENECE]->(t:Temperatura)
    MATCH (f)-[:PERTENECE]->(s:Sabor)
    MATCH (f)-[:PERTENECE]->(tx:Textura)
    MATCH (f)-[:PERTENECE]->(l:Lugar)
    MATCH (f)-[:PERTENECE]->(tp:Tipo)
    WITH t, s, tx, l, tp
    MATCH (otherFoods:Comida)
    WHERE (otherFoods)-[:PERTENECE]->(t) ANd
          (otherFoods)-[:PERTENECE]->(s) AND
          (otherFoods)-[:PERTENECE]->(tx) AND
          (otherFoods)-[:PERTENECE]->(l) AND
          (otherFoods)-[:PERTENECE]->(tp) AND
          (otherFoods) <> f
    RETURN otherFoods.name AS name
    """
    result = tx.run(query, user_name=user_name)
    return [record["name"] for record in result]


# Configuración de conexión y ejecución de la creación de datos
uri = "neo4j+ssc://6ed9a403.databases.neo4j.io"
user = "neo4j"
password = "0iIoDYVv8wV4MZIcF_405l5muLHL3mMjuXN2tUevJ_w"

# Crear una instancia de la clase y ejecutar la creación de nodos y relaciones
example = Neo4j_C(uri, user, password)
example.mostrar_datos()
example.create_nodes_and_relationships()
example.recomendar_comida("David")

# Cerrar la conexión al finalizar
example.close()