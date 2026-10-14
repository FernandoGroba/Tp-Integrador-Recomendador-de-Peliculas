import sys
import os
import json
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.pelicula import Pelicula
from estructuras.arbol_avl import Arbol_avl_Catalogo
from services.arbol_catalogo import ArbolCatalogo

def ejecutar_experimento():
    print("=== INICIANDO EXPERIMENTO DE DESBALANCEO (TP04) ===\n")

    ruta_json = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.json')
    try:
        with open(ruta_json, 'r', encoding='utf-8') as archivo:
            datos_json = json.load(archivo)
    except FileNotFoundError:
        return

    peliculas_sin_ordenar = []
    for item in datos_json:
        nueva_peli = Pelicula(
            id_peli=item.get("id", 1),
            titulo=item.get("title", item.get("titulo", "Sin título")),
            anio=item.get("year", item.get("anio", 0)),
            genero=item.get("genre", item.get("genero", "Desconocido")),
            director=item.get("director", "Desconocido"),
            actores=item.get("actors", item.get("actores", "Desconocido")),
            rating=float(item.get("rating", 0.0)),
            sinopsis=item.get("synopsis", item.get("sinopsis", "Sin sinopsis"))
        )
        peliculas_sin_ordenar.append(nueva_peli)

    # Ordenamos TODO el catálogo para potenciar el desbalanceo
    peliculas_ordenadas = sorted(peliculas_sin_ordenar, key=lambda p: p.titulo)
    
    # Elegimos la ÚLTIMA película como nuestro "Peor Caso" de búsqueda
    ultima_pelicula = peliculas_ordenadas[-1].titulo

    print(f"Se insertarán {len(peliculas_ordenadas)} películas en ESTRICTO ORDEN ALFABÉTICO.")
    print(f"Objetivo de búsqueda (Peor caso): '{ultima_pelicula}'\n")

    # ==========================================
    # CASO A: EL ÁRBOL ENFERMO (TP3 - BST Común)
    # ==========================================
    bst_comun = ArbolCatalogo()
    
    # Inserción
    for p in peliculas_ordenadas:
        bst_comun.insertar(p)
    altura_bst = bst_comun.obtener_altura() 

    # Búsqueda (Medimos el O(n))
    inicio_bst_busqueda = time.perf_counter()
    bst_comun.buscar_exacto(ultima_pelicula)
    fin_bst_busqueda = time.perf_counter()
    tiempo_busq_bst = (fin_bst_busqueda - inicio_bst_busqueda) * 1000000 # En microsegundos
    
    print("--- RESULTADOS ÁRBOL BINARIO VIEJO (BST) ---")
    print(f"⚠️ Altura final: {altura_bst}")
    print(f"⏱️ Tiempo de BÚSQUEDA (Peor caso): {tiempo_busq_bst:.2f} microsegundos")
    print("--------------------------------------------\n")


    # ==========================================
    # CASO B: EL ÁRBOL SANO (TP4 - AVL)
    # ==========================================
    avl = Arbol_avl_Catalogo()
    
    # Inserción
    for p in peliculas_ordenadas:
        avl.insertar(p)
    altura_avl = avl.obtener_altura()
    
    # Búsqueda (Medimos el O(log n))
    inicio_avl_busqueda = time.perf_counter()
    avl.buscar_exacto(ultima_pelicula)
    fin_avl_busqueda = time.perf_counter()
    tiempo_busq_avl = (fin_avl_busqueda - inicio_avl_busqueda) * 1000000 # En microsegundos
    
    print("--- RESULTADOS NUEVO ÁRBOL AVL ---")
    print(f"🚀 Altura final: {altura_avl}")
    print(f"⏱️ Tiempo de BÚSQUEDA (Peor caso): {tiempo_busq_avl:.2f} microsegundos")
    print("--------------------------------------------\n")

if __name__ == "__main__":
    ejecutar_experimento()