# BeanRunner 🫘

Plataforma ligera de gestión y ejecución de trabajos en segundo plano para sistemas Linux, desarrollada para la materia de **Programación de Sistemas Avanzados (2026B)** en CUCEI, Universidad de Guadalajara.

---

## 📌 Propósito del Proyecto

**BeanRunner** es un servicio (demonio) y cliente de línea de comandos para registrar, ejecutar, supervisar y controlar trabajos del sistema operativo en entornos Linux con concurrencia controlada, gestión de procesos (`fork`/`exec`), captura de salidas (`stdout`/`stderr`), persistencia y tolerancia a fallos.

---

## 👥 Integrantes del Equipo (Beanner)

| Integrante | Rol Principal | Módulo Técnico Base | GitHub |
| :--- | :--- | :--- | :--- |
| **Alvarez Orozco Admin** | Líder de Proyecto & Scrum Master | Motor de Procesos y Concurrencia (`fork`/`exec`) | [@AdminAlvarez](https://github.com/AdminAlvarez) |
| **Avila Arellano Bryan Aaron** | Ingeniero de Redes & CLI | Interfaz CLI y Protocolo de Red Sockets TCP | [@AviAre16](https://github.com/AviAre16) |
| **Alvarado Ahedo Alan Ricardo** | Guardián de Datos & Resiliencia | Persistencia, Logs, Captura `stdout`/`stderr` y Recuperación | [@AlanAlvarado23](https://github.com/AlanAlvarado23) |
| **Ortega Gutiérrez Franco Josep** | QA Lead, Git Admin & DevOps | Suite de Pruebas, Matriz de Trazabilidad, Makefile y Repositorio | [@FrancoJOG](https://github.com/FrancoJOG) |

---

## 🛠️ Prerrequisitos y Tecnologías

El proyecto se desarrolla bajo el paradigma de **Programación Orientada a Objetos** en **C++17** y **Programación de Sistemas Linux (API POSIX)**.

* **Sistema Operativo:** Linux (Ubuntu 22.04 LTS / 24.04 LTS nativo o mediante **WSL2** en Windows 10/11).
* **Compilador:** `g++` (versión 11 o superior) con soporte para C++17.
* **Herramientas de Construcción y Depuración:** `make`, `gdb`, `git`.
* **Editor Recomendado:** Visual Studio Code con la extensión **WSL**.

---

## 🚀 Guía de Instalación y Configuración del Entorno (Windows / WSL2)

Este proyecto cumple con los requisitos **RNF-01** (ejecución nativa en Linux) y **RNF-02** (construcción reproducible).

### 1. Instalación de Ubuntu mediante WSL2 en Windows
1. Abre **PowerShell** o **Terminal de Windows** como Administrador y ejecuta:
   ```powershell
   wsl --install -d Ubuntu
   ```
2. Reinicia tu computadora.
3. Al iniciar, asigna tu nombre de usuario y contraseña en la terminal de Ubuntu.

### 2. Instalación del Compilador `g++`, `make`, `git` y Depurador `gdb`
Dentro de la terminal de Ubuntu (WSL2), ejecuta los siguientes comandos completos para actualizar el sistema e instalar el herramental de desarrollo:

```bash
# 1. Actualizar la lista de paquetes del sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar compilador g++, make, git y depurador gdb
sudo apt install -y build-essential g++ gdb git make
```

Confirma que todas las herramientas están listas verificando sus versiones:
```bash
g++ --version
make --version
git --version
gdb --version
```

---

## 💻 Clonar y Abrir el Proyecto

1. **Clonar el repositorio mediante SSH:**
   ```bash
   cd ~
   git clone git@github.com:AdminAlvarez/BeanRunner.git
   cd BeanRunner
   ```

2. **Abrir en VS Code conectado a WSL:**
   ```bash
   code .
   ```

---

## 🔨 Construcción y Compilación

El proyecto cumple con el estándar de ingeniería de Beanner y el requisito **RNF-19**. Todo el código debe compilar sin advertencias (*zero warnings*) utilizando las banderas estrictas del compilador:
`-std=c++17 -Wall -Wextra -Werror -pedantic`

* **Compilar el proyecto completo:**
  ```bash
  make
  ```

* **Limpiar binarios y archivos objeto generados:**
  ```bash
  make clean
  ```

* **Recompilar desde cero (limpiar y compilar):**
  ```bash
  make re
  ```

---

## 🧪 Ejecución de Pruebas y Verificación Automatizada

Cumpliendo con **RNF-20** (ejecución de pruebas con un único comando), el repositorio cuenta con reglas en el `Makefile` y scripts bash para ejecutar la suite de pruebas unitarias y de integración.

### 1. Ejecutar la suite completa de pruebas
```bash
make test
```

### 2. Ejecutar scripts de verificación individual (Casos TC-001 a TC-006)
Los scripts de prueba se encuentran en el directorio `verif/scripts/`:

```bash
# Otorgar permisos de ejecución a los scripts
chmod +x verif/scripts/*.sh

# Ejecutar el script inicial de verificación del Hito 1
./verif/scripts/verify_hito1.sh
```

### 3. Probar el archivo de verificación de entorno
```bash
# Compilar y ejecutar el test de entorno de compilación
g++ -std=c++17 -Wall -Wextra -Werror -pedantic test.cpp -o test_bin
./test_bin
rm test_bin
```

Las evidencias producidas por las ejecuciones de prueba se almacenan en la carpeta `verif/results/` en formato log con marca temporal y commit asociado.

---

## 📂 Estructura del Repositorio

Cumpliendo con la norma oficial de arquitectura y repositorio de la materia:

```text
BeanRunner/
├── README.md                           # Visión, construcción, ejecución y pruebas
├── Makefile                            # Script de compilación estricta (-Werror)
├── .gitignore                          # Exclusión de binarios y temporales
├── src/                                # Código fuente de producción (.cpp y .hpp)
├── docs/                               # Documentación técnica del proyecto
│   ├── user-guide/                     # Guía de instalación y operación
│   ├── technical-guide/                # Arquitectura, protocolo, persistencia y procesos
│   ├── decisions/                      # Registros de decisiones de arquitectura (ADRs)
│   ├── ai-usage/                       # Evidencia y registro del uso de IA
│   ├── change-requests/                # Análisis de cambios de alcance (CR)
│   └── incidents/                      # Registro de incidentes y regresiones
├── verif/                              # Plan de pruebas, matriz y automatización
│   ├── verification-plan/              # Matriz de trazabilidad (traceability-matrix.md)
│   ├── test-cases/                     # Especificación de casos (TC-001 a TC-024)
│   ├── scripts/                        # Scripts bash de verificación automatizada
│   ├── test-data/                      # Datos controlados para pruebas
│   └── results/                        # Evidencia reproducible por ejecución
├── project-management/                 # Roles, RACI, minutas y cronograma
└── .github/
    └── ISSUE_TEMPLATE/                 # Plantillas para requisitos, tareas y defectos
```

---

## 📈 Estado del Proyecto y Próximo Hito

* **Hito Actual:** **Hito 1 - Núcleo Local**
* **Fecha de Entrega de Avance:** 2 de Octubre de 2026
* **Revisión Técnica 1 (RT-1 / Presencial Obligatoria):** 6 de Octubre de 2026
* **Estado de Desarrollo:** En fase de integración del motor de procesos local (`fork`/`exec`), máquina de estados preliminar (`QUEUED`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELED`), trazabilidad de requisitos `RF-01` a `RF-10` y creación de casos de prueba `TC-001` a `TC-006`.
