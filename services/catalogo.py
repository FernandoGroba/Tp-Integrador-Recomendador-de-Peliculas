import json 

from models.pelicula import Pelicula

class Catalogo:
    def __init__(self)-> None:
        self._elementos: list[Pelicula] = []


# ====== Carga Json ======
    def cargar_json(self, ruta: str)-> None:
        with open (ruta, encoding = 'utf-8') as archivo:
            data = json.load(archivo)
        for item in data:
            self._elementos.append(
                Pelicula(item['id'], item['titulo'], item['anio'], item['genero'], item['director'], item['actores'], item['rating'], item['sinopsis'],)
            )        

# ====== Búsqueda por titulo ======
#cuando buscaba una pelicula tenia que escribir el titulo entero, asi que lo cambie para que busque por coincidencia parcial y me de las peliculas dependiendo la palabra que pongas
    def buscar(self, titulo: str) -> list[Pelicula]:
        busqueda = titulo.lower()
        coincidencias = []
        for peli in self._elementos:
            if busqueda in peli.titulo.lower():
                coincidencias.append(peli)
        return coincidencias

# ====== Listar películas ======

    def listar(self) -> list[Pelicula]:
        return list(self._elementos)



# ====== Filtro por genero ======

    def filtrar_genero(self, genero:str)->list[Pelicula]:
        #tuve un problema con los acentos en los géneros y pensé esta solución poco elegante:
        busqueda = genero.lower()
        if busqueda == "fantasia":
            busqueda = "fantasía"
        elif busqueda == "animacion":
            busqueda = "animación"
        elif busqueda == "accion":
            busqueda = "acción"
        elif busqueda == "ficcion":
            busqueda = "ficción"
        elif busqueda == "biografia":
             busqueda = "biografía"

        return[
            pelicula for pelicula in self._elementos
            if busqueda  in pelicula.genero.lower()
        ]

# ====== Cantidaad de elementos ======
    
    def __len__(self) -> int:
        return len(self._elementos)





