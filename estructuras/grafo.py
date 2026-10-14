# ==========================================
# TDA COLA (Estructura de control FIFO)
# =========================================

class NodoColaVertice():
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ColaVertice():
    def __init__(self):
        self.frente = None
        self.final = None

    def esta_vacia(self):
        return self.frente is None

    def encolar(self, dato):
        nuevo_visitado = NodoColaVertice(dato)
        if self.esta_vacia():
            self.frente = nuevo_visitado
            self.final = nuevo_visitado
        else:
            if self.final is not None:
                self.final.siguiente = nuevo_visitado
            self.final= nuevo_visitado

    def desencolar(self):
        if self.esta_vacia():
            return None 
        dato_extrido = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None

        return dato_extrido
# ==========================================
# CLASES DE ESTRUCTURA DEL GRAFO
# ==========================================

class NodoArista:
    def __init__(self, info, destino):
        self.info = info
        self.destino = destino
        self.sig = None

class Arista():
    def __init__(self):
        self.inicio = None
        self.tamaño = 0

class NodoVertice():
    def __init__(self, info):
        self.info = info
        self.sig = None
        self.visitado = False
        self.adyacentes = Arista()

class Grafo():
    def __init__(self, dirigido=True):
        self.inicio = None
        self.dirigido = dirigido
        self.tamanio = 0

# ==========================================
# FUNCIÓN DE BÚSQUEDA POR AMPLITUD (BFS)
# ==========================================
def buscar_titulo_amplitud(grafo, titulo_buscado):
    if grafo.inicio is None:
        return None

    
    cola = ColaVertice()
    nodo_inicial = grafo.inicio 
    nodo_inicial.visitado = True
    cola.encolar(nodo_inicial)

    while not cola.esta_vacia():
        actual = cola.desencolar()
        if actual.info.titulo == titulo_buscado:
            return actual

        aux_arista = actual.adyacentes.inicio
        while aux_arista is not None:
            vertice_destino = aux_arista.destino
            if not vertice_destino.visitado:
                vertice_destino.visitado = True
                cola.encolar(vertice_destino)
            aux_arista = aux_arista.sig 

    return None





