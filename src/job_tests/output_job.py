import time

for i in range(100):
    print(f"Línea de salida número {i + 1}", flush=True)
    time.sleep(0.1)

print("Fin del trabajo")