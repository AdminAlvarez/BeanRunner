# BeanRunner

BeanRunner es un prototipo académico para enviar, ejecutar y supervisar
trabajos locales como procesos separados. Se desarrolla para la materia
Programación de Sistemas Avanzados (2026B), CUCEI, Universidad de Guadalajara.

## Alcance del Hito 1

La versión actual permite iniciar trabajos locales desde una CLI interactiva,
asignarles un ID, ejecutarlos en procesos hijos con concurrencia limitada,
consultar/listar trabajos, cancelarlos y recuperar su código de salida y
`stdout`/`stderr`. Una entrada inválida se informa sin cerrar la sesión.

Los trabajos y sus resultados solo viven en memoria. No se incluye un daemon
permanente, persistencia, recuperación tras reinicio ni operación remota.

## Requisitos

- Python 3.10 o posterior.
- Sistema objetivo del equipo: Linux (Ubuntu 22.04/24.04 o WSL2).
- No se requieren paquetes externos; se utiliza la biblioteca estándar.
- `make` es opcional.

## Instalación en Ubuntu o WSL2

En Windows, instala Ubuntu si todavía no tienes una distribución:

```powershell
wsl --install -d Ubuntu
```

En la terminal de Ubuntu:

```bash
sudo apt update
sudo apt install -y python3 git make
git clone https://github.com/AdminAlvarez/BeanRunner.git
cd BeanRunner
```

## Ejecución interactiva

Desde la raíz del repositorio:

```bash
python3 -m src.main --interactive
```

Comandos disponibles:

| Comando | Acción |
|---|---|
| `submit <comando>` | Valida, registra y ejecuta un trabajo; muestra su ID. |
| `status <job-id>` | Consulta estado, PID y metadatos del trabajo. |
| `list [ESTADO]` | Lista los trabajos o filtra por estado. |
| `output <job-id>` | Muestra `stdout` y `stderr` cuando estén disponibles. |
| `cancel <job-id>` | Cancela un trabajo en cola o solicita terminar su proceso. |
| `help` | Muestra ayuda. |
| `exit` | Cierra la sesión y cancela procesos todavía activos. |

Ejemplo de sesión:

```text
beanrunner> submit python3 -c "print('hola')"
beanrunner> list
beanrunner> status <job-id>
beanrunner> output <job-id>
beanrunner> exit
```

Los argumentos se separan respetando comillas, pero los trabajos se inician
sin shell implícito. Envía únicamente comandos y programas confiables.
`max_concurrency` es 3 por defecto; el resto de trabajos válidos espera en
cola hasta que haya un espacio disponible.

Sin opciones, `python3 -m src.main` conserva el comportamiento de arranque
simple y termina después de mostrar un mensaje. Para una demostración
automatizada de ejecución y cancelación:

```bash
python3 -m src.main --run-job-demo
```

Para ver los ejemplos de recepción y validación sin ejecutar los comandos:

```bash
python3 -m src.main --demo
```

## Pruebas y verificación

```bash
python3 -m unittest discover -s tests -v
python3 verif/scripts/verify_hito1.py
```

Con `make` también se puede ejecutar:

```bash
make check
make test
```

`make test` ejecuta la suite unitaria y el script end-to-end. Los casos de
prueba están en [`verif/test-cases/`](verif/test-cases/); el reporte de la
verificación actual se guarda en [`verif/results/`](verif/results/).

## Estructura

```text
src/                         Código del servicio local y la CLI
tests/                       Pruebas unitarias
docs/decisions/              ADR de arquitectura
docs/technical-guide/        Guías técnicas, incluido el modelo de estados
docs/ai-usage/               Registro del apoyo de herramientas de IA
verif/test-cases/            Casos de prueba funcionales
verif/scripts/               Verificación automatizada
verif/results/               Reportes de ejecución
project-management/          Material de gestión del proyecto
```

## Arquitectura y trazabilidad

- [ADR-001](docs/decisions/ADR-001.md): lenguaje y plataforma.
- [ADR-002](docs/decisions/ADR-002.md): aislamiento de procesos y concurrencia.
- [ADR-003](docs/decisions/ADR-003.md): estrategia futura de persistencia; todavía no implementada.
- [Modelo de estados](docs/technical-guide/state-model.md): ciclo de vida
  implementado y funciones futuras distinguidas.
- [Matriz de trazabilidad del Hito 1](verif/traceability-matrix.md): relación
  entre los requisitos, casos de prueba, implementación y evidencia.

## Equipo

| Integrante | Responsabilidad principal | GitHub |
|---|---|---|
| Alvarez Orozco Admin | Liderazgo; motor de procesos y concurrencia | [@AdminAlvarez](https://github.com/AdminAlvarez) |
| Avila Arellano Bryan Aaron | CLI, redes y gestión del proyecto | [@AviAre16](https://github.com/AviAre16) |
| Alvarado Ahedo Alan Ricardo | Persistencia, registros y resiliencia | [@AlanAlvarado23](https://github.com/AlanAlvarado23) |
| Ortega Gutiérrez Franco Josep | QA, trazabilidad y repositorio | [@FrancoJOG](https://github.com/FrancoJOG) |

## Estado de entrega

El prototipo y sus pruebas automatizadas se han verificado en Windows con
Python 3.14.3. La revisión técnica está dirigida a Linux/Ubuntu/WSL2; el equipo
debe ejecutar y conservar también el resultado en esa plataforma antes de
presentar la evidencia como validación Linux. Consulta el reporte de
verificación para conocer el entorno exacto de cada ejecución.
