import psycopg2
import redis

def vaciar_sistemas():
    print("\n" + "=" * 70)
    print("VACIADO TOTAL DE BASES DE DATOS")
    print("Qué hace: Ejecuta FLUSHDB en Redis y TRUNCATE en la tabla de PostgreSQL.")
    print("=" * 70)

    # 1. Vaciar Redis
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        claves_antes = r.dbsize()
        r.flushdb()
        print(f"  [Redis] FLUSHDB ejecutado. Se han eliminado {claves_antes} claves.")
    except Exception as e:
        print(f"  [Redis] Error al conectar o limpiar: {e}")

    # 2. Vaciar PostgreSQL
    try:
        conn_pg = psycopg2.connect(
            host="localhost", database="refugio", user="usuario", password="password", port="5432"
        )
        cursor = conn_pg.cursor()
        
        cursor.execute("TRUNCATE TABLE mascotas_sql RESTART IDENTITY;")
        conn_pg.commit()
        
        print("  [PostgreSQL] TRUNCATE ejecutado. Tabla 'mascotas_sql' vaciada y contadores reiniciados.")
        
        cursor.close()
        conn_pg.close()
    except Exception as e:
        print(f"  [PostgreSQL] Error al conectar o limpiar: {e}")

    print("\nResultado: Ambos sistemas han sido restablecidos a 0.")

if __name__ == "__main__":
    vaciar_sistemas()