import time

print("Trabajo iniciado")

for i in range(5):
    print(f"Procesando paso {i + 1}/5")
    time.sleep(1)

print("Trabajo terminado correctamente")