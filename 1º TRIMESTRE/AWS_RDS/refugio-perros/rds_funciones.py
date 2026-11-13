import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")


def conectar(con_base_de_datos=True):
    """Abre la conexión con RDS. Sin base de datos sirve para poder crearla."""
    config = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "connection_timeout": 15,
        # "use_pure": True -> Usa la implementación en Python pura del conector:
        # evita fallos de la extensión C en Windows y muestra bien los errores de conexión
        "use_pure": True,
    }
    
    if con_base_de_datos:
        config["database"] = DB_NAME
    return mysql.connector.connect(**config)


def crear_base_datos():
    cnx = conectar(con_base_de_datos=False)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute("SHOW DATABASES")
    bases = [fila["Database"] for fila in cursor.fetchall()]
    cursor.close()
    cnx.close()
    return {"base_de_datos": DB_NAME, "existe": DB_NAME in bases}


def crear_tablas():
    cnx = conectar()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS razas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(60) NOT NULL UNIQUE,
            tamano VARCHAR(10) NOT NULL
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            raza_id INT NOT NULL,
            sexo VARCHAR(10) NOT NULL,
            fecha_ingreso DATE NOT NULL,
            estado VARCHAR(15) NOT NULL DEFAULT 'Disponible',
            FOREIGN KEY (raza_id) REFERENCES razas(id)
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adoptantes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(120) NOT NULL UNIQUE,
            ciudad VARCHAR(60)
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adopciones (
            id INT AUTO_INCREMENT PRIMARY KEY,
            perro_id INT NOT NULL UNIQUE,
            adoptante_id INT NOT NULL,
            fecha_adopcion DATE NOT NULL,
            FOREIGN KEY (perro_id) REFERENCES perros(id),
            FOREIGN KEY (adoptante_id) REFERENCES adoptantes(id)
        )""")

    cursor.execute("SHOW TABLES")
    tablas = [list(fila.values())[0] for fila in cursor.fetchall()]
    cursor.close()
    cnx.close()
    return {"tablas": tablas}

########        INSERCION DE DATOS DE EJEMPLOS      #########
def insertar_datos_ejemplo():
    """Inserta datos de prueba solo si la tabla perros está vacía (no duplica)."""
    cnx = conectar()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total FROM perros")
    if cursor.fetchone()["total"] > 0:
        cursor.close()
        cnx.close()
        return {"insertados": False, "motivo": "Ya había datos; no se duplican."}

    cursor.executemany(
        "INSERT INTO razas (nombre, tamano) VALUES (%s, %s)",
        [("Labrador", "Grande"), ("Mestizo", "Mediano"), ("Chihuahua", "Pequeño"),
         ("Pastor Alemán", "Grande"), ("Beagle", "Mediano"), ("Yorkshire", "Pequeño")])
    cursor.executemany(
        "INSERT INTO perros (nombre, raza_id, sexo, fecha_ingreso, estado) VALUES (%s,%s,%s,%s,%s)",
        [("Toby", 1, "Macho", "2025-01-15", "Disponible"),
         ("Luna", 2, "Hembra", "2025-02-20", "Disponible"),
         ("Coco", 3, "Macho", "2025-03-05", "Adoptado"),
         ("Nala", 4, "Hembra", "2025-03-18", "En acogida"),
         ("Rocky", 5, "Macho", "2025-04-02", "Disponible"),
         ("Mía", 6, "Hembra", "2025-04-25", "Adoptado"),
         ("Thor", 4, "Macho", "2025-05-10", "Disponible"),
         ("Lola", 2, "Hembra", "2025-06-01", "Disponible"),
         ("Max", 1, "Macho", "2025-06-15", "Adoptado"),
         ("Kira", 5, "Hembra", "2025-07-01", "En acogida")])
    cursor.executemany(
        "INSERT INTO adoptantes (nombre, email, ciudad) VALUES (%s,%s,%s)",
        [("Ana Ruiz", "ana.ruiz@example.com", "Sevilla"),
         ("Carlos Gil", "carlos.gil@example.com", "Dos Hermanas"),
         ("Marta Peña", "marta.pena@example.com", "Málaga")])
    cursor.executemany(
        "INSERT INTO adopciones (perro_id, adoptante_id, fecha_adopcion) VALUES (%s,%s,%s)",
        [(3, 1, "2025-04-10"), (6, 2, "2025-05-30"), (9, 3, "2025-07-20")])
    cnx.commit()
    cursor.close()
    cnx.close()
    return {"insertados": True, "razas": 6, "perros": 10, "adoptantes": 3, "adopciones": 3}


def _consultar(sql):
    cnx = conectar()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(sql)
    filas = cursor.fetchall()
    cursor.close()
    cnx.close()
    return filas


def consulta_perros_disponibles():
    """Consulta 1: perros disponibles con su raza y tamaño."""
    return _consultar("""
        SELECT p.id, p.nombre, r.nombre AS raza, r.tamano, p.sexo, p.fecha_ingreso
        FROM perros p JOIN razas r ON r.id = p.raza_id
        WHERE p.estado = 'Disponible'
        ORDER BY p.nombre""")


def consulta_perros_por_estado():
    """Consulta 2: cuántos perros hay en cada estado."""
    return _consultar("""
        SELECT estado, COUNT(*) AS total
        FROM perros
        GROUP BY estado
        ORDER BY total DESC, estado""")


def consulta_adopciones():
    """Consulta 3: adopciones realizadas con perro, raza y adoptante."""
    return _consultar("""
        SELECT a.fecha_adopcion, p.nombre AS perro, r.nombre AS raza,
               d.nombre AS adoptante, d.ciudad
        FROM adopciones a
        JOIN perros p ON p.id = a.perro_id
        JOIN razas r ON r.id = p.raza_id
        JOIN adoptantes d ON d.id = a.adoptante_id
        ORDER BY a.fecha_adopcion""")
