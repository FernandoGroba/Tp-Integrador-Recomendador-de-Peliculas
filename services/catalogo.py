import json
import unicodedata

from models.pelicula import Pelicula

class Catalogo:
    def __init__(self)-> None:
        self._elementos: list[Pelicula] = []

# ====== Normalizador general ======
    def _normalizar(self, texto: str) -> str:
        """Remueve acentos/tildes y pasa todo el texto a minúsculas."""
        if not texto:
            return ""
        texto_nfd = unicodedata.normalize("NFD", texto)
        return "".join(
            c for c in texto_nfd if unicodedata.category(c) != "Mn"
        ).lower()

# ====== Carga Json ======
    def cargar_json(self, ruta: str)-> None:
        with open (ruta, encoding = 'utf-8') as archivo:
            data = json.load(archivo)
        for item in data:
            self._elementos.append(
                Pelicula(item['id'], item['titulo'], item['anio'], item['genero'], item['director'], item['actores'], item['rating'], item['sinopsis'],)
            )        

# ====== Búsqueda por titulo ======
    def buscar(self, titulo: str) -> list[Pelicula]:
            """Devuelve una lista con las películas que contengan la palabra buscada."""
            busqueda = self._normalizar(titulo)
            return [
                p for p in self._elementos if busqueda in self._normalizar(p.titulo)
            ]

# ====== Listar películas ======

    def listar(self) -> list[Pelicula]:
        return list(self._elementos)



# ====== Filtro por genero ======
    def filtrar_genero(self, genero: str) -> list[Pelicula]:
            busqueda = self._normalizar(genero)
            return [
                pelicula
                for pelicula in self._elementos
                if busqueda in self._normalizar(pelicula.genero)
            ]

# ====== Cantidaad de elementos ======
    
    def __len__(self) -> int:
        return len(self._elementos)





