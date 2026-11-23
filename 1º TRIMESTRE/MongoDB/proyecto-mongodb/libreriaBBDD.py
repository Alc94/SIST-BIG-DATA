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

libreriaBD = cliente["libreria"]
librosColeccion = libreriaBD["libros"]
libros = [
   { "titulo": "Cien Años de Soledad", "paginas": 417, "precio": 19.99,"disponible": True },
   { "titulo": "1984", "paginas": 328, "precio": 14.50, "disponible": False },
   { "titulo": "Don Quijote de la Mancha", "paginas": 1072, "precio": 24.99, "disponible": True },
   { "titulo": "El Principito", "paginas": 96, "precio": 7.99, "disponible": False }
]

libros_creados = librosColeccion.insert_many(libros)
print(libros_creados.inserted_ids)