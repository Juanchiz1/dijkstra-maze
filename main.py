import pygame
import sys
from grid import Grid, CELL_SIZE, ROWS, COLS

pygame.init()

ANCHO = COLS * CELL_SIZE
ALTO = ROWS * CELL_SIZE

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dijkstra Maze")
reloj = pygame.time.Clock()

grid = Grid(ROWS, COLS)

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    pantalla.fill((255, 255, 255))
    grid.dibujar(pantalla)
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()