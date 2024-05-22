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

    def recomendar_comida(self, ComidaN, TempN, SaborN, TexturaN, LugarN, TipoN, RateN):
        with self._driver.session() as session:
            recommendations = session.read_transaction(
                self._recommend_food, ComidaN, TempN, SaborN, TexturaN, LugarN, TipoN, RateN
            )
        
        return recommendations

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
        result = tx.run("MATCH (n:Comida) RETURN n.name AS name")
        names = [record["name"] for record in result]
        return names

    @staticmethod
    def _recommend_food(tx, ComidaN, TempN, SaborN, TexturaN, LugarN, TipoN, RateN):
        query = """
        MATCH (f:Comida {name: $ComidaN})-[:PERTENECE]->(t:Temperatura),
            (f)-[:PERTENECE]->(s:Sabor),
            (f)-[:PERTENECE]->(tx:Textura),
            (f)-[:PERTENECE]->(l:Lugar),
            (f)-[:PERTENECE]->(tp:Tipo)
        WITH t, s, tx, l, tp
        MATCH (otherFoods:Comida)
        WHERE otherFoods.name <> $ComidaN
        OPTIONAL MATCH (otherFoods)-[r1:PERTENECE]->(t)
        OPTIONAL MATCH (otherFoods)-[r2:PERTENECE]->(s)
        OPTIONAL MATCH (otherFoods)-[r3:PERTENECE]->(tx)
        OPTIONAL MATCH (otherFoods)-[r4:PERTENECE]->(l)
        OPTIONAL MATCH (otherFoods)-[r5:PERTENECE]->(tp)
        WITH otherFoods, count(r1) + count(r2) + count(r3) + count(r4) + count(r5) AS relevance
        RETURN otherFoods.name AS name, relevance
        ORDER BY relevance DESC
        LIMIT 2
        """
        result = tx.run(query, ComidaN=ComidaN, TempN=TempN, SaborN=SaborN, TexturaN=TexturaN, LugarN=LugarN, TipoN=TipoN, RateN=RateN)
        
        # Ensure at least 2 results are returned
        recommendations = [record["name"] for record in result]
        while len(recommendations) < 2:
            recommendations.append(None)
        
        return recommendations


# Configuración de conexión y ejecución de la creación de datos
uri = "neo4j+ssc://6ed9a403.databases.neo4j.io"
user = "neo4j"
password = "0iIoDYVv8wV4MZIcF_405l5muLHL3mMjuXN2tUevJ_w"

# Crear una instancia de la clase y ejecutar la creación de nodos y relaciones
example = Neo4j_C(uri, user, password)
# Se pasan los parámetros deseados
#example.create_nodes_and_relationships("Pepito", "Helado", "Frio", "Dulce", "Cremoso", "Restaurante", "Chatarra", "10")

example.mostrar_datos()

# pruebas 
#example.create_nodes_and_relationships("Juan", "Pizza", "Caliente", "Salado", "Suave", "Restaurante", "Chatarra", "9")
#example.create_nodes_and_relationships("David", "Helado", "Frio", "Dulce", "Cremoso", "Calle", "Chatarra", "7")
#example.create_nodes_and_relationships("Luis", "Nachos", "Templado", "Salado", "Crujiente", "Casa", "Chatarra", "10")
#example.create_nodes_and_relationships("Bran", "Lasagna", "Caliente", "Salado", "Suave", "Casa", "Chatarra", "10")
#example.create_nodes_and_relationships("Gabriel", "Gomitas", "Templado", "Acido", "Suave", "Calle", "Chatarra", "8")
#example.create_nodes_and_relationships("Jose", "Huevos", "Caliente", "Picante", "Cremoso", "Casa", "Saludable", "6")
#example.create_nodes_and_relationships("Padilla", "Chilaquiles", "Caliente", "Salado", "Suave", "Restaurante", "Chatarra", "8")
#example.create_nodes_and_relationships("Dom", "Chicharrones", "Caliente", "Picante", "Crujiente", "Calle", "Chatarra", "10")
#example.create_nodes_and_relationships("Anggie", "Pasta", "Caliente", "Salado", "Cremoso", "Restaurante", "Chatarra", "8")
#example.create_nodes_and_relationships("Quezada", "Sandwich", "Templado", "Salado", "Suave", "Casa", "Saludable", "5")
#example.create_nodes_and_relationships("Joni", "Carne", "Caliente", "Salado", "Suave", "Restaurante", "Saludable", "10")
#example.create_nodes_and_relationships("Díaz", "Shake", "Frio", "Dulce", "Liquído", "Casa", "Saludable", "5")
#example.create_nodes_and_relationships("Iris", "Ensalada", "Templado", "Salado", "Crujiente", "Restaurante", "Saludable", "6")
#example.create_nodes_and_relationships("Willfredo", "Papitas", "Caliente", "Salado", "Crujiente", "Calle", "Chatarra", "9")
#example.create_nodes_and_relationships("Patricio", "Donas", "Templado", "Dulce", "Suave", "Restaurante", "Chatarra", "6")
#example.create_nodes_and_relationships("Mario", "Coca", "Frio", "Dulce", "Liquido", "Calle", "Chatarra", "8")
#example.create_nodes_and_relationships("Rodrigo", "Hamburguesa", "Caliente", "Salado", "Suave", "Restaurante", "Chatarra", "10")
#example.create_nodes_and_relationships("Gerardo", "Pulpo", "Templado", "Salado", "Suave", "Restaurante", "Saludable", "4")
#example.create_nodes_and_relationships("Carmen", "Sopa", "Caliente", "Salado", "Liquido", "Casa", "Saludable", "9")
#example.create_nodes_and_relationships("Jack", "Cuquito", "Frio", "Dulce", "Liquido", "Casa", "Chatarra", "6")
#example.create_nodes_and_relationships("Pedro", "Pizza", "Caliente", "Salado", "Crujiente", "Casa", "Chatarra", "10")
#example.create_nodes_and_relationships("Lopez", "Sevenup", "Frio", "Dulce", "Liquido", "Restaurante", "Chatarra", "8")
#example.create_nodes_and_relationships("Martin", "Sprite", "Frio", "Dulce", "Liquido", "Restaurante", "Chatarra", "7")
#example.create_nodes_and_relationships("Lupita", "Medicina", "Templada", "Dulce", "Liquida", "Casa", "Saludable", "7")

#print(type(example.recomendar_comida("Sprite", "Frio", "Dulce", "Liquido", "Restaurante", "Chatarra", "10")))
# Cerrar la conexión al finalizar
#example.close()