# Reporte de verificación — Ubuntu en WSL2

## Datos de la ejecución

| Campo | Valor |
|---|---|
| Fecha y hora local | 2026-10-04 22:08, UTC-06:00 |
| Plataforma | Ubuntu sobre WSL2 |
| Python | 3.14.4 |
| Rama | `francojog/hito-1-complete-submission` |
| Dependencias externas | Ninguna |

## Resultado de la ejecución

Tras corregir la prueba interactiva para usar `sys.executable` en lugar de
depender de que el nombre `python` esté instalado, se ejecutaron:

```bash
python3 -m unittest discover -s tests -v
python3 verif/scripts/verify_hito1.py
```

| Comando | Resultado |
|---|---|
| Suite unitaria | PASS — 19 pruebas aprobadas. |
| Verificación funcional | PASS — 4/4: arranque, entrada inválida y recuperación, código de salida no cero y cancelación de proceso activo. |

La suite había fallado inicialmente en
`test_interactive_mode_recovers_from_invalid_command_and_accepts_job`: la
prueba intentaba iniciar `python`, pero esa instalación de Ubuntu solo
proporciona `python3`. Ahora usa la misma ruta de intérprete que ejecuta la
suite, de modo que la prueba funciona en Windows y Linux.

## Demostración manual registrada

En la CLI interactiva se ejecutó `submit ls -la`. El trabajo pasó de
`RUNNING` a `SUCCEEDED`, con código de salida `0`; el listado mostró el ID y
PID del proceso.

## Alcance

Estos resultados corresponden a Ubuntu sobre WSL2 con Python 3.14.4. Los
trabajos se mantienen solo en memoria; este reporte no verifica persistencia,
recuperación tras reinicio ni operación remota.
