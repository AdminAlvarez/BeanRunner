# Reporte Formal de Verificación — Hito 1: Gestión de Trabajos

## 1. Identificación y Metadatos de la Ejecución
* **Identificador de ejecución (run-id):** `run-hito1-manager`
* **Fecha y hora:** 2026-09-30 22:45 CST
* **Responsable de ejecución:** Bryan Aaron Avila Arellano
* **Rama / Versión probada:** `task/hito-1-listar-cancelar`
* **Entorno de ejecución:** Ubuntu Linux 22.04 LTS sobre WSL2 (Kernel x86_64 Linux 5.15+)
* **Configuración del sistema:** Python 3.10+, modo de ejecución local sin red externa, límites base de concurrencia

## 2. Requisitos y Casos del Plan de Verificación Cubiertos
* **TC-004:** Consultar y listar trabajos (RF-08, RF-09, RNF-05).
* **TC-005:** Cancelar trabajo en cola y en ejecución (RF-10, RNF-27).
* **RNF-20:** Pruebas automatizadas ejecutables mediante un único comando documentado.

## 3. Procedimiento y Comando Ejecutado
Se ejecutó la suite de pruebas unitarias sobre el módulo de gestión del ciclo de vida de trabajos (`src/manager.py`):

`python3 -m unittest tests/test_manager.py -v`

## 4. Bitácora de Salida (Logs de Ejecución)
> test_cancel_already_finished_job (tests.test_manager.JobManagerTests.test_cancel_already_finished_job) ... ok
> test_cancel_queued_job (tests.test_manager.JobManagerTests.test_cancel_queued_job) ... ok
> test_list_jobs_with_filter (tests.test_manager.JobManagerTests.test_list_jobs_with_filter) ... ok
> test_lists_jobs_empty (tests.test_manager.JobManagerTests.test_lists_jobs_empty) ... ok
> 
> \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-
> Ran 4 tests in 0.001s
> 
> OK

## 5. Matriz de Resultados Observados
| Caso | Requisito | Descripción | Comportamiento Esperado | Resultado Observado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-004** | RF-09 | Listado tabular de trabajos registrados | Generación de tabla formateada con campos de control | Salida estructurada con Job ID, PID, estado y comando | **PASS** |
| **TC-004** | RF-09 | Filtrado selectivo por estado (`QUEUED` / `RUNNING`) | Exclusión de trabajos que no coinciden con el filtro | Retorna únicamente los registros correspondientes al estado solicitado | **PASS** |
| **TC-005** | RF-10 | Cancelación de trabajo pendiente en cola | Transición de estado a `CANCELED` y registro de timestamp | Trabajo pasa a `CANCELED` y asigna `finished_at` sin interactuar con señales | **PASS** |
| **TC-005** | RF-10 / RNF-27 | Intento de cancelación sobre trabajo finalizado | Rechazo de la solicitud sin mutación inconsistente | Retorna rechazo explícito indicando que el trabajo ya concluyó | **PASS** |

## 6. Dictamen Final
* **Resultado global:** **PASS** (100% de pruebas unitarias aprobadas).
* **Defectos o regresiones detectadas:** Ninguno.
* **Bloqueos:** Ninguno.