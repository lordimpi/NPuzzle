from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
import random

Tablero = Tuple[int, ...]

@dataclass(frozen=True)
class NPuzzle:
    """
    Representa un tablero del rompecabezas deslizante N-Puzzle.
    
    Ejemplo (8-puzzle):
        1 2 3
        4 5 6
        7 8 0   ← el 0 representa el espacio vacío
    """
    tablero: Tablero
    tamano: int

    @staticmethod
    def objetivo(tamano: int) -> 'NPuzzle':
        """
        Devuelve el tablero objetivo (ordenado) para un tamaño dado.
        Ejemplo: [1,2,3,4,5,6,7,8,0]
        """
        n = tamano * tamano
        return NPuzzle(tuple(list(range(1, n)) + [0]), tamano)

    @staticmethod
    def desde_lista(valores: List[int]) -> 'NPuzzle':
        """
        Crea una instancia del puzzle a partir de una lista de números.
        Ejemplo: NPuzzle.desde_lista([1, 2, 3, 4, 5, 6, 7, 0, 8])
        """
        n = len(valores)
        tamano = int(n ** 0.5)
        if tamano * tamano != n:
            raise ValueError("La lista no forma un cuadrado perfecto (ej. 9 elementos = 3x3).")
        return NPuzzle(tuple(valores), tamano)

    def es_objetivo(self) -> bool:
        """Retorna True si el tablero está en el estado objetivo."""
        return self == NPuzzle.objetivo(self.tamano)

    def indice_de_cero(self) -> int:
        """Devuelve el índice donde se encuentra el espacio vacío (0)."""
        return self.tablero.index(0)

    def obtener_vecinos(self) -> List['NPuzzle']:
        """
        Retorna una lista de nuevos estados que pueden generarse
        moviendo el espacio vacío (0) en una de las 4 direcciones posibles.
        """
        indice_cero = self.indice_de_cero()
        fila, columna = divmod(indice_cero, self.tamano)
        vecinos = []

        def intercambiar(nueva_fila, nueva_columna):
            nuevo_indice = nueva_fila * self.tamano + nueva_columna
            b = list(self.tablero)
            b[indice_cero], b[nuevo_indice] = b[nuevo_indice], b[indice_cero]
            return NPuzzle(tuple(b), self.tamano)

        if fila > 0:
            vecinos.append(intercambiar(fila - 1, columna))
        if fila < self.tamano - 1:
            vecinos.append(intercambiar(fila + 1, columna))
        if columna > 0:
            vecinos.append(intercambiar(fila, columna - 1))
        if columna < self.tamano - 1:
            vecinos.append(intercambiar(fila, columna + 1))

        return vecinos

    def formato_bonito(self) -> str:
        """Devuelve el tablero formateado en filas y columnas, listo para imprimir."""
        lineas = []
        for i in range(self.tamano):
            fila = self.tablero[i * self.tamano:(i + 1) * self.tamano]
            lineas.append(" ".join("{:2}".format(v) if v != 0 else "  " for v in fila))
        return "\n".join(lineas)

    def __hash__(self):
        return hash(self.tablero)

    @staticmethod
    def contar_inversiones(valores: List[int]) -> int:
        """
        Calcula el número de inversiones en la lista (pares fuera de orden).
        Se ignora el valor 0 (espacio vacío).
        """
        arr = [v for v in valores if v != 0]
        inv = 0
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    inv += 1
        return inv

    @staticmethod
    def es_resoluble(valores: List[int]) -> bool:
        """
        Determina si el estado dado es resoluble según las reglas del N-Puzzle.
        """
        n = len(valores)
        tamano = int(n ** 0.5)
        inv = NPuzzle.contar_inversiones(valores)

        if tamano % 2 == 1:
            return inv % 2 == 0
        else:
            fila_desde_abajo = tamano - (valores.index(0) // tamano)
            if fila_desde_abajo % 2 == 0:
                return inv % 2 == 1
            else:
                return inv % 2 == 0

    @staticmethod
    def generar_aleatorio(tamano: int, mezclas: int = 20, semilla: Optional[int] = None) -> 'NPuzzle':
        """
        Genera un puzzle aleatorio a partir del estado objetivo aplicando
        una serie de movimientos válidos (de modo que siempre sea resoluble).
        """
        if semilla is not None:
            random.seed(semilla)
        estado = NPuzzle.objetivo(tamano)
        for _ in range(mezclas):
            estado = random.choice(estado.obtener_vecinos())
        return estado
