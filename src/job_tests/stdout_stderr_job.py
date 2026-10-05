"""Trabajo que escribe en stdout y stderr para verificar su separación."""

import sys
import time

# Genera mensajes normales mientras el proceso sigue en ejecución.
for i in range(10):
    print(f"INFO: paso {i + 1}", flush=True)

    if i == 4:
        # El parámetro file dirige este aviso al canal separado de errores.
        print("WARNING: ocurrió algo inesperado", file=sys.stderr, flush=True)

    time.sleep(0.5)

print("Trabajo completado", flush=True)