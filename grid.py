import pygame

COLOR_COSTO_1 = (200, 230, 200)
COLOR_COSTO_2 = (230, 220, 150)
COLOR_COSTO_3 = (230, 160, 120)
COLOR_COSTO_4 = (180, 90, 90)
COLOR_MURO = (30, 30, 30)
COLOR_BORDE = (60, 60, 60)
COLOR_ORIGEN = (60, 120, 220)
COLOR_DESTINO = (170, 60, 200)


class Celda:
    def __init__(self, fila, col, costo):
        self.fila = fila
        self.col = col
        self.costo = costo

    def es_muro(self):
        return self.costo == 0

    def color(self):
        if self.costo == 0:
            return COLOR_MURO
        elif self.costo == 1:
            return COLOR_COSTO_1
        elif self.costo == 2:
            return COLOR_COSTO_2
        elif self.costo == 3:
            return COLOR_COSTO_3
        else:
            return COLOR_COSTO_4


class Grid:
    def __init__(self, mapa):
        self.filas = len(mapa)
        self.columnas = len(mapa[0])
        self.celdas = [
            [Celda(f, c, mapa[f][c]) for c in range(self.columnas)]
            for f in range(self.filas)
        ]

    def celda(self, fila, col):
        return self.celdas[fila][col]

    def dentro_del_grid(self, fila, col):
        return 0 <= fila < self.filas and 0 <= col < self.columnas

    def dibujar(self, pantalla, cell_size, origen=None, destino=None):
        for fila in self.celdas:
            for celda in fila:
                x = celda.col * cell_size
                y = celda.fila * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)

                if origen and (celda.fila, celda.col) == origen:
                    color = COLOR_ORIGEN
                elif destino and (celda.fila, celda.col) == destino:
                    color = COLOR_DESTINO
                else:
                    color = celda.color()

                pygame.draw.rect(pantalla, color, rect)
                pygame.draw.rect(pantalla, COLOR_BORDE, rect, 1)