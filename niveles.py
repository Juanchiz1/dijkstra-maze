import random
from collections import deque

NIVEL_CONFIGS = [
    {"numero": 1,  "filas": 10, "columnas": 12, "densidad_muros": 0.15, "enemigos": 0, "semilla": 1,
     "historia": "La tortuga quiere volver a su nido, donde la esperan sus huevos."},
    {"numero": 2,  "filas": 12, "columnas": 14, "densidad_muros": 0.20, "enemigos": 0, "semilla": 2,
     "historia": "El terreno se vuelve mas irregular."},
    {"numero": 3,  "filas": 14, "columnas": 16, "densidad_muros": 0.24, "enemigos": 1, "semilla": 3,
     "historia": "Un cangrejo hambriento ronda cerca del nido."},
    {"numero": 4,  "filas": 16, "columnas": 18, "densidad_muros": 0.27, "enemigos": 0, "semilla": 4,
     "historia": "Zona rocosa. El costo de moverse aumenta."},
    {"numero": 5,  "filas": 18, "columnas": 20, "densidad_muros": 0.30, "enemigos": 1, "semilla": 5,
     "historia": "Otro cangrejo patrulla, mas rapido que el anterior."},
    {"numero": 6,  "filas": 20, "columnas": 22, "densidad_muros": 0.32, "enemigos": 0, "semilla": 6,
     "historia": "El laberinto se hace mas denso."},
    {"numero": 7,  "filas": 22, "columnas": 24, "densidad_muros": 0.34, "enemigos": 2, "semilla": 7,
     "historia": "Dos cangrejos cazan juntos."},
    {"numero": 8,  "filas": 24, "columnas": 26, "densidad_muros": 0.36, "enemigos": 0, "semilla": 8,
     "historia": "Casi llegas. El terreno es traicionero."},
    {"numero": 9,  "filas": 26, "columnas": 28, "densidad_muros": 0.38, "enemigos": 2, "semilla": 9,
     "historia": "La guardia del nido enemigo se intensifica."},
    {"numero": 10, "filas": 28, "columnas": 30, "densidad_muros": 0.40, "enemigos": 3, "semilla": 10,
     "historia": "Ultimo tramo. Tres cangrejos protegen el camino final."},
]


def _hay_camino(mapa, inicio, meta):
    filas = len(mapa)
    columnas = len(mapa[0])
    visitados = {inicio}
    cola = deque([inicio])

    while cola:
        fila, col = cola.popleft()
        if (fila, col) == meta:
            return True
        for d_fila, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nf, nc = fila + d_fila, col + d_col
            if 0 <= nf < filas and 0 <= nc < columnas and (nf, nc) not in visitados:
                if mapa[nf][nc] != 0:
                    visitados.add((nf, nc))
                    cola.append((nf, nc))
    return False


def _celdas_libres(mapa, excluir):
    libres = []
    for f in range(len(mapa)):
        for c in range(len(mapa[0])):
            if mapa[f][c] != 0 and (f, c) not in excluir:
                libres.append((f, c))
    return libres


def generar_mapa(filas, columnas, densidad_muros, semilla):
    random.seed(semilla)
    inicio = (0, 0)
    meta = (filas - 1, columnas - 1)

    intentos = 0
    while True:
        intentos += 1
        mapa = []
        for f in range(filas):
            fila_actual = []
            for c in range(columnas):
                if random.random() < densidad_muros:
                    fila_actual.append(0)
                else:
                    fila_actual.append(random.choice([1, 1, 1, 2, 2, 3, 4]))
            mapa.append(fila_actual)

        mapa[inicio[0]][inicio[1]] = 1
        mapa[meta[0]][meta[1]] = 1

        if _hay_camino(mapa, inicio, meta):
            return mapa, inicio, meta

        if intentos > 300:
            densidad_muros *= 0.85


def crear_nivel(config):
    mapa, inicio, meta = generar_mapa(
        config["filas"], config["columnas"], config["densidad_muros"], config["semilla"]
    )

    random.seed(config["semilla"] + 1000)  # semilla distinta para no repetir el patron del mapa
    libres = _celdas_libres(mapa, excluir={inicio, meta})
    random.shuffle(libres)
    posiciones_enemigos = libres[: config["enemigos"]]

    return {
        "numero": config["numero"],
        "mapa": mapa,
        "inicio": inicio,
        "meta": meta,
        "posiciones_enemigos": posiciones_enemigos,
        "historia": config["historia"],
    }


def crear_todos_los_niveles():
    return [crear_nivel(cfg) for cfg in NIVEL_CONFIGS]