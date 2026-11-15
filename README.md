# CineMatch — Recomendador de Películas

**Trabajo práctico integrador de la cátedra ESTRUCTURA DE DATOS de la carrera TECNICATURA EN PROGRAMACIÓN de la UNIVERSIDAD NACIONAL GUILLERMO BROWN**

## Integrantes de la comisión 2

- **Matias Jesus Bermudez**
- **Joaquin Rafael Rodriguez**
- **Fernando Daniel Groba**

## Profesores

- **Ing. Maximiliano Zorzoli**
- **Lic. Angel Leonardo Bianco**

## Descripción

CineMatch es un sistema de recomendaciones de películas que funciona por
terminal. Permite cargar un catálogo desde JSON, buscar y filtrar películas,
explorar categorías, ver un ranking de las mejores, consultar películas
relacionadas y encontrar caminos dentro de una red de relaciones.

El proyecto se construyó de forma incremental: cada etapa agrega una estructura
de datos real y la integra a una funcionalidad concreta del producto.

## Estado del proyecto

| Etapa | Tema | Estado |
| --- | --- | --- |
| TP1 | Objetos, clases y catálogo | ✅ Integrado |
| TP2 | Análisis de complejidad | ✅ Documentado y con pruebas |
| TP3 | Árbol binario de búsqueda | ✅ Integrado (opción 1, búsqueda exacta por título) |
| TP4 | AVL | ✅ Implementado y probado (experimento de desbalanceo) |
| TP5 | Árbol general de categorías | ✅ Integrado en la terminal |
| TP6 | Heap / cola de prioridades | ✅ Integrado (Top 10) |
| TP7 | Grafo de relaciones | ✅ Integrado (relacionadas, BFS, DFS) |

## Requisitos

- Python 3.10 o superior.
- No se usan librerías externas: solo la biblioteca estándar (`json`,
  `unicodedata`, `unittest`).

## Cómo ejecutar

Desde la carpeta del proyecto:

```bash
python main.py
```

El programa carga `data/data.json` (30 películas) y muestra el menú:

```text
1 - Buscar película por título
2 - Listar todas las películas
3 - Filtrar por género
4 - Explorar categorías (Árbol)
5 - Ver Top 10 (Heap)
6 - Ver películas relacionadas (Grafo)
7 - Buscar camino entre películas (BFS)
8 - Explorar la red (BFS / DFS)
0 - Salir
```

## Cómo ejecutar las pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas cubren catálogo, búsqueda con árbol, heap/ranking, grafo y recorridos.

## Estructura del proyecto

```text
├── data/
│   └── data.json                 # Catálogo de 30 películas
├── docs/
│   ├── 01_requerimientos.md      # Requerimientos funcionales y no funcionales
│   ├── 02_casos_de_uso.md        # Casos de uso paso a paso
│   ├── 03_diagrama_de_clases.md  # Diagrama de clases (Mermaid)
│   ├── 04_diagrama_de_datos.md   # Conexión entre estructuras
│   ├── 05_gestion_proyecto.md    # Organización del proyecto
│   ├── 06_heap.md                # TP6: heap y ranking
│   ├── 07_grafo.md               # TP7: grafo de relaciones
│   └── capturas/                 # Evidencias de ejecución
├── estructuras/
│   ├── arbol_avl.py              # Árbol AVL
│   ├── arbol_general.py          # Árbol general de categorías
│   ├── grafo.py                  # Grafo con lista de adyacencia, BFS y DFS
│   └── heap.py                   # Max-heap manual
├── models/
│   └── pelicula.py               # Entidad Pelicula
├── services/
│   ├── arbol_catalogo.py         # BST de catálogo
│   ├── catalogo.py               # Carga, búsqueda y filtros
│   ├── grafo_peliculas.py        # Servicio de relaciones entre películas
│   └── ranking.py                # Ranking con heap
├── tests/
│   ├── test_avl.py
│   ├── test_catalogo.py
│   ├── test_complejidad.py
│   ├── test_grafo.py
│   └── test_heap.py
├── UI/
│   └── terminal.py               # Menú e interacción por consola
├── main.py                       # Punto de entrada
└── README.md
```

## Estructuras implementadas

### Catálogo y búsquedas

- `Catalogo`: carga el JSON, busca por título y filtra por género.
- `ArbolCatalogo` / `Arbol_avl_Catalogo`: árbol binario y AVL ordenados por
  título.
- La opción 1 del menú inserta el catálogo en el BST al iniciar y busca la
  coincidencia exacta con `buscar_exacto` (O(log n) promedio). Después suma las
  coincidencias parciales de `Catalogo.buscar`, sin repetir, para que "el
  padrino" devuelva toda la saga.

### Árbol general

- `ArbolGeneralCategorias`: jerarquía de categorías que se explora desde la
  opción 4 de la terminal.

### Heap (TP6)

- `HeapMax`: max-heap manual con `insertar`, `extraer_max`, `ver_max`,
  `top_n` y construcción O(n).
- `RankingPeliculas`: ranking de películas por rating con desempate FIFO.
- La terminal muestra el Top 10 en la opción 5.

### Grafo (TP7)

- `Grafo`: grafo no dirigido con lista de adyacencia, BFS, DFS y camino más
  corto sin pesos.
- `GrafoPeliculas`: conecta películas que comparten género, director o actor.
- Opción 6: películas relacionadas con su motivo.
- Opción 7: camino más corto entre dos películas (BFS).
- Opción 8: comparación de recorridos BFS y DFS.

## Documentación

- [Requerimientos](docs/01_requerimientos.md)
- [Casos de uso](docs/02_casos_de_uso.md)
- [Diagrama de clases](docs/03_diagrama_de_clases.md)
- [Diagrama de conexión entre estructuras](docs/04_diagrama_de_datos.md)
- [Gestión del proyecto](docs/05_gestion_proyecto.md)
- [TP6 — Heap](docs/06_heap.md)
- [TP7 — Grafo](docs/07_grafo.md)

## Decisiones de diseño

- **Heap para el ranking:** permite consultar el Top-N en O(k log n) sin
  ordenar todo el catálogo en cada consulta.
- **Desempate FIFO:** hace que el ranking sea determinista cuando varias
  películas comparten rating.
- **Grafo no dirigido con lista de adyacencia:** las relaciones son simétricas
  y la lista guarda solo las relaciones que existen, a diferencia de una matriz
  que guarda todos los pares posibles.
- **BFS para el camino más corto:** todas las relaciones cuestan lo mismo, así
  que BFS encuentra el camino con menos saltos.
- **DFS para explorar:** permite recorrer una rama completa de relaciones.
