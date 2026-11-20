from conectarse import conectarseDynamoDBCliente


def crearTablaRegistroPaseos():
    """Crea la tabla registro_paseos (si no existe).
    Clave de partición: perro_id (id del perro en RDS). Clave de ordenación: fecha_hora (AAAA-MM-DD HH:MM)."""
    client = conectarseDynamoDBCliente()
    nombre = "registro_paseos"

    if nombre in client.list_tables()["TableNames"]:
        return {"tabla": nombre, "creada": False, "motivo": "Ya existía."}

    client.create_table(
        TableName=nombre,
        AttributeDefinitions=[
            {"AttributeName": "perro_id", "AttributeType": "N"},    # Partition Key
            {"AttributeName": "fecha_hora", "AttributeType": "S"},  # Sort Key
        ],
        KeySchema=[
            {"AttributeName": "perro_id", "KeyType": "HASH"},       # Partition Key
            {"AttributeName": "fecha_hora", "KeyType": "RANGE"},    # Sort Key
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,   # Lecturas por segundo
            "WriteCapacityUnits": 5,  # Escrituras por segundo
        },
    )
    # Waiter: esperamos a que la tabla esté lista
    client.get_waiter("table_exists").wait(TableName=nombre)
    return {"tabla": nombre, "creada": True}
