import argparse
import time
import tracemalloc
from puzzle import NPuzzle
from algorithms import bfs, dfs, a_estrella
from visualizer import mostrar_camino, imprimir_camino

def resolver(args):
    """
    Ejecuta el proceso completo para resolver el N-Puzzle.

    1. Obtiene el estado inicial (ya sea ingresado o generado aleatoriamente).
    2. Aplica el algoritmo de búsqueda seleccionado (BFS, DFS o A*).
    3. Mide tiempo y memoria usados.
    4. Muestra o visualiza los resultados.
    """
    if args.inicial:
        valores = [int(v) for v in args.inicial]

        if not NPuzzle.es_resoluble(valores):
            raise SystemExit("El estado inicial NO es resoluble según las reglas del N-Puzzle.")
        
        inicio = NPuzzle.desde_lista(valores)
    else:
        inicio = NPuzzle.generar_aleatorio(tamano=args.tamano, mezclas=args.mezclas, semilla=args.semilla)

    print("Estado inicial del tablero:")
    print(inicio.formato_bonito())

    if args.algoritmo == "bfs":
        algoritmo = bfs
    elif args.algoritmo == "dfs":
        def _dfs(estado_inicial):
            return dfs(estado_inicial, limite=args.limite)
        algoritmo = _dfs
    elif args.algoritmo in ["a_estrella", "astar"]:
        algoritmo = a_estrella
    else:
        raise SystemExit("Algoritmo no soportado. Usa: bfs, dfs o a_estrella.")

    tracemalloc.start()
    tiempo_inicio = time.perf_counter()
    resultado = algoritmo(inicio)
    duracion = time.perf_counter() - tiempo_inicio
    _, pico_memoria = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if resultado.encontrado and resultado.camino:
        print(f"\n¡Solución encontrada! Movimientos: {len(resultado.camino) - 1}")
        print(f"Tiempo: {duracion:.4f} s | Nodos expandidos: {resultado.expandidos} | Pico de memoria: {pico_memoria / 1024 / 1024:.3f} MB")

        if args.visualizar:
            mostrar_camino(resultado.camino, pausa=args.pausa)
        else:
            imprimir_camino(resultado.camino)
    else:
        print("\nNo se encontró solución.")
        print(f"Tiempo: {duracion:.4f} s | Nodos expandidos: {resultado.expandidos} | Pico de memoria: {pico_memoria / 1024 / 1024:.3f} MB")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resolución del N-Puzzle (BFS, DFS, A*)")

    parser.add_argument("--algoritmo", choices=["bfs", "dfs", "a_estrella"], default="a_estrella",
                        help="Algoritmo de búsqueda a usar (bfs, dfs o a_estrella)")
    parser.add_argument("--tamano", type=int, default=3, help="Tamaño del tablero (3=8-puzzle, 4=15-puzzle)")
    parser.add_argument("--mezclas", type=int, default=20, help="Número de movimientos aleatorios desde el estado objetivo (asegura solvencia)")
    parser.add_argument("--inicial", nargs="+", help="Estado inicial plano, ej: 1 2 3 4 0 6 7 5 8")
    parser.add_argument("--limite", type=int, default=None, help="Límite de profundidad (solo para DFS)")
    parser.add_argument("--visualizar", action="store_true", help="Muestra la solución con animación en matplotlib")
    parser.add_argument("--pausa", type=float, default=0.5, help="Tiempo de pausa entre movimientos (en segundos)")
    parser.add_argument("--semilla", type=int, default=None, help="Semilla aleatoria para resultados reproducibles")

    args = parser.parse_args()
    resolver(args)