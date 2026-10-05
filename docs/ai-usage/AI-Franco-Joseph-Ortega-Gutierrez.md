# Registro personal de uso de IA — Franco Joseph Ortega Gutiérrez

## Para qué utilicé la IA

Durante el desarrollo de BeanRunner utilicé un asistente de IA como apoyo
para entender el proyecto y avanzar en tareas de implementación, pruebas y
documentación. En particular, le pedí ayuda para:

- Entender los requisitos del Hito 1, revisar qué funcionalidades faltaban y
  relacionarlas con casos de prueba e issues.
- Completar y explicar el flujo local de trabajos: envío, identificador,
  ejecución como proceso separado, consulta, listado, cancelación y código de
  salida.
- Investigar y resolver dudas de Git y GitHub, como trabajar en una rama,
  actualizarla desde `main`, revisar cambios y organizar commits.
- Ejecutar y entender las pruebas, interpretar errores y registrar qué se
  había validado en Windows y qué faltaba comprobar en Ubuntu/WSL2.
- Mejorar documentación del proyecto, incluyendo el README, la matriz de
  trazabilidad, el modelo de estados y los registros de verificación.
- Comprender cómo ejecutar BeanRunner y qué hacen sus directorios y archivos,
  para poder explicar el proyecto y usarlo en la demostración.

## Justificación

Utilicé IA porque todavía estoy aprendiendo programación y algunas partes del
proyecto —procesos, concurrencia, señales, pruebas y flujo de Git— me resultan
difíciles de comprender o implementar sin orientación. La asistencia me
ayudó a dividir problemas grandes en pasos más manejables, aclarar conceptos y
detectar diferencias entre ejecutar comandos en Windows y hacerlo en Linux.

También la utilicé para acelerar tareas repetitivas de documentación y para
comprobar que las instrucciones correspondieran con las funciones existentes.
La IA fue una herramienta de apoyo; no sustituye mi responsabilidad de
entender lo que se entrega ni la revisión del equipo.

## Revisión y verificación

Cuando recibí cambios o explicaciones, pedí que se contrastaran con los
archivos del repositorio y con las pruebas disponibles. La primera verificación
registrada en el [reporte original](../../verif/results/run-hito1-submission/test-report.md)
se hizo en Windows con Python 3.14.3. Después, al ejecutar la suite en Ubuntu
WSL2 con Python 3.14.4, una prueba falló porque usaba el nombre `python`, que
no estaba disponible en esa instalación. Se actualizó la prueba para usar el
intérprete activo; después del cambio pasaron las 19 pruebas y las 4
verificaciones funcionales, como se documenta en el
[reporte de Ubuntu](../../verif/results/run-hito1-ubuntu/test-report.md).

Antes de presentar el proyecto, debo revisar el código que explicaré,
comprender el recorrido de una solicitud y poder describir las limitaciones
actuales, como la falta de persistencia y de operación remota.

## Aprendizaje

Aprendí que tener código o una respuesta generada no demuestra por sí mismo
que una función esté terminada. Es necesario ejecutar pruebas, revisar el
resultado en el entorno objetivo y ser claro sobre lo que todavía falta.
También aprendí a usar la CLI con comandos compatibles con el sistema
operativo donde se ejecuta BeanRunner.
