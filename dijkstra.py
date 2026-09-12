import heapq


def dijkstra(grid, origen):
    """
    Implementacion directa del pseudocodigo:
    - distancia[u] = INFINITO para todos, salvo el origen = 0
    - cola de prioridad: siempre se extrae el nodo de distancia minima
    - relajacion: si distancia[v] > distancia[u] + peso(u,v), se actualiza
    """
    distancias = {}
    for f in range(grid.filas):
        for c in range(grid.columnas):
            if not grid.celda(f, c).es_muro():
                distancias[(f, c)] = float("inf")

    distancias[origen] = 0
    previos = {}
    visitados = set()
    cola = [(0, origen)]  # (distancia, nodo)

    while cola:
        distancia_actual, actual = heapq.heappop(cola)

        if actual in visitados:
            continue
        visitados.add(actual)

        fila, col = actual
        for d_fila, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            vecino = (fila + d_fila, col + d_col)
            vf, vc = vecino

            if not grid.dentro_del_grid(vf, vc):
                continue
            if grid.celda(vf, vc).es_muro():
                continue

            peso = grid.celda(vf, vc).costo
            nueva_distancia = distancia_actual + peso

            if nueva_distancia < distancias.get(vecino, float("inf")):
                distancias[vecino] = nueva_distancia
                previos[vecino] = actual
                heapq.heappush(cola, (nueva_distancia, vecino))

    return distancias, previos


def reconstruir_camino(previos, origen, destino):
    if destino == origen:
        return [origen]
    if destino not in previos:
        return None  # no existe camino

    camino = [destino]
    actual = destino
    while actual != origen:
        actual = previos[actual]
        camino.append(actual)
    camino.reverse()
    return camino