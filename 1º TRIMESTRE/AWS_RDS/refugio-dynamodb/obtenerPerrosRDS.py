import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def obtenerPerrosRDS(estado="Disponible", tamano=None):
    """Consulta RDS (MariaDB) con filtros opcionales: estado del perro y tamaño de su raza."""
    cnx = mysql.connector.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME"),
        connection_timeout=15,
        use_pure=True,  # Usa el conector en Python puro: evita fallos de la extensión C en Windows
    )
    cursor = cnx.cursor(dictionary=True)

    sql = """
        SELECT p.id AS perro_id, p.nombre, r.nombre AS raza, r.tamano,
               p.sexo, p.estado, p.fecha_ingreso
        FROM perros p JOIN razas r ON r.id = p.raza_id
        WHERE 1 = 1"""
    parametros = []
    if estado:
        sql += " AND p.estado = %s"
        parametros.append(estado)
    if tamano:
        sql += " AND r.tamano = %s"
        parametros.append(tamano)
    sql += " ORDER BY p.id"

    cursor.execute(sql, parametros)
    perros = cursor.fetchall()
    cursor.close()
    cnx.close()
    return perros