"""Trabajo que genera muchas líneas para probar la captura de stdout."""

import time

# `i` identifica la línea que el proceso está escribiendo.
for i in range(100):
    print(f"Línea de salida número {i + 1}", flush=True)
    time.sleep(0.1)

print("Fin del trabajo")