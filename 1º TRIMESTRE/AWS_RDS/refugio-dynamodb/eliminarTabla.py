from botocore.exceptions import ClientError

from conectarse import conectarseDynamoDBCliente


def eliminarTabla(nombre):
    """Elimina una tabla de DynamoDB (si existe)."""
    client = conectarseDynamoDBCliente()
    try:
        client.delete_table(TableName=nombre)
        client.get_waiter("table_not_exists").wait(TableName=nombre)
        return {"tabla": nombre, "eliminada": True}
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            return {"tabla": nombre, "eliminada": False, "motivo": "No existía."}
        raise
