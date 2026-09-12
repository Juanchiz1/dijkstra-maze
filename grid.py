import pygame

COLOR_COSTO_1 = (222, 235, 230)
COLOR_COSTO_2 = (180, 210, 220)
COLOR_COSTO_3 = (130, 170, 195)
COLOR_COSTO_4 = (85, 120, 155)
COLOR_MURO = (18, 18, 18)
COLOR_BORDE = (50, 50, 50)
COLOR_DESTINO = (210, 60, 220)
COLOR_DESTINO_BORDE = (255, 255, 255)
COLOR_PISTA = (255, 230, 40)


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

    def dibujar(self, pantalla, cell_size, offset_x=0, offset_y=0, destino=None, camino_pista=None):
        camino_set = set(camino_pista) if camino_pista else set()

        for fila in self.celdas:
            for celda in fila:
                x = offset_x + celda.col * cell_size
                y = offset_y + celda.fila * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)

                pygame.draw.rect(pantalla, celda.color(), rect)

                if (celda.fila, celda.col) in camino_set:
                    pygame.draw.rect(pantalla, COLOR_PISTA, rect, 3)

                pygame.draw.rect(pantalla, COLOR_BORDE, rect, 1)

        if destino:
            fila_d, col_d = destino
            x = offset_x + col_d * cell_size + cell_size // 2
            y = offset_y + fila_d * cell_size + cell_size // 2
            radio = max(cell_size // 3, 5)
            pygame.draw.circle(pantalla, COLOR_DESTINO_BORDE, (x, y), radio + 2)
            pygame.draw.circle(pantalla, COLOR_DESTINO, (x, y), radio)