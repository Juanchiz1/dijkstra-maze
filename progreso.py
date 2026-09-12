import json
import os
from datetime import datetime

ARCHIVO_PROGRESO = "progreso.json"


def cargar_progreso():
    if not os.path.exists(ARCHIVO_PROGRESO):
        return {"mejor_puntaje": 0, "nivel_maximo_alcanzado": 0, "historial": []}

    try:
        with open(ARCHIVO_PROGRESO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return {"mejor_puntaje": 0, "nivel_maximo_alcanzado": 0, "historial": []}


def guardar_partida(puntaje, nivel_alcanzado):
    progreso = cargar_progreso()

    progreso["historial"].append({
        "puntaje": puntaje,
        "nivel_alcanzado": nivel_alcanzado,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    progreso["historial"] = progreso["historial"][-10:]  # solo las ultimas 10 partidas

    if puntaje > progreso["mejor_puntaje"]:
        progreso["mejor_puntaje"] = puntaje

    if nivel_alcanzado > progreso["nivel_maximo_alcanzado"]:
        progreso["nivel_maximo_alcanzado"] = nivel_alcanzado

    with open(ARCHIVO_PROGRESO, "w", encoding="utf-8") as archivo:
        json.dump(progreso, archivo, indent=2, ensure_ascii=False)

    return progreso