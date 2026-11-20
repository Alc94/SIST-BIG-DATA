import json
import os

from mostrarElementos import mostrarElementos
from obtenerPerrosRDS import obtenerPerrosRDS
from utilidades import convertir

# ---- Filtros (cámbialos para probar otras combinaciones) ----
ESTADO = "Disponible"    # RDS: Disponible | En acogida | Adoptado (None = todos)
TAMANO = None            # RDS: Pequeño | Mediano | Grande (None = todos)
TIPO = "Vacuna"          # DynamoDB: Vacuna | Revisión | Cirugía | Tratamiento
DESDE = "2025-04-01"     # DynamoDB: fecha mínima AAAA-MM-DD


def titulo(numero, funcion, descripcion):
    print("\n" + "=" * 70)
    print(f"PASO {numero} | Función a ejecutar: {funcion}")
    print(f"Qué hace: {descripcion}")
    print("-" * 70)


def unirBasesDatos(perros, eventos):
    """Une los perros de RDS con sus eventos médicos de DynamoDB usando perro_id."""
    eventos_por_perro = {}
    for evento in eventos:
        eventos_por_perro.setdefault(evento["perro_id"], []).append({
            "fecha": evento["fecha"],
            "tipo": evento["tipo"],
            "descripcion": evento["descripcion"],
            "veterinario": evento["veterinario"],
            "coste": evento["coste"],
        })

    unificado = []
    for perro in perros:
        historial = eventos_por_perro.get(perro["perro_id"], [])
        unificado.append({
            **perro,
            "historial_medico": historial,
            "total_eventos": len(historial),
            "coste_total": sum(e["coste"] for e in historial),
        })
    return unificado


if __name__ == "__main__":
    print("UNIÓN DE RDS Y DYNAMODB - REFUGIO DE PERROS")

    titulo(1, "obtenerPerrosRDS()",
           f"Consulta RDS: perros con estado='{ESTADO}' y tamaño='{TAMANO or 'cualquiera'}'.")
    perros = obtenerPerrosRDS(estado=ESTADO, tamano=TAMANO)
    print(f"Perros encontrados en RDS: {len(perros)}")

    titulo(2, "mostrarElementos()",
           f"Consulta DynamoDB (scan con filtro): eventos de tipo '{TIPO}' desde {DESDE}.")
    eventos = mostrarElementos(tipo=TIPO, desde=DESDE)
    print(f"Eventos encontrados en DynamoDB: {len(eventos)}")

    titulo(3, "unirBasesDatos()",
           "Une ambos resultados por perro_id y guarda un único archivo JSON.")
    resultado = {
        "filtros": {"rds": {"estado": ESTADO, "tamano": TAMANO},
                    "dynamodb": {"tipo": TIPO, "desde": DESDE}},
        "total_perros": len(perros),
        "perros": unirBasesDatos(perros, eventos),
    }

    carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salida")
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, "refugio_unificado.json")
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(resultado, archivo, indent=2, ensure_ascii=False, default=convertir)

    print("Resultado:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False, default=convertir))
    print(f"\nArchivo generado: {ruta}")