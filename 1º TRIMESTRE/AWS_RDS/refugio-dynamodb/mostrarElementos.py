from boto3.dynamodb.conditions import Attr

from conectarse import conectarseDynamoDBResource


def mostrarElementos(tipo="Vacuna", desde="2025-04-01"):
    """Recorre historial_medico con scan() y devuelve solo los eventos del tipo indicado
    con fecha igual o posterior a 'desde' (FilterExpression)."""
    dynamodb = conectarseDynamoDBResource()
    tabla = dynamodb.Table("historial_medico")

    parametros = {"FilterExpression": Attr("tipo").eq(tipo) & Attr("fecha").gte(desde)}
    elementos = []
    while True:
        respuesta = tabla.scan(**parametros)
        elementos.extend(respuesta["Items"])
        # Si hay más páginas de resultados, seguimos desde donde se quedó
        if "LastEvaluatedKey" not in respuesta:
            break
        parametros["ExclusiveStartKey"] = respuesta["LastEvaluatedKey"]

    return sorted(elementos, key=lambda e: (e["perro_id"], e["fecha"]))
