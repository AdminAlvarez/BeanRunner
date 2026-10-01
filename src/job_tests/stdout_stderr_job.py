import sys
import time

for i in range(10):
    print(f"INFO: paso {i + 1}", flush=True)

    if i == 4:
        print("WARNING: ocurrió algo inesperado", file=sys.stderr, flush=True)

    time.sleep(0.5)

print("Trabajo completado", flush=True)