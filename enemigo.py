import pygame
import random

COLOR_ENEMIGO = (220, 50, 50)


class Enemigo:
    def __init__(self, fila_inicial, col_inicial, intervalo_movimiento=500):
        self.fila = fila_inicial
        self.col = col_inicial
        self.intervalo_movimiento = intervalo_movimiento  # ms entre movimientos
        self.ultimo_movimiento = pygame.time.get_ticks()
        self.vivo = True

    def actualizar(self, grid):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_movimiento < self.intervalo_movimiento:
            return
        self.ultimo_movimiento = ahora

        # Movimiento aleatorio temporal - se reemplaza por persecucion con Dijkstra
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(direcciones)
        for d_fila, d_col in direcciones:
            nf, nc = self.fila + d_fila, self.col + d_col
            if grid.dentro_del_grid(nf, nc) and not grid.celda(nf, nc).es_muro():
                self.fila, self.col = nf, nc
                break

    def dibujar(self, pantalla, cell_size):
        centro_x = self.col * cell_size + cell_size // 2
        centro_y = self.fila * cell_size + cell_size // 2
        radio = max(cell_size // 3, 4)
        pygame.draw.circle(pantalla, COLOR_ENEMIGO, (centro_x, centro_y), radio)