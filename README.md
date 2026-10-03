# BeanRunner 🫘

Plataforma ligera para gestionar y ejecutar trabajos en segundo plano en Linux, desarrollada para la materia de **Programación de Sistemas Avanzados (2026B)** en CUCEI, Universidad de Guadalajara.

## Propósito

BeanRunner está planeado como un servicio (demonio) y cliente de línea de comandos para registrar, ejecutar, supervisar y controlar trabajos con concurrencia limitada, aislamiento de procesos, captura de `stdout`/`stderr`, persistencia y tolerancia a fallos. Actualmente están implementadas la validación y recepción inicial de comandos con asignación de UUID (RF-01/RF-02), junto con el modelo base de trabajos; el motor de ejecución y las funciones avanzadas siguen pendientes.

## Integrantes

| Integrante | Rol principal | Módulo técnico base | GitHub |
| :--- | :--- | :--- | :--- |
| **Alvarez Orozco Admin** | Líder de Proyecto y Scrum Master | Motor de procesos y concurrencia | [@AdminAlvarez](https://github.com/AdminAlvarez) |
| **Avila Arellano Bryan Aaron** | Ingeniero de Redes y CLI | Interfaz CLI y protocolo de red | [@AviAre16](https://github.com/AviAre16) |
| **Alvarado Ahedo Alan Ricardo** | Guardián de Datos y Resiliencia | Persistencia, logs y recuperación | [@AlanAlvarado23](https://github.com/AlanAlvarado23) |
| **Ortega Gutiérrez Franco Josep** | QA Lead, Git Admin y DevOps | Pruebas, trazabilidad y repositorio | [@FrancoJOG](https://github.com/FrancoJOG) |

## Tecnología y requisitos

- **Lenguaje:** Python 3.10 o posterior.
- **Sistema objetivo:** Linux (Ubuntu 22.04/24.04 o WSL2).
- **Dependencias externas:** ninguna; se utiliza la biblioteca estándar.
- **Herramientas opcionales:** `make` para los atajos de desarrollo y Git.

Python permite extender el proyecto con módulos de alto nivel sin perder acceso a capacidades del sistema operativo: `subprocess` para aislar procesos, `signal` para controlarlos, `socket` para comunicación y `json`/`os` para persistencia. La decisión está documentada en [ADR-001](docs/decisions/ADR-001.md).

## Instalación en Ubuntu o WSL2

En Windows, instala Ubuntu con `wsl --install -d Ubuntu` desde PowerShell como administrador y reinicia si se solicita. En la terminal de Ubuntu:

```bash
sudo apt update
sudo apt install -y python3 git make
git clone git@github.com:AdminAlvarez/BeanRunner.git
cd BeanRunner
```

No es necesario compilar el proyecto ni instalar un compilador C/C++.

## Ejecución

Ejecuta el programa directamente:

```bash
python3 -m src.main
```

Esto inicia el punto de entrada. Para ver ejemplos de validación y recepción de trabajos (sin ejecutar los comandos):

```bash
python3 -m src.main --demo
```

El receptor acepta un comando como texto (separado respetando comillas, sin
expansiones de shell) o como una lista de argumentos de texto, por ejemplo:
`"python3 -c \"print('hola')\""` o `["python3", "-c", "print('hola')"]`.
Rechaza valores vacíos, argumentos no textuales y cadenas con comillas sin
cerrar sin registrar un trabajo.

O usa los atajos del `Makefile`:

```bash
make          # Verifica la sintaxis Python
make run      # Inicia el punto de entrada de BeanRunner
make test     # Prueba el arranque, validación y recepción de trabajos
make clean    # Elimina cachés Python generadas
```

También puedes ejecutar las pruebas sin `make`:

```bash
python3 -m unittest discover -s tests -v
python3 verif/scripts/verify_hito1.py
```

## Estructura del repositorio

```text
BeanRunner/
├── README.md
├── Makefile
├── src/
│   ├── main.py                 # Punto de entrada y demostración opcional
│   ├── models.py               # Modelo de trabajo y estados
│   └── submitter.py            # Validación y recepción (RF-01/RF-02)
├── tests/
│   ├── test_main.py            # Pruebas del punto de entrada
│   └── test_submitter.py       # Pruebas de validación y recepción
├── docs/
│   ├── user-guide/
│   ├── technical-guide/
│   └── decisions/              # Registros de decisiones de arquitectura
├── verif/
│   ├── verification-plan/
│   ├── test-cases/
│   ├── scripts/                 # Verificación automatizada en Python
│   ├── test-data/
│   └── results/
└── project-management/
```

## Estado del proyecto

- **Hito actual:** Hito 1 - Núcleo local.
- **Entrega de avance:** 2 de octubre de 2026.
- **Revisión Técnica 1:** 6 de octubre de 2026.
- **Estado:** el arranque, el modelo base y la recepción/validación de trabajos están en Python. El motor de ejecución, la CLI completa, la concurrencia y la persistencia descritos en los requisitos aún deben desarrollarse.
