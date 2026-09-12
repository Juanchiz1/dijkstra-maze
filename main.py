import pygame
import sys
from grid import Grid
from avatar import Avatar
from enemigo import Enemigo
from niveles import crear_todos_los_niveles

pygame.init()
fuente = pygame.font.SysFont("arial", 22)
fuente_grande = pygame.font.SysFont("arial", 30, bold=True)

VENTANA_ANCHO = 960
VENTANA_ALTO_JUEGO = 680
ALTO_HUD = 50

niveles = crear_todos_los_niveles()

TECLAS_MOVIMIENTO = {
    pygame.K_UP: (-1, 0),
    pygame.K_DOWN: (1, 0),
    pygame.K_LEFT: (0, -1),
    pygame.K_RIGHT: (0, 1),
}

pantalla = pygame.display.set_mode((VENTANA_ANCHO, VENTANA_ALTO_JUEGO + ALTO_HUD))
pygame.display.set_caption("Dijkstra Maze")


class Juego:
    def __init__(self):
        self.vidas = 3
        self.indice_nivel = 0
        self.estado = "historia"
        self.cargar_nivel(self.indice_nivel)

    def cargar_nivel(self, indice):
        self.nivel = niveles[indice]
        self.grid = Grid(self.nivel["mapa"])
        self.avatar = Avatar(*self.nivel["inicio"])
        self.enemigos = [Enemigo(f, c) for (f, c) in self.nivel["posiciones_enemigos"]]

        self.cell_size = min(
            VENTANA_ANCHO // self.grid.columnas,
            VENTANA_ALTO_JUEGO // self.grid.filas,
        )
        self.estado = "historia"

    def dibujar_hud(self, superficie_hud):
        superficie_hud.fill((20, 20, 20))
        texto = f"Nivel {self.nivel['numero']}/10   Vidas: {self.vidas}"
        render = fuente.render(texto, True, (255, 255, 255))
        superficie_hud.blit(render, (10, 12))

    def dibujar_historia(self, pantalla):
        pantalla.fill((15, 15, 25))
        lineas = [self.nivel["historia"], "", "Presiona ESPACIO para continuar"]
        for i, linea in enumerate(lineas):
            render = fuente_grande.render(linea, True, (255, 255, 255))
            rect = render.get_rect(center=(pantalla.get_width() // 2, 150 + i * 45))
            pantalla.blit(render, rect)

    def actualizar_juego(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key in TECLAS_MOVIMIENTO:
            d_fila, d_col = TECLAS_MOVIMIENTO[evento.key]
            self.avatar.mover(d_fila, d_col, self.grid)

            if (self.avatar.fila, self.avatar.col) == self.nivel["meta"]:
                self.avanzar_nivel()

    def actualizar_enemigos(self):
        for enemigo in self.enemigos:
            enemigo.actualizar(self.grid)

    def avanzar_nivel(self):
        if self.indice_nivel + 1 < len(niveles):
            self.indice_nivel += 1
            self.cargar_nivel(self.indice_nivel)
        else:
            self.estado = "victoria"

    def dibujar_victoria(self, pantalla):
        pantalla.fill((15, 15, 25))
        render = fuente_grande.render("¡Completaste los 10 niveles!", True, (255, 255, 255))
        rect = render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2))
        pantalla.blit(render, rect)


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
        juego.dibujar_historia(pantalla)

    elif juego.estado == "jugando":
        juego.actualizar_enemigos()

        pantalla.fill((255, 255, 255))
        superficie_hud = pantalla.subsurface((0, 0, VENTANA_ANCHO, ALTO_HUD))
        juego.dibujar_hud(superficie_hud)

        superficie_juego = pantalla.subsurface(
            (0, ALTO_HUD, VENTANA_ANCHO, VENTANA_ALTO_JUEGO)
        )
        juego.grid.dibujar(superficie_juego, juego.cell_size, origen=juego.nivel["inicio"], destino=juego.nivel["meta"])
        juego.avatar.dibujar(superficie_juego, juego.cell_size)
        for enemigo in juego.enemigos:
            enemigo.dibujar(superficie_juego, juego.cell_size)

    elif juego.estado == "victoria":
        juego.dibujar_victoria(pantalla)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()