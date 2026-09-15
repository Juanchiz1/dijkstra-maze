import pygame
import sys
from grid import Grid
from avatar import Avatar, VELOCIDAD_BASE
from enemigo import Enemigo
from dijkstra import dijkstra, reconstruir_camino
from niveles import crear_todos_los_niveles
from progreso import cargar_progreso, guardar_partida

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
        self.progreso_guardado = cargar_progreso()
        self.estado = "menu"
        
    def iniciar_juego(self):
        self.vidas = 3
        self.puntaje = 0
        self.pistas_restantes = 3
        self.indice_nivel = 0
        self.cargar_nivel(0)    

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
        if not self.mostrar_pista and self.pistas_restantes <= 0:
            return  # no quedan pistas, no hace nada

        self.mostrar_pista = not self.mostrar_pista
        if self.mostrar_pista:
            self.pistas_restantes -= 1
            self.calcular_pista()
        else:
            self.camino_pista = None

    def perder_vida(self):
        self.vidas -= 1
        if self.vidas <= 0:
            self.estado = "derrota"
            self.progreso_guardado = guardar_partida(self.puntaje, self.nivel["numero"])
        else:
            self.avatar.reposicionar(*self.nivel["inicio"])
            self.avatar.resetear_velocidad()

    def avanzar_nivel(self):
        self.puntaje += 100 * self.nivel["numero"]
        if self.indice_nivel + 1 < len(niveles):
            self.indice_nivel += 1
            self.cargar_nivel(self.indice_nivel)
        else:
            self.estado = "victoria"
            self.progreso_guardado = guardar_partida(self.puntaje, self.nivel["numero"])

    def volver_al_menu(self):
        self.progreso_guardado = cargar_progreso()
        self.estado = "menu"

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
                    self.puntaje += 50
                else:
                    self.perder_vida()
                    return

    def dibujar_hud(self, superficie_hud):
        superficie_hud.fill((15, 15, 20))
        texto = (f"Nivel {self.nivel['numero']}/10   Vidas: {self.vidas}   "
                 f"Puntaje: {self.puntaje}   Pistas: {self.pistas_restantes}")
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
        rect = render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 - 50))
        pantalla.blit(render, rect)

        texto_puntaje = f"Tu puntaje: {self.puntaje}   Mejor puntaje: {self.progreso_guardado['mejor_puntaje']}"
        render2 = fuente.render(texto_puntaje, True, (220, 220, 220))
        rect2 = render2.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2))
        pantalla.blit(render2, rect2)

        render3 = fuente.render("Presiona ENTER para reiniciar", True, (200, 200, 200))
        rect3 = render3.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 + 40))
        pantalla.blit(render3, rect3)
        
    def dibujar_menu(self, pantalla):
        pantalla.fill(COLOR_FONDO)
        titulo = fuente_grande.render("Dijkstra Maze", True, (255, 255, 255))
        rect = titulo.get_rect(center=(pantalla.get_width() // 2, 140))
        pantalla.blit(titulo, rect)

        opciones = [
            "ENTER - Jugar",
            "H - Ver historial de partidas",
            f"Mejor puntaje: {self.progreso_guardado['mejor_puntaje']}",
        ]
        for i, linea in enumerate(opciones):
            render = fuente.render(linea, True, (220, 220, 220))
            rect = render.get_rect(center=(pantalla.get_width() // 2, 230 + i * 40))
            pantalla.blit(render, rect)

    def dibujar_historial(self, pantalla):
        pantalla.fill(COLOR_FONDO)
        titulo = fuente_grande.render("Historial de partidas", True, (255, 255, 255))
        rect = titulo.get_rect(center=(pantalla.get_width() // 2, 60))
        pantalla.blit(titulo, rect)

        resumen = (f"Mejor puntaje: {self.progreso_guardado['mejor_puntaje']}   "
                   f"Nivel maximo alcanzado: {self.progreso_guardado['nivel_maximo_alcanzado']}")
        render_resumen = fuente.render(resumen, True, (200, 200, 200))
        rect_resumen = render_resumen.get_rect(center=(pantalla.get_width() // 2, 110))
        pantalla.blit(render_resumen, rect_resumen)

        historial = list(reversed(self.progreso_guardado["historial"]))
        if not historial:
            render = fuente.render("Todavia no hay partidas registradas", True, (180, 180, 180))
            rect = render.get_rect(center=(pantalla.get_width() // 2, 180))
            pantalla.blit(render, rect)
        else:
            for i, partida in enumerate(historial[:8]):
                linea = f"{partida['fecha']}   Nivel {partida['nivel_alcanzado']}/10   Puntaje: {partida['puntaje']}"
                render = fuente.render(linea, True, (220, 220, 220))
                pantalla.blit(render, (pantalla.get_width() // 2 - 220, 160 + i * 32))

        render_volver = fuente.render("ENTER - Volver al menu", True, (180, 180, 180))
        rect_volver = render_volver.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() - 40))
        pantalla.blit(render_volver, rect_volver)    


juego = Juego()
reloj = pygame.time.Clock()
corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:
            if juego.estado == "menu":
                if evento.key == pygame.K_RETURN:
                    juego.iniciar_juego()
                elif evento.key == pygame.K_h:
                    juego.estado = "historial"

            elif juego.estado == "historial":
                if evento.key == pygame.K_RETURN:
                    juego.estado = "menu"

            elif juego.estado == "historia" and evento.key == pygame.K_SPACE:
                juego.estado = "jugando"

            elif juego.estado == "jugando" and evento.key == pygame.K_h:
                juego.alternar_pista()

            elif juego.estado in ("victoria", "derrota") and evento.key == pygame.K_RETURN:
                juego.volver_al_menu()

    if juego.estado == "menu":
        juego.dibujar_menu(pantalla)

    elif juego.estado == "historial":
        juego.dibujar_historial(pantalla)

    elif juego.estado == "historia":
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