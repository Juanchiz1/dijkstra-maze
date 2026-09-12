import pygame
import sys
from grid import Grid, CELL_SIZE
from avatar import Avatar
from niveles import crear_todos_los_niveles

pygame.init()
fuente = pygame.font.SysFont("arial", 22)
fuente_grande = pygame.font.SysFont("arial", 32, bold=True)

ALTO_HUD = 50
niveles = crear_todos_los_niveles()

TECLAS_MOVIMIENTO = {
    pygame.K_UP: (-1, 0),
    pygame.K_DOWN: (1, 0),
    pygame.K_LEFT: (0, -1),
    pygame.K_RIGHT: (0, 1),
}


class Juego:
    def __init__(self):
        self.vidas = 3
        self.indice_nivel = 0
        self.estado = "historia"  # "historia" o "jugando"
        self.pantalla = None
        self.cargar_nivel(self.indice_nivel)

    def cargar_nivel(self, indice):
        self.nivel = niveles[indice]
        self.grid = Grid(self.nivel["mapa"])
        self.avatar = Avatar(*self.nivel["inicio"])
        self.estado = "historia"

        ancho = self.grid.columnas * CELL_SIZE
        alto = self.grid.filas * CELL_SIZE + ALTO_HUD
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption(f"Dijkstra Maze - Nivel {self.nivel['numero']}")

    def dibujar_hud(self):
        pygame.draw.rect(self.pantalla, (20, 20, 20), (0, 0, self.pantalla.get_width(), ALTO_HUD))
        texto = f"Nivel {self.nivel['numero']}/10   Vidas: {self.vidas}"
        superficie = fuente.render(texto, True, (255, 255, 255))
        self.pantalla.blit(superficie, (10, 12))

    def dibujar_historia(self):
        self.pantalla.fill((15, 15, 25))
        lineas = [self.nivel["historia"], "", "Presiona ESPACIO para continuar"]
        for i, linea in enumerate(lineas):
            superficie = fuente_grande.render(linea, True, (255, 255, 255))
            rect = superficie.get_rect(center=(self.pantalla.get_width() // 2, 150 + i * 45))
            self.pantalla.blit(superficie, rect)

    def actualizar_juego(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key in TECLAS_MOVIMIENTO:
            d_fila, d_col = TECLAS_MOVIMIENTO[evento.key]
            self.avatar.mover(d_fila, d_col, self.grid)

            if (self.avatar.fila, self.avatar.col) == self.nivel["meta"]:
                self.avanzar_nivel()

    def avanzar_nivel(self):
        if self.indice_nivel + 1 < len(niveles):
            self.indice_nivel += 1
            self.cargar_nivel(self.indice_nivel)
        else:
            self.estado = "victoria"

    def dibujar_victoria(self):
        self.pantalla.fill((15, 15, 25))
        superficie = fuente_grande.render("¡Completaste los 10 niveles!", True, (255, 255, 255))
        rect = superficie.get_rect(center=(self.pantalla.get_width() // 2, self.pantalla.get_height() // 2))
        self.pantalla.blit(superficie, rect)


juego = Juego()
reloj = pygame.time.Clock()
corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if juego.estado == "historia" and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                juego.estado = "jugando"

        elif juego.estado == "jugando":
            juego.actualizar_juego(evento)

    if juego.estado == "historia":
        juego.dibujar_historia()
    elif juego.estado == "jugando":
        juego.pantalla.fill((255, 255, 255))
        juego.dibujar_hud()
        juego.grid.dibujar(
            juego.pantalla.subsurface((0, ALTO_HUD, juego.grid.columnas * CELL_SIZE, juego.grid.filas * CELL_SIZE)),
            origen=juego.nivel["inicio"], destino=juego.nivel["meta"]
        )
        juego.avatar.dibujar(juego.pantalla.subsurface((0, ALTO_HUD, juego.grid.columnas * CELL_SIZE, juego.grid.filas * CELL_SIZE)))
    elif juego.estado == "victoria":
        juego.dibujar_victoria()

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()