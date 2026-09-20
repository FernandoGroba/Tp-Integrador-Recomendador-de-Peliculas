import random
import time
from models.pelicula import Pelicula
from services.arbol_catalogo import ArbolCatalogo
from services.catalogo import Catalogo


def generar_datos_prueba(n: int) -> tuple[Catalogo, ArbolCatalogo]:
    """Genera n películas de prueba y las carga tanto en el Catalogo como en el ArbolCatalogo."""
    cat = Catalogo()
    arbol = ArbolCatalogo()

    titulos_base = [
        "Matrix",
        "Avatar",
        "Inception",
        "Titanic",
        "Gladiador",
        "El Botin",
        "Interestelar",
        "El Padrino",
        "Star Wars",
        "Alien",
    ]

    for i in range(n):
        titulo_generado = f"{random.choice(titulos_base)} {i}"
        # Pasamos los parámetros por posición matching con Pelicula(id, titulo, anio, genero, director, actores, rating, sinopsis)
        p = Pelicula(
            i,
            titulo_generado,
            2020,
            "Acción",
            "Director Test",
            "Actores Test",
            8.0,
            "Sinopsis de prueba",
        )
        cat._elementos.append(p)
        arbol.insertar(p)

    return cat, arbol


def probar_rendimiento() -> None:
    """Ejecuta los experimentos de búsqueda con distintos tamaños de datos (N)."""
    tamanios = [1000, 10000, 100000]
    repeticiones = 200  # Número de iteraciones para obtener un promedio preciso

    print("=" * 68)
    print(" ⚡ EXPERIMENTO DE COMPLEJIDAD: BÚSQUEDA SECUENCIAL vs ÁRBOL (BST)")
    print("=" * 68)
    print(
        f"{'N elementos':<15} | {'Búsqueda Secuencial (Lista)':<28} | {'Búsqueda en Árbol (BST)':<22}"
    )
    print("-" * 68)

    for n in tamanios:
        cat, arbol = generar_datos_prueba(n)

        # Buscamos una película específica que fuerce el recorrido
        titulo_a_buscar = f"Titanic {n - 1}"

        # -------------------------------------------------------------
        # 1. Medición: Búsqueda Secuencial (Lista / Catalogo)
        # -------------------------------------------------------------
        inicio = time.perf_counter()
        for _ in range(repeticiones):
            cat.buscar(titulo_a_buscar)
        fin = time.perf_counter()
        tiempo_secuencial_ms = ((fin - inicio) / repeticiones) * 1000

        # -------------------------------------------------------------
        # 2. Medición: Búsqueda en Árbol Binario (BST / ArbolCatalogo)
        # -------------------------------------------------------------
        inicio = time.perf_counter()
        for _ in range(repeticiones):
            arbol.buscar(titulo_a_buscar)
        fin = time.perf_counter()
        tiempo_arbol_ms = ((fin - inicio) / repeticiones) * 1000

        # Imprimimos la fila de resultados
        print(
            f"{n:<15} | {tiempo_secuencial_ms:.4f} ms{'':<19} | {tiempo_arbol_ms:.4f} ms"
        )

    print("=" * 68)


if __name__ == "__main__":
    probar_rendimiento()