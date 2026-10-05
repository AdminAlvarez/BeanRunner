"""Trabajo de prueba que escribe un error y sale con código 1."""

import time
import sys

print("Iniciando trabajo")

time.sleep(2)

# Se usa stderr para comprobar que BeanRunner no lo mezcla con stdout.
print("ERROR: ocurrió un problema", file=sys.stderr)

# El código distinto de cero hace que el estado final sea FAILED.
sys.exit(1)