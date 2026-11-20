import json
from decimal import Decimal

from crearTablaHistorialMedico import crearTablaHistorialMedico
from crearTablaRegistroPaseos import crearTablaRegistroPaseos
from crearTablaSolicitudesAdopcion import crearTablaSolicitudesAdopcion
from crearIndiceGlobal import crearIndiceGlobal
from crearElementos import crearElementos
from crearElementosJSON import crearElementosJSON
from mostrarElementos import mostrarElementos
from obtenerUnElemento import obtenerUnElemento
from obtenerHistorialPorTipo import obtenerHistorialPorTipo
from obtenerSolicitudesPorEstado import obtenerSolicitudesPorEstado
from obtenerElementosPartiQL import obtenerElementosPartiQL


def convertir(obj):
    """Los números de DynamoDB llegan como Decimal: los pasamos a int o float para el JSON."""
    if isinstance(obj, Decimal):
        return int(obj) if obj == obj.to_integral_value() else float(obj)
    return str(obj)


def ejecutar(numero, funcion, descripcion):
    """Muestra qué función se ejecuta, qué hace y su resultado en JSON."""
    print("\n" + "=" * 70)
    print(f"PASO {numero} | Función a ejecutar: {funcion.__name__}()")
    print(f"Qué hace: {descripcion}")
    print("-" * 70)
    resultado = funcion()
    print("Resultado:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False, default=convertir))


if __name__ == "__main__":
    print("GESTIÓN DE DYNAMODB - REFUGIO DE PERROS")
    ejecutar(1, crearTablaHistorialMedico,
             "Crea la tabla historial_medico (perro_id + fecha) con el índice local TipoIndex.")
    ejecutar(2, crearTablaRegistroPaseos,
             "Crea la tabla registro_paseos (perro_id + fecha_hora) si no existe.")
    ejecutar(3, crearTablaSolicitudesAdopcion,
             "Crea la tabla solicitudes_adopcion (adoptante_id + fecha_solicitud) si no existe.")
    ejecutar(4, crearIndiceGlobal,
             "Añade a solicitudes_adopcion el índice global EstadoFechaIndex (estado + fecha_solicitud).")
    ejecutar(5, crearElementos,
             "Inserta historial médico y paseos de ejemplo (put_item). Si ya existen, se sobrescriben sin duplicar.")
    ejecutar(6, crearElementosJSON,
             "Inserta solicitudes de adopción con cuestionario (mapas, listas, decimales y nulos).")
    ejecutar(7, mostrarElementos,
             "scan() con filtro: vacunas de historial_medico desde el 2025-04-01.")
    ejecutar(8, obtenerUnElemento,
             "get_item(): un evento concreto (perro 7, 2025-10-03) con solo algunos atributos.")
    ejecutar(9, obtenerHistorialPorTipo,
             "query() con el índice local TipoIndex: revisiones del perro 7.")
    ejecutar(10, obtenerSolicitudesPorEstado,
             "query() con el índice global EstadoFechaIndex: solicitudes de adopción pendientes.")
    ejecutar(11, obtenerElementosPartiQL,
             "PartiQL: paseos del voluntario Pablo de 45 minutos o más (execute_statement con el client).")