import pygame
import sys
from grid import Grid
from avatar import Avatar, VELOCIDAD_BASE
from enemigo import Enemigo
from dijkstra import dijkstra, reconstruir_camino
from niveles import crear_todos_los_niveles

pygame.init()
fuente = pygame.font.SysFont("arial", 20)
fuente_grande = pygame.font.SysFont("arial", 30, bold=True)

VENTANA_ANCHO = 960
VENTANA_ALTO_JUEGO = 680
ALTO_HUD = 50
COLOR_FONDO = (25, 25, 35)

niveles = crear_todos_los_niveles()

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
        self.mostrar_pista = False
        self.camino_pista = None

        self.cell_size = min(
            VENTANA_ANCHO // self.grid.columnas,
            VENTANA_ALTO_JUEGO // self.grid.filas,
        )
        ancho_grid = self.grid.columnas * self.cell_size
        alto_grid = self.grid.filas * self.cell_size
        self.offset_x = (VENTANA_ANCHO - ancho_grid) // 2
        self.offset_y = (VENTANA_ALTO_JUEGO - alto_grid) // 2

        self.estado = "historia"

    def calcular_pista(self):
        _, previos = dijkstra(self.grid, (self.avatar.fila, self.avatar.col))
        self.camino_pista = reconstruir_camino(previos, (self.avatar.fila, self.avatar.col), self.nivel["meta"])

    def alternar_pista(self):
        self.mostrar_pista = not self.mostrar_pista
        if self.mostrar_pista:
            self.calcular_pista()
        else:
            self.camino_pista = None

    def perder_vida(self):
        self.vidas -= 1
        if self.vidas <= 0:
            self.estado = "derrota"
        else:
            self.avatar.reposicionar(*self.nivel["inicio"])
            self.avatar.resetear_velocidad()

    def avanzar_nivel(self):
        if self.indice_nivel + 1 < len(niveles):
            self.indice_nivel += 1
            self.cargar_nivel(self.indice_nivel)
        else:
            self.estado = "victoria"

    def reiniciar_juego(self):
        self.vidas = 3
        self.indice_nivel = 0
        self.cargar_nivel(0)

    def actualizar_jugando(self):
        avatar_movio = self.avatar.actualizar(self.grid)

        if self.mostrar_pista and avatar_movio:
            self.calcular_pista()

        if avatar_movio and (self.avatar.fila, self.avatar.col) == self.nivel["meta"]:
            self.avanzar_nivel()
            return

        posicion_avatar = (self.avatar.fila, self.avatar.col)
        for enemigo in self.enemigos:
            enemigo_movio = enemigo.actualizar(self.grid, posicion_avatar)

            if not enemigo.vivo:
                continue

            if (enemigo.fila, enemigo.col) == posicion_avatar:
                if avatar_movio:
                    enemigo.vivo = False
                    self.avatar.aumentar_velocidad()
                else:
                    self.perder_vida()
                    return

    def dibujar_hud(self, superficie_hud):
        superficie_hud.fill((15, 15, 20))
        texto = f"Nivel {self.nivel['numero']}/10   Vidas: {self.vidas}   Pista (H): {'ON' if self.mostrar_pista else 'OFF'}"
        render = fuente.render(texto, True, (255, 255, 255))
        superficie_hud.blit(render, (10, 14))

    def dibujar_historia(self, pantalla):
        pantalla.fill(COLOR_FONDO)
        lineas = [self.nivel["historia"], "", "Presiona ESPACIO para continuar"]
        for i, linea in enumerate(lineas):
            render = fuente_grande.render(linea, True, (255, 255, 255))
            rect = render.get_rect(center=(pantalla.get_width() // 2, 150 + i * 45))
            pantalla.blit(render, rect)

    def dibujar_final(self, pantalla, mensaje):
        pantalla.fill(COLOR_FONDO)
        render = fuente_grande.render(mensaje, True, (255, 255, 255))
        rect = render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 - 20))
        pantalla.blit(render, rect)
        render2 = fuente.render("Presiona ENTER para reiniciar", True, (200, 200, 200))
        rect2 = render2.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 + 30))
        pantalla.blit(render2, rect2)


juego = Juego()
reloj = pygame.time.Clock()
corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:
            if juego.estado == "historia" and evento.key == pygame.K_SPACE:
                juego.estado = "jugando"

            elif juego.estado == "jugando" and evento.key == pygame.K_h:
                juego.alternar_pista()

            elif juego.estado in ("victoria", "derrota") and evento.key == pygame.K_RETURN:
                juego.reiniciar_juego()

    if juego.estado == "historia":
        juego.dibujar_historia(pantalla)

    elif juego.estado == "jugando":
        juego.actualizar_jugando()

        pantalla.fill(COLOR_FONDO)

        superficie_hud = pantalla.subsurface((0, 0, VENTANA_ANCHO, ALTO_HUD))
        juego.dibujar_hud(superficie_hud)

        superficie_juego = pantalla.subsurface((0, ALTO_HUD, VENTANA_ANCHO, VENTANA_ALTO_JUEGO))
        juego.grid.dibujar(
            superficie_juego, juego.cell_size,
            offset_x=juego.offset_x, offset_y=juego.offset_y,
            destino=juego.nivel["meta"],
            camino_pista=juego.camino_pista,
        )
        juego.avatar.dibujar(superficie_juego, juego.cell_size, juego.offset_x, juego.offset_y)
        for enemigo in juego.enemigos:
            enemigo.dibujar(superficie_juego, juego.cell_size, juego.offset_x, juego.offset_y)

    elif juego.estado == "victoria":
        juego.dibujar_final(pantalla, "¡Completaste los 10 niveles!")

    elif juego.estado == "derrota":
        juego.dibujar_final(pantalla, "Te quedaste sin vidas")

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()