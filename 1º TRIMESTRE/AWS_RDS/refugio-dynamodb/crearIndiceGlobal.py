import time

from conectarse import conectarseDynamoDBCliente


def crearIndiceGlobal():
    """Añade a solicitudes_adopcion el índice global EstadoFechaIndex (si no existe).
    Permite consultar las solicitudes por estado (Pendiente, Aprobada, Rechazada) ordenadas por fecha."""
    client = conectarseDynamoDBCliente()
    tabla = "solicitudes_adopcion"
    indice = "EstadoFechaIndex"

    descripcion = client.describe_table(TableName=tabla)["Table"]
    existentes = [i["IndexName"] for i in descripcion.get("GlobalSecondaryIndexes", [])]
    if indice in existentes:
        return {"tabla": tabla, "indice": indice, "creado": False, "motivo": "Ya existía."}

    client.update_table(
        TableName=tabla,
        AttributeDefinitions=[
            {"AttributeName": "estado", "AttributeType": "S"},
            {"AttributeName": "fecha_solicitud", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexUpdates=[
            {
                "Create": {
                    "IndexName": indice,
                    "KeySchema": [
                        {"AttributeName": "estado", "KeyType": "HASH"},
                        {"AttributeName": "fecha_solicitud", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                }
            }
        ],
    )

    # El índice tarda un poco en estar ACTIVE: esperamos hasta que lo esté
    for _ in range(60):
        descripcion = client.describe_table(TableName=tabla)["Table"]
        estado = [i["IndexStatus"] for i in descripcion["GlobalSecondaryIndexes"]
                  if i["IndexName"] == indice][0]
        if estado == "ACTIVE":
            return {"tabla": tabla, "indice": indice, "creado": True, "estado": estado}
        time.sleep(5)
    return {"tabla": tabla, "indice": indice, "creado": True,
            "estado": estado, "aviso": "Aún se está creando; compruébalo en la consola."}
