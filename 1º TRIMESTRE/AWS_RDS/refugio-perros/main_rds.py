import json
import rds_funciones as rds

def ejecutar(numero, funcion, descripcion):
    print("\n" + "=" * 70)
    print(f"PASO {numero} | Función a ejecutar: {funcion.__name__}()")
    print(f"Qué hace: {descripcion}")
    print("-" * 70)
    resultado = funcion()
    print("Resultado:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))


print("GESTIÓN DE LA BASE DE DATOS RDS - REFUGIO DE PERROS")
ejecutar(1, rds.crear_base_datos, "Crea la base de datos del refugio si no existe.")
ejecutar(2, rds.crear_tablas, "Crea las tablas razas, perros, adoptantes y adopciones.")
ejecutar(3, rds.insertar_datos_ejemplo, "Inserta datos de ejemplo del refugio (solo si no hay datos).")
ejecutar(4, rds.consulta_perros_disponibles, "CONSULTA 1: perros disponibles para adopción con su raza y tamaño.")
ejecutar(5, rds.consulta_perros_por_estado, "CONSULTA 2: cuántos perros hay en cada estado.")
ejecutar(6, rds.consulta_adopciones, "CONSULTA 3: adopciones realizadas con perro, raza y adoptante.")