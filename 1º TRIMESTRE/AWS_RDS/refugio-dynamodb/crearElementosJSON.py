from decimal import Decimal

from conectarse import conectarseDynamoDBResource

# adoptante_id = id del adoptante en la tabla adoptantes de RDS
# perro_id_interes = id del perro por el que se interesa (tabla perros de RDS)
# Cada solicitud tiene un cuestionario distinto: eso es lo que encaja bien en DynamoDB
SOLICITUDES = [
    {"adoptante_id": 1, "fecha_solicitud": "2025-03-20", "estado": "Aprobada", "perro_id_interes": 3,
     "cuestionario": {"vivienda": "Piso", "tiene_patio": False, "horas_solo_al_dia": Decimal("4.5"),
                      "otras_mascotas": ["gato"]},
     "notas": "Visita previa realizada.", "fecha_resolucion": "2025-04-10"},
    {"adoptante_id": 2, "fecha_solicitud": "2025-05-01", "estado": "Aprobada", "perro_id_interes": 6,
     "cuestionario": {"vivienda": "Casa con patio", "tiene_patio": True, "horas_solo_al_dia": Decimal("3"),
                      "otras_mascotas": []},
     "notas": "Familia con niños.", "fecha_resolucion": "2025-05-30"},
    {"adoptante_id": 3, "fecha_solicitud": "2025-07-01", "estado": "Aprobada", "perro_id_interes": 9,
     "cuestionario": {"vivienda": "Piso", "tiene_patio": False, "horas_solo_al_dia": Decimal("2"),
                      "otras_mascotas": ["perro"], "experiencia": "Ha tenido perros mayores"},
     "notas": "Busca un perro tranquilo.", "fecha_resolucion": "2025-07-20"},
    {"adoptante_id": 3, "fecha_solicitud": "2025-02-10", "estado": "Rechazada", "perro_id_interes": 4,
     "cuestionario": {"vivienda": "Piso pequeño", "tiene_patio": False, "horas_solo_al_dia": Decimal("9"),
                      "otras_mascotas": []},
     "notas": "Demasiadas horas solo.", "fecha_resolucion": "2025-02-18"},
    {"adoptante_id": 1, "fecha_solicitud": "2025-09-15", "estado": "Pendiente", "perro_id_interes": 1,
     "cuestionario": {"vivienda": "Piso", "tiene_patio": False, "horas_solo_al_dia": Decimal("4"),
                      "otras_mascotas": ["gato"]},
     "notas": None, "fecha_resolucion": None},
    {"adoptante_id": 2, "fecha_solicitud": "2025-10-02", "estado": "Pendiente", "perro_id_interes": 7,
     "cuestionario": {"vivienda": "Casa con patio", "tiene_patio": True, "horas_solo_al_dia": Decimal("3"),
                      "otras_mascotas": ["perro"]},
     "notas": "Quiere un perro grande.", "fecha_resolucion": None},
]


def crearElementosJSON():
    """Inserta solicitudes de adopción (elementos con mapas, listas, decimales y nulos) con put_item."""
    dynamodb = conectarseDynamoDBResource()
    tabla = dynamodb.Table("solicitudes_adopcion")
    for solicitud in SOLICITUDES:
        tabla.put_item(Item=solicitud)
    return {"solicitudes_adopcion": len(SOLICITUDES)}
