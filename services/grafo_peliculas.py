"""Servicio que construye el grafo de relaciones entre películas (TP7).

Cada película es un vértice. Dos películas se conectan si comparten al menos
un género, un director o un actor. La arista guarda el motivo y un puntaje de
afinidad que sirve para ordenar las recomendaciones.
"""

from __future__ import annotations

import unicodedata

from estructuras.grafo import Grafo
from models.pelicula import Pelicula

Relacion = tuple[Pelicula, str, float]


def _normalizar(texto: str) -> str:
    """Pasa a minúsculas y quita tildes para comparar sin falsos negativos."""
    if not texto:
        return ""
    sin_tildes = unicodedata.normalize("NFD", texto)
    sin_tildes = "".join(c for c in sin_tildes if unicodedata.category(c) != "Mn")
    return sin_tildes.strip().lower()


def _partes(texto: str) -> list[str]:
    """Separa un campo multivaluado por comas: 'Drama, Crimen' -> 2 partes."""
    return [parte.strip() for parte in texto.split(",") if parte.strip()]


class GrafoPeliculas:
    """Grafo no dirigido de películas relacionadas.

    - ``relacionadas(pelicula)``: vecinos directos ordenados por afinidad.
    - ``camino(origen, destino)``: camino con menos aristas usando BFS.
    - ``explorar(pelicula)``: recorrido en profundidad (DFS) de la red.
    """

    def __init__(self, peliculas: list[Pelicula] | None = None) -> None:
        self._grafo = Grafo(dirigido=False)
        self._por_titulo: dict[str, Pelicula] = {}
        if peliculas:
            self.cargar(peliculas)

    # ------------------------------------------------------------------
    # Construcción
    # ------------------------------------------------------------------
    def cargar(self, peliculas: list[Pelicula]) -> None:
        """Reconstruye el grafo completo a partir del catálogo."""
        self._grafo = Grafo(dirigido=False)
        self._por_titulo = {}

        for pelicula in peliculas:
            self._grafo.insertar_vertice(pelicula)
            self._por_titulo[_normalizar(pelicula.titulo)] = pelicula

        for indice, origen in enumerate(peliculas):
            for destino in peliculas[indice + 1:]:
                relacion = self._calcular_relacion(origen, destino)
                if relacion is not None:
                    motivo, peso = relacion
                    self._grafo.insertar_arista(origen, destino, motivo, peso)

    def _calcular_relacion(self, a: Pelicula, b: Pelicula) -> tuple[str, float] | None:
        """Devuelve el motivo y la afinidad si las películas se relacionan."""
        motivos: list[str] = []
        peso = 0.0

        if a.director and b.director and _normalizar(a.director) == _normalizar(b.director):
            motivos.append(f"mismo director ({a.director})")
            peso += 3.0

        actores_a = {_normalizar(actor): actor for actor in _partes(a.actores)}
        actores_b = {_normalizar(actor): actor for actor in _partes(b.actores)}
        actores_comunes = sorted(
            actores_a[clave] for clave in actores_a.keys() & actores_b.keys()
        )
        if actores_comunes:
            motivos.append("actor en común: " + ", ".join(actores_comunes))
            peso += 2.0 * len(actores_comunes)

        generos_a = {_normalizar(genero): genero for genero in _partes(a.genero)}
        generos_b = {_normalizar(genero): genero for genero in _partes(b.genero)}
        generos_comunes = sorted(
            generos_a[clave] for clave in generos_a.keys() & generos_b.keys()
        )
        if generos_comunes:
            motivos.append("género en común: " + ", ".join(generos_comunes))
            peso += len(generos_comunes)

        if not motivos:
            return None

        return "; ".join(motivos), peso

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self._grafo)

    def esta_vacio(self) -> bool:
        return self._grafo.esta_vacio()

    def buscar(self, titulo: str) -> Pelicula | None:
        """Busca por título exacto (ignorando mayúsculas y tildes)."""
        return self._por_titulo.get(_normalizar(titulo))

    def existe(self, pelicula: Pelicula) -> bool:
        return self._grafo.buscar_vertice(pelicula) is not None

    def grado(self, pelicula: Pelicula) -> int:
        return len(self._grafo.adyacentes(pelicula))

    def relacionadas(self, pelicula: Pelicula, limite: int = 5) -> list[Relacion]:
        """Vecinos directos ordenados por afinidad y, en empate, por rating."""
        if limite <= 0:
            return []

        vecinos: list[Relacion] = []
        for arista in self._grafo.adyacentes(pelicula):
            vecinos.append((arista.destino.info, arista.info, arista.peso))

        vecinos.sort(key=lambda item: (-item[2], -item[0].rating, item[0].titulo))
        return vecinos[:limite]

    def camino(self, origen: Pelicula, destino: Pelicula) -> list[Pelicula] | None:
        """Camino con menos relaciones entre dos películas (BFS)."""
        return self._grafo.camino_mas_corto(origen, destino)

    def explorar(self, pelicula: Pelicula) -> list[Pelicula]:
        """Recorrido en profundidad desde una película (DFS)."""
        return self._grafo.dfs(pelicula)

    def recorrido_amplitud(self, pelicula: Pelicula) -> list[Pelicula]:
        """Recorrido por amplitud desde una película (BFS)."""
        return self._grafo.bfs(pelicula)
