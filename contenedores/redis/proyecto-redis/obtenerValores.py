import redis

conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0)
baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

print(baseDatosRedis.get("libro_1"))

print(baseDatosRedis.get("libro_1").decode("utf-8"))

print(baseDatosRedis.get("libro_2"))

baseDatosRedis.close()