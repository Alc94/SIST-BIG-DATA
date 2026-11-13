import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

NOMBRE_INSTANCIA = "refugio-perros-db"

session = boto3.session.Session(
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
    aws_session_token=os.getenv("SESSION_TOKEN"),
    region_name=os.getenv("REGION"),
)

rds = session.client("rds")

# Si ya existe, no la volvemos a crear (así no da error al repetir el script)
try:
    rds.describe_db_instances(DBInstanceIdentifier=NOMBRE_INSTANCIA)
    print(f"La instancia '{NOMBRE_INSTANCIA}' ya existe.")
except ClientError as e:
    if e.response["Error"]["Code"] != "DBInstanceNotFound":
        raise
    print(f"Creando la instancia '{NOMBRE_INSTANCIA}'...")
    rds.create_db_instance(
        DBInstanceIdentifier=NOMBRE_INSTANCIA,  # Nombre de la instancia
        AllocatedStorage=20,                    # Tamaño en GiB
        DBInstanceClass="db.t4g.micro",         # Tipo de instancia
        Engine="mariadb",                       # Motor de base de datos
        MasterUsername=os.getenv("DB_USER"),    # Usuario
        MasterUserPassword=os.getenv("DB_PASSWORD"),
        PubliclyAccessible=True,                # Accesible desde fuera
    )

print("Esperando a que esté disponible (puede tardar 5-10 minutos)...")
waiter = rds.get_waiter("db_instance_available")
waiter.wait(DBInstanceIdentifier=NOMBRE_INSTANCIA)

info = rds.describe_db_instances(DBInstanceIdentifier=NOMBRE_INSTANCIA)
endpoint = info["DBInstances"][0]["Endpoint"]["Address"]

print("Instancia disponible.")
print(f"Endpoint: {endpoint}")