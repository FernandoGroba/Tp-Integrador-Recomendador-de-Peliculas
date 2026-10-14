import unicodedata
from models.pelicula import Pelicula


class NodoArbol:
    """Nodo individual de un Árbol Binario de Búsqueda que almacena una película."""

    def __init__(self, pelicula: Pelicula) -> None:
        self.pelicula: Pelicula = pelicula
        self.izquierdo: "NodoArbol | None" = None
        self.derecho: "NodoArbol | None" = None


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

    def buscar_exacto(self, titulo: str) -> Pelicula | None:
        """Busca una película en el árbol mediante Búsqueda Binaria O(log N)."""
        busqueda = self._normalizar(titulo)
        actual = self.raiz

        while actual:
            clave_actual = self._normalizar(actual.pelicula.titulo)

            # Si encontramos coincidencia exacta 
            if busqueda == clave_actual:
                return actual.pelicula
            elif busqueda < clave_actual:
                actual = actual.izquierdo
            else:
                actual = actual.derecho

        return None
# ====== Recorridos (in/pre/pos order) ======

    def inorder(self)-> list[Pelicula]:
        """Recorrido In-Order: Devuelve las películas ordenadas alfabéticamente."""
        return self._inorder_recursivo(self.raiz)
    
    def _inorder_recursivo(self, nodo: NodoArbol | None) -> list[Pelicula]:
        if not nodo:
            return []
        return self._inorder_recursivo(nodo.izquierdo) + [nodo.pelicula] + self._inorder_recursivo(nodo.derecho)
        

    def preorder (self)-> list[Pelicula]:
        '''Recorrido preorder: Raíz - izq - der'''
        return self._preorder_recursivo(self.raiz)

    def _preorder_recursivo(self, nodo:NodoArbol | None) -> list[Pelicula]:
        if not nodo:
            return []
        return [nodo.pelicula] + self._preorder_recursivo(nodo.izquierdo) + self._preorder_recursivo(nodo.derecho)

    def postorder(self) -> list[Pelicula]:
        '''Recorido postorder izq - der - raiz'''
        return self._postorder_recursivo(self.raiz)

    def _postorder_recursivo(self, nodo:NodoArbol | None)->list[Pelicula]:
        if not nodo:
            return []
        return self._postorder_recursivo(nodo.izquierdo) + self._postorder_recursivo(nodo.derecho) + [nodo.pelicula]

    # ==========================================
    # MÉTODO DE ALTURA (Para el test de desbalanceo)
    # ==========================================
    def obtener_altura(self):
        return self._altura_recursiva(self.raiz)

    def _altura_recursiva(self, nodo):
        if nodo is None:
            return 0
        
        # OJO: Si tu árbol viejo usaba .izq y .der en vez de .izquierdo y .derecho, cambialo acá abajo:
        altura_izq = self._altura_recursiva(nodo.izquierdo)
        altura_der = self._altura_recursiva(nodo.derecho)
        
        return 1 + max(altura_izq, altura_der)