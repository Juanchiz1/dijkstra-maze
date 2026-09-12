import pygame
from grid import CELL_SIZE

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

    def dibujar(self, pantalla):
        centro_x = self.col * CELL_SIZE + CELL_SIZE // 2
        centro_y = self.fila * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(pantalla, COLOR_AVATAR, (centro_x, centro_y), CELL_SIZE // 3)