import os

import boto3
from dotenv import load_dotenv

load_dotenv()

session = boto3.session.Session(
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
    aws_session_token=os.getenv("SESSION_TOKEN"),
    region_name=os.getenv("REGION"),
)

client_rds = session.client("rds")
instancias = client_rds.describe_db_instances()["DBInstances"]
print("Instancias RDS:", [i["DBInstanceIdentifier"] for i in instancias])

print("Conexión correcta con AWS.")