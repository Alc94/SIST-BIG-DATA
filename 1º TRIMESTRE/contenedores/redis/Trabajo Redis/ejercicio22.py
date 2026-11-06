import psycopg2
import redis

def ejercicio22():
    print("\n" + "=" * 70)
    print("EJERCICIO 22: Obtener datos de Redis e incluirlos en SQL (PostgreSQL)")
    print("Qué hace: Busca registros en Redis con el prefijo 'nueva_mascota:*',")
    print("los lee con HGETALL y los inserta en la tabla 'mascotas_sql' de PostgreSQL.")
    print("=" * 70)

    # 1. Conexiones
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    conn_pg = psycopg2.connect(
        host="localhost", database="refugio", user="usuario", password="password", port="5432"
    )
    cursor = conn_pg.cursor()

    # 2. Crear un dato de prueba en Redis simulando una nueva entrada en el sistema
    clave_prueba = "nueva_mascota:99"
    r.hset(clave_prueba, mapping={"nombre": "Zeus", "raza": "Dóberman", "edad": 3})
    print(f"  -> Dato simulado creado en Redis: {clave_prueba}\n")

    # 3. Buscar y leer los datos de Redis
    claves = r.keys("nueva_mascota:*")
    print(f"  -> Se encontraron {len(claves)} registros en Redis para exportar a SQL.")

    # 4. Insertar en PostgreSQL
    for clave in claves:
        datos = r.hgetall(clave)
        
        consulta = "INSERT INTO mascotas_sql (nombre, raza, edad) VALUES (%s, %s, %s) RETURNING id;"
        cursor.execute(consulta, (datos["nombre"], datos["raza"], datos["edad"]))
        
        nuevo_id = cursor.fetchone()[0]
        conn_pg.commit()
        
        print(f"    INSERT SQL -> {datos['nombre']} guardado en PostgreSQL con el nuevo ID: {nuevo_id}")

    print(f"\nResultado: Migración de Redis a SQL completada con éxito.")

    cursor.close()
    conn_pg.close()

if __name__ == "__main__":
    ejercicio22()