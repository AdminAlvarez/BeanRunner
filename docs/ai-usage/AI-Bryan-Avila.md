# Bitácora de Uso de Inteligencia Artificial
**Autor:** Bryan Aarón Avila Arellano
**Módulo/Funcionalidad:** JobManager (Listado y Cancelación de Trabajos - RF-09, RF-10), Pruebas Unitarias y Debugging de Integración.
**Herramienta Utilizada:** Gemini

## 1. Propósito General
Se utilizó asistencia de Inteligencia Artificial durante el desarrollo del Hito 1 (Avance 1) para comprender los requerimientos técnicos del proyecto, estructurar el código inicial de los módulos asignados y resolver problemas para la integración del código.

## 2. Casos de Uso Específicos

### A. Comprensión de Requisitos y Teoría
* **Interacción:** Se solicitó a la IA explicar la diferencia entre el uso de hilos (`threading`) y procesos (`subprocess`) en Python para cumplir con el requerimiento de aislamiento.
* **Resultado:** Comprensión profunda de cómo Linux maneja los procesos hijos, la asignación de PIDs y el uso de señales POSIX. Esto permitió entender por qué un proceso cancelado arroja un *Exit Code* de `-15` (SIGTERM).

### B. Generación de Código y Estructura
* **Interacción:** Se requirió apoyo para crear la clase `JobManager` enfocada en cumplir los requerimientos **RF-09** (Listar trabajos) y **RF-10** (Cancelar trabajos).
* **Resultado:** Generación de la lógica para filtrar trabajos por estado, formatear la salida en una tabla legible para la CLI y manejar el estado de cancelación en memoria antes de acoplarlo al sistema de procesos.

### C. Refactorización e Integración Continua
* **Interacción:** Tras el *push* y la refactorización arquitectónica realizada por el equipo (orquestador `JobRunner`), se usó la IA para analizar los cambios remotos y entender cómo adaptar el `JobManager`.
* **Resultado:** Se integró exitosamente el módulo de listado y cancelación delegando la llamada POSIX al `JobExecutor`, respetando el patrón de concurrencia y los bloqueos (`threading.RLock`) del nuevo motor central.

### D. Resolución de Errores (Debugging)
Durante las pruebas de la consola interactiva (`main.py`), la IA fue clave para rastrear y solucionar un bug crítico a la hora de integrar los archivos:
* **AttributeError en `executor.py`:** Se diagnosticó un fallo al ejecutar el comando `status`, causado porque las fechas se estaban guardando como texto (`.isoformat()`) prematuramente en lugar de objetos `datetime` nativos.

### E. Apoyo para manipular archivos entre GitHub y la terminal WSL2
Debido a que contaba con poca experiencia usando GitHub de forma avanzada para la elaboración de proyectos grupales, se utilizó a la IA como asesor para el uso básico de GitHub mediante una terminal (clonar GitHub, realizar commits, etc.).

## 3. Impacto y Reflexión
El uso de la IA no se basó únicamente en generar código, sino que funcionó como un tutor a la hora de comprender la estructura de un JobRunner y permitió agilizar el desarrollo de la tabla de la CLI, diagnosticar errores de dependencias compartidas.
