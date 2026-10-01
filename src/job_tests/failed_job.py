import time
import sys

print("Iniciando trabajo")

time.sleep(2)

print("ERROR: ocurrió un problema", file=sys.stderr)

sys.exit(1)