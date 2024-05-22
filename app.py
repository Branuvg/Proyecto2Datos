from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db

# Importa tu módulo de Neo4j aquí
from n4j.DriverN4 import *

app = Flask(__name__)

# Variable global para almacenar recomendaciones
dos_recomendaciones = []

# Inicializa la aplicación de Firebase
def initialize_firebase():
    try:
        # Carga las credenciales de Firebase desde el archivo JSON
        cred = credentials.Certificate('config.json')
        
        # Inicializa la aplicación de Firebase con la URL de la base de datos
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://dbdatos-a185d-default-rtdb.firebaseio.com"
        })
    except Exception as e:
        print(f"Error al inicializar Firebase: {e}")

initialize_firebase()

# Agrega un nuevo usuario a la base de datos
def agregar_usuario(nombre, contraseña):
    try:
        ref = db.reference("/usuarios")
        nuevo_usuario_ref = ref.push()
        nuevo_usuario_ref.set({
            "name": nombre,
            "contraseña": contraseña
        })
        print(f"Usuario {nombre} agregado con éxito.")
    except firebase_admin.exceptions.FirebaseError as e:
        print(f"Error al agregar usuario a Firebase: {e}")
    except Exception as e:
        print(f"Se produjo un error: {e}")

# Verifica las credenciales del usuario
def verificar_usuario(nombre, contraseña):
    try:
        ref = db.reference("/usuarios")
        usuarios = ref.get()
        if usuarios is not None:
            for key, usuario in usuarios.items():
                if usuario['name'] == nombre and usuario['contraseña'] == contraseña:
                    return True
        return False
    except firebase_admin.exceptions.FirebaseError as e:
        print(f"Error al verificar usuario en Firebase: {e}")
        return False
    except Exception as e:
        print(f"Se produjo un error: {e}")
        return False

# ----------------- Flask --------------------------------

@app.route('/')
def inicio():
    return render_template('Inicio.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/login', methods=['POST'])
def handle_login():
    name = request.form['name']
    password = request.form['password']
    if verificar_usuario(name, password):
        return redirect(url_for('preguntas', nombre_usuario=name))
    else:
        return redirect(url_for('login'))  # Redirige al login si la verificación falla

@app.route('/register', methods=['POST'])
def handle_register():
    name = request.form['name']
    password = request.form['password']
    agregar_usuario(name, password)
    return redirect(url_for('login'))

@app.route('/preguntas')
def preguntas():
    nombre_usuario = request.args.get('nombre_usuario')
    return render_template('Preguntas.html', nombre_usuario=nombre_usuario)

@app.route('/procesar_preguntas', methods=['POST'])
def procesar_preguntas():
    # Captura los datos del formulario
    nombre_usuario = request.form['usuario']
    comida = request.form['comida']
    q1 = request.form['q1']
    q2 = request.form['q2']
    q3 = request.form['q3']
    q4 = request.form['q4']
    q5 = request.form['q5']
    rating = request.form['rating']
    
    # Llama a otra función pasando los datos como parámetros
    procesar_respuestas(nombre_usuario, comida, q1, q2, q3, q4, q5, rating)
    
    return redirect(url_for('recomendaciones'))

@app.route('/recomendaciones')
def recomendaciones():
    return render_template('Recomendaciones.html', recomendaciones=dos_recomendaciones)

def procesar_respuestas(nombre_usuario, comida, q1, q2, q3, q4, q5, rating):
    # Aquí puedes procesar las respuestas como desees
    print(f"Usuario: {nombre_usuario}")
    print(f"Comida: {comida}")
    print(f"Q1: {q1}")
    print(f"Q2: {q2}")
    print(f"Q3: {q3}")
    print(f"Q4: {q4}")
    print(f"Q5: {q5}")
    print(f"Rating: {rating}")

    # UserN, ComidaN, TempN, SaborN, TexturaN, LugarN, TipoN, RateN
    example.create_nodes_and_relationships(nombre_usuario, comida, q1, q2, q3, q4, q5, rating)

    global dos_recomendaciones
    dos_recomendaciones = example.recomendar_comida(comida, q1, q2, q3, q4, q5, rating)
    example.close()

if __name__ == "__main__":
    app.run(debug=True)
