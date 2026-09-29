# Trabajo Práctico 2 - Inteligencia Artificial (Siglo 21)
## Simulación de Búsqueda en Espacio de Estados para Brazo Robotizado Industrial

**Autor:** Lisandro Paolini  
**Asignatura:** Inteligencia Artificial  

---

## 📋 Descripción del Proyecto

Este proyecto implementa una simulación en Python para la resolución de desfasajes en el montaje del bloque de motor en una línea de producción automatizada. 

El brazo robotizado industrial parte de una posición teórica inicial programada ($B = 0$) y debe localizar la posición real del orificio de montaje ($A = 6$) a lo largo de un eje horizontal $H$.

Se comparan dos enfoques fundamentales de búsqueda en espacios de estados:
1. **Búsqueda Exhaustiva a Ciegas (Primero en Anchura):** Explora el espacio de estados sistemáticamente a izquierda y derecha usando una estructura FIFO (Cola), sin información sobre la dirección de la meta.
2. **Búsqueda Heurística Informada (Primero el Mejor):** Utiliza un sensor de relieve como función heurística $h(n) = |\text{pos} - \text{pos}_A|$ para guiar al robot en dirección a la meta óptima.

---

## 🚀 Requisitos Previos

* **Python 3.7+** (No se requieren librerías de terceros; utiliza módulos nativos de Python como `time`).

Para verificar que posees Python instalado, ejecuta en tu terminal:
```bash
python3 --version
```

---

## 💻 Guía Paso a Paso de Uso

### Paso 1: Clonar o descargar el repositorio desde GitHub
Abre tu terminal y clona el repositorio desde GitHub (o descarga y descomprime el código fuente) e ingresa al directorio del proyecto:

```bash
git clone https://github.com/lisandropaolini/IA-TP2.git
cd IA-TP2
```

### Paso 2: Ejecutar el prototipo de simulación
Ejecuta el script principal con el siguiente comando:

```bash
python3 prototipo_robot.py
```

---

## 📊 Ejemplo de Salida e Interpretación de Resultados

Al ejecutar el comando, la consola mostrará la ejecución secuencial de ambos algoritmos y una comparativa final de eficiencia:

```text
SISTEMA DE CONTROL DE BRAZO ROBÓTICO - PLANTA DE MOTORES
Simulación de corrección de desfasaje horizontal H (Posición B -> Posición A)

============================================================
 1. EJECUCIÓN DE BÚSQUEDA EXHAUSTIVA (PRIMERO EN ANCHURA - BFS)
============================================================
Paso 01 | Palpando posición H =  0 ... No encaja (Continuando exploración a ciegas).
Paso 02 | Palpando posición H = -1 ... No encaja (Continuando exploración a ciegas).
...
Paso 13 | Palpando posición H =  6 ... ¡ÉXITO! (Agujero de montaje 'A' localizado)
------------------------------------------------------------
Resultados BFS:
 - Posiciones palpadas (evaluaciones): 13
 - Desplazamientos del brazo: 6
 - Secuencia de nodos visitados: [0, 1, 2, 3, 4, 5, 6]
 - Tiempo de cómputo: 0.4307 ms

============================================================
 2. EJECUCIÓN DE BÚSQUEDA HEURÍSTICA (PRIMERO EL MEJOR)
============================================================
Paso 01 | Robot en H =  0 (Relieve h(n) = 6) ... Ajustando trayectoria según gradiente de relieve.
...
Paso 07 | Robot en H =  6 (Relieve h(n) = 0) ... ¡ÉXITO! (Posición óptima alcanzada)
------------------------------------------------------------
Resultados Búsqueda Heurística:
 - Posiciones evaluadas: 7
 - Desplazamientos del brazo: 6
 - Trayectoria optimizada: [0, 1, 2, 3, 4, 5, 6]
 - Tiempo de cómputo: 0.2815 ms

============================================================
 COMPARATIVA DE EFICIENCIA OPERATIVA EN LÍNEA DE MONTAJE
============================================================
• Búsqueda Exhaustiva (BFS): 13 palpaciones requeridas (Exploración ciega redundante)
• Búsqueda Heurística:  7 evaluaciones requeridas (Trayectoria directa hacia A)
• Reducción de palpaciones: 46.2% de ahorro operativo.
============================================================
```

---

## 🛠️ Estructura del Código (`prototipo_robot.py`)

- `EntornoMontajeMotor`: Modela la cinta transportadora, las posiciones $B$ (inicial) y $A$ (meta), la prueba de palpado y la función heurística del sensor de relieve.
- `busqueda_exhaustiva_bfs`: Algoritmo BFS que explora sin heurística acumulando estados en una cola FIFO.
- `busqueda_heuristica_best_first`: Algoritmo Best-First Search que prioriza los nodos basándose en $h(n)$.
- `__main__`: Bloque de ejecución principal que coordina la simulación e imprime las métricas de rendimiento.
