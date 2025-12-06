# Algoritmos de búsqueda: BFS, DFS y A*

from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Callable, Set
import heapq
from puzzle import NPuzzle
from heuristics import distancia_manhattan

@dataclass
class ResultadoBusqueda:
    """Representa el resultado de la ejecución de un algoritmo de búsqueda."""
    camino: Optional[List[NPuzzle]]
    expandidos: int
    encontrado: bool

def reconstruir_camino(padres: Dict[NPuzzle, Optional[NPuzzle]], meta: NPuzzle) -> List[NPuzzle]:
    """Reconstruye el camino desde el estado inicial hasta el estado meta."""
    camino = [meta]
    actual = meta
    while padres[actual] is not None:
        actual = padres[actual]
        camino.append(actual)
    camino.reverse()
    return camino

def bfs(inicio: NPuzzle) -> ResultadoBusqueda:
    """Implementa la búsqueda en amplitud (BFS)."""
    frontera = deque([inicio])
    padres: Dict[NPuzzle, Optional[NPuzzle]] = {inicio: None}
    explorados: Set[NPuzzle] = set()
    expandidos = 0

    while frontera:
        estado = frontera.popleft()
        if estado.es_objetivo():
            return ResultadoBusqueda(reconstruir_camino(padres, estado), expandidos, True)
        
        explorados.add(estado)
        expandidos += 1

        for vecino in estado.obtener_vecinos():
            if vecino not in explorados and vecino not in padres:
                padres[vecino] = estado
                frontera.append(vecino)
    
    return ResultadoBusqueda(None, expandidos, False)

def dfs(inicio: NPuzzle, limite: Optional[int] = None) -> ResultadoBusqueda:
    """Implementa la búsqueda en profundidad (DFS) con un límite opcional de profundidad."""
    pila = [inicio]
    padres: Dict[NPuzzle, Optional[NPuzzle]] = {inicio: None}
    explorados: Set[NPuzzle] = set()
    profundidad: Dict[NPuzzle, int] = {inicio: 0}
    expandidos = 0

    while pila:
        estado = pila.pop()
        if estado.es_objetivo():
            return ResultadoBusqueda(reconstruir_camino(padres, estado), expandidos, True)
        
        if limite is not None and profundidad[estado] >= limite:
            continue
        
        explorados.add(estado)
        expandidos += 1

        for vecino in estado.obtener_vecinos():
            if vecino not in explorados and vecino not in padres:
                padres[vecino] = estado
                profundidad[vecino] = profundidad[estado] + 1
                pila.append(vecino)
    
    return ResultadoBusqueda(None, expandidos, False)

def a_estrella(inicio: NPuzzle, heuristica: Callable[[NPuzzle], int] = distancia_manhattan) -> ResultadoBusqueda:
    """Implementa el algoritmo A* usando la heurística de distancia Manhattan."""
    contador = 0
    costo_g: Dict[NPuzzle, int] = {inicio: 0}
    padres: Dict[NPuzzle, Optional[NPuzzle]] = {inicio: None}
    frontera: List[Tuple[int, int, NPuzzle]] = []
    heapq.heappush(frontera, (heuristica(inicio), contador, inicio))
    cerrados: Set[NPuzzle] = set()
    expandidos = 0

    while frontera:
        f, _, estado = heapq.heappop(frontera)
        if estado in cerrados:
            continue
        if estado.es_objetivo():
            return ResultadoBusqueda(reconstruir_camino(padres, estado), expandidos, True)
        
        cerrados.add(estado)
        expandidos += 1

        for vecino in estado.obtener_vecinos():
            nuevo_g = costo_g[estado] + 1
            if vecino in cerrados and nuevo_g >= costo_g.get(vecino, float("inf")):
                continue
            if nuevo_g < costo_g.get(vecino, float("inf")):
                padres[vecino] = estado
                costo_g[vecino] = nuevo_g
                contador += 1
                f_total = nuevo_g + heuristica(vecino)
                heapq.heappush(frontera, (f_total, contador, vecino))
    
    return ResultadoBusqueda(None, expandidos, False)
