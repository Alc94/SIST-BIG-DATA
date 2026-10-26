import os
import redis

def conectar():
    cliente = redis.Redis(
        host = os.getenv("REDIS_HOST", "localhost"),
        port = int(os.getenv("REDIS_HOST", 6379)),
        decode_responses = True,
    )

    cliente.ping()
    return cliente