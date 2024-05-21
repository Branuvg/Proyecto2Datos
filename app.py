from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

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
        return redirect(url_for('preguntas'))
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
    return render_template('Preguntas.html')

if __name__ == "__main__":
    app.run(debug=True)
