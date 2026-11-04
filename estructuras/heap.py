"""Cola de prioridades implementada como un max-heap binario.

La cátedra pide implementar la heap manualmente, así que este módulo no usa
`heapq`. La raíz (índice 0 del vector) es siempre el elemento de mayor
prioridad.

En este proyecto la prioridad de una película es su `rating`: cuanto más alto,
antes sale. Si dos películas tienen el mismo rating, sale primero la que llegó
primero (criterio FIFO) para que el Top-N sea determinista.
"""

from __future__ import annotations

from typing import Any, Iterable


class _EntradaHeap:
    """Entrada interna del heap: prioridad + dato + orden de llegada."""

    __slots__ = ("prioridad", "secuencia", "dato")

    def __init__(self, prioridad: float, secuencia: int, dato: Any) -> None:
        self.prioridad = prioridad
        self.secuencia = secuencia
        self.dato = dato


class HeapMax:
    """Max-heap binario sobre un vector.

    Operaciones principales:
      - ``insertar(dato, prioridad)``: O(log n).
      - ``ver_max()``: O(1).
      - ``extraer_max()``: O(log n).
      - ``top_n(n)``: O(n + k log n) porque copia el vector para no destruir
        el heap original.
      - ``desde_elementos(...)``: O(n) usando el método de hundir desde la
        mitad del vector (monticulizar).
    """

    def __init__(self) -> None:
        self._datos: list[_EntradaHeap] = []
        self._secuencia = 0

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self._datos)

    def esta_vacia(self) -> bool:
        return not self._datos

    def tamanio(self) -> int:
        return len(self._datos)

    def ver_max(self) -> Any | None:
        """Devuelve el elemento de mayor prioridad sin extraerlo."""
        if self.esta_vacia():
            return None
        return self._datos[0].dato

    def frente(self) -> Any | None:
        """Alias pedagógico de ``ver_max``."""
        return self.ver_max()

    # ------------------------------------------------------------------
    # Operaciones
    # ------------------------------------------------------------------
    def insertar(self, dato: Any, prioridad: float) -> None:
        """Agrega un elemento al final y lo flota hasta su lugar."""
        entrada = _EntradaHeap(prioridad, self._secuencia, dato)
        self._secuencia += 1
        self._datos.append(entrada)
        self._flotar(len(self._datos) - 1)

    def arribo(self, dato: Any, prioridad: float) -> None:
        """Alias pedagógico de ``insertar`` (arribo de la cola de prioridades)."""
        self.insertar(dato, prioridad)

    def extraer_max(self) -> Any | None:
        """Quita y devuelve la raíz; deja el último elemento y lo hunde."""
        if self.esta_vacia():
            return None

        raiz = self._datos[0]
        ultimo = self._datos.pop()

        if self._datos:
            self._datos[0] = ultimo
            self._hundir(0)

        return raiz.dato

    def atencion(self) -> Any | None:
        """Alias pedagógico de ``extraer_max`` (atención de la cola)."""
        return self.extraer_max()

    def top_n(self, n: int) -> list[Any]:
        """Devuelve los ``n`` elementos de mayor prioridad sin modificar el heap.

        Se copia el vector (que ya cumple la propiedad de heap) y se extrae
        sobre la copia. Así el ranking original queda intacto.
        """
        if n <= 0 or self.esta_vacia():
            return []

        copia = HeapMax()
        copia._datos = list(self._datos)
        copia._secuencia = self._secuencia

        return [copia.extraer_max() for _ in range(min(n, len(copia)))]

    def cambiar_prioridad(self, dato: Any, nueva_prioridad: float) -> bool:
        """Actualiza la prioridad de un dato y reacomoda el heap.

        Recorre el vector buscando el dato por identidad. Es O(n), porque el
        heap no permite búsquedas arbitrarias eficientes.
        """
        for indice, entrada in enumerate(self._datos):
            if entrada.dato is dato:
                entrada.prioridad = nueva_prioridad
                self._flotar(indice)
                self._hundir(indice)
                return True
        return False

    # ------------------------------------------------------------------
    # Construcción / monticulización
    # ------------------------------------------------------------------
    @classmethod
    def desde_elementos(cls, elementos: Iterable[tuple[Any, float]]) -> "HeapMax":
        """Construye un heap en O(n) a partir de pares ``(dato, prioridad)``."""
        heap = cls()
        for dato, prioridad in elementos:
            heap._datos.append(_EntradaHeap(prioridad, heap._secuencia, dato))
            heap._secuencia += 1

        heap._monticulizar()
        return heap

    def _monticulizar(self) -> None:
        """Aplica hundir desde el último padre hasta la raíz: O(n)."""
        for indice in range(len(self._datos) // 2 - 1, -1, -1):
            self._hundir(indice)

    # ------------------------------------------------------------------
    # Helpers de índices y comparación
    # ------------------------------------------------------------------
    @staticmethod
    def _padre(indice: int) -> int:
        return (indice - 1) // 2

    @staticmethod
    def _izquierdo(indice: int) -> int:
        return 2 * indice + 1

    @staticmethod
    def _derecho(indice: int) -> int:
        return 2 * indice + 2

    def _mayor(self, a: _EntradaHeap, b: _EntradaHeap) -> bool:
        """Compara dos entradas; en empate gana la que llegó antes."""
        if a.prioridad != b.prioridad:
            return a.prioridad > b.prioridad
        return a.secuencia < b.secuencia

    def _intercambiar(self, i: int, j: int) -> None:
        self._datos[i], self._datos[j] = self._datos[j], self._datos[i]

    def _flotar(self, indice: int) -> None:
        while indice > 0:
            padre = self._padre(indice)
            if not self._mayor(self._datos[indice], self._datos[padre]):
                break
            self._intercambiar(indice, padre)
            indice = padre

    def _hundir(self, indice: int) -> None:
        n = len(self._datos)

        while True:
            mayor = indice
            izquierdo = self._izquierdo(indice)
            derecho = self._derecho(indice)

            if izquierdo < n and self._mayor(self._datos[izquierdo], self._datos[mayor]):
                mayor = izquierdo
            if derecho < n and self._mayor(self._datos[derecho], self._datos[mayor]):
                mayor = derecho

            if mayor == indice:
                break

            self._intercambiar(indice, mayor)
            indice = mayor
