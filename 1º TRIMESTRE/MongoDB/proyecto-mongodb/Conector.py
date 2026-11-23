from pymongo import MongoClient
from dotenv import load_dotenv
import os

class ConectorMongoDB():

    def conectarse(self):
        load_dotenv()

        usuario= os.getenv("USUARIO_MONGODB")
        password = os.getenv("PASSWORD_MONGODB")
        cluster= os.getenv("CLUSTER_MONGODB")
        dominio = os.getenv("DOMINIO_MONGODB")

        uri = f'mongodb+srv://{usuario}:{password}@{cluster}.{dominio}.mongodb.net/'

        cliente = MongoClient(uri,maxPoolSize=50)
        return cliente