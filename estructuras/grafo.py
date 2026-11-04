"""Grafo no dirigido con lista de adyacencia.

TP7: las relaciones del dominio se modelan como un grafo.

- **Vértice:** una película.
- **Arista:** dos películas están conectadas si comparten al menos un género,
  un director o un actor.
- **Tipo:** no dirigido (la relación es simétrica) y no pesado para los
  recorridos. Cada arista guarda además un texto con el motivo de la relación
  y un puntaje de afinidad que se usa solo para ordenar recomendaciones.
- **Representación:** lista de adyacencia enlazada. Para un catálogo grande la
  mayoría de las parejas no estaría conectada, así que una matriz de
  adyacencia desperdiciaría O(V²) de memoria.

El módulo mantiene los nombres usados en TP anteriores (`NodoVertice`,
`NodoArista`, `Grafo`) y agrega las operaciones de inserción, recorridos BFS y
DFS, y camino más corto sin pesos.
"""

from __future__ import annotations

from typing import Any, Iterable


# ==========================================
# TDA COLA (para BFS)
# ==========================================
class NodoColaVertice:
    def __init__(self, dato: Any) -> None:
        self.dato = dato
        self.siguiente: NodoColaVertice | None = None


class ColaVertice:
    def __init__(self) -> None:
        self.frente: NodoColaVertice | None = None
        self.final: NodoColaVertice | None = None

    def esta_vacia(self) -> bool:
        return self.frente is None

    def encolar(self, dato: Any) -> None:
        nuevo = NodoColaVertice(dato)
        if self.esta_vacia():
            self.frente = nuevo
            self.final = nuevo
        else:
            if self.final is not None:
                self.final.siguiente = nuevo
            self.final = nuevo

    def desencolar(self) -> Any:
        if self.esta_vacia():
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        return dato


# ==========================================
# CLASES DE LA ESTRUCTURA DEL GRAFO
# ==========================================
class NodoArista:
    def __init__(self, info: str, destino: "NodoVertice", peso: float = 1.0) -> None:
        self.info = info          # motivo legible de la relación
        self.destino = destino
        self.peso = peso          # afinidad, solo para ordenar sugerencias
        self.sig: NodoArista | None = None


class Arista:
    def __init__(self) -> None:
        self.inicio: NodoArista | None = None
        self.tamanio = 0


class NodoVertice:
    def __init__(self, info: Any) -> None:
        self.info = info
        self.sig: NodoVertice | None = None
        self.visitado = False
        self.adyacentes = Arista()


class Grafo:
    def __init__(self, dirigido: bool = False) -> None:
        self.inicio: NodoVertice | None = None
        self.dirigido = dirigido
        self.tamanio = 0
        self._ultimo: NodoVertice | None = None

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------
    def esta_vacio(self) -> bool:
        return self.inicio is None

    def __len__(self) -> int:
        return self.tamanio

    def buscar_vertice(self, info: Any) -> NodoVertice | None:
        actual = self.inicio
        while actual is not None:
            if actual.info is info or actual.info == info:
                return actual
            actual = actual.sig
        return None

    def adyacentes(self, info: Any) -> list[NodoArista]:
        """Devuelve las aristas que salen del vértice indicado."""
        vertice = self.buscar_vertice(info)
        if vertice is None:
            return []

        resultado: list[NodoArista] = []
        actual = vertice.adyacentes.inicio
        while actual is not None:
            resultado.append(actual)
            actual = actual.sig
        return resultado

    # ------------------------------------------------------------------
    # Inserción
    # ------------------------------------------------------------------
    def insertar_vertice(self, info: Any) -> NodoVertice:
        existente = self.buscar_vertice(info)
        if existente is not None:
            return existente

        nuevo = NodoVertice(info)
        if self.inicio is None:
            self.inicio = nuevo
        elif self._ultimo is not None:
            self._ultimo.sig = nuevo
        self._ultimo = nuevo
        self.tamanio += 1
        return nuevo

    def insertar_arista(
        self,
        origen_info: Any,
        destino_info: Any,
        info: str = "",
        peso: float = 1.0,
    ) -> bool:
        """Conecta origen con destino. En un grafo no dirigido agrega ambas."""
        origen = self.buscar_vertice(origen_info)
        destino = self.buscar_vertice(destino_info)

        if origen is None or destino is None or origen is destino:
            return False
        if self._existe_arista(origen, destino):
            return False

        self._agregar_adyacente(origen, destino, info, peso)
        if not self.dirigido:
            self._agregar_adyacente(destino, origen, info, peso)
        return True

    def _existe_arista(self, origen: NodoVertice, destino: NodoVertice) -> bool:
        actual = origen.adyacentes.inicio
        while actual is not None:
            if actual.destino is destino:
                return True
            actual = actual.sig
        return False

    def _agregar_adyacente(
        self,
        origen: NodoVertice,
        destino: NodoVertice,
        info: str,
        peso: float,
    ) -> None:
        nueva = NodoArista(info, destino, peso)
        if origen.adyacentes.inicio is None:
            origen.adyacentes.inicio = nueva
        else:
            actual = origen.adyacentes.inicio
            while actual.sig is not None:
                actual = actual.sig
            actual.sig = nueva
        origen.adyacentes.tamanio += 1

    # ------------------------------------------------------------------
    # Recorridos
    # ------------------------------------------------------------------
    def reiniciar_visitados(self) -> None:
        actual = self.inicio
        while actual is not None:
            actual.visitado = False
            actual = actual.sig

    def bfs(self, inicio_info: Any) -> list[Any]:
        """Recorrido por amplitud. Devuelve los datos en orden de visita."""
        inicio = self.buscar_vertice(inicio_info)
        if inicio is None:
            return []

        self.reiniciar_visitados()
        orden: list[Any] = []
        cola = ColaVertice()

        inicio.visitado = True
        cola.encolar(inicio)

        while not cola.esta_vacia():
            actual = cola.desencolar()
            orden.append(actual.info)

            arista = actual.adyacentes.inicio
            while arista is not None:
                if not arista.destino.visitado:
                    arista.destino.visitado = True
                    cola.encolar(arista.destino)
                arista = arista.sig

        return orden

    def dfs(self, inicio_info: Any) -> list[Any]:
        """Recorrido en profundidad. Devuelve los datos en orden de visita."""
        inicio = self.buscar_vertice(inicio_info)
        if inicio is None:
            return []

        self.reiniciar_visitados()
        orden: list[Any] = []
        self._dfs_rec(inicio, orden)
        return orden

    def _dfs_rec(self, vertice: NodoVertice, orden: list[Any]) -> None:
        vertice.visitado = True
        orden.append(vertice.info)

        arista = vertice.adyacentes.inicio
        while arista is not None:
            if not arista.destino.visitado:
                self._dfs_rec(arista.destino, orden)
            arista = arista.sig

    def camino_mas_corto(self, origen_info: Any, destino_info: Any) -> list[Any] | None:
        """Camino con menos aristas entre dos vértices (BFS).

        En un grafo no pesado, BFS encuentra el camino más corto en cantidad de
        aristas. Devuelve la lista de datos desde origen hasta destino, o
        ``None`` si no existe camino.
        """
        origen = self.buscar_vertice(origen_info)
        destino = self.buscar_vertice(destino_info)
        if origen is None or destino is None:
            return None
        if origen is destino:
            return [origen.info]

        self.reiniciar_visitados()
        cola = ColaVertice()
        padres: dict[NodoVertice, NodoVertice | None] = {origen: None}

        origen.visitado = True
        cola.encolar(origen)

        encontrado = False
        while not cola.esta_vacia() and not encontrado:
            actual = cola.desencolar()
            arista = actual.adyacentes.inicio

            while arista is not None:
                vecino = arista.destino
                if not vecino.visitado:
                    vecino.visitado = True
                    padres[vecino] = actual
                    if vecino is destino:
                        encontrado = True
                        break
                    cola.encolar(vecino)
                arista = arista.sig

        if not encontrado:
            return None

        camino: list[Any] = []
        actual: NodoVertice | None = destino
        while actual is not None:
            camino.append(actual.info)
            actual = padres.get(actual)
        camino.reverse()
        return camino


# ==========================================
# COMPATIBILIDAD CON TP ANTERIORES
# ==========================================
def buscar_titulo_amplitud(grafo: Grafo, titulo_buscado: str) -> NodoVertice | None:
    """Busca un vértice cuyo ``info.titulo`` coincida, usando BFS."""
    if grafo.inicio is None:
        return None

    grafo.reiniciar_visitados()
    objetivo = titulo_buscado.strip().lower()
    cola = ColaVertice()

    nodo_inicial = grafo.inicio
    nodo_inicial.visitado = True
    cola.encolar(nodo_inicial)

    while not cola.esta_vacia():
        actual = cola.desencolar()
        titulo = getattr(actual.info, "titulo", "")
        if titulo.strip().lower() == objetivo:
            return actual

        arista = actual.adyacentes.inicio
        while arista is not None:
            if not arista.destino.visitado:
                arista.destino.visitado = True
                cola.encolar(arista.destino)
            arista = arista.sig

    return None
