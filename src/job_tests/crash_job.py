"""Trabajo de prueba que termina con una excepción no controlada."""

import time

print("Trabajo iniciado", flush=True)

time.sleep(3)

# La excepción hace que Python termine con un código de salida distinto de cero.
print("Provocando error...", flush=True)

raise RuntimeError("Error simulado del programa")