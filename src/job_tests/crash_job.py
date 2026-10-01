import time

print("Trabajo iniciado", flush=True)

time.sleep(3)

print("Provocando error...", flush=True)

raise RuntimeError("Error simulado del programa")