# My SoulMate - Un Sistema de Recomendaciones  
## Fase 2. Implementando sistema de recomendaciones  

Universidad del Valle de Guatemala  
Facultad de Ingeniería  
Departamento de Ciencias de la Computación  
Algoritmos y Estructura de Datos  

Gabriel Bran - 23590  
David Dominguez - 23712  
Luis Padilla - 23663  

## Descripción del Proyecto
Este proyecto es una aplicación web desarrollada con Flask que permite a los usuarios registrarse, iniciar sesión, responder preguntas sobre sus preferencias de comida, y obtener recomendaciones de alimentos basadas en sus respuestas. La aplicación utiliza Firebase para la gestión de usuarios y Neo4j para las recomendaciones basadas en grafos.

## Requerimientos de Software
Python 3.x: Asegúrate de tener instalada la versión más reciente de Python 3.  
pip: La herramienta de gestión de paquetes para Python.  
Flask: Un micro framework para aplicaciones web en Python.  
Firebase Admin SDK: Para interactuar con Firebase.  
Neo4j: Para la base de datos de grafos.  
Credenciales de Firebase: Un archivo config.json con las credenciales de tu proyecto Firebase.  

## Instalación
Paso 1: Primero, clona el repositorio del proyecto.  
Paso 2: Instala las dependencias necesarias usando pip  
Librerías de Python  
Flask: Microframework web para Python.  

Uso: Manejo de rutas, renderización de plantillas HTML y gestión de peticiones HTTP.  
Instalación: pip install Flask  
firebase-admin: SDK de administración para Firebase.  

Uso: Conexión y operaciones con la base de datos en tiempo real de Firebase.  
Instalación: pip install firebase-admin  
neo4j: Driver oficial de Neo4j para Python.  

Uso: Conexión y operaciones con la base de datos de grafos Neo4j.  
Instalación: pip install neo4j  

n4j.DriverN4: Módulo propio para gestionar las operaciones con Neo4j.  
Uso: Contiene la clase Neo4j_C con métodos para crear nodos, establecer relaciones y obtener recomendaciones.  

## Uso
Paso 1: Ejecutar la base de datos en neo4j  
Paso 2: Ejecuta la aplicación Flask.
- python app.py  

Paso 3: Abre un navegador web y navega a http://127.0.0.1:5000/

## Funcionalidades
Registro de Usuarios  
Los usuarios pueden registrarse proporcionando un nombre de usuario y una contraseña. La información se almacena en Firebase.  

Inicio de Sesión  
Los usuarios pueden iniciar sesión con su nombre de usuario y contraseña. Las credenciales se verifican contra los datos almacenados en Firebase.  

Responder Preguntas  
Una vez que un usuario inicia sesión, puede responder a una serie de preguntas sobre sus preferencias de comida.  

Obtener Recomendaciones  
Basado en las respuestas del usuario, la aplicación consulta la base de datos Neo4j y proporciona dos recomendaciones de alimentos.  

## Estructura del Proyecto
Explicación breve de los archivos y directorios principales del proyecto.  

- app.py: Contiene la lógica principal de la aplicación Flask.  
- templates/: Directorio que contiene las plantillas HTML.  
 -Inicio.html  
 -login.html  
 -signin.html  
 -Preguntas.html  
 -Recomendaciones.html  
- static/: Directorio para archivos estáticos como CSS e Imagenes.  
-config.json: Archivo de configuración de Firebase.  
-n4j/DriverN4.py: Módulo que contiene la lógica de conexión y operaciones con Neo4j.  
-neo4j_snapshot.dump


