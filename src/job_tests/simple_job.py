"""Trabajo corto de ejemplo que imprime progreso y termina correctamente."""

import time

print("Trabajo iniciado")

# Simula cinco pasos para que haya progreso visible durante su ejecución.
for i in range(5):
    print(f"Procesando paso {i + 1}/5")
    time.sleep(1)

print("Trabajo terminado correctamente")