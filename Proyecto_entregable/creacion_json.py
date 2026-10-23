import json
import mysql.connector
import psycopg2
import pymysql
from datetime import date
from decimal import Decimal

# Helper para que json.dump pueda procesar fechas y decimales sin dar error
def conversor_json(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Tipo {type(obj)} no serializable")

def exportar_a_json(nombre_archivo, explicacion, datos, columnas):
    # Formatear los resultados en una lista de diccionarios
    resultados = [dict(zip(columnas, fila)) for fila in datos]
    
    estructura_final = {
        "explicacion_del_analisis": explicacion,
        "total_registros": len(resultados),
        "datos": resultados
    }
    
    with open(nombre_archivo, 'w', encoding='utf-8') as file:
        json.dump(estructura_final, file, default=conversor_json, indent=4, ensure_ascii=False)
    print(f"Archivo '{nombre_archivo}' generado correctamente.")

def main():
    # 1. ANÁLISIS MYSQL: Eficacia de Adopciones
    # Cruza Dogs, Adopters y Adoptions para evaluar la salida de perros del refugio.
    try:
        conn_mysql = mysql.connector.connect(
            host='127.0.0.1', port=3306, user='root', password='mi_password', database='refugio_db'
        )
        cursor_mysql = conn_mysql.cursor()
        query_mysql = """
            SELECT d.name AS perro, d.breed AS raza, a.first_name AS adoptante, a.email, ad.adoption_date AS fecha_adopcion
            FROM Adoptions ad
            JOIN Dogs d ON ad.dog_id = d.id
            JOIN Adopters a ON ad.adopter_id = a.id
            ORDER BY ad.adoption_date DESC;
        """
        cursor_mysql.execute(query_mysql)
        datos_mysql = cursor_mysql.fetchall()
        columnas_mysql = [desc[0] for desc in cursor_mysql.description]
        
        explicacion_mysql = "Importante para el negocio: Permite analizar la tasa de éxito del refugio cruzando los perros adoptados con los datos de contacto de sus nuevos dueños. Es vital para realizar seguimientos post-adopción y evaluar qué razas encuentran hogar más rápido."
        exportar_a_json('analisis_adopciones_mysql.json', explicacion_mysql, datos_mysql, columnas_mysql)
        
        cursor_mysql.close()
        conn_mysql.close()
    except Exception as e:
        print(f"Error en MySQL: {e}")

    # 2. ANÁLISIS POSTGRESQL: Impacto Financiero Médico
    # Cruza Dogs, Medical_records y Veterinarians para analizar gastos.
    try:
        conn_pg = psycopg2.connect(
            host='127.0.0.1', port=5432, user='postgres', password='mi_password', database='refugio_postgres'
        )
        cursor_pg = conn_pg.cursor()
        query_pg = """
            SELECT d.name AS perro, m.visit_day AS fecha_visita, m.diagnosis AS diagnostico, m.cost AS coste, v.clinic_name AS clinica
            FROM Medical_records m
            JOIN Dogs d ON m.dog_id = d.id
            JOIN Veterinarians v ON m.veterinarian_id = v.id
            ORDER BY m.cost DESC;
        """
        cursor_pg.execute(query_pg)
        datos_pg = cursor_pg.fetchall()
        columnas_pg = [desc[0] for desc in cursor_pg.description]
        
        explicacion_pg = "Importante para el negocio: Controla el mayor gasto de un refugio (veterinario). Cruzar el historial médico con las clínicas externas permite auditar qué tratamientos consumen más presupuesto y negociar tarifas con las clínicas más visitadas."
        exportar_a_json('analisis_gastos_medicos_postgres.json', explicacion_pg, datos_pg, columnas_pg)
        
        cursor_pg.close()
        conn_pg.close()
    except Exception as e:
        print(f"Error en PostgreSQL: {e}")

    # 3. ANÁLISIS MARIADB: Gestión de Recursos Humanos (Voluntarios)
    # Cruza Volunteers, Dog_assignments y Dogs para evaluar la carga de trabajo.
    try:
        conn_maria = pymysql.connect(
            host='127.0.0.1', port=3307, user='root', password='mi_password', database='refugio_mariadb'
        )
        cursor_maria = conn_maria.cursor()
        query_maria = """
            SELECT v.first_name AS voluntario, v.phone AS telefono, da.care_role AS tarea, d.name AS perro, da.assignment_date AS fecha
            FROM Dog_assignments da
            JOIN Volunteers v ON da.volunteer_id = v.id
            JOIN Dogs d ON da.dog_id = d.id
            ORDER BY da.assignment_date DESC;
        """
        cursor_maria.execute(query_maria)
        datos_maria = cursor_maria.fetchall()
        columnas_maria = [desc[0] for desc in cursor_maria.description]
        
        explicacion_maria = "Importante para el negocio: Optimiza la logística diaria. Al cruzar los voluntarios con las tareas asignadas a perros concretos, los coordinadores del refugio garantizan que ningún animal se quede sin cuidado y evalúan el compromiso de los voluntarios."
        exportar_a_json('analisis_voluntariado_mariadb.json', explicacion_maria, datos_maria, columnas_maria)
        
        cursor_maria.close()
        conn_maria.close()
    except Exception as e:
        print(f"Error en MariaDB: {e}")

if __name__ == "__main__":
    main()