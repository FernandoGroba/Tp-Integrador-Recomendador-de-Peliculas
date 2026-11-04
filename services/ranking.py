"""Ranking de películas usando una cola de prioridades (max-heap).

La estructura `HeapMax` vive en `estructuras.heap` y se implementa a mano,
sin `heapq`. Este servicio la conecta con el dominio: la prioridad es el
rating de cada película.
"""

from __future__ import annotations

from estructuras.heap import HeapMax
from models.pelicula import Pelicula


class RankingPeliculas:
    """Mantiene las películas en una heap ordenada por rating.

    - La película con mayor rating queda en la raíz.
    - En caso de empate, respeta el orden de llegada (FIFO).
    - ``top(n)`` no destruye el ranking: se puede consultar varias veces.
    """

    def __init__(self, peliculas: list[Pelicula] | None = None) -> None:
        self._heap = HeapMax()
        if peliculas:
            self.cargar(peliculas)

    def cargar(self, peliculas: list[Pelicula]) -> None:
        """Reconstruye el ranking en O(n) a partir del catálogo."""
        self._heap = HeapMax.desde_elementos(
            (pelicula, pelicula.rating) for pelicula in peliculas
        )

    def top(self, cantidad: int = 10) -> list[Pelicula]:
        """Devuelve las ``cantidad`` películas mejor rankeadas."""
        return self._heap.top_n(cantidad)

    def mejor(self) -> Pelicula | None:
        """Devuelve la película con mayor rating sin sacarla del ranking."""
        return self._heap.ver_max()

    def __len__(self) -> int:
        return len(self._heap)

    def esta_vacio(self) -> bool:
        return self._heap.esta_vacia()
