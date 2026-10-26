import redis

conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0)
baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

baseDatosRedis.set("libro_1","Juego de Tronos")

baseDatosRedis.close()