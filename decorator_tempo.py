import time
from functools import wraps

def medir_tempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()
        duracao = fim - inicio

        with open("log.txt", "a") as log:
            log.write(f"{func.__name__}: {duracao:.6f} segundos\n")

        return resultado
    return wrapper