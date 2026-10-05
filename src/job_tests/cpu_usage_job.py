"""Trabajo de prueba que ocupa CPU durante aproximadamente 20 segundos."""

import time

print("Iniciando trabajo intensivo de CPU", flush=True)

# `inicio` permite detener el ciclo después del tiempo definido.
inicio = time.time()

while time.time() - inicio < 20:
    # Trabajo deliberado de CPU para observar el proceso desde el sistema.
    x = 0
    for i in range(1000000):
        x += i * i

print("Trabajo terminado", flush=True)