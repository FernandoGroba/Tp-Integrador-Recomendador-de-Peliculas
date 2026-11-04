import unittest

from estructuras.grafo import Grafo, buscar_titulo_amplitud
from models.pelicula import Pelicula
from services.catalogo import Catalogo
from services.grafo_peliculas import GrafoPeliculas


class TestGrafoEstructura(unittest.TestCase):

    def setUp(self):
        self.grafo = Grafo(dirigido=False)
        for nombre in ["A", "B", "C", "D", "E"]:
            self.grafo.insertar_vertice(nombre)

        # A-B, A-C, B-D, C-D, D-E
        self.grafo.insertar_arista("A", "B", "conexión", 1)
        self.grafo.insertar_arista("A", "C", "conexión", 1)
        self.grafo.insertar_arista("B", "D", "conexión", 1)
        self.grafo.insertar_arista("C", "D", "conexión", 1)
        self.grafo.insertar_arista("D", "E", "conexión", 1)

    def test_insertar_vertice_no_duplica(self):
        self.grafo.insertar_vertice("A")

        self.assertEqual(len(self.grafo), 5)

    def test_arista_es_no_dirigida(self):
        self.assertTrue(self.grafo.buscar_vertice("A"))
        self.assertEqual(len(self.grafo.adyacentes("A")), 2)
        self.assertEqual(len(self.grafo.adyacentes("B")), 2)
        self.assertEqual(len(self.grafo.adyacentes("E")), 1)

    def test_insertar_arista_con_vertice_inexistente_falla(self):
        self.assertFalse(self.grafo.insertar_arista("A", "Z"))

    def test_bfs_recorre_por_niveles(self):
        self.assertEqual(self.grafo.bfs("A"), ["A", "B", "C", "D", "E"])

    def test_dfs_recorre_en_profundidad(self):
        self.assertEqual(self.grafo.dfs("A"), ["A", "B", "D", "C", "E"])

    def test_camino_mas_corto_usa_bfs(self):
        camino = self.grafo.camino_mas_corto("A", "E")

        self.assertEqual(len(camino), 4)
        self.assertEqual(camino[0], "A")
        self.assertEqual(camino[-1], "E")
        self.assertIn("D", camino)

    def test_camino_inexistente_devuelve_none(self):
        self.grafo.insertar_vertice("Aislado")

        self.assertIsNone(self.grafo.camino_mas_corto("A", "Aislado"))

    def test_buscar_titulo_amplitud(self):
        pelicula = Pelicula(1, "Matrix", 1999, "Ciencia Ficción", "Wachowski", "Keanu Reeves", 5.0, "")
        grafo = Grafo()
        grafo.insertar_vertice(pelicula)

        encontrado = buscar_titulo_amplitud(grafo, "matrix")

        self.assertIsNotNone(encontrado)
        self.assertIs(encontrado.info, pelicula)


class TestGrafoPeliculas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.catalogo = Catalogo()
        cls.catalogo.cargar_json("data/data.json")
        cls.grafo = GrafoPeliculas(cls.catalogo.listar())

    def _pelicula(self, titulo):
        pelicula = self.grafo.buscar(titulo)
        self.assertIsNotNone(pelicula, f"No se encontró {titulo}")
        return pelicula

    def test_todos_los_vertices_estan_cargados(self):
        self.assertEqual(len(self.grafo), len(self.catalogo.listar()))

    def test_peliculas_del_mismo_director_se_relacionan(self):
        padrino = self._pelicula("El Padrino")
        parte_ii = self._pelicula("El Padrino: Parte II")

        relaciones = self.grafo.relacionadas(padrino, limite=30)
        titulos = [relacion[0].titulo for relacion in relaciones]

        self.assertIn(parte_ii.titulo, titulos)

    def test_relacionadas_ordena_por_afinidad_y_rating(self):
        matrix = self._pelicula("Matrix")
        relaciones = self.grafo.relacionadas(matrix, limite=5)

        self.assertGreater(len(relaciones), 0)
        claves = [(-peso, -pelicula.rating) for pelicula, _motivo, peso in relaciones]
        self.assertEqual(claves, sorted(claves))

    def test_relacionadas_incluye_motivo(self):
        matrix = self._pelicula("Matrix")
        relaciones = self.grafo.relacionadas(matrix, limite=1)

        self.assertIn("común", relaciones[0][1].lower())

    def test_pelicula_aislada_no_tiene_relaciones(self):
        aislada = self._pelicula("El Bueno, el Malo y el Feo")

        self.assertEqual(self.grafo.grado(aislada), 0)
        self.assertEqual(self.grafo.relacionadas(aislada), [])

    def test_camino_entre_peliculas_conectadas(self):
        matrix = self._pelicula("Matrix")
        oppenheimer = self._pelicula("Oppenheimer")

        camino = self.grafo.camino(matrix, oppenheimer)

        self.assertIsNotNone(camino)
        self.assertIs(camino[0], matrix)
        self.assertIs(camino[-1], oppenheimer)

    def test_camino_a_pelicula_aislada_es_none(self):
        matrix = self._pelicula("Matrix")
        aislada = self._pelicula("El Bueno, el Malo y el Feo")

        self.assertIsNone(self.grafo.camino(matrix, aislada))

    def test_bfs_y_dfs_alcanzan_las_mismas_peliculas(self):
        matrix = self._pelicula("Matrix")
        amplitud = self.grafo.recorrido_amplitud(matrix)
        profundidad = self.grafo.explorar(matrix)

        self.assertEqual(len(amplitud), len(profundidad))
        self.assertEqual(
            {pelicula.id_peli for pelicula in amplitud},
            {pelicula.id_peli for pelicula in profundidad},
        )


if __name__ == "__main__":
    unittest.main()
