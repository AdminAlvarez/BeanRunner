# Matriz de trazabilidad — Hito 1

Esta matriz relaciona las funciones del núcleo local con su implementación,
casos de prueba y evidencia disponible. `Automatizado` significa que existe
una prueba en el repositorio; no implica que se haya ejecutado en cada sistema
operativo objetivo. La evidencia por plataforma se documenta en
[`results/`](results/).

| Función / requisito | Implementación principal | Caso(s) / prueba(s) | Estado y alcance |
|---|---|---|---|
| Enviar y registrar un trabajo válido (RF-01) | `src/submitter.py`, `src/models.py` | TC-001; `test_submitter.py` | Implementado; creación en memoria. |
| Validar entrada y devolver ID único (RF-02) | `src/submitter.py` | TC-001, TC-002; `test_submitter.py` | Implementado; entradas inválidas producen error controlado. |
| Ejecutar como proceso separado (RF-04) | `src/executor.py`, `src/Job_Runner.py` | TC-003, TC-005, TC-006; `test_job_runner.py` | Implementado con `subprocess.Popen`; sin shell implícito. |
| Limitar concurrencia y encolar trabajos (RF-05) | `src/Job_Runner.py` | `test_runner_starts_queued_jobs_when_a_slot_frees` | Implementado; máximo predeterminado 3, solo durante la ejecución actual. |
| Mantener estados del ciclo de vida (RF-06) | `src/models.py`, `src/executor.py` | TC-003, TC-005, TC-006; `test_job_runner.py` | `QUEUED`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELED`. |
| Registrar timestamps y código de salida (RF-07) | `src/models.py`, `src/executor.py` | TC-003, TC-006; `test_job_runner.py` | Implementado para procesos lanzados. |
| Consultar el estado por ID (RF-08) | `src/manager.py`, `src/main.py` | TC-003; `test_main.py` | Implementado en CLI local; los datos son en memoria. |
| Listar y filtrar trabajos (RF-09) | `src/manager.py`, `src/main.py` | TC-004; `test_manager.py` | Implementado, incluidos lista vacía y filtros. |
| Solicitar cancelación (RF-10) | `src/executor.py`, `src/manager.py` | TC-005; `test_job_runner.py`, `test_manager.py` | Implementado para trabajos en cola y procesos activos. |
| Capturar `stdout` y `stderr` (RF-11) | `src/executor.py`, `src/models.py`, `src/main.py` | TC-006; `test_job_runner.py` | Capturados por separado y consultables al finalizar. |
| Continuar tras una solicitud inválida (RNF-08) | `src/main.py`, `src/submitter.py` | TC-002; `test_main.py`, `test_submitter.py` | Automatizado: un envío inválido no cierra la CLI ni impide otro válido. |
| Verificación repetible (RNF-20) | `Makefile`, `verif/scripts/verify_hito1.py` | Suite unitaria y 4 verificaciones funcionales | Un comando para la suite y otro para la verificación end-to-end; requiere Python. |

## Entregables de ingeniería

| Entregable | Ubicación | Estado |
|---|---|---|
| Estructura y ejecución local | `src/`, `tests/`, `verif/`, `Makefile` | Disponible. |
| Instrucciones de construcción/ejecución | [`../README.md`](../README.md) | Actualizadas para el CLI interactivo y las pruebas. |
| Arquitectura y decisiones | [`../docs/decisions/`](../docs/decisions/) | ADR-001, ADR-002 y ADR-003. |
| Modelo preliminar de estados | [`../docs/technical-guide/state-model.md`](../docs/technical-guide/state-model.md) | Describe estados implementados y distingue la recuperación futura. |
| Casos de prueba | [`test-cases/`](test-cases/) | TC-001 a TC-006. |
| Script de verificación | [`scripts/verify_hito1.py`](scripts/verify_hito1.py) | Comprueba arranque, recuperación de entrada inválida, código no cero y cancelación. |
| Evidencia ejecutada | [`results/`](results/) | Separada por corrida y entorno; revisar el reporte antes de afirmar soporte Linux. |
| Responsabilidades y cronograma del equipo | GitHub Projects | Gestionados en el proyecto del equipo, fuera de este repositorio. |
| Registros de uso de IA | [`../docs/ai-usage/`](../docs/ai-usage/) | Incluye registro de apoyo y validación realizada en esta rama. |

## Fuera del alcance implementado

No se marca como completada la persistencia, recuperación tras reinicio,
`INTERRUPTED`, daemon permanente ni operación remota. Estos elementos
requieren trabajo posterior y no deben inferirse de la existencia de ADR o
requisitos documentados.
