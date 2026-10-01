import time

print("Iniciando trabajo intensivo de CPU", flush=True)

inicio = time.time()

while time.time() - inicio < 20:
    x = 0
    for i in range(1000000):
        x += i * i

print("Trabajo terminado", flush=True)