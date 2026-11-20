from conectarse import conectarseDynamoDBCliente


def crearTablaHistorialMedico():
    """Crea la tabla historial_medico (si no existe).
    Clave de partición: perro_id (id del perro en RDS). Clave de ordenación: fecha (AAAA-MM-DD).
    Índice local TipoIndex: mismo perro_id pero ordenado por tipo (Vacuna, Revisión, Cirugía...)."""
    client = conectarseDynamoDBCliente()
    nombre = "historial_medico"

    if nombre in client.list_tables()["TableNames"]:
        return {"tabla": nombre, "creada": False, "motivo": "Ya existía."}

    client.create_table(
        TableName=nombre,
        AttributeDefinitions=[
            {"AttributeName": "perro_id", "AttributeType": "N"},  # Partition Key
            {"AttributeName": "fecha", "AttributeType": "S"},     # Sort Key tabla principal
            {"AttributeName": "tipo", "AttributeType": "S"},      # Sort Key del índice local
        ],
        KeySchema=[
            {"AttributeName": "perro_id", "KeyType": "HASH"},     # Partition Key
            {"AttributeName": "fecha", "KeyType": "RANGE"},       # Sort Key
        ],
        LocalSecondaryIndexes=[
            {
                "IndexName": "TipoIndex",
                "KeySchema": [
                    {"AttributeName": "perro_id", "KeyType": "HASH"},
                    {"AttributeName": "tipo", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},  # Puede ser ALL, KEYS_ONLY o INCLUDE
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,   # Lecturas por segundo
            "WriteCapacityUnits": 5,  # Escrituras por segundo
        },
    )
    # Waiter: esperamos a que la tabla esté lista
    client.get_waiter("table_exists").wait(TableName=nombre)
    return {"tabla": nombre, "creada": True, "indice_local": "TipoIndex"}
