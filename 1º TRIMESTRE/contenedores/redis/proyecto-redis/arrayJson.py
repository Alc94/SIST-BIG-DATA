import redis


# conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0)
conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0,decode_responses=True)

baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

baseDatosRedis.json().set("usuarios_array", "$", [])
res3 = baseDatosRedis.json().arrappend("usuarios_array", "$", {"nombre": "Pepe", "apellido": "Sanchez", "edad": 45})
res4 = baseDatosRedis.json().arrappend("usuarios_array", "$", {"nombre": "Calisto", "apellido": "Melibea", "edad": 67})

res1 = baseDatosRedis.json().get("usuarios_array", '$[?(@.edad > 50)]')
res2 = baseDatosRedis.json().get("usuarios_array", '$[?(@.nombre == "Pepe")]')

print("Resultado de los mayores de 50 años: ", res1)
print("Resultado de quien se llame Pepe: ", res2)

baseDatosRedis.close()