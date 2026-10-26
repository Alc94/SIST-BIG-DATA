import redis


# conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0)
conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0,decode_responses=True)

baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

res1 = baseDatosRedis.json().set("usuarios:1", "$", {"nombre": "Jorge", "apellido": "Baron", "edad": 37})
res2 = baseDatosRedis.json().set("usuarios:2", "$", {"nombre": "Lucía", "apellido": "Benitez", "edad": 24})

print("Usuarios: ")   
for clave in baseDatosRedis.scan_iter('usuarios*'):
   print(clave)


baseDatosRedis.close()