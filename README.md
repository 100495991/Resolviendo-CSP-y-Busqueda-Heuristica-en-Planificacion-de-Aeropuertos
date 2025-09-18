# Satisfacción de Restricciones y Búsqueda Heurística ✈️

El objetivo es **modelar y resolver problemas de planificación en aviación** mediante técnicas de **satisfacción de restricciones (CSP)** y **búsqueda heurística (A\*)**, evaluando su eficiencia y validez en distintos escenarios.

---

## 📌 Descripción del proyecto

El proyecto se divide en **dos partes principales**:

### 🔹 Parte 1: Mantenimiento de flota de aviones (CSP con python-constraint)
Se modela el problema de mantenimiento de una flota de aviones como un **problema de satisfacción de restricciones**.  
Las condiciones incluyen:
- Asignación de aviones a talleres/parkings en franjas horarias.
- Restricciones de capacidad de talleres (máximo 2 aviones, 1 jumbo como límite).
- Diferenciación de talleres estándar (STD) y especialistas (SPC).
- Cumplimiento de dependencias entre tareas de tipo 1 (estándar) y tipo 2 (especialistas).
- Restricciones espaciales de maniobrabilidad entre talleres adyacentes.
- Prohibición de talleres adyacentes ocupados por dos JUMBO.

**Ejecución**  
Usar el script principal: `python CSPMaintenance.py <path maintenance>`

**Output**  
- Un archivo CSV con el número de soluciones encontradas y las asignaciones de cada avión.  
- Ejemplo de salida: `maintenance01.csv`

**Script de pruebas**  
Ejecutar: `sh CSP-calls.sh`

---

### 🔹 Parte 2: Planificación de rodaje de aviones (A* con heurísticas)
Se aborda el problema del **rodaje de aviones en un aeropuerto** como un problema de **búsqueda heurística**.  
Los objetivos son:
- Modelar el rodaje como un problema de planificación para minimizar el **makespan** (tiempo total hasta que todos los aviones llegan a sus pistas).
- Implementar **A\*** con al menos dos heurísticas admisibles distintas.
- Garantizar la ausencia de colisiones y cumplimiento de reglas de seguridad (no compartir pista ni intercambiar posiciones simultáneamente).
- Analizar comparativamente las heurísticas implementadas.

**Ejecución**  
Usar: `python ASTARRodaje.py <path mapa.csv> <num-h>`  
Donde `<num-h>` es 1 o 2 (la heurística a usar).

**Output**  
- Archivo ` <mapa>-<num-h>.output `: secuencia de movimientos para cada avión.  
- Archivo ` <mapa>-<num-h>.stat `: estadísticas (tiempo, makespan, nodos expandidos, etc).

**Script de pruebas**  
Ejecutar: `sh ASTAR-calls.sh`

---

## 🛠️ Tecnologías utilizadas
- **Lenguaje**: Python 3  
- **Librerías**:  
  - `python-constraint` → Parte 1 (CSP)  
  - Implementación propia de A* → Parte 2  
- **Entorno**: Linux/Unix (ejecución mediante shell-scripts)

---

---

## 👥 Autores
Trabajo realizado **Guillermo Sancho González** y **Manuel Roldán Matea**.
