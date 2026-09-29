"""
==============================================================================
TRABAJO PRÁCTICO 2 - INTELIGENCIA ARTIFICIAL
Simulación de Búsqueda en Espacio de Estados para Brazo Robotizado Industrial
Autor: Lisandro Paolini
==============================================================================
"""

import time


class EntornoMontajeMotor:
    """
    Representa el entorno físico de la cinta transportadora.
    eje H: eje horizontal donde ocurre el desfasaje imprevisto.
    pos_B: Posición teórica inicial programada (ej. H = 0).
    pos_A: Posición real donde quedó el orificio de montaje (ej. H = 6).
    """

    def __init__(self, pos_inicial_B=0, pos_meta_A=6, paso=1):
        self.pos_B = pos_inicial_B
        self.pos_A = pos_meta_A
        self.paso = paso

    def palpar_posicion(self, pos):
        """
        Simula el palpado físico del brazo robotizado.
        Retorna True si la herramienta encaja perfectamente en el orificio A.
        """
        return pos == self.pos_A

    def sensor_relieve_h(self, pos):
        """
        Función Heurística h(n):
        Simula la lectura del perfil de superficie frente al plano patrón.
        Retorna la estimación de distancia absoluta restante hasta el punto A:
        |pos - pos_A|
        """
        return abs(pos - self.pos_A)


def busqueda_exhaustiva_bfs(entorno, max_evaluaciones=30):
    """
    1. BÚSQUEDA EXHAUSTIVA (PRIMERO EN ANCHURA - BFS)
    --------------------------------------------------
    No posee información direccional. Explora sistemáticamente a izquierda
    y derecha acumulando estados en una estructura FIFO (Cola).
    """
    print("\n" + "=" * 60)
    print(" 1. EJECUCIÓN DE BÚSQUEDA EXHAUSTIVA (PRIMERO EN ANCHURA - BFS)")
    print("=" * 60)

    # Cola FIFO: almacena tuplas de (posicion_actual, camino_recorrido)
    cola_fifo = [(entorno.pos_B, [entorno.pos_B])]
    visitados = set([entorno.pos_B])
    evaluaciones = 0
    inicio_tiempo = time.perf_counter()

    while cola_fifo and evaluaciones < max_evaluaciones:
        pos_actual, camino = cola_fifo.pop(0)  # Extracción FIFO
        evaluaciones += 1
        print(f"Paso {evaluaciones:02d} | Palpando posición H = {pos_actual:2d} ... ", end="")

        # Prueba de meta
        if entorno.palpar_posicion(pos_actual):
            tiempo_ejecucion = (time.perf_counter() - inicio_tiempo) * 1000
            print("¡ÉXITO! (Agujero de montaje 'A' localizado)")
            print("-" * 60)
            print("Resultados BFS:")
            print(f" - Posiciones palpadas (evaluaciones): {evaluaciones}")
            print(f" - Desplazamientos del brazo: {len(camino) - 1}")
            print(f" - Secuencia de nodos visitados: {camino}")
            print(f" - Tiempo de cómputo: {tiempo_ejecucion:.4f} ms")
            return camino, evaluaciones

        print("No encaja (Continuando exploración a ciegas).")

        # Operadores de movimiento horizontal: -paso (izquierda), +paso (derecha)
        for delta in [-entorno.paso, entorno.paso]:
            vecino = pos_actual + delta
            if vecino not in visitados:
                visitados.add(vecino)
                cola_fifo.append((vecino, camino + [vecino]))

    print("Error: Límite de evaluaciones alcanzado sin encontrar la meta.")
    return None, evaluaciones


def busqueda_heuristica_best_first(entorno, max_evaluaciones=30):
    """
    2. BÚSQUEDA HEURÍSTICA (PRIMERO EL MEJOR / BEST-FIRST SEARCH)
    --------------------------------------------------------------
    Utiliza el sensor de relieve h(n) para seleccionar en cada iteración
    el nodo con menor estimación de distancia hacia la meta A.
    """
    print("\n" + "=" * 60)
    print(" 2. EJECUCIÓN DE BÚSQUEDA HEURÍSTICA (PRIMERO EL MEJOR)")
    print("=" * 60)

    # Lista abierta priorizada por h(n): tuplas (h_val, pos_actual, camino)
    h_inicial = entorno.sensor_relieve_h(entorno.pos_B)
    lista_abierta = [(h_inicial, entorno.pos_B, [entorno.pos_B])]
    lista_cerrada = set()
    evaluaciones = 0
    inicio_tiempo = time.perf_counter()

    while lista_abierta and evaluaciones < max_evaluaciones:
        # Ordenar lista abierta de menor a mayor valor de h(n)
        lista_abierta.sort(key=lambda x: x[0])
        h_val, pos_actual, camino = lista_abierta.pop(0)
        lista_cerrada.add(pos_actual)
        evaluaciones += 1
        print(f"Paso {evaluaciones:02d} | Robot en H = {pos_actual:2d} (Relieve h(n) = {h_val}) ... ", end="")

        # Prueba de meta
        if entorno.palpar_posicion(pos_actual):
            tiempo_ejecucion = (time.perf_counter() - inicio_tiempo) * 1000
            print("¡ÉXITO! (Posición óptima alcanzada)")
            print("-" * 60)
            print("Resultados Búsqueda Heurística:")
            print(f" - Posiciones evaluadas: {evaluaciones}")
            print(f" - Desplazamientos del brazo: {len(camino) - 1}")
            print(f" - Trayectoria optimizada: {camino}")
            print(f" - Tiempo de cómputo: {tiempo_ejecucion:.4f} ms")
            return camino, evaluaciones

        print("Ajustando trayectoria según gradiente de relieve.")

        # Generación de sucesores inmediatos
        for delta in [-entorno.paso, entorno.paso]:
            vecino = pos_actual + delta
            if vecino not in lista_cerrada and not any(elem[1] == vecino for elem in lista_abierta):
                h_vecino = entorno.sensor_relieve_h(vecino)
                lista_abierta.append((h_vecino, vecino, camino + [vecino]))

    print("Error: Límite de evaluaciones alcanzado.")
    return None, evaluaciones


if __name__ == "__main__":
    # Configuración del escenario del caso práctico:
    # Posición inicial B = 0, Posición real del orificio A = 6
    entorno_simulacion = EntornoMontajeMotor(pos_inicial_B=0, pos_meta_A=6, paso=1)

    print("SISTEMA DE CONTROL DE BRAZO ROBÓTICO - PLANTA DE MOTORES")
    print("Simulación de corrección de desfasaje horizontal H (Posición B -> Posición A)")

    # 1. Ejecutar Búsqueda Exhaustiva
    camino_bfs, eval_bfs = busqueda_exhaustiva_bfs(entorno_simulacion)

    # 2. Ejecutar Búsqueda Heurística
    camino_heur, eval_heur = busqueda_heuristica_best_first(entorno_simulacion)

    # 3. Resumen y Comparativa para el Informe
    print("\n" + "=" * 60)
    print(" COMPARATIVA DE EFICIENCIA OPERATIVA EN LÍNEA DE MONTAJE")
    print("=" * 60)
    print(f"• Búsqueda Exhaustiva (BFS): {eval_bfs:2d} palpaciones requeridas (Exploración ciega redundante)")
    print(f"• Búsqueda Heurística: {eval_heur:2d} evaluaciones requeridas (Trayectoria directa hacia A)")
    print(f"• Reducción de palpaciones: {((eval_bfs - eval_heur) / eval_bfs) * 100:.1f}% de ahorro operativo.")
    print("=" * 60 + "\n")