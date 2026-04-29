import time
from functools import wraps
from datetime import datetime

def medir_tempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()
        duracao = fim - inicio

        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensagem = f"[{agora}] {func.__name__}: {duracao:.3f} segundos"

        print(mensagem)

        with open("log.txt", "a") as log:
            log.write(mensagem + "\n")

        return resultado
    return wrapper