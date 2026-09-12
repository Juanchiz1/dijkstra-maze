import pygame

COLOR_AVATAR = (255, 225, 40)
COLOR_AVATAR_BORDE = (255, 255, 255)

VELOCIDAD_BASE = 180
VELOCIDAD_MINIMA = 60


class Avatar:
    def __init__(self, fila_inicial, col_inicial):
        self.fila = fila_inicial
        self.col = col_inicial
        self.intervalo_movimiento = VELOCIDAD_BASE
        self.ultimo_movimiento = pygame.time.get_ticks()

    def reposicionar(self, fila, col):
        self.fila = fila
        self.col = col

    def resetear_velocidad(self):
        self.intervalo_movimiento = VELOCIDAD_BASE

    def aumentar_velocidad(self):
        self.intervalo_movimiento = max(VELOCIDAD_MINIMA, int(self.intervalo_movimiento * 0.85))

    def actualizar(self, grid):
        teclas = pygame.key.get_pressed()
        direccion = None
        if teclas[pygame.K_UP]:
            direccion = (-1, 0)
        elif teclas[pygame.K_DOWN]:
            direccion = (1, 0)
        elif teclas[pygame.K_LEFT]:
            direccion = (0, -1)
        elif teclas[pygame.K_RIGHT]:
            direccion = (0, 1)

        if direccion is None:
            return False

        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_movimiento < self.intervalo_movimiento:
            return False

        d_fila, d_col = direccion
        nueva_fila, nueva_col = self.fila + d_fila, self.col + d_col

        if not grid.dentro_del_grid(nueva_fila, nueva_col):
            return False
        if grid.celda(nueva_fila, nueva_col).es_muro():
            return False

        self.fila, self.col = nueva_fila, nueva_col
        self.ultimo_movimiento = ahora
        return True

    def dibujar(self, pantalla, cell_size, offset_x=0, offset_y=0):
        x = offset_x + self.col * cell_size + cell_size // 2
        y = offset_y + self.fila * cell_size + cell_size // 2
        radio = max(cell_size // 3, 5)
        pygame.draw.circle(pantalla, COLOR_AVATAR_BORDE, (x, y), radio + 2)
        pygame.draw.circle(pantalla, COLOR_AVATAR, (x, y), radio)