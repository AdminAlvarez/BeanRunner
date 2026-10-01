import time

print("Trabajo largo iniciado", flush=True)

for i in range(60):
    print(f"Segundo {i + 1}/60", flush=True)
    time.sleep(1)

print("Trabajo terminado", flush=True)