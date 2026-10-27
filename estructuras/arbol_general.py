

class NodoArbolGeneral:
    def __init__(self, valor:str) -> None:

        self.valor = valor
        self.hijos: list['NodoArbolGeneral'] = []

    def agregar_hijo(self, nodo_hijo: 'NodoArbolGeneral')->None:
        self.hijos.append(nodo_hijo)

#============================================================================================

class ArbolGeneralCategorias:
    def __init__(self, raiz_valor: str = 'Películas')-> None:
        self.raiz = NodoArbolGeneral(raiz_valor)

    def buscar_nodo(self, valor_buscado:str, nodo_actual: NodoArbolGeneral | None = None ) -> NodoArbolGeneral | None:

        if nodo_actual is None:
            nodo_actual = self.raiz

        if nodo_actual.valor.lower() == valor_buscado.lower():
            return nodo_actual

        #buscamos y aplicamos recursion
        for hijo in nodo_actual.hijos:
            resultado = self.buscar_nodo(valor_buscado, hijo)
            if resultado:
                return resultado

        return None

    def insertar (self, valor_nuevo: str, valor_padre: str = "Peliculas")-> bool:
        #Insertar nuevo nodo como hijo del un padre específico
        padre= self.buscar_nodo(valor_padre)
        if padre:
            padre.agregar_hijo(NodoArbolGeneral(valor_nuevo))
            return True
        else:
            print(f"No se encontro la categoría {valor_padre}")
            return False

    def mostrar_jerarquia(self, nodo_actual: NodoArbolGeneral | None = None, nivel:int =0)-> None:
        #Recorrido pre-order para imprimir arbol en terminal
        if nodo_actual is None:
            nodo_actual = self.raiz
        # Formateo visual para la terminal
        sangria = "│   " * (nivel - 1) if nivel > 0 else ""
        rama = "├── " if nivel > 0 else ""
        print(f"{sangria}{rama}{nodo_actual.valor}")

        for hijo in nodo_actual.hijos:
            self.mostrar_jerarquia(hijo, nivel + 1)

if __name__ == "__main__":
    # Instanciamos el árbol (la raíz por defecto es "Películas")
    jerarquia = ArbolGeneralCategorias()

    # Insertamos las categorías principales
    jerarquia.insertar("Ciencia ficción", "Películas")
    jerarquia.insertar("Acción", "Películas")
    jerarquia.insertar("Comedia", "Películas")

    # Insertamos subcategorías dentro de Ciencia ficción
    jerarquia.insertar("Cyberpunk", "Ciencia ficción")
    jerarquia.insertar("Viajes temporales", "Ciencia ficción")
    jerarquia.insertar("Inteligencia artificial", "Ciencia ficción")
    
    # Insertamos subcategorías para Acción
    jerarquia.insertar("Artes Marciales", "Acción")
    jerarquia.insertar("Superhéroes", "Acción")

    print("\n JERARQUÍA DE CATEGORÍAS \n")
    jerarquia.mostrar_jerarquia()
        
