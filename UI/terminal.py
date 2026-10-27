from services.catalogo import Catalogo
from estructuras.arbol_general import ArbolGeneralCategorias  # <-- IMPORTAMOS TU NUEVO ÁRBOL

class Terminal:
    def __init__(self, catalogo: Catalogo) -> None:
        self._catalogo = catalogo
        # Construimos el árbol automáticamente al iniciar la terminal
        self._arbol_categorias = self._construir_arbol()

    def _construir_arbol(self) -> ArbolGeneralCategorias:
        """Helper interno para armar la jerarquía de categorías usando el catálogo."""
        jerarquia = ArbolGeneralCategorias("Cine")
        jerarquia.insertar("Géneros", "Cine")
        
        generos_unicos = set()
        # Recorremos los objetos película que ya maneja tu catálogo
        for peli in self._catalogo.listar():
            # Separamos géneros múltiples y evitamos vacíos
            generos_separados = [g.strip() for g in peli.genero.split(",")]
            for g in generos_separados:
                if g:
                    generos_unicos.add(g)
                    
        # Insertamos alfabéticamente en el árbol general
        for genero in sorted(generos_unicos):
            jerarquia.insertar(genero, "Géneros")
            
        return jerarquia

    def iniciar(self) -> None:
        while True:
            self._mostrar_menu()
            opcion = input("Opcion: ").strip()
            if opcion == "1":
                self._buscar()
            elif opcion == "2":
                self._listar()
            elif opcion == "3":
                self._filtrar()
            elif opcion == "4":                   # <-- NUEVA OPCIÓN
                self._explorar_categorias()       
            elif opcion == "0":
                print("Gracias por su consulta")
                break
            else:
                print("Esa opción no es válida")
            print()

    def _mostrar_menu(self) -> None:
        print("\n" + "=" * 40)
        print("BIENVENIDOS A CINEMATCH")
        print("=" * 40)
        print("1 - Buscar película por título")
        print("2 - Listar todas las películas")
        print("3 - Filtrar por género")
        print("4 - Explorar categorías (Árbol)") # <-- NUEVO TEXTO EN EL MENÚ
        print("0 - Salir")
        print("-" * 40)

    def _buscar(self) -> None:
        titulo = input("Buscar por titulo: ").strip()
        resultados = self._catalogo.buscar(titulo)
        if resultados:
            for pelicula in resultados:
                print(f"Encontrada: {pelicula}")
        else:
            print(f"No se encontraron peliculas que contengan '{titulo}'")

    def _listar(self) -> None:
        for pelicula in self._catalogo.listar():
            print(f" - {pelicula}")

    def _filtrar(self) -> None:
        genero = input("Categoria: ").strip()
        resultados = self._catalogo.filtrar_genero(genero)
        if resultados:
            for pelicula in resultados:
                print(f"- {pelicula}")
        else:
            print(f"No hay elementos en {genero}")

    
    def _explorar_categorias(self) -> None:
        print("\n--- 🌲 EXPLORADOR DE CATEGORÍAS 🌲 ---")
        # 1. Dibujamos el árbol general
        self._arbol_categorias.mostrar_jerarquia()
        
        # 2. Le damos interactividad
        cat_elegida = input("\nEscriba un género de la lista para ver sus películas (o presione Enter para volver): ").strip()
        
        if cat_elegida:
            # 3. Validamos usando la búsqueda profunda (DFS) del TP05
            nodo_encontrado = self._arbol_categorias.buscar_nodo(cat_elegida)
            
            if nodo_encontrado:
                print(f"\n🎬 Películas en la categoría '{nodo_encontrado.valor}':")
                # 4. Reutilizamos la lógica genial que ya tenías en _filtrar()
                resultados = self._catalogo.filtrar_genero(nodo_encontrado.valor)
                if resultados:
                    for pelicula in resultados:
                        print(f"- {pelicula}")
                else:
                    print("No hay películas cargadas para esta categoría.")
            else:
                print("❌ Categoría no encontrada en el árbol. Respete los nombres mostrados.")