import sys
import time

duracion = int(sys.argv[1]) if len(sys.argv) > 1 else 5

print(f"Trabajo iniciado. Duración: {duracion} segundos", flush=True)

for i in range(duracion):
    print(f"Progreso: {i + 1}/{duracion}", flush=True)
    time.sleep(1)

print("Trabajo completado correctamente", flush=True)