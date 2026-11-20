from decimal import Decimal

from conectarse import conectarseDynamoDBResource

# perro_id = id del perro en la tabla perros de RDS
HISTORIAL = [
    {"perro_id": 1, "fecha": "2025-01-16", "tipo": "Vacuna", "descripcion": "Rabia", "veterinario": "Dra. Soto", "coste": Decimal("25.00")},
    {"perro_id": 1, "fecha": "2025-03-02", "tipo": "Revisión", "descripcion": "Revisión general", "veterinario": "Dra. Soto", "coste": Decimal("30.00")},
    {"perro_id": 2, "fecha": "2025-02-21", "tipo": "Vacuna", "descripcion": "Polivalente", "veterinario": "Dr. Vega", "coste": Decimal("35.00")},
    {"perro_id": 2, "fecha": "2025-08-10", "tipo": "Cirugía", "descripcion": "Esterilización", "veterinario": "Dr. Vega", "coste": Decimal("120.00")},
    {"perro_id": 3, "fecha": "2025-03-06", "tipo": "Vacuna", "descripcion": "Rabia", "veterinario": "Dra. Soto", "coste": Decimal("25.00")},
    {"perro_id": 4, "fecha": "2025-03-19", "tipo": "Revisión", "descripcion": "Control de displasia", "veterinario": "Dr. Vega", "coste": Decimal("45.00")},
    {"perro_id": 4, "fecha": "2025-09-01", "tipo": "Vacuna", "descripcion": "Leishmaniasis", "veterinario": "Dra. Soto", "coste": Decimal("60.00")},
    {"perro_id": 5, "fecha": "2025-04-03", "tipo": "Vacuna", "descripcion": "Polivalente", "veterinario": "Dr. Vega", "coste": Decimal("35.00")},
    {"perro_id": 6, "fecha": "2025-04-26", "tipo": "Vacuna", "descripcion": "Rabia", "veterinario": "Dra. Soto", "coste": Decimal("25.00")},
    {"perro_id": 7, "fecha": "2025-05-11", "tipo": "Vacuna", "descripcion": "Rabia", "veterinario": "Dra. Soto", "coste": Decimal("25.00")},
    {"perro_id": 7, "fecha": "2025-10-03", "tipo": "Revisión", "descripcion": "Control dental", "veterinario": "Dr. Vega", "coste": Decimal("40.00")},
    {"perro_id": 8, "fecha": "2025-06-02", "tipo": "Vacuna", "descripcion": "Polivalente", "veterinario": "Dra. Soto", "coste": Decimal("35.00")},
    {"perro_id": 9, "fecha": "2025-06-16", "tipo": "Revisión", "descripcion": "Control geriátrico", "veterinario": "Dr. Vega", "coste": Decimal("50.00")},
    {"perro_id": 10, "fecha": "2025-07-02", "tipo": "Tratamiento", "descripcion": "Desparasitación", "veterinario": "Dr. Vega", "coste": Decimal("20.00")},
]

PASEOS = [
    {"perro_id": 1, "fecha_hora": "2025-10-01 09:00", "voluntario": "Laura", "duracion_min": 30, "comportamiento": ["tranquilo", "sociable"]},
    {"perro_id": 1, "fecha_hora": "2025-10-03 18:30", "voluntario": "Pablo", "duracion_min": 45, "comportamiento": ["enérgico"]},
    {"perro_id": 2, "fecha_hora": "2025-10-01 10:00", "voluntario": "Laura", "duracion_min": 30, "comportamiento": ["tímido"]},
    {"perro_id": 2, "fecha_hora": "2025-10-05 17:00", "voluntario": "Marta", "duracion_min": 40, "comportamiento": ["tranquilo"]},
    {"perro_id": 4, "fecha_hora": "2025-10-02 11:00", "voluntario": "Pablo", "duracion_min": 20, "comportamiento": ["nervioso", "tira de la correa"]},
    {"perro_id": 5, "fecha_hora": "2025-10-02 12:00", "voluntario": "Marta", "duracion_min": 35, "comportamiento": ["enérgico", "sociable"]},
    {"perro_id": 5, "fecha_hora": "2025-10-06 09:30", "voluntario": "Laura", "duracion_min": 30, "comportamiento": ["sociable"]},
    {"perro_id": 7, "fecha_hora": "2025-10-03 19:00", "voluntario": "Pablo", "duracion_min": 50, "comportamiento": ["enérgico", "obediente"]},
    {"perro_id": 7, "fecha_hora": "2025-10-07 18:00", "voluntario": "Marta", "duracion_min": 45, "comportamiento": ["obediente"]},
    {"perro_id": 8, "fecha_hora": "2025-10-04 10:30", "voluntario": "Laura", "duracion_min": 25, "comportamiento": ["juguetona"]},
    {"perro_id": 10, "fecha_hora": "2025-10-04 11:30", "voluntario": "Pablo", "duracion_min": 20, "comportamiento": ["tímido", "tranquilo"]},
    {"perro_id": 10, "fecha_hora": "2025-10-08 09:00", "voluntario": "Marta", "duracion_min": 30, "comportamiento": ["tranquilo"]},
]


def crearElementos():
    """Inserta elementos de ejemplo en historial_medico y registro_paseos con put_item."""
    dynamodb = conectarseDynamoDBResource()

    tabla_historial = dynamodb.Table("historial_medico")
    for evento in HISTORIAL:
        tabla_historial.put_item(Item=evento)

    tabla_paseos = dynamodb.Table("registro_paseos")
    for paseo in PASEOS:
        tabla_paseos.put_item(Item=paseo)

    return {"historial_medico": len(HISTORIAL), "registro_paseos": len(PASEOS)}
