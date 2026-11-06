import psycopg2
import redis

def ejercicio21():
    print("\n" + "=" * 70)
    print("EJERCICIO 21: Obtener datos de SQL (PostgreSQL) e incluirlos en Redis")
    print("Qué hace: Se conecta a PostgreSQL, hace un SELECT de la tabla 'mascotas_sql',")
    print("y guarda cada registro en Redis usando HSET con la clave 'sql_mascota:<id>'.")
    print("=" * 70)

    # 1. Conexión a PostgreSQL
    conn_pg = psycopg2.connect(
        host="localhost",
        database="refugio",
        user="usuario",
        password="password",
        port="5432"
    )
    cursor = conn_pg.cursor()

    # 2. Conexión a Redis
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    # 3. Leer datos de PostgreSQL
    cursor.execute("SELECT id, nombre, raza, edad FROM mascotas_sql;")
    mascotas_pg = cursor.fetchall()
    
    print(f"  -> Se han recuperado {len(mascotas_pg)} registros de PostgreSQL.")

    # 4. Insertar en Redis
    for mascota in mascotas_pg:
        id_sql, nombre, raza, edad = mascota
        clave_redis = f"sql_mascota:{id_sql}"
        
        r.hset(clave_redis, mapping={
            "nombre": nombre,
            "raza": raza,
            "edad": edad
        })
        print(f"    HSET {clave_redis} -> {nombre} ({raza}), {edad} años")

    print(f"\nResultado: Migración de SQL a Redis completada. Se crearon {len(mascotas_pg)} claves nuevas en Redis.")

    cursor.close()
    conn_pg.close()

if __name__ == "__main__":
    ejercicio21()