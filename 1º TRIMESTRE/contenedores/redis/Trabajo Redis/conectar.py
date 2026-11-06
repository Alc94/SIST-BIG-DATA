import os
import redis

def conectar():
    conexionRedis = redis.ConnectionPool(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=0,
        decode_responses=True,
    )
    baseDatosRedis = redis.Redis(connection_pool=conexionRedis)
    baseDatosRedis.ping()
    return baseDatosRedis