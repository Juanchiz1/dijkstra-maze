import pygame
from dijkstra import dijkstra, reconstruir_camino

COLOR_ENEMIGO = (230, 35, 35)
COLOR_ENEMIGO_BORDE = (15, 15, 15)


class Enemigo:
    def __init__(self, fila_inicial, col_inicial, intervalo_movimiento=450):
        self.fila = fila_inicial
        self.col = col_inicial
        self.intervalo_movimiento = intervalo_movimiento
        self.ultimo_movimiento = pygame.time.get_ticks()
        self.vivo = True

    def actualizar(self, grid, posicion_avatar):
        if not self.vivo:
            return False

        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_movimiento < self.intervalo_movimiento:
            return False
        self.ultimo_movimiento = ahora

        _, previos = dijkstra(grid, (self.fila, self.col))
        camino = reconstruir_camino(previos, (self.fila, self.col), posicion_avatar)

        if camino and len(camino) > 1:
            self.fila, self.col = camino[1]
            return True
        return False

    def dibujar(self, pantalla, cell_size, offset_x=0, offset_y=0):
        if not self.vivo:
            return
        x = offset_x + self.col * cell_size + cell_size // 2
        y = offset_y + self.fila * cell_size + cell_size // 2
        radio = max(cell_size // 3, 5)
        pygame.draw.circle(pantalla, COLOR_ENEMIGO_BORDE, (x, y), radio + 2)
        pygame.draw.circle(pantalla, COLOR_ENEMIGO, (x, y), radio)