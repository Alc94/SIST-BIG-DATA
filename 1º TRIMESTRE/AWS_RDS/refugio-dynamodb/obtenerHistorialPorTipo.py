from boto3.dynamodb.conditions import Key

from conectarse import conectarseDynamoDBResource


def obtenerHistorialPorTipo(perro_id=7, tipo="Revisión"):
    """query() con el ÍNDICE LOCAL TipoIndex de historial_medico:
    eventos de un perro concretos de un tipo (Vacuna, Revisión, Cirugía...)."""
    dynamodb = conectarseDynamoDBResource()
    tabla = dynamodb.Table("historial_medico")

    respuesta = tabla.query(
        IndexName="TipoIndex",  # Nombre del índice local
        KeyConditionExpression=Key("perro_id").eq(perro_id) & Key("tipo").eq(tipo),
    )
    return respuesta["Items"]