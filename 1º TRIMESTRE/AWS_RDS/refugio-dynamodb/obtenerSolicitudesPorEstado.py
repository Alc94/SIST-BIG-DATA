from boto3.dynamodb.conditions import Key

from conectarse import conectarseDynamoDBResource


def obtenerSolicitudesPorEstado(estado="Pendiente"):
    """query() con el ÍNDICE GLOBAL EstadoFechaIndex de solicitudes_adopcion:
    todas las solicitudes con ese estado, ordenadas por fecha, sin recorrer toda la tabla."""
    dynamodb = conectarseDynamoDBResource()
    tabla = dynamodb.Table("solicitudes_adopcion")

    respuesta = tabla.query(
        IndexName="EstadoFechaIndex",            # Nombre del índice global
        KeyConditionExpression=Key("estado").eq(estado),
        ScanIndexForward=True,                   # True = fecha ascendente, False = descendente
    )
    return respuesta["Items"]