from models.pelicula import Pelicula
from services.catalogo import Catalogo
from services.grafo_peliculas import GrafoPeliculas
from services.ranking import RankingPeliculas
from services.arbol_catalogo import ArbolCatalogo
from estructuras.arbol_general import ArbolGeneralCategorias  # <-- IMPORTAMOS TU NUEVO ÁRBOL

class Terminal:
    def __init__(self, catalogo: Catalogo) -> None:
        self._catalogo = catalogo
        # Construimos el árbol automáticamente al iniciar la terminal
        self._arbol_categorias = self._construir_arbol()
        # BST por título (TP3): se arma una sola vez insertando cada película
        self._arbol_titulos = ArbolCatalogo()
        for pelicula in self._catalogo.listar():
            self._arbol_titulos.insertar(pelicula)
        # El ranking se construye una sola vez con una heap por rating (TP6)
        self._ranking = RankingPeliculas(self._catalogo.listar())
        # El grafo de relaciones se arma una sola vez al iniciar (TP7)
        self._grafo_pelis = GrafoPeliculas(self._catalogo.listar())

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
            elif opcion == "4":                   
                self._explorar_categorias()
            elif opcion == "5":
                self._mostrar_top()
            elif opcion == "6":
                self._ver_relacionadas()
            elif opcion == "7":
                self._buscar_camino()
            elif opcion == "8":
                self._explorar_red()
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
        print("4 - Explorar categorías") 
        print("5 - Ver Top 10 (Heap)")
        print("6 - Ver películas relacionadas ")
        print("7 - Buscar camino entre películas ")
        print("8 - Explorar la red (BFS / DFS)")
        print("0 - Salir")
        print("-" * 40)

    def _buscar_titulo(self, titulo: str) -> list[Pelicula]:
        """Coincidencia exacta en el BST (O(log n)) y el resto por 'contiene'.

        La película exacta, si existe, va primero; después se suman las demás
        coincidencias parciales (por ejemplo, otras partes de una saga) sin repetir.
        """
        resultados: list[Pelicula] = []
        exacta = self._arbol_titulos.buscar_exacto(titulo)
        if exacta is not None:
            resultados.append(exacta)

        for pelicula in self._catalogo.buscar(titulo):
            if pelicula is not exacta:
                resultados.append(pelicula)
        return resultados

    def _buscar(self) -> None:
        titulo = input("Buscar por titulo: ").strip()
        resultados = self._buscar_titulo(titulo)
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

    def _mostrar_top(self) -> None:
        """Muestra el Top 10 usando el ranking con heap (TP6)."""
        print("\n--- 🏆 TOP 10 MEJOR RANKEADAS ---")

        mejores = self._ranking.top(10)
        if not mejores:
            print("No hay películas cargadas para armar el ranking.")
            return

        medallas = {1: "🥇", 2: "🥈", 3: "🥉"}
        for posicion, pelicula in enumerate(mejores, start=1):
            marca = medallas.get(posicion, f"{posicion:>2}.")
            print(f"{marca} {pelicula.titulo} — ⭐ {pelicula.rating:.1f} ({pelicula.anio})")

        print("\n(El ranking se obtuvo con una cola de prioridades implementada como max-heap.)")

    def _elegir_pelicula(self, etiqueta: str = "Título") -> Pelicula | None:
        """Pide un título y resuelve la película, ofreciendo opciones si hay varias."""
        consulta = input(f"{etiqueta}: ").strip()
        if not consulta:
            return None

        exacta = self._grafo_pelis.buscar(consulta)
        if exacta is not None:
            return exacta

        resultados = self._catalogo.buscar(consulta)
        if not resultados:
            print(f"No se encontraron películas que contengan '{consulta}'.")
            return None
        if len(resultados) == 1:
            return resultados[0]

        print("Se encontraron varias películas:")
        for indice, pelicula in enumerate(resultados, start=1):
            print(f"  {indice}. {pelicula.titulo} ({pelicula.anio})")

        eleccion = input("Número (Enter para cancelar): ").strip()
        if not eleccion.isdigit():
            return None

        indice = int(eleccion)
        if 1 <= indice <= len(resultados):
            return resultados[indice - 1]

        print("Número inválido.")
        return None

    def _ver_relacionadas(self) -> None:
        """Muestra los vecinos del grafo con el motivo de cada relación (TP7)."""
        print("\n--- 🕸️ PELÍCULAS RELACIONADAS ---")
        pelicula = self._elegir_pelicula()
        if pelicula is None:
            return

        relaciones = self._grafo_pelis.relacionadas(pelicula, limite=5)
        print(f"\nSi te gustó «{pelicula.titulo}», quizás te interesen:")

        if not relaciones:
            print("  (Esta película no tiene relaciones cargadas en el grafo.)")
            return

        for posicion, (relacionada, motivo, _peso) in enumerate(relaciones, start=1):
            print(
                f"  {posicion}. {relacionada.titulo} — "
                f"⭐ {relacionada.rating:.1f} ({relacionada.anio})"
            )
            print(f"     ↳ {motivo}")

        print(
            f"\n(«{pelicula.titulo}» tiene "
            f"{self._grafo_pelis.grado(pelicula)} relaciones en el grafo.)"
        )

    def _buscar_camino(self) -> None:
        """Encuentra el camino con menos aristas entre dos películas (BFS)."""
        print("\n--- 🧭 CAMINO MÁS CORTO ENTRE PELÍCULAS (BFS) ---")
        origen = self._elegir_pelicula("Película de origen")
        if origen is None:
            return

        destino = self._elegir_pelicula("Película de destino")
        if destino is None:
            return

        if origen is destino:
            print("El origen y el destino son la misma película.")
            return

        camino = self._grafo_pelis.camino(origen, destino)
        if not camino:
            print(
                f"\nNo hay un camino de relaciones entre "
                f"«{origen.titulo}» y «{destino.titulo}»."
            )
            return

        print(f"\nCamino encontrado ({len(camino) - 1} saltos):")
        print("  " + " → ".join(pelicula.titulo for pelicula in camino))

    def _explorar_red(self) -> None:
        """Muestra BFS y DFS desde una película para comparar los recorridos (TP8)."""
        print("\n--- 🌐 EXPLORAR LA RED (BFS / DFS) ---")
        pelicula = self._elegir_pelicula("Película de inicio")
        if pelicula is None:
            return

        amplitud = self._grafo_pelis.recorrido_amplitud(pelicula)
        profundidad = self._grafo_pelis.explorar(pelicula)

        print(f"\nBFS (por niveles) — {len(amplitud)} películas alcanzables:")
        print("  " + " → ".join(p.titulo for p in amplitud))

        print(f"\nDFS (en profundidad) — {len(profundidad)} películas alcanzables:")
        print("  " + " → ".join(p.titulo for p in profundidad))

        print(
            "\n(Ambos recorren las mismas películas; cambia el orden de visita. "
            "BFS sirve para la relación más cercana y DFS para explorar una rama completa.)"
        )