import sys
import os
import json

# Soluciona las rutas para poder importar desde otras carpetas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 1. Importamos TU estructura y TU modelo real
from estructuras.grafo import Grafo, NodoVertice, NodoArista, buscar_titulo_amplitud
from models.pelicula import Pelicula

# 2. Instanciamos el grafo
mi_grafo = Grafo()

# 3. Creamos las películas usando tu clase real
# (Ajustá los parámetros si tu clase Pelicula recibe otras cosas)
# 3. Creamos las películas con TODOS los parámetros obligatorios
peli1 = Pelicula(
    id_peli=1, 
    titulo="El Padrino", 
    anio=1972, 
    genero="Crimen", 
    director="Coppola", 
    actores="Marlon Brando", 
    rating=9.2, 
    sinopsis="Mafia"
)
peli2 = Pelicula(
    id_peli=2, 
    titulo="Scarface", 
    anio=1983, 
    genero="Crimen", 
    director="De Palma", 
    actores="Al Pacino", 
    rating=8.3, 
    sinopsis="Drogas en Miami"
)
peli3 = Pelicula(
    id_peli=3, 
    titulo="Goodfellas", 
    anio=1990, 
    genero="Crimen", 
    director="Scorsese", 
    actores="Robert De Niro", 
    rating=8.7, 
    sinopsis="Mafia en NY"
)

# 4. Metemos tus objetos Pelicula reales adentro de los vértices
v1 = NodoVertice(peli1)
v2 = NodoVertice(peli2)
v3 = NodoVertice(peli3)

# 5. Armamos la red
mi_grafo.inicio = v1
v1.sig = v2
v2.sig = v3

conexion_1 = NodoArista("Mismo género", v2)
conexion_2 = NodoArista("Mismo género", v3)

v1.adyacentes.inicio = conexion_1
conexion_1.sig = conexion_2

# 6. Ejecutamos la búsqueda
print("=======================================")
print("Iniciando prueba con la clase Pelicula real...")
print("=======================================")

resultado = buscar_titulo_amplitud(mi_grafo, "Goodfellas")

if resultado is not None:
    # ATENCIÓN: Si te da un error de "AttributeError" acá, cambiá .titulo por ._titulo y .director por ._director
    print(f"✅ Éxito: Encontrada -> {resultado.info._titulo} (Dir: {resultado.info._director})")
else:
    print("❌ Fallo: No se encontró la película.")