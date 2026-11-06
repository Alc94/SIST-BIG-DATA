import redis


# conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0)
conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0,decode_responses=True)

baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

claves = baseDatosRedis.keys()

for clave in claves:
 		print('Clave:', clave , ' y Valor: ', baseDatosRedis.get(clave))
