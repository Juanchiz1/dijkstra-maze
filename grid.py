import pygame

# Configuración visual
CELL_SIZE = 40
ROWS = 15
COLS = 20

# Colores por rango de costo (terreno)
COLOR_COSTO_1 = (200, 230, 200)   # verde claro - barato
COLOR_COSTO_2 = (230, 220, 150)   # amarillo - medio
COLOR_COSTO_3 = (230, 160, 120)   # naranja - costoso
COLOR_COSTO_4 = (180, 90, 90)     # rojo - muy costoso
COLOR_BORDE = (60, 60, 60)


class Celda:
    def __init__(self, fila, col, costo):
        self.fila = fila
        self.col = col
        self.costo = costo  # peso de moverse hacia esta celda

    def color(self):
        if self.costo == 1:
            return COLOR_COSTO_1
        elif self.costo == 2:
            return COLOR_COSTO_2
        elif self.costo == 3:
            return COLOR_COSTO_3
        else:
            return COLOR_COSTO_4


class Grid:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.celdas = self._generar_grid()

    def _generar_grid(self):
        import random
        celdas = []
        for f in range(self.filas):
            fila_celdas = []
            for c in range(self.columnas):
                costo = random.choice([1, 1, 1, 2, 2, 3, 4])  # más probabilidad de costo bajo
                fila_celdas.append(Celda(f, c, costo))
            celdas.append(fila_celdas)
        return celdas

    def dibujar(self, pantalla):
        for fila in self.celdas:
            for celda in fila:
                x = celda.col * CELL_SIZE
                y = celda.fila * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(pantalla, celda.color(), rect)
                pygame.draw.rect(pantalla, COLOR_BORDE, rect, 1)