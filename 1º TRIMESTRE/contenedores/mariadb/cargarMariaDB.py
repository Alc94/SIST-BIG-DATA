"""
10 GENERADORES / PROVIDERS DE FAKER UTILIZADOS:
------------------------------------------------
1. fake.first_name()       -> Nombres de personas
2. fake.last_name()        -> Apellidos
3. fake.email()            -> Correos electrónicos
4. fake.address()          -> Direcciones físicas
5. fake.phone_number()     -> Números de teléfono
6. fake.date_between()     -> Fechas aleatorias en un rango
7. fake.random_element()   -> Selección aleatoria de listas personalizadas
8. fake.pydecimal()        -> Números decimales (pesos, costes, montos)
9. fake.sentence()         -> Frases breves (diagnósticos, tareas)
10. fake.company()         -> Nombres de clínicas / empresas
"""

import pymysql
from faker import Faker
import random

# Inicializar Faker en español
fake = Faker("es_ES")

# Configuración de conexión al contenedor de MySQL
config = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "mi_password",
    "database": "refugio_mariadb",
}


def crear_tablas(cursor):
    # DDL para las 10 tablas del refugio de perros
    sql_statements = [
        """
        CREATE TABLE IF NOT EXISTS Veterinarians (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            clinic_name VARCHAR(150),
            license_number VARCHAR(50) NOT NULL UNIQUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Dogs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            breed VARCHAR(100),
            birth_date DATE,
            weight DECIMAL(5, 2),
            arrival_date DATE NOT NULL,
            adoption_status VARCHAR(50) DEFAULT 'Disponible'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Medical_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            dog_id INT NOT NULL,
            veterinarian_id INT NOT NULL,
            visit_day DATE NOT NULL,
            diagnosis TEXT,
            treatment TEXT,
            cost DECIMAL(8, 2),
            FOREIGN KEY (dog_id) REFERENCES Dogs(id) ON DELETE CASCADE,
            FOREIGN KEY (veterinarian_id) REFERENCES Veterinarians(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Adopters (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            address VARCHAR(255),
            approval_status VARCHAR(50) DEFAULT 'Pendiente'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Adoptions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            dog_id INT NOT NULL,
            adopter_id INT NOT NULL,
            adoption_date DATE NOT NULL,
            status VARCHAR(50) DEFAULT 'Completada',
            FOREIGN KEY (dog_id) REFERENCES Dogs(id) ON DELETE CASCADE,
            FOREIGN KEY (adopter_id) REFERENCES Adopters(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Volunteers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            phone VARCHAR(20),
            join_date DATE NOT NULL,
            adoption_status VARCHAR(50) DEFAULT 'Activo'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Shifts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            volunteer_id INT NOT NULL,
            shift_date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            task_description TEXT,
            FOREIGN KEY (volunteer_id) REFERENCES Volunteers(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Dog_assignments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            volunteer_id INT NOT NULL,
            dog_id INT NOT NULL,
            assignment_date DATE NOT NULL,
            care_role VARCHAR(100),
            FOREIGN KEY (volunteer_id) REFERENCES Volunteers(id) ON DELETE CASCADE,
            FOREIGN KEY (dog_id) REFERENCES Dogs(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Donations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            donor_name VARCHAR(150),
            amount DECIMAL(10, 2) NOT NULL,
            donation_date DATE NOT NULL,
            payment_method VARCHAR(50)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Supplies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_name VARCHAR(100) NOT NULL,
            category VARCHAR(50),
            quantity INT NOT NULL DEFAULT 0,
            unit VARCHAR(20)
        )
        """,
    ]
    for statement in sql_statements:
        cursor.execute(statement)


def poblar_datos(cursor):
    # 1. Veterinarians
    vets_ids = []
    for _ in range(5):
        sql = "INSERT INTO Veterinarians (first_name, last_name, clinic_name, license_number) VALUES (%s, %s, %s, %s)"
        val = (
            fake.first_name(),
            fake.last_name(),
            fake.company(),
            fake.unique.bothify(text="LIC-#####"),
        )
        cursor.execute(sql, val)
        vets_ids.append(cursor.lastrowid)

    # 2. Dogs
    dogs_ids = []
    razas = ["Labrador", "Pastor Alemán", "Mestizo", "Beagle", "Bulldog", "Podenco"]
    estados = ["Disponible", "Adoptado", "En Tratamiento"]
    for _ in range(15):
        sql = "INSERT INTO Dogs (name, breed, birth_date, weight, arrival_date, adoption_status) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (
            fake.first_name(),
            fake.random_element(razas),
            fake.date_between(start_date="-10y", end_date="-1y"),
            float(
                fake.pydecimal(
                    left_digits=2,
                    right_digits=1,
                    positive=True,
                    min_value=3,
                    max_value=40,
                )
            ),
            fake.date_between(start_date="-1y", end_date="today"),
            fake.random_element(estados),
        )
        cursor.execute(sql, val)
        dogs_ids.append(cursor.lastrowid)

    # 3. Medical_records
    for _ in range(20):
        sql = "INSERT INTO Medical_records (dog_id, veterinarian_id, visit_day, diagnosis, treatment, cost) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (
            random.choice(dogs_ids),
            random.choice(vets_ids),
            fake.date_between(start_date="-6m", end_date="today"),
            fake.sentence(nb_words=5),
            fake.sentence(nb_words=4),
            float(
                fake.pydecimal(
                    left_digits=3,
                    right_digits=2,
                    positive=True,
                    min_value=20,
                    max_value=300,
                )
            ),
        )
        cursor.execute(sql, val)

    # 4. Adopters
    adopters_ids = []
    for _ in range(8):
        sql = "INSERT INTO Adopters (first_name, last_name, email, address, approval_status) VALUES (%s, %s, %s, %s, %s)"
        val = (
            fake.first_name(),
            fake.last_name(),
            fake.unique.email(),
            fake.address(),
            fake.random_element(["Aprobado", "Pendiente", "Rechazado"]),
        )
        cursor.execute(sql, val)
        adopters_ids.append(cursor.lastrowid)

    # 5. Adoptions
    for _ in range(5):
        sql = "INSERT INTO Adoptions (dog_id, adopter_id, adoption_date, status) VALUES (%s, %s, %s, %s)"
        val = (
            random.choice(dogs_ids),
            random.choice(adopters_ids),
            fake.date_between(start_date="-3m", end_date="today"),
            "Completada",
        )
        cursor.execute(sql, val)

    # 6. Volunteers
    volunteers_ids = []
    for _ in range(10):
        sql = "INSERT INTO Volunteers (first_name, last_name, email, phone, join_date, adoption_status) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (
            fake.first_name(),
            fake.last_name(),
            fake.unique.email(),
            fake.phone_number(),
            fake.date_between(start_date="-2y", end_date="today"),
            "Activo",
        )
        cursor.execute(sql, val)
        volunteers_ids.append(cursor.lastrowid)

    # 7. Shifts
    for _ in range(15):
        sql = "INSERT INTO Shifts (volunteer_id, shift_date, start_time, end_time, task_description) VALUES (%s, %s, %s, %s, %s)"
        val = (
            random.choice(volunteers_ids),
            fake.date_between(start_date="-1m", end_date="+1m"),
            "09:00:00",
            "14:00:00",
            fake.sentence(nb_words=6),
        )
        cursor.execute(sql, val)

    # 8. Dog_assignments
    for _ in range(12):
        sql = "INSERT INTO Dog_assignments (volunteer_id, dog_id, assignment_date, care_role) VALUES (%s, %s, %s, %s)"
        val = (
            random.choice(volunteers_ids),
            random.choice(dogs_ids),
            fake.date_between(start_date="-1m", end_date="today"),
            fake.random_element(["Paseo", "Alimentación", "Aseo"]),
        )
        cursor.execute(sql, val)

    # 9. Donations
    metodos = ["Tarjeta", "Transferencia", "Efectivo", "PayPal"]
    for _ in range(15):
        sql = "INSERT INTO Donations (donor_name, amount, donation_date, payment_method) VALUES (%s, %s, %s, %s)"
        val = (
            fake.first_name() + " " + fake.last_name(),
            float(
                fake.pydecimal(
                    left_digits=3,
                    right_digits=2,
                    positive=True,
                    min_value=10,
                    max_value=500,
                )
            ),
            fake.date_between(start_date="-1y", end_date="today"),
            fake.random_element(metodos),
        )
        cursor.execute(sql, val)

    # 10. Supplies
    suministros = [
        "Pienso Adultos",
        "Pienso Cachorros",
        "Vacuna Rabia",
        "Desparasitante",
        "Mantas",
        "Juguetes",
    ]
    for item in suministros:
        sql = "INSERT INTO Supplies (item_name, category, quantity, unit) VALUES (%s, %s, %s, %s)"
        val = (
            item,
            (
                "Alimentación"
                if "Pienso" in item
                else (
                    "Sanidad"
                    if "Vacuna" in item or "Desparasitante" in item
                    else "General"
                )
            ),
            random.randint(10, 200),
            "Kg" if "Pienso" in item else "Unidades",
        )
        cursor.execute(sql, val)


def main():
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        print("Conectando a MySQL...")

        crear_tablas(cursor)
        print("Tablas creadas correctamente.")

        poblar_datos(cursor)
        conn.commit()
        print("Datos insertados con éxito mediante Faker.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al ejecutar: {e}")


if __name__ == "__main__":
    main()
