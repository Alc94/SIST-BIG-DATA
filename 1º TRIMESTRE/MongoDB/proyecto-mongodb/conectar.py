from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

usuario= os.getenv("USUARIO_MONGODB")
password = os.getenv("PASSWORD_MONGODB")
cluster= os.getenv("CLUSTER_MONGODB")
dominio = os.getenv("DOMINIO_MONGODB")


cliente = MongoClient(f'mongodb+srv://{usuario}:{password}@{cluster}.{dominio}.mongodb.net/')

try:
    cliente.admin.command('ping')
    print("NOS CONECTAMOS CORRECTAMENTE")

except Exception as e:
    print("Error al conectar a MongoDB:", e)