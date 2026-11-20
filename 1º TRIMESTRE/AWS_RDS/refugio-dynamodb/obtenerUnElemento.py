from conectarse import conectarseDynamoDBResource


def obtenerUnElemento(perro_id=7, fecha="2025-10-03"):
    """Obtiene UN evento de historial_medico con get_item().
    Hay que indicar la clave completa (perro_id + fecha). ProjectionExpression elige los atributos."""
    dynamodb = conectarseDynamoDBResource()
    tabla = dynamodb.Table("historial_medico")

    respuesta = tabla.get_item(
        Key={"perro_id": perro_id, "fecha": fecha},
        ProjectionExpression="perro_id, fecha, tipo, descripcion, veterinario",
    )
    return respuesta.get("Item", {"mensaje": "No existe ningún evento con esa clave."})
