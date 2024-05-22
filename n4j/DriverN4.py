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

    def create_nodes_and_relationships(self, UserN, ComidaN, TempN, SaborN, TexturaN, LugarN, TipoN, RateN):
        with self._driver.session() as session:
            session.write_transaction(self._create_data, UserN, ComidaN, TempN, SaborN, TexturaN, LugarN, TipoN, RateN)

    def mostrar_datos(self):
        with self._driver.session() as session:
            names = session.read_transaction(self._view_data)
            for i in range(len(names)):
                listName.append(names[i])

    def recomendation_comida(self, ComidaN, TempN, SaborN, TexturaN, LugarN, TipoN, RateN):
        recommendations = self.recomendar_comida(ComidaN, TempN, SaborN, TexturaN, LugarN, TipoN, RateN)
        print(f"Recomendaciones para comida con características dadas:")
        for nodo in recommendations:
            reclist.append(nodo)
        print(reclist)

# Nodos y sus relaciones
    @staticmethod
    def _create_data(tx, UserN, ComidaN, TempN, SaborN, TexturaN, LugarN, TipoN, RateN):
        UserN = UserN
        ComidaN = ComidaN
        TempN = TempN
        SaborN = SaborN
        TexturaN = TexturaN
        LugarN = LugarN
        TipoN = TipoN
        RateN = RateN

        global listName

        print(listName, "*")

        # Crear nodos de usuario y comida con parámetros
        tx.run("CREATE (:User {name: $UserN})", UserN=UserN)

        # Crear nodos de características de comida con parámetros
        if ComidaN not in listName:
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
        #tx.run("MATCH (u:User {name: $UserN}), (c:Comida {name: $ComidaN}) "
               #"MERGE (u)-[:WATCH]->(c)", UserN=UserN, ComidaN=ComidaN)

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
        query = """
        MATCH (n:Comida)
        RETURN n.name AS name
        """
        result = tx.run(query)
        return [record["name"] for record in result]

    @staticmethod
    def _recommend_food(tx, user_name):
        properties = ["Temperatura", "Sabor", "Textura", "Lugar", "Tipo"]
        
        base_query = [
            "MATCH (u:User {name: $user_name})-[:WATCH]->(f:Comida)"
        ]

        # Add MATCH clauses for each property
        for prop in properties:
            base_query.append(f"MATCH (f)-[:PERTENECE]->(t:{prop})")
        
        base_query.append("WITH " + ", ".join([f"t:{prop}" for prop in properties]))
        base_query.append("MATCH (otherFoods:Comida)")

        # Create where_clauses iteratively
        where_clauses = []
        for prop in properties:
            where_clauses.append(f"(otherFoods)-[:PERTENECE]->(t:{prop})")
        
        # Construct the WHERE clause
        where_clause = "WHERE (" + " OR ".join(where_clauses) + ") AND (otherFoods) <> f"
        
        # Combine the full query
        full_query = "\n".join(base_query) + "\n" + where_clause + "\nRETURN otherFoods.name AS name"
        
        result = tx.run(full_query, user_name=user_name)
        return [record["name"] for record in result]



# Configuración de conexión y ejecución de la creación de datos
uri = "neo4j+ssc://6ed9a403.databases.neo4j.io"
user = "neo4j"
password = "0iIoDYVv8wV4MZIcF_405l5muLHL3mMjuXN2tUevJ_w"

# Crear una instancia de la clase y ejecutar la creación de nodos y relaciones
example = Neo4j_C(uri, user, password)
# Se pasan los parámetros deseados
#example.create_nodes_and_relationships("Pepito", "Helado", "Frio", "Dulce", "Cremoso", "Restaurante", "Chatarra", "10")

#example.mostrar_datos()
#example.recomendar_comida("David")

# pruebas 
"""
example.recomendar_comida("Pizza", "Caliente", "Salado", "Suave", "Casa", "Chatarra", "10")
example.recomendar_comida("Pizza", "Caliente", "Salado", "Crujiente", "Restaurante", "Chatarra", "10")

example.recomendar_comida("Hamburguesa", "Caliente", "Salado", "Crujiente", "Restaurante", "Chatarra", "7")

example.recomendar_comida("Helado", "Frio", "Dulce", "Liquido", "Casa", "Chatarra", "10")
example.recomendar_comida("Sopa", "Frio", "Dulce", "Liquido", "Casa", "Saludable", "8")

example.recomendar_comida("Papitas", "Caliente", "Salado", "Crujiente", "Restaurante", "Chatarra", "10")

"""
#example.recomendar_comida("Sprite", "Frio", "Dulce", "Liquido", "Restaurante", "Chatarra", "10")

#print(type(example.recomendar_comida("Sprite", "Frio", "Dulce", "Liquido", "Restaurante", "Chatarra", "10")))
# Cerrar la conexión al finalizar
#example.close()
