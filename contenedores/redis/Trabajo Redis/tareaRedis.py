import os
import redis
from conectar import conectar

def titulo(numero, texto, explicacion):
    print("\n" + "=" * 70)
    print(f"EJERCICIO {numero}: {texto}")
    print(f"Qué hace: {explicacion}")
    print("=" * 70)

""" 1- Crear registros clave-valor """
def ejercicio01(r):

    titulo(1, "Crear registros clave-valor", "Guarda 5 perros con SET. La clave es perro;<id> y el valor es la raza.")

    perros = {
        "perros:1": "Labrador",
        "perros:2": "Podenco",
        "perros:3": "Husky",
        "perros:4": "Labrador",
        "perros:5": "Mastín",
    }

    for clave, valor in perros.items():
        r.set(clave, valor)

        print(f"    SET {clave}: {valor}")
    
    print(f"Resultado: se han creado {len(perros)} registros.")


""" 2- Obtener y mostrar el numero de claves registradas """
def ejercicio02(r):

    titulo(2, "Obtener y mostrar el numero de claves registradas", "Uso de DBSIZE para saber cuantas claves hay guardadas en la base de datos.")

    # total_db = r.dbsize()
    total_claves = len(r.keys())

    print(f"Resultado: La base de datos contiene {total_claves} claves")


""" 3- Obtener y mostrar un registro en base a una clave """
def ejercicio03(r):
    titulo(3, "Obtener y mostrar un registro en base a una clave.", "Mediante GET, leemos el valor de una clave en concreto. Si no existe, Redis devuelve NONE.")

    clave = "perro:3"
    valor = r.get(clave)
    print(f"    GET {clave}: {valor}.")
    
    clave_inexistente = "perro:99"
    valor_inexistente = r.get(clave_inexistente)

    print(f"    GET {clave_inexistente}: {valor_inexistente}.")

if __name__ == "__main__":
    r = conectar()

    ejercicio01(r)
    ejercicio02(r)
    ejercicio03(r)
