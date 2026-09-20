import unicodedata
from models.pelicula import Pelicula


class NodoArbol:
    """Nodo individual de un Árbol Binario de Búsqueda que almacena una película."""

    def __init__(self, pelicula: Pelicula) -> None:
        self.pelicula: Pelicula = pelicula
        self.izquierdo: NodoArbol | None = None
        self.derecho: NodoArbol | None = None


class ArbolCatalogo:
    """Estructura de Árbol Binario de Búsqueda (BST) para gestionar películas organizadas por título."""

    def __init__(self) -> None:
        self.raiz: NodoArbol | None = None

    def _normalizar(self, texto: str) -> str:
        """Remueve acentos/tildes y pasa el texto a minúsculas para comparaciones parejas."""
        if not texto:
            return ""
        texto_nfd = unicodedata.normalize("NFD", texto)
        return "".join(
            c for c in texto_nfd if unicodedata.category(c) != "Mn"
        ).lower()

    def insertar(self, pelicula: Pelicula) -> None:
        """Inserta una película en el árbol respetando el orden alfabético del título."""
        nuevo_nodo = NodoArbol(pelicula)
        if not self.raiz:
            self.raiz = nuevo_nodo
            return

        actual = self.raiz
        clave_nueva = self._normalizar(pelicula.titulo)

        while True:
            clave_actual = self._normalizar(actual.pelicula.titulo)

            # Si el título nuevo es menor alfabéticamente, va a la izquierda
            if clave_nueva < clave_actual:
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo_nodo
                    break
                actual = actual.izquierdo
            # Si es mayor o igual, va a la derecha
            else:
                if actual.derecho is None:
                    actual.derecho = nuevo_nodo
                    break
                actual = actual.derecho

    def buscar(self, titulo: str) -> Pelicula | None:
        """Busca una película en el árbol mediante Búsqueda Binaria O(log N)."""
        busqueda = self._normalizar(titulo)
        actual = self.raiz

        while actual:
            clave_actual = self._normalizar(actual.pelicula.titulo)

            # Si encontramos coincidencia exacta o parcial
            if busqueda == clave_actual or busqueda in clave_actual:
                return actual.pelicula
            elif busqueda < clave_actual:
                actual = actual.izquierdo
            else:
                actual = actual.derecho

        return None