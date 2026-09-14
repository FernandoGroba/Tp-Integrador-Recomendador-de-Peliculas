from services.catalogo import Catalogo

class Terminal:
    def __init__(self, catalogo:Catalogo)->None:
        self._catalogo = catalogo

  

    def iniciar(self)->None:
        while True:
            self._mostrar_menu()
            opcion = input("Opcion: ").strip()
            if opcion == "1":
                self._buscar()
            elif opcion == "2":
                self._listar()
            elif opcion == "3":
                self._filtrar()
            elif opcion == "0":
                print ("Gracias por su consulta")
                break
            else:
                print("esa opción no es valida")
            print()

    def _mostrar_menu(self)->None:
        print("\n" + "=" * 40)
        print("BIENVENIDOS A CINEMATCH")
        print("=" * 40)
        print("1 - Buscar película por título")
        print("2 - Listar todas las películas")
        print("3 - Filtrar por género ")
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

    def _listar(self)->None:
        for pelicula in self._catalogo.listar():
            print(f" - {pelicula}")

    def _filtrar(self)->None:
        genero = input("Categoria: ").strip()
        resultados = self._catalogo.filtrar_genero(genero)
        if resultados:
            for pelicula in resultados:
                print(f"- {pelicula}")
        else:
            print(f"No hay elementos en {genero}")

    
