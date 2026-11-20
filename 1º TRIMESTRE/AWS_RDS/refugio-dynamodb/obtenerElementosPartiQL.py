from boto3.dynamodb.types import TypeDeserializer

from conectarse import conectarseDynamoDBCliente


def obtenerElementosPartiQL(voluntario="Pablo", duracion_minima=45):
    """PartiQL (SQL para DynamoDB) con execute_statement() usando el CLIENT:
    paseos hechos por un voluntario que duraron al menos 'duracion_minima' minutos."""
    client = conectarseDynamoDBCliente()

    consulta = (
        'SELECT perro_id, fecha_hora, voluntario, duracion_min, comportamiento '
        'FROM "registro_paseos" '
        f"WHERE voluntario = '{voluntario}' AND duracion_min >= {int(duracion_minima)}"
    )
    respuesta = client.execute_statement(Statement=consulta)

    # El client devuelve los valores con su tipo ({'N': '7'}, {'S': 'Pablo'}...):
    # los convertimos a valores normales de Python
    deserializador = TypeDeserializer()
    elementos = [{clave: deserializador.deserialize(valor) for clave, valor in elemento.items()}
                 for elemento in respuesta["Items"]]
    return sorted(elementos, key=lambda e: (e["perro_id"], e["fecha_hora"]))