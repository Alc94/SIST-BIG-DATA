import redis

conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0)
baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

baseDatosRedis.set('libro_1', 'Quijote')
baseDatosRedis.set('libro_2', 'Hamlet', ex=10)
baseDatosRedis.set('libro_3', 'El Señor de los Anillos')
baseDatosRedis.set('libro_4', 'Juegos de Tronos')
baseDatosRedis.set('libro_5', 'Las Crónicas de Narnia')
baseDatosRedis.set('libro_6', 'Mortadelo y Filemón')

baseDatosRedis.close()