import unittest

from estructuras.heap import HeapMax
from services.catalogo import Catalogo
from services.ranking import RankingPeliculas


class TestHeapMax(unittest.TestCase):

    def test_extrae_en_orden_de_prioridad(self):
        heap = HeapMax()
        for prioridad, dato in [(3, "c"), (5, "a"), (1, "b"), (4, "d")]:
            heap.insertar(dato, prioridad)

        resultado = [heap.extraer_max() for _ in range(4)]
        self.assertEqual(resultado, ["a", "d", "c", "b"])

    def test_ver_max_no_extrae(self):
        heap = HeapMax()
        heap.insertar("a", 5)
        heap.insertar("b", 3)

        self.assertEqual(heap.ver_max(), "a")
        self.assertEqual(len(heap), 2)
        self.assertEqual(heap.extraer_max(), "a")
        self.assertEqual(heap.ver_max(), "b")

    def test_empate_respeta_orden_de_llegada(self):
        heap = HeapMax()
        heap.insertar("primero", 5)
        heap.insertar("segundo", 5)
        heap.insertar("tercero", 5)

        self.assertEqual(heap.top_n(3), ["primero", "segundo", "tercero"])

    def test_top_n_no_modifica_el_heap(self):
        heap = HeapMax.desde_elementos([("a", 5), ("b", 3), ("c", 4)])

        self.assertEqual(heap.top_n(2), ["a", "c"])
        self.assertEqual(len(heap), 3)
        self.assertEqual(heap.extraer_max(), "a")

    def test_top_n_con_limites(self):
        heap = HeapMax.desde_elementos([("a", 1), ("b", 2)])

        self.assertEqual(heap.top_n(0), [])
        self.assertEqual(heap.top_n(10), ["b", "a"])

    def test_heap_vacio(self):
        heap = HeapMax()

        self.assertTrue(heap.esta_vacia())
        self.assertIsNone(heap.ver_max())
        self.assertIsNone(heap.extraer_max())
        self.assertEqual(heap.top_n(10), [])

    def test_desde_elementos_monticuliza(self):
        heap = HeapMax.desde_elementos(
            [("a", 1), ("b", 5), ("c", 3), ("d", 4), ("e", 2)]
        )

        self.assertEqual(heap.top_n(5), ["b", "d", "c", "e", "a"])


class TestRankingPeliculas(unittest.TestCase):

    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_json("data/data.json")
        self.ranking = RankingPeliculas(self.catalogo.listar())

    def test_top_10_tiene_diez_y_esta_ordenado(self):
        top = self.ranking.top(10)

        self.assertEqual(len(top), 10)
        ratings = [pelicula.rating for pelicula in top]
        self.assertEqual(ratings, sorted(ratings, reverse=True))

    def test_top_10_coincide_con_ordenamiento_estable(self):
        esperado = sorted(self.catalogo.listar(), key=lambda p: -p.rating)[:10]
        obtenido = self.ranking.top(10)

        self.assertEqual(
            [pelicula.id_peli for pelicula in obtenido],
            [pelicula.id_peli for pelicula in esperado],
        )

    def test_mejor_es_el_maximo(self):
        max_rating = max(pelicula.rating for pelicula in self.catalogo.listar())

        self.assertEqual(self.ranking.mejor().rating, max_rating)

    def test_top_no_vacia_el_ranking(self):
        self.ranking.top(3)

        self.assertEqual(len(self.ranking), len(self.catalogo.listar()))


if __name__ == "__main__":
    unittest.main()
