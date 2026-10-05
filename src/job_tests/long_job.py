"""Trabajo largo para demostrar supervisión y cancelación."""

import time

print("Trabajo largo iniciado", flush=True)

# Cada iteración dura un segundo y permite observar el progreso del proceso.
for i in range(60):
    print(f"Segundo {i + 1}/60", flush=True)
    time.sleep(1)

print("Trabajo terminado", flush=True)