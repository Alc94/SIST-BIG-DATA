from conectar import conectar
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.aggregation import AggregateRequest
from redis.commands.search import reducers
from redis.exceptions import ResponseError
from redis.commands.search.query import Query


def titulo(numero, texto, explicacion):
    print("\n" + "=" * 70)
    print(f"EJERCICIO {numero}: {texto}")
    print(f"Qué hace: {explicacion}")
    print("=" * 70)


def limpiar_datos(r):
    r.flushdb()

""" 1- Crear registros clave-valor """
def ejercicio01(r):

    titulo(
        1,
        "Crear registros clave-valor",
        "Guarda 5 perros con SET. La clave es perro;<id> y el valor es la raza.",
    )

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

    titulo(
        2,
        "Obtener y mostrar el numero de claves registradas",
        "Uso de DBSIZE para saber cuantas claves hay guardadas en la base de datos.",
    )

    # total_db = r.dbsize()
    total_claves = len(r.keys())

    print(f"Resultado: La base de datos contiene {total_claves} claves")


""" 3- Obtener y mostrar un registro en base a una clave """
def ejercicio03(r):
    titulo(
        3,
        "Obtener y mostrar un registro en base a una clave.",
        "Mediante GET, leemos el valor de una clave en concreto. Si no existe, Redis devuelve NONE.",
    )

    clave = "perros:3"
    valor = r.get(clave)
    print(f"    GET {clave}: {valor}.")

    clave_inexistente = "perros:99"
    valor_inexistente = r.get(clave_inexistente)

    print(f"    GET {clave_inexistente}: {valor_inexistente}.")



""" 4- Actualizar el valor de una clave """
def ejercicio04(r):
    titulo(
        4,
        "Actualizar el valor de una clave.",
        "Usar SET sobre una clave existente: Redis lo sobreescribe.",
    )

    clave = "perros:2"

    if not r.exists(clave):
        print(f" La vale '{clave}' no existe, ejecuta antes del ejercicio 1.")
        return

    valor_antiguo = r.get(clave)
    print(f" Valor antes de actualizar: GET {clave}: {valor_antiguo}")

    r.set(clave, "Galgo")
    print(f" SET {clave}: Galgo")



""" 5- Eliminar una clave-valor y mostrar la clave y el valor eliminado"""
def ejercicio05(r):
    titulo(
        5,
        "Eliminar una clave-valor",
        "Lee el valor con GET, lo guarda en una variable y después borra la clave con DEL.",
    )
    clave = "perros:5"

    valor = r.get(clave)
    if valor is None:
        print(f"  La clave '{clave}' no existe, ejecuta antes el ejercicio 1.")
        return

    print(f"  Antes de borrar: GET {clave} -> {valor}")
    borradas = r.delete(clave)
    print(f"  DEL {clave} -> {borradas} clave borrada")

    print(f"  Comprobación: GET {clave} -> {r.get(clave)}")
    print(f"  Claves restantes en la base: {r.dbsize()}")
    print(
        f"Resultado: se ha eliminado la clave '{clave}' que contenía el valor '{valor}'."
    )


""" 6- Obtener y mostrar todas las claves guardadas """
def ejercicio06(r):
    titulo(
        6,
        "Obtener y mostrar todas las claves",
        "Usa KEYS para obtener la lista de todas las claves guardadas en la base de datos.",
    )

    claves = r.keys()

    print(f"  KEYS -> {len(claves)} claves encontradas:")

    for clave in sorted(claves):
        print(f"    - {clave}")

    print(f"Resultado: la base de datos contiene {len(claves)} claves.")


""" 7- Obtener y mostrar todos los valores guardados """
def ejercicio07(r):
    titulo(
        7,
        "Obtener y mostrar todos los valores",
        "Recorre todas las claves con KEYS y lee el valor de cada una con GET.",
    )

    claves = sorted(r.keys())

    for clave in claves:
        if r.type(clave) != "string":
            print(
                f"  (se omite '{clave}': es de tipo {r.type(clave)}, GET solo lee strings)"
            )
            continue
        valor = r.get(clave)
        print(f"  GET {clave} -> {valor}")



""" 8- Obtener y mostrar varios registros con una clave con un patrón en común usando * """
def mostrar_claves_patron(r, patron):
    """Busca las claves que encajan con el patrón y muestra clave y valor."""
    claves = sorted(r.scan_iter(patron))
    print(f"  scan_iter('{patron}') -> {len(claves)} claves encontradas")
    for clave in claves:
        if r.type(clave) == "string":
            print(f"    - {clave} -> {r.get(clave)}")
        else:
            print(f"    - {clave} (tipo {r.type(clave)})")
    return claves


def ejercicio08(r):
    titulo(
        8,
        "Buscar claves con un patrón usando *",
        "Usa scan_iter con el comodín * (cualquier número de caracteres, o ninguno).",
    )

    print("\n  a) 'perro:*' -> claves que EMPIEZAN por 'perros:'")
    mostrar_claves_patron(r, "perros:*")

    print("\n  b) '*:2' -> claves que TERMINAN en ':2'")
    mostrar_claves_patron(r, "*:2")

    print("\n  c) '*erro*' -> claves que CONTIENEN 'erro' en cualquier posición")
    mostrar_claves_patron(r, "*erro*")



""" 9- Obtener y mostrar varios registros con una clave con un patrón en común usando [] """
def ejercicio09(r):
    titulo(
        9,
        "Buscar claves con un patrón usando []",
        "Usa scan_iter con corchetes: encaja con UN carácter que sea uno de los indicados.",
    )

    print("\n  a) 'perros:[13]' -> el carácter tras 'perros:' es un 1 o un 3")
    mostrar_claves_patron(r, "perros:[13]")

    print(
        "\n  b) 'perros:[1-3]' -> el carácter tras 'perros:' está en el rango del 1 al 3"
    )
    mostrar_claves_patron(r, "perros:[1-3]")

    print("\n  c) 'perro:[^1]' -> el carácter tras 'perro:' es cualquiera EXCEPTO el 1")
    mostrar_claves_patron(r, "perros:[^1]")


""" 10- Obtener y mostrar varios registros con una clave con un patrón en común usando ? """
def ejercicio10(r):
    titulo(
        10,
        "Buscar claves con un patrón usando ?",
        "Usa scan_iter con ?, que encaja con UN carácter cualquiera (ni más ni menos).",
    )

    # Clave temporal para que se vea la diferencia entre ? y *
    r.set("perros:10", "Bodeguero")
    print("  (Se crea la clave temporal perro:10 -> Bodeguero para la demostración)")

    print("\n  a) 'perros:?' -> UN solo carácter tras 'perros:'")
    mostrar_claves_patron(r, "perros:?")

    print("\n  b) 'perros:??' -> DOS caracteres tras 'perros:'")
    mostrar_claves_patron(r, "perros:??")

    print("\n  c) 'perros:*' -> para comparar: cualquier cantidad de caracteres")
    mostrar_claves_patron(r, "perros:*")

    print(
        "\n  d) '?erros:1' -> el ? puede ir en cualquier posición, aquí sustituye a la 'p'"
    )
    mostrar_claves_patron(r, "?erros:1")

    r.delete("perros:10")
    print("\n  (Se borra la clave temporal perros:10)")


""" 11- Obtener y mostrar varios registros y filtrarlos por un valor en concreto. """
""" Funcion auxiliar para ejercicios 11, 12 y 13 """
def buscar_por_valor(r, patron, valor_buscado):
    """Devuelve {clave: valor} de las claves del patrón cuyo valor coincide."""
    encontrados = {}
    for clave in sorted(r.scan_iter(patron)):
        if r.type(clave) != "string":
            continue
        valor = r.get(clave)
        if valor == valor_buscado:
            encontrados[clave] = valor
    return encontrados


def ejercicio11(r):
    titulo(
        11,
        "Filtrar registros por un valor concreto",
        "Recorre las claves 'perro:*' con scan_iter, lee cada valor con GET y se queda "
        "solo con las que tienen el valor buscado.",
    )

    print("\n  Todos los registros antes de filtrar:")
    for clave in sorted(r.scan_iter("perros:*")):
        print(f"    - {clave} -> {r.get(clave)}")

    raza = "Labrador"
    print(f"\n  Filtro: valor == '{raza}'")
    encontrados = buscar_por_valor(r, "perros:*", raza)
    for clave, valor in encontrados.items():
        print(f"    - {clave} -> {valor}")

    print(f"\n  Filtro: valor == 'Dálmata' (no existe ninguno)")
    vacio = buscar_por_valor(r, "perros:*", "Dálmata")
    print(f"    Encontrados: {len(vacio)}")

    print(
        f"\nResultado: {len(encontrados)} registros tienen el valor '{raza}': "
        f"{list(encontrados.keys())}"
    )


""" 12- Actualizar una serie de registros en base a un filtro (por ejemplo aumentar su valor en 1 ) """
def ejercicio12(r):
    titulo(
        12,
        "Actualizar una serie de registros según un filtro",
        "Crea claves visitas:* con valores numéricos, filtra las que tienen más de 4 visitas "
        "y les suma 1 con INCR.",
    )

    visitas = {"visitas:1": 5, "visitas:2": 3, "visitas:3": 8, "visitas:4": 1}
    for clave, valor in visitas.items():
        r.set(clave, valor)
    print("  Datos de partida creados con SET")

    print("\n  Antes de actualizar:")
    for clave in sorted(r.scan_iter("visitas:*")):
        print(f"    - {clave} -> {r.get(clave)}")

    umbral = 4
    print(f"\n  Filtro: valor > {umbral}")
    filtradas = [c for c in sorted(r.scan_iter("visitas:*")) if int(r.get(c)) > umbral]
    for clave in filtradas:
        anterior = r.get(clave)
        nuevo = r.incr(clave)
        print(f"    INCR {clave}: {anterior} -> {nuevo}")

    print("\n  Después de actualizar:")
    for clave in sorted(r.scan_iter("visitas:*")):
        print(f"    - {clave} -> {r.get(clave)}")

    print(
        f"\nResultado: se han actualizado {len(filtradas)} registros ({filtradas}). "
        f"Los que no cumplían el filtro se han quedado igual."
    )


""" 13- Eliminar una serie de registros en base a un filtro """
def ejercicio13(r):
    titulo(
        13,
        "Eliminar una serie de registros según un filtro",
        "Recorre las claves visitas:* con scan_iter, filtra las que tienen menos de 4 visitas "
        "y las borra con DEL.",
    )

    # Si se ejecuta solo, por si no existen los datos del ejercicio 12
    if not list(r.scan_iter("visitas:*")):
        for clave, valor in {
            "visitas:1": 6,
            "visitas:2": 3,
            "visitas:3": 9,
            "visitas:4": 1,
        }.items():
            r.set(clave, valor)
        print("  (No había claves visitas:*, se han creado de nuevo)")

    print("\n  Antes de eliminar:")
    for clave in sorted(r.scan_iter("visitas:*")):
        print(f"    - {clave} -> {r.get(clave)}")

    umbral = 4
    print(f"\n  Filtro: valor < {umbral}")
    a_borrar = {
        c: r.get(c) for c in sorted(r.scan_iter("visitas:*")) if int(r.get(c)) < umbral
    }
    for clave, valor in a_borrar.items():
        print(f"    Se eliminará: {clave} -> {valor}")

    borradas = r.delete(*a_borrar.keys()) if a_borrar else 0
    print(f"\n  DEL de {len(a_borrar)} claves -> Redis confirma {borradas} borradas")

    print("\n  Después de eliminar:")
    for clave in sorted(r.scan_iter("visitas:*")):
        print(f"    - {clave} -> {r.get(clave)}")

    print(
        f"\nResultado: se han eliminado {borradas} registros {list(a_borrar.keys())}. "
        f"Los que no cumplían el filtro siguen en la base."
    )


""" 14- Crear una estructura en JSON de array de los datos que vayais a almacenar(0.5 puntos) """
PERROS_JSON = [
    {
        "id": 1,
        "nombre": "Luna",
        "raza": "Labrador",
        "edad": 3,
        "peso": 28.5,
        "estado_adopcion": "Disponible",
    },
    {
        "id": 2,
        "nombre": "Rocky",
        "raza": "Podenco",
        "edad": 5,
        "peso": 21.0,
        "estado_adopcion": "Adoptado",
    },
    {
        "id": 3,
        "nombre": "Toby",
        "raza": "Labrador",
        "edad": 7,
        "peso": 31.2,
        "estado_adopcion": "Disponible",
    },
    {
        "id": 4,
        "nombre": "Nala",
        "raza": "Mastín",
        "edad": 2,
        "peso": 52.0,
        "estado_adopcion": "En tratamiento",
    },
    {
        "id": 5,
        "nombre": "Coco",
        "raza": "Beagle",
        "edad": 9,
        "peso": 12.8,
        "estado_adopcion": "Disponible",
    },
    {
        "id": 6,
        "nombre": "Max",
        "raza": "Husky",
        "edad": 4,
        "peso": 24.0,
        "estado_adopcion": "Adoptado",
    },
]


def ejercicio14(r):
    titulo(
        14,
        "Crear una estructura JSON de array",
        "Con RedisJSON crea un array vacío (JSON.SET) y le añade un perro tras otro (JSON.ARRAPPEND).",
    )

    r.json().set("perros_array", "$", [])
    print("  JSON.SET perros_array $ [] -> array vacío creado")

    for perro in PERROS_JSON:
        longitud = r.json().arrappend("perros_array", "$", perro)
        print(
            f"  JSON.ARRAPPEND {perro['nombre']:<6} -> el array ya tiene {longitud[0]} elementos"
        )

    total = r.json().arrlen("perros_array", "$")[0]
    print(f"\n  JSON.ARRLEN perros_array -> {total}")
    print("\n  Contenido guardado (JSON.GET perros_array):")
    for perro in r.json().get("perros_array"):
        print(f"    {perro}")

    print(
        f"\nResultado: la clave 'perros_array' contiene un array JSON con {total} perros, "
        f"cada uno con los atributos {list(PERROS_JSON[0].keys())}."
    )
    
    

""" 15- Realizar un filtro por cada atributo de la estructura JSON anterior """
def filtrar_json(r, explicacion, ruta):
    """Ejecuta un filtro JSONPath sobre perros_array y muestra los perros que lo cumplen."""
    resultado = r.json().get("perros_array", ruta)
    print(f"\n  {explicacion}")
    print(f"  JSON.GET perros_array '{ruta}'")
    print(f"  -> {len(resultado)} resultados")
    for perro in resultado:
        print(
            f"     {perro['nombre']:<6} | raza: {perro['raza']:<9} | edad: {perro['edad']} "
            f"| peso: {perro['peso']} | {perro['estado_adopcion']}"
        )
    return resultado


def ejercicio15(r):
    titulo(
        15,
        "Filtro por cada atributo de la estructura JSON",
        "Usa JSON.GET con filtros JSONPath [?(@.atributo ...)] para filtrar en Redis, "
        "uno por cada atributo de los perros.",
    )

    # Seguro por si se ejecuta este ejercicio sin haber pasado por el 14
    if not r.exists("perros_array"):
        r.json().set("perros_array", "$", PERROS_JSON)
        print("  (No existía perros_array, se ha creado de nuevo)")

    filtrar_json(r, "1) Atributo 'id' (igualdad numérica): id == 4", "$[?(@.id == 4)]")
    filtrar_json(
        r,
        "2) Atributo 'nombre' (igualdad de texto): nombre == Luna",
        '$[?(@.nombre == "Luna")]',
    )
    filtrar_json(
        r,
        "3) Atributo 'raza' (igualdad de texto): raza == Labrador",
        '$[?(@.raza == "Labrador")]',
    )
    filtrar_json(r, "4) Atributo 'edad' (comparación): edad > 5", "$[?(@.edad > 5)]")


""" 16- Crear una lista en Redis """
LISTA_TAREAS = "refugio:tareas"


def ejercicio16(r):
    titulo(
        16,
        "Crear una lista en Redis",
        "Crea la lista 'refugio:tareas' añadiendo elementos con LPUSH y la lee con LRANGE.",
    )

    r.delete(LISTA_TAREAS)  # así, si se ejecuta dos veces, no se duplican los elementos
    tareas = [
        "paseo:Luna",
        "vacuna:Rocky",
        "paseo:Toby",
        "bano:Nala",
        "paseo:Coco",
        "vacuna:Max",
        "bano:Luna",
    ]

    for tarea in tareas:
        longitud = r.lpush(LISTA_TAREAS, tarea)

    elementos = r.lrange(LISTA_TAREAS, 0, -1)
    print(f"\n  LRANGE {LISTA_TAREAS} -> {len(elementos)} elementos:")
    for posicion, elemento in enumerate(elementos):
        print(f"    posición {posicion}: {elemento}")

    print(f"\nResultado: se ha creado la lista '{LISTA_TAREAS}' con {len(elementos)} tareas.")
    
    
""" 17- Obtener elementos de una lista con un filtro en concreto """
def ejercicio17(r):
    titulo(
        17,
        "Obtener elementos de una lista con un filtro en concreto",
        "Obtiene todas las tareas de la lista 'refugio:tareas' con LRANGE y filtra mediante Python las que correspondan a un 'paseo'."
    )

    lista = "refugio:tareas"
    
    # Obtener todos los elementos de la lista
    elementos = r.lrange(lista, 0, -1)
    
    if not elementos:
        print(f"  La lista '{lista}' está vacía. Ejecuta el ejercicio 16 primero.")
        return

    print(f"  LRANGE {lista} -> Se han recuperado {len(elementos)} tareas en total.")

    # Definir el filtro
    filtro = "paseo"
    print(f"  Aplicando filtro: buscar tareas que contengan la palabra '{filtro}'...\n")

    # Filtrar los elementos
    tareas_filtradas = [tarea for tarea in elementos if filtro in tarea]

    # Mostrar los resultados
    if tareas_filtradas:
        for tarea in tareas_filtradas:
            print(f"    - {tarea}")
    else:
        print(f"    No se encontró ninguna tarea que coincida con el filtro '{filtro}'.")

    print(
        f"\nResultado: De {len(elementos)} tareas en la lista, "
        f"se han filtrado {len(tareas_filtradas)} que coinciden con '{filtro}'."
    )
    
    
""" 18- Crea datos con índices, definiendo un esquema de al menos tres campos """
def ejercicio18(r):
    titulo(
        18,
        "Crear datos con índices y definir un esquema",
        "Usa RediSearch para crear un índice ('idx:mascotas') sobre Hashes con el prefijo 'mascota:'. Define 3 campos: nombre (Text), raza (Tag) y edad (Numeric)."
    )

    indice = "idx:mascotas"
    prefijo = "mascota:"

    # Borrar el índice si ya existe (evita errores de duplicidad al ejecutar el script varias veces)
    try:
        r.ft(indice).info()
        print(f"  El índice '{indice}' ya existía. Se procede a borrarlo.")
        r.ft(indice).dropindex(delete_documents=True)
    except ResponseError:
        pass # Si salta la excepción, el índice no existía. Todo correcto.

    # Definir el esquema con al menos 3 campos de distinto tipo
    esquema = (
        TextField("nombre", weight=5.0), # Texto completo, soporta búsquedas parciales
        TagField("raza"),                # Texto exacto, ideal para categorías o filtros rápidos
        NumericField("edad")             # Numérico, ideal para filtrar rangos (ej. edad > 3)
    )

    # Crear el índice indicando qué prefijo debe vigilar
    definicion = IndexDefinition(prefix=[prefijo], index_type=IndexType.HASH)
    r.ft(indice).create_index(esquema, definition=definicion)
    print(f"  FT.CREATE -> Índice '{indice}' creado exitosamente.\n")

    # Crear los datos (Hashes independientes para que RediSearch los indexe automáticamente)
    mascotas = [
        {"id": 1, "nombre": "Luna", "raza": "Labrador", "edad": 3},
        {"id": 2, "nombre": "Rocky", "raza": "Podenco", "edad": 5},
        {"id": 3, "nombre": "Toby", "raza": "Labrador", "edad": 7},
        {"id": 4, "nombre": "Nala", "raza": "Mastín", "edad": 2},
        {"id": 5, "nombre": "Coco", "raza": "Beagle", "edad": 9}
    ]

    print("  Insertando datos indexables (HSET):")
    for m in mascotas:
        clave = f"{prefijo}{m['id']}"
        
        # Redis guarda todos los valores del Hash como strings internamente,
        # pero RediSearch los interpretará según el esquema que definimos.
        r.hset(clave, mapping={
            "nombre": m["nombre"],
            "raza": m["raza"],
            "edad": m["edad"]
        })
        print(f"    HSET {clave} -> Nombre: {m['nombre']:<6} | Raza: {m['raza']:<9} | Edad: {m['edad']}")

    print(f"\nResultado: Se ha creado el índice '{indice}' y se han guardado e indexado automáticamente {len(mascotas)} registros independientes.")


""" 19- Realiza una búsqueda con índices en base a un campo """
def ejercicio19(r):
    titulo(
        19,
        "Realizar una búsqueda con índices en base a un campo",
        "Usa FT.SEARCH para buscar en el índice 'idx:mascotas' aquellas mascotas que coincidan con una raza específica usando el TagField."
    )

    indice = "idx:mascotas"
    
    # Comprobación de seguridad: verificar que el índice existe
    try:
        r.ft(indice).info()
    except ResponseError:
        print(f"  El índice '{indice}' no existe. Por favor, ejecuta el ejercicio 18 primero.")
        return

    # Definir el campo y el valor que vamos a buscar
    raza_buscada = "Labrador"
    
    # La sintaxis de RediSearch para los campos Tag (TagField) es @campo:{valor}
    # Usamos triple llave en el f-string porque necesitamos que queden llaves literales en el string final
    consulta_str = f"@raza:{{{raza_buscada}}}"
    
    print(f"  Consulta generada: FT.SEARCH {indice} '{consulta_str}'\n")

    # Ejecutar la búsqueda
    q = Query(consulta_str)
    resultados = r.ft(indice).search(q)

    # Mostrar los resultados
    print(f"  Se han encontrado {resultados.total} mascotas de la raza '{raza_buscada}':")
    
    for doc in resultados.docs:
        # RediSearch devuelve los campos como atributos del documento
        print(f"    - Clave: {doc.id:<10} | Nombre: {doc.nombre:<6} | Edad: {doc.edad}")

    print(f"\nResultado: La búsqueda indexada por el campo 'raza' devolvió {resultados.total} registros de forma instantánea.")
    
    
""" 20- Realiza un group  by usando los índices """
def ejercicio20(r):
    titulo(
        20,
        "Realizar un GROUP BY usando los índices",
        "Usa FT.AGGREGATE para agrupar las mascotas por raza y aplicar un reductor que cuente cuántas hay de cada una."
    )

    indice = "idx:mascotas"
    
    # Verificación de seguridad
    try:
        r.ft(indice).info()
    except ResponseError:
        print(f"  El índice '{indice}' no existe. Por favor, ejecuta el ejercicio 18 primero.")
        return

    print("  Ejecutando agregación: Agrupar por 'raza' y contar (COUNT)...\n")

    # Construir la consulta de agregación
    # - "*" indica que procese todos los documentos del índice
    # - group_by agrupa por el atributo "@raza"
    # - reducers.count() cuenta los elementos de cada grupo y le da el alias "cantidad"
    peticion = (
        AggregateRequest("*")
        .group_by("@raza", reducers.count().alias("cantidad"))
    )

    # Ejecutar la agregación
    resultados = r.ft(indice).aggregate(peticion)

    # Mostrar los resultados procesados
    print(f"  Se han formado {len(resultados.rows)} grupos distintos de razas:")
    
    for fila in resultados.rows:
        # RediSearch devuelve cada fila como una lista intercalada: ['raza', 'Labrador', 'cantidad', '2']
        # La convertimos en un diccionario para poder extraer los datos limpiamente
        datos_grupo = {fila[i]: fila[i+1] for i in range(0, len(fila), 2)}
        
        raza = datos_grupo.get("raza", "Desconocida")
        cantidad = datos_grupo.get("cantidad", 0)
        
        print(f"    - Raza: {raza:<9} | Total de mascotas: {cantidad}")

    print("\nResultado: La operación GROUP BY se ha completado internamente en Redis con éxito.")

if __name__ == "__main__":
    r = conectar()
    limpiar_datos(r)

    ejercicio01(r)
    ejercicio02(r)
    ejercicio03(r)
    ejercicio04(r)
    ejercicio05(r)
    ejercicio06(r)
    ejercicio07(r)
    ejercicio08(r)
    ejercicio09(r)
    ejercicio10(r)
    ejercicio11(r)
    ejercicio12(r)
    ejercicio13(r)
    ejercicio14(r)
    ejercicio15(r)
    ejercicio16(r)
    ejercicio17(r)
    ejercicio18(r)
    ejercicio19(r)
    ejercicio20(r)