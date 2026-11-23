from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# VARIABLES DE ENTORNO
usuario= os.getenv("USUARIO_MONGODB")
password = os.getenv("PASSWORD_MONGODB")
cluster= os.getenv("CLUSTER_MONGODB")
dominio = os.getenv("DOMINIO_MONGODB")

cliente = MongoClient(f'mongodb+srv://{usuario}:{password}@{cluster}.{dominio}.mongodb.net/')

# 1º Se crea la base de datos
baseDatos = cliente["mi_primera_base_datos"]
# 2º Se crea la coleccion
coleccion = baseDatos["mi_primera_coleccion"]
# 3º Se crea un documento
documento = { "nombre": "Alejandro", "apellido": "López" }
# Se inserta el documento en la coleccion
insercion = coleccion.insert_one(documento)