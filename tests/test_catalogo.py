import unittest
from services.catalogo import Catalogo

class TestCatalogo(unittest.TestCase):

    def setUp(self): 
        self.catalogo = Catalogo()
        self.catalogo.cargar_json("data/data.json")

    def test_buscar_por_titulo(self):
        resultado = self.catalogo.buscar("El señor de los anillos")
        self.assertTrue(len(resultado)>0)
        self.assertEqual(resultado[0].titulo, "El Señor de los Anillos: El Retorno del Rey")

    def test_buscar_devuelve_lista_vacia_si_no_existe(self):
        resultados= self.catalogo.buscar("no-existe")
        self.assertEqual(resultados, [])        

  
      

    def test_listar_devuelve_todos(self):
        self.assertTrue(len(self.catalogo.listar())> 0)

    def test_filtrar_por_genero(self):
        resultados = self.catalogo.filtrar_genero("fantasía")

        self.assertTrue (all("fantasía" in pelicula.genero.lower() for pelicula in resultados ))

class TestBusquedaConArbol(unittest.TestCase):
    """La opción 1 de la terminal: exacta en el BST más 'contiene' sin repetir."""

    def setUp(self):
        from UI.terminal import Terminal
        catalogo = Catalogo()
        catalogo.cargar_json("data/data.json")
        self.terminal = Terminal(catalogo)

    def test_exacta_va_primero_y_suma_la_saga(self):
        resultados = self.terminal._buscar_titulo("el padrino")
        self.assertEqual(
            [p.titulo for p in resultados],
            ["El Padrino", "El Padrino: Parte II"],
        )

    def test_parcial_sin_exacta_usa_contiene(self):
        resultados = self.terminal._buscar_titulo("padrino")
        self.assertEqual(len(resultados), 2)

    def test_exacta_unica_no_se_repite(self):
        resultados = self.terminal._buscar_titulo("matrix")
        self.assertEqual([p.titulo for p in resultados], ["Matrix"])

    def test_sin_resultados(self):
        self.assertEqual(self.terminal._buscar_titulo("no-existe"), [])

    def test_arbol_contiene_todo_el_catalogo(self):
        self.assertEqual(
            len(self.terminal._arbol_titulos.inorder()),
            len(self.terminal._catalogo),
        )


if __name__ == "__main__":
    unittest.main()