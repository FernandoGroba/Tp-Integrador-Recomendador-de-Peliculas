class Pelicula:
    def __init__(self, id_peli, titulo, anio, genero, director, actores, rating, sinopsis):
        self._id_peli = id_peli
        self._titulo = titulo
        self._anio = anio
        self._genero = genero
        self._director = director
        self._actores = actores
        self._rating = float(rating)
        self._sinopsis = sinopsis

    @property
    def id_peli(self):
        return self.id_peli

    @property
    def titulo(self):
        return self._titulo

    @property
    def anio(self):
        return self._anio

    
    @property
    def genero(self):
        return self._genero

    @property
    def director(self):
        return self._director

    @property
    def actores(self):
        return self._actores

    @property
    def rating(self):
        return self._rating

    @property
    def sinopsis(self):
        return self._sinopsis


    def __repr__(self):
        return self._titulo + "(" + self._genero + ") ⭐ " + str(self._rating)

