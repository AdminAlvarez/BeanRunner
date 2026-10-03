# Uso de Inteligencia Artificial

Esta carpeta contiene los registros representativos del uso de herramientas de inteligencia artificial durante el desarrollo de **BeanRunner**.

La inteligencia artificial se utilizó como una herramienta de apoyo técnico de manera controlada y supervisada por el equipo de desarrollo. Su uso se limitó a actividades como exploración de alternativas, apoyo en diseño de arquitectura, definición de la máquina de estados, elaboración de documentación técnica y estructuración de casos de prueba.

---

## Control del uso de IA

El uso de inteligencia artificial no se consideró como sustituto de las decisiones técnicas ni de la responsabilidad del equipo sobre el proyecto.

Cada propuesta obtenida mediante IA fue revisada antes de ser incorporada al repositorio. En particular, cualquier estructura, diagrama o fragmento de código generado por la herramienta fue:
* Revisado y comprendido antes de su incorporación.
* Evaluado respecto al contexto y a los requisitos de BeanRunner (`RF-01`, `RF-02`, `RF-06`, `RF-10`, etc.).
* Modificado cuando se identificaron inconsistencias técnicas o casos de borde.
* Aceptado únicamente después de comprobar su validez técnica y alineación con las especificaciones.

La validación y revisión de las propuestas documentales y de código generadas mediante IA fue realizada por el equipo de desarrollo, asegurando que ninguna respuesta fuera incorporada al proyecto únicamente por haber sido generada o recomendada por la herramienta.

---

## Objetivo de los registros

Los registros de esta carpeta documentan de forma representativa el proceso de utilización y revisión de IA durante el desarrollo.

Cada registro identifica:
* El objetivo de la consulta.
* El resultado recibido de la herramienta.
* La revisión realizada por el equipo.
* Los cambios y correcciones aplicados.
* Las pruebas o verificaciones ejecutadas.
* El resultado de la verificación.
* El aprendizaje obtenido.

---

## Registros

### AI-001 — Flujo de Trabajo Git y Subida de Cambios
Uso de IA para definir y validar el flujo de trabajo en la línea de comandos (Git), manejo de ramas breves (`Revision`), higiene del repositorio (exclusión de `__pycache__` vía `.gitignore`) y apertura de Pull Requests.  
**Registro:** `docs/ai-usage/AI-001-git-workflow.md`

### AI-002 — Modelo Preliminar de Estados y Transiciones
Uso de IA como apoyo para formalizar la máquina de estados del trabajo (`QUEUED`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELED`, `INTERRUPTED`), la matriz de transiciones y el diagrama en sintaxis Mermaid (RF-06).  
**Registro:** `docs/ai-usage/AI-002-state-model.md`

### AI-003 — Depuración y Casos de Borde en la Máquina de Estados
Uso de IA para identificar y resolver inconsistencias en el modelo de estados: incorporación de la transición directa `QUEUED` → `FAILED` (fallo al invocar ejecutable sin pasar por `RUNNING`) y clarificación de metadatos nulos (`pid = null`, `started_at = null`) al cancelar un trabajo en cola (`CANCELED`).  
**Registro:** `docs/ai-usage/AI-003-state-model-edge-cases.md`

### AI-004 — Definición de Primeros Casos de Prueba (Hito 1)
Uso de IA para la estructuración formal de los primeros casos de prueba en Markdown (`TC-001`, `TC-002`, `TC-003` y `TC-005`), garantizando la cobertura de los requisitos de recepción, validación, estado y cancelación de trabajos.  
**Registro:** `docs/ai-usage/AI-004-test-cases-setup.md`

---

## Criterio de aceptación

Una propuesta generada por IA solo puede incorporarse al proyecto cuando el equipo:
1. Comprende su funcionamiento y lógica subyacente.
2. Verifica su compatibilidad con los requisitos de BeanRunner.
3. Comprueba su comportamiento mediante ejecución o revisión técnica.
4. Realiza las modificaciones necesarias para corregir deficiencias.
5. Valida y aprueba el resultado final.

El hecho de que una solución haya sido generada por IA no constituye por sí mismo una justificación técnica ni evidencia de funcionamiento.

---

## Responsabilidad del desarrollo

Las decisiones finales de arquitectura, diseño e implementación pertenecen al equipo de desarrollo.

La inteligencia artificial se considera únicamente una herramienta de asistencia. Cualquier elemento incorporado al repositorio debe poder ser explicado, modificado, ejecutado y verificado por el equipo.

---

## Verificación

Las pruebas y revisiones realizadas sobre las propuestas incorporadas deberán quedar respaldadas por la documentación y los casos de prueba del proyecto (`verif/test-cases/`).

Cuando una propuesta de IA presente una deficiencia (como la omisión de transiciones o metadatos nulos en el modelo de estados), esta deberá documentarse junto con la modificación realizada y el criterio aplicado para su corrección.

---

## Nota

Este registro busca documentar un uso controlado, revisado y verificable de herramientas de inteligencia artificial durante el desarrollo de **BeanRunner**.