# Comparación de rendimiento de los algoritmos (BFS, DFS, A*)
import argparse
import time
import tracemalloc
from typing import List
from puzzle import NPuzzle
from algorithms import bfs, dfs, a_estrella

def ejecutar_caso(tamano: int, mezclas: int, nombre_algoritmo: str, limite_dfs=None, semilla=None):
    """
    Ejecuta un solo caso de prueba del N-Puzzle utilizando el algoritmo especificado.
    """
    inicio = NPuzzle.generar_aleatorio(tamano=tamano, mezclas=mezclas, semilla=semilla)

    if nombre_algoritmo == "bfs":
        algoritmo = bfs
    elif nombre_algoritmo == "dfs":
        def _dfs(s): return dfs(s, limite=limite_dfs)
        algoritmo = _dfs
    elif nombre_algoritmo in ["a_estrella", "astar"]:
        algoritmo = a_estrella
    else:
        raise ValueError("Nombre de algoritmo no válido. Usa: bfs, dfs o a_estrella.")

    tracemalloc.start()
    tiempo_inicio = time.perf_counter()
    resultado = algoritmo(inicio)
    duracion = time.perf_counter() - tiempo_inicio
    _, pico_memoria = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    pasos = len(resultado.camino) - 1 if resultado.camino else None

    return {
        "algoritmo": nombre_algoritmo,
        "tamano": tamano,
        "mezclas": mezclas,
        "encontrado": resultado.encontrado,
        "pasos": pasos,
        "expandidos": resultado.expandidos,
        "tiempo_seg": round(duracion, 6),
        "pico_memoria_mb": round(pico_memoria / 1024 / 1024, 6)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Comparador de algoritmos de búsqueda para el N-Puzzle")
    parser.add_argument("--algoritmo", choices=["bfs", "dfs", "a_estrella", "todos"], default="todos",
                        help="Algoritmo a ejecutar (bfs, dfs, a_estrella o 'todos')")
    parser.add_argument("--tamano", type=int, default=3, help="Tamaño del puzzle (por defecto 3x3)")
    parser.add_argument("--casos", type=int, default=5, help="Número de casos de prueba")
    parser.add_argument("--mezclas", type=int, default=25, help="Número de movimientos aleatorios para desordenar el puzzle")
    parser.add_argument("--limite_dfs", type=int, default=None, help="Límite de profundidad para DFS")
    parser.add_argument("--csv", type=str, default="resultados.csv", help="Archivo CSV donde guardar los resultados")
    parser.add_argument("--semilla", type=int, default=None, help="Semilla aleatoria para reproducibilidad")
    args = parser.parse_args()

    algoritmos = ["bfs", "dfs", "a_estrella"] if args.algoritmo in ["todos", "all"] else [args.algoritmo]

    resultados: List[dict] = []

    print("\n==============================")
    print(" COMPARACIÓN DE ALGORITMOS ")
    print("==============================\n")

    for i in range(args.casos):
        for alg in algoritmos:
            semilla = None if args.semilla is None else args.semilla + i
            res = ejecutar_caso(args.tamano, args.mezclas, alg,
                                 limite_dfs=args.limite_dfs, semilla=semilla)
            res["caso"] = i + 1
            resultados.append(res)
            print(f"Caso {i+1} ({alg}): {res}")

    import csv as _csv
    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        escritor = _csv.DictWriter(f, fieldnames=list(resultados[0].keys()))
        escritor.writeheader()
        escritor.writerows(resultados)

    print(f"\nResultados guardados correctamente en: {args.csv}")
