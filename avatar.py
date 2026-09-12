import pygame

COLOR_AVATAR = (250, 220, 40)


class Avatar:
    def __init__(self, fila_inicial, col_inicial):
        self.fila = fila_inicial
        self.col = col_inicial

    def mover(self, d_fila, d_col, grid):
        nueva_fila = self.fila + d_fila
        nueva_col = self.col + d_col

        if not grid.dentro_del_grid(nueva_fila, nueva_col):
            return
        if grid.celda(nueva_fila, nueva_col).es_muro():
            return

        self.fila = nueva_fila
        self.col = nueva_col

    def dibujar(self, pantalla, cell_size):
        centro_x = self.col * cell_size + cell_size // 2
        centro_y = self.fila * cell_size + cell_size // 2
        radio = max(cell_size // 3, 4)
        pygame.draw.circle(pantalla, COLOR_AVATAR, (centro_x, centro_y), radio)