"""Trabajo de prueba cuya duración se puede indicar como argumento."""

import sys
import time

# Tiempo en segundos solicitado al programa; usa cinco segundos por defecto.
duracion = int(sys.argv[1]) if len(sys.argv) > 1 else 5

print(f"Trabajo iniciado. Duración: {duracion} segundos", flush=True)

# `i` cuenta el progreso desde cero; el mensaje mostrado comienza desde uno.
for i in range(duracion):
    print(f"Progreso: {i + 1}/{duracion}", flush=True)
    time.sleep(1)

print("Trabajo completado correctamente", flush=True)