import unicodedata
from models.pelicula import Pelicula


class Nodo_Arbol_avl:
    """Nodo individual de un Árbol Binario de Búsqueda que almacena una película."""

    def __init__(self, pelicula: Pelicula) -> None:
        self.pelicula: Pelicula = pelicula
        self.izquierdo: "Nodo_Arbol_avl | None" = None
        self.derecho: "Nodo_Arbol_avl | None" = None
        self.altura = 1


class Arbol_avl_Catalogo:
    """Estructura de Árbol Binario de Búsqueda (BST) para gestionar películas organizadas por título."""

    def __init__(self) -> None:
        self.raiz: Nodo_Arbol_avl | None = None

    def _normalizar(self, texto: str) -> str:
        """Remueve acentos/tildes y pasa el texto a minúsculas para comparaciones parejas."""
        if not texto:
            return ""
        texto_nfd = unicodedata.normalize("NFD", texto)
        return "".join(
            c for c in texto_nfd if unicodedata.category(c) != "Mn"
        ).lower()

  

# ==========================================
    # MÉTODO DE INSERCIÓN 
# ==========================================
    def insertar(self, nueva_pelicula: Pelicula) -> None:
                self.raiz = self._insertar_recursivo(self.raiz, nueva_pelicula)
    
    def _insertar_recursivo(self, raiz: "Nodo_Arbol_avl", nueva_pelicula: Pelicula):
        if raiz is None:
            return Nodo_Arbol_avl(nueva_pelicula)

        #Normaliza los titulos

        titulo_nuevo = self._normalizar(nueva_pelicula.titulo)
        titulo_actual = self._normalizar(raiz.pelicula.titulo)

        if titulo_nuevo < titulo_actual:
            raiz.izquierdo = self._insertar_recursivo(raiz.izquierdo, nueva_pelicula) 
        elif titulo_nuevo > titulo_actual:
            raiz.derecho = self._insertar_recursivo(raiz.derecho, nueva_pelicula)
        else:
            return raiz

        #modifiica altura

        raiz.altura = 1 + max(self._obtener_altura_nodo(raiz.izquierdo), self._obtener_altura_nodo(raiz.derecho))
        
        
        return self._balancear(raiz) 
        
    
    
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


# ==========================================
    #Recorridos (in/pre/pos order)
# ==========================================

    def inorder(self)-> list[Pelicula]:
        """Recorrido In-Order: Devuelve las películas ordenadas alfabéticamente."""
        return self._inorder_recursivo(self.raiz)
    
    def _inorder_recursivo(self, nodo: Nodo_Arbol_avl | None) -> list[Pelicula]:
        if not nodo:
            return []
        return self._inorder_recursivo(nodo.izquierdo) + [nodo.pelicula] + self._inorder_recursivo(nodo.derecho)
        

    def preorder (self)-> list[Pelicula]:
        '''Recorrido preorder: Raíz - izq - der'''
        return self._preorder_recursivo(self.raiz)

    def _preorder_recursivo(self, nodo:Nodo_Arbol_avl | None) -> list[Pelicula]:
        if not nodo:
            return []
        return [nodo.pelicula] + self._preorder_recursivo(nodo.izquierdo) + self._preorder_recursivo(nodo.derecho)

    def postorder(self) -> list[Pelicula]:
        '''Recorido postorder izq - der - raiz'''
        return self._postorder_recursivo(self.raiz)

    def _postorder_recursivo(self, nodo:Nodo_Arbol_avl | None)->list[Pelicula]:
        if not nodo:
            return []
        return self._postorder_recursivo(nodo.izquierdo) + self._postorder_recursivo(nodo.derecho) + [nodo.pelicula]

# ==========================================
# ALTURA DEL NODO / FACTOR DE EQUILIBRIO
# ==========================================
    def _obtener_altura_nodo(self, nodo: "Nodo_Arbol_avl"):
        if not nodo:
            return 0
        return nodo.altura
    
    def _obtener_balance(self, nodo: "Nodo_Arbol_avl"):
        if not nodo:
            return 0
        return self._obtener_altura_nodo(nodo.izquierdo) - self._obtener_altura_nodo(nodo.derecho)

    def obtener_altura(self):
        #Altura total del arbol
        return self._obtener_altura_nodo(self.raiz)
    
# ==========================================
    # ROTACIONES SIMPLE Y DOBLE
# ==========================================
    def _rotar_simple(self, raiz:"Nodo_Arbol_avl", control: bool):
        # Hace una rotación simple; control=True (Derecha), control=False (Izquierda)
        if control:
            # Rotación a la Derecha (Caso Izquierda-Izquierda)
            nueva_raiz = raiz.izquierdo
            libre = nueva_raiz.derecho

            raiz.izquierdo = libre
            nueva_raiz.derecho = raiz
        else:
            # Rotación a la Izquierda (Caso Derecha-Derecha)
            nueva_raiz = raiz.derecho 
            libre = nueva_raiz.izquierdo

            raiz.derecho = libre
            nueva_raiz.izquierdo = raiz

        # Actualiza alturas
        raiz.altura = 1 + max(self._obtener_altura_nodo(raiz.izquierdo), self._obtener_altura_nodo(raiz.derecho))
        nueva_raiz.altura = 1 + max(self._obtener_altura_nodo(nueva_raiz.izquierdo), self._obtener_altura_nodo(nueva_raiz.derecho))

        return nueva_raiz

    def _rotar_doble(self, raiz:"Nodo_Arbol_avl", control: bool):
        """Rotación doble. control=True (LR), control=False (RL)"""
        if control: 
            raiz.izquierdo = self._rotar_simple(raiz.izquierdo, False)
            return self._rotar_simple(raiz, True)
        else:
            raiz.derecho = self._rotar_simple(raiz.derecho, True)
            return self._rotar_simple(raiz, False)

# ==========================================
   # BALANCEAR
# ==========================================
    def _balancear(self, raiz:"Nodo_Arbol_avl"):
        if raiz is None:
            return None

        balance = self._obtener_balance(raiz)

        # Peso a la IZQUIERDA (Diferencia > 1)
        if balance > 1:
            if self._obtener_balance(raiz.izquierdo) >= 0:
                raiz = self._rotar_simple(raiz, True)
            else:
                raiz = self._rotar_doble(raiz, True)

        # Peso a la DERECHA (Diferencia < -1)    
        elif balance < -1:
            if self._obtener_balance(raiz.derecho) <= 0:
                raiz = self._rotar_simple(raiz, False)
            else:
                raiz = self._rotar_doble(raiz, False)

        return raiz