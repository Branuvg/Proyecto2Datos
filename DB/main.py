import firebase_admin
from firebase_admin import credentials, db

# Inicializa la aplicación de Firebase
def initialize_firebase():
    try:
        # Carga las credenciales de Firebase desde el archivo JSON
        cred = credentials.Certificate('DB/credentials.json')
        
        # Inicializa la aplicación de Firebase con la URL de la base de datos
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://dbdatos-a185d-default-rtdb.firebaseio.com"  # Asegúrate de que esta URL sea la correcta para tu base de datos
        })
    except Exception as e:
        print(f"Error al inicializar Firebase: {e}")

# Agrega un nuevo usuario a la base de datos
def agregar_usuario(nombre, contraseña):
    try:
        ref = db.reference("/usuarios")  # Cambio a /usuarios para permitir múltiples entradas
        nuevo_usuario_ref = ref.push()  # Crea una nueva referencia única
        nuevo_usuario_ref.set({
            "name": nombre,
            "contraseña": contraseña
        })
        print(f"Usuario {nombre} agregado con éxito.")
    except firebase_admin.exceptions.FirebaseError as e:
        print(f"Error al agregar usuario a Firebase: {e}")
    except Exception as e:
        print(f"Se produjo un error: {e}")

# Obtén todos los usuarios de la base de datos
def obtener_usuarios():
    try:
        ref = db.reference("/usuarios")
        usuarios = ref.get()
        
        if usuarios is not None:
            for key, usuario in usuarios.items():
                print(f"ID: {key}, Nombre: {usuario['name']}, contraseña : {usuario['contraseña']}")
        else:
            print("No se encontraron usuarios.")
    except firebase_admin.exceptions.FirebaseError as e:
        print(f"Error al obtener usuarios de Firebase: {e}")
    except Exception as e:
        print(f"Se produjo un error: {e}","**")

if __name__ == "__main__":
    initialize_firebase()

    # Agrega nuevos usuarios
    agregar_usuario("Dom", "zxxzxl")
    agregar_usuario("Bran", "xjhxcs")
    agregar_usuario("Luis", "ajjsjs")

    # Obtén y muestra todos los usuarios
    obtener_usuarios()
