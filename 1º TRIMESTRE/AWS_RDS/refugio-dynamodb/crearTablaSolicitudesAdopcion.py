from conectarse import conectarseDynamoDBCliente


def crearTablaSolicitudesAdopcion():
    """Crea la tabla solicitudes_adopcion (si no existe).
    Clave de partición: adoptante_id (id del adoptante en RDS). Clave de ordenación: fecha_solicitud (AAAA-MM-DD)."""
    client = conectarseDynamoDBCliente()
    nombre = "solicitudes_adopcion"

    if nombre in client.list_tables()["TableNames"]:
        return {"tabla": nombre, "creada": False, "motivo": "Ya existía."}

    client.create_table(
        TableName=nombre,
        AttributeDefinitions=[
            {"AttributeName": "adoptante_id", "AttributeType": "N"},     # Partition Key
            {"AttributeName": "fecha_solicitud", "AttributeType": "S"},  # Sort Key
        ],
        KeySchema=[
            {"AttributeName": "adoptante_id", "KeyType": "HASH"},        # Partition Key
            {"AttributeName": "fecha_solicitud", "KeyType": "RANGE"},    # Sort Key
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,   # Lecturas por segundo
            "WriteCapacityUnits": 5,  # Escrituras por segundo
        },
    )
    # Waiter: esperamos a que la tabla esté lista
    client.get_waiter("table_exists").wait(TableName=nombre)
    return {"tabla": nombre, "creada": True}
