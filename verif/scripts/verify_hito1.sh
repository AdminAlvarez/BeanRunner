#!/bin/bash
set -e

echo "=================================================="
echo "  BeanRunner - Verificación de Entorno (Hito 1)  "
echo "=================================================="

if [ -f "./bin/jobrunnerd" ]; then
    ./bin/jobrunnerd
    echo "[PASS] El ejecutable se construyó correctamente y retornó código de salida 0."
else
    echo "[FAIL] No se encontró el ejecutable bin/jobrunnerd."
    exit 1
fi