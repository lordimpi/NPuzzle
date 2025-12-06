# Heurística de Distancia Manhattan para el N-Puzzle

from puzzle import NPuzzle

def distancia_manhattan(puzzle: NPuzzle) -> int:
    """
    Calcula la heurística de **Distancia Manhattan** para un estado del N-Puzzle.

    Esta heurística estima cuán lejos está el tablero actual del estado objetivo.
    Para cada ficha (excepto el espacio vacío), se calcula la distancia entre
    su posición actual y su posición correcta en el tablero meta, sumando las
    diferencias en filas (dx) y columnas (dy).

    En el algoritmo A*, esta heurística se usa como 'h(n)' en la fórmula:
        f(n) = g(n) + h(n)
    donde:
        g(n) = costo acumulado desde el inicio (número de movimientos)
        h(n) = estimación de movimientos restantes (esta función)

    Parámetros:
        puzzle (NPuzzle): Estado actual del tablero.

    Retorna:
        int: Suma total de distancias Manhattan para todas las fichas.
    """

    total = 0
    tamano = puzzle.tamano

    for indice, valor in enumerate(puzzle.tablero):
        if valor == 0:
            continue

        # Posición objetivo de la ficha (coordenadas esperadas)
        fila_objetivo, col_objetivo = divmod(valor - 1, tamano)

        # Posición actual de la ficha (coordenadas actuales)
        fila_actual, col_actual = divmod(indice, tamano)

        # Distancia Manhattan = |dx| + |dy|
        total += abs(fila_objetivo - fila_actual) + abs(col_objetivo - col_actual)

    return total
