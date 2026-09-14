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

if __name__ == "__main__":
    unittest.main()