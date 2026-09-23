# BeanRunner 🫘

Plataforma ligera de gestión y ejecución de trabajos en segundo plano para sistemas Linux, desarrollada como parte de la materia de **Programación de Sistemas Avanzados (2026B)** en CUCEI, Universidad de Guadalajara.

---

## 📌 Propósito del Proyecto

**BeanRunner** es un servicio (demonio) y cliente de línea de comandos diseñado para registrar, ejecutar, supervisar y controlar trabajos del sistema operativo en entornos Linux con concurrencia controlada, gestión estricta de procesos, captura de salidas (`stdout`/`stderr`), persistencia y tolerancia a fallos.

---

## 👥 Integrantes del Equipo (Beanner)

| Integrante | Rol Principal | Módulo Técnico Base | GitHub |
| :--- | :--- | :--- | :--- |
| **Alvarez Orozco Admin** | Líder de Proyecto & Scrum Master | Motor de Procesos y Concurrencia (`fork`/`exec`) | [@AdminAlvarez](https://github.com/AdminAlvarez) |
| **Avila Arellano Bryan Aaron** | Ingeniero de Redes & CLI | Interfaz CLI y Protocolo de Red Sockets TCP | [@AviAre16](https://github.com/AviAre16) |
| **Alvarado Ahedo Alan Ricardo** | Guardián de Datos | Persistencia, Logs, Captura `stdout`/`stderr` y Recuperación | [@AlanAlvarado23](https://github.com/AlanAlvarado23) |
| **Ortega Gutiérrez Franco Josep** | QA Lead, Git Admin & DevOps | Automatización de Pruebas, Trazabilidad y Repositorio | [@FrancoJOG](https://github.com/FrancoJOG) |

---

## 🛠️ Prerrequisitos y Tecnologías

El proyecto está desarrollado bajo el paradigma de **Programación Orientada a Objetos** en **C++17** y **Programación de Sistemas Linux (API POSIX)**.

* **Sistema Operativo:** Linux (Ubuntu 22.04 LTS / 24.04 LTS nativo o mediante **WSL2** en Windows 10/11).
* **Compilador:** `g++` (versión 11 o superior) con soporte para C++17.
* **Herramientas de Construcción y Depuración:** `make`, `gdb`, `git`.
* **Editor Recomendado:** Visual Studio Code (con extensión WSL).

---

## 🚀 Guía de Instalación y Configuración del Entorno (Windows / WSL2)

Este proyecto cumple con el requisito **RNF-01** (ejecución nativa en Linux) y **RNF-02** (construcción reproducible).

### 1. Instalación de Ubuntu mediante WSL2 en Windows
1. Abre **PowerShell** como Administrador en Windows y ejecuta:
   ```powershell
   wsl --install -d Ubuntu
