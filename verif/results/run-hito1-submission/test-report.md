# Reporte de verificación — Entrega del Hito 1

## Datos de la ejecución

| Campo | Valor |
|---|---|
| Fecha y hora local | 2026-10-03 00:10, UTC-06:00 |
| Plataforma | Windows |
| Python | 3.14.3 |
| Rama | `francojog/hito-1-complete-submission` |
| Dependencias externas | Ninguna |

## Comandos y resultados

| Comando | Resultado |
|---|---|
| `python -m unittest discover -s tests -v` | PASS — 19 pruebas aprobadas. |
| `python verif/scripts/verify_hito1.py` | PASS — 4/4 verificaciones: arranque, entrada inválida y recuperación, código de salida no cero y cancelación de proceso activo. |
| `python -m src.main --help` | PASS — se muestran las opciones CLI. |
| `git -c core.whitespace=cr-at-eol diff --check HEAD` | PASS — sin errores de whitespace en el diff completo de la rama. |

## Alcance y limitaciones de evidencia

Los resultados anteriores corresponden a Windows y a la versión de código
presente en esta rama al ejecutar los comandos. No prueban por sí mismos el
comportamiento en Linux.

Se consultaron las distribuciones WSL instaladas; la única listada fue
`docker-desktop`. No hay una distribución Ubuntu disponible en este entorno,
así que no se ejecutaron aquí los comandos de prueba en Ubuntu/WSL2. Antes de
la revisión técnica, un integrante debe ejecutar la suite y el script de
verificación en la plataforma Linux objetivo y guardar una corrida separada
con sus resultados reales.

La aplicación tampoco implementa persistencia ni recuperación después de
cerrarse; los trabajos y resultados se conservan solo durante la sesión.
