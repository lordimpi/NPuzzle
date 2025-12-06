import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import imageio.v2 as imageio
from typing import List
from puzzle import NPuzzle
import threading
import time


class VisualizadorPuzzle:
    """Visualizador interactivo del N-Puzzle con controles de avance, retroceso y exportación a GIF."""

    def __init__(self, camino: List[NPuzzle], pausa: float = 0.5):
        self.camino = camino
        self.pausa = pausa
        self.indice = 0
        self.ejecutando = False
        self.figura, self.ejes = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        self.tamano = camino[0].tamano if camino else 3
        self._configurar_interfaz()
        if self.camino:
            self._dibujar_estado(self.camino[self.indice])
        plt.show()

    def _configurar_interfaz(self):
        ax_prev = plt.axes([0.20, 0.05, 0.08, 0.075])
        ax_play = plt.axes([0.35, 0.05, 0.08, 0.075])
        ax_next = plt.axes([0.50, 0.05, 0.08, 0.075])
        ax_gif  = plt.axes([0.65, 0.05, 0.10, 0.075])
        ax_close= plt.axes([0.80, 0.05, 0.10, 0.075])

        self.b_prev = Button(ax_prev, '⬅️')
        self.b_play = Button(ax_play, '▶️')
        self.b_next = Button(ax_next, '➡️')
        self.b_gif  = Button(ax_gif,  'Guardar')
        self.b_close= Button(ax_close, 'Cerrar')

        self.b_prev.on_clicked(self.anterior)
        self.b_play.on_clicked(self.toggle_reproducir)
        self.b_next.on_clicked(self.siguiente)
        self.b_gif.on_clicked(self.exportar_gif)
        self.b_close.on_clicked(self.cerrar)

    def _dibujar_estado(self, estado: NPuzzle):
        self.ejes.clear()
        tablero = np.array(estado.tablero).reshape(self.tamano, self.tamano)
        self.ejes.imshow(tablero, interpolation='none', cmap='coolwarm')

        for i in range(self.tamano):
            for j in range(self.tamano):
                valor = tablero[i, j]
                if valor != 0:
                    self.ejes.text(
                        j, i, str(valor),
                        ha='center', va='center',
                        color='white', fontsize=16, weight='bold'
                    )

        self.ejes.set_xticks([]); self.ejes.set_yticks([])
        self.ejes.set_title(f"Resolución del N-Puzzle  ({self.indice + 1}/{len(self.camino)})")

    def siguiente(self, event=None):
        """Avanza un paso en la secuencia."""
        if self.indice < len(self.camino) - 1:
            self.indice += 1
            self._dibujar_estado(self.camino[self.indice])
            self.figura.canvas.draw_idle()

    def anterior(self, event=None):
        """Retrocede un paso en la secuencia."""
        if self.indice > 0:
            self.indice -= 1
            self._dibujar_estado(self.camino[self.indice])
            self.figura.canvas.draw_idle()

    def toggle_reproducir(self, event=None):
        """Activa o detiene la animación automática."""
        if not self.ejecutando:
            self.ejecutando = True
            self.b_play.label.set_text('PAUSAR')
            threading.Thread(target=self._reproduccion_automatica, daemon=True).start()
        else:
            self.ejecutando = False
            self.b_play.label.set_text('▶️')

    def _reproduccion_automatica(self):
        """Reproduce la solución paso a paso automáticamente."""
        while self.ejecutando and self.indice < len(self.camino) - 1:
            time.sleep(self.pausa)
            self.siguiente()
        self.ejecutando = False
        self.b_play.label.set_text('▶️')

    def exportar_gif(self, event=None):
        """Exporta la animación completa como un archivo GIF."""
        nombre_archivo = "solucion_n_puzzle.gif"
        cuadros = []

        for estado in self.camino:
            fig, ax = plt.subplots()
            tablero = np.array(estado.tablero).reshape(self.tamano, self.tamano)
            ax.imshow(tablero, interpolation='none', cmap='coolwarm')

            for i in range(self.tamano):
                for j in range(self.tamano):
                    valor = tablero[i, j]
                    if valor != 0:
                        ax.text(j, i, str(valor), ha='center', va='center', color='white', fontsize=16)
            ax.set_xticks([]); ax.set_yticks([])
            fig.canvas.draw()

            buf = np.asarray(fig.canvas.buffer_rgba())
            cuadro = buf[..., :3]
            cuadros.append(cuadro)
            plt.close(fig)

        imageio.mimsave(nombre_archivo, cuadros, duration=self.pausa)
        print(f"GIF exportado correctamente: {nombre_archivo}")

    def cerrar(self, event=None):
        """Cierra la ventana del visualizador."""
        self.ejecutando = False
        plt.close(self.figura)

def mostrar_camino(camino: List[NPuzzle], pausa: float = 0.5):
    """Muestra la animación de la secuencia de movimientos."""
    if not camino:
        print("No hay camino que visualizar.")
        return
    VisualizadorPuzzle(camino, pausa=pausa)


def imprimir_camino(camino: List[NPuzzle]):
    """Imprime en consola los estados del tablero paso a paso."""
    for paso, estado in enumerate(camino):
        print(f"\nPaso {paso}:")
        print(estado.formato_bonito())
