# Diagrama de conexión entre estructuras

El siguiente esquema muestra cómo se transforman los datos y qué estructura
resuelve cada consulta del sistema.

```text
                        ┌─────────────────────┐
                        │   data/data.json    │
                        │  30 películas       │
                        └──────────┬──────────┘
                                   │ json.load
                                   ▼
                        ┌─────────────────────┐
                        │      Catalogo       │
                        │ List<Pelicula>      │
                        └──────────┬──────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
┌──────────────────┐    ┌────────────────────┐    ┌────────────────────┐
│  Árbol general   │    │    RankingPeliculas│    │   GrafoPeliculas   │
│  de categorías   │    │      └─ HeapMax    │    │      └─ Grafo      │
│  (TP5)           │    │      (TP6)         │    │      (TP7)         │
└────────┬─────────┘    └─────────┬──────────┘    └─────────┬──────────┘
         │                        │                          │
         │ explorar categorías    │ Top 10 por rating        │ relaciones
         │                        │                          │
         │                        │                ┌─────────┴─────────┐
         │                        │                │                   │
         │                        │                ▼                   ▼
         │                        │            BFS (camino)        DFS (explorar)
         │                        │                │                   │
         ▼                        ▼                ▼                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         UI / Terminal                                    │
│  1 Buscar   2 Listar   3 Filtrar   4 Categorías   5 Top 10               │
│  6 Relacionadas   7 Camino (BFS)   8 Explorar (BFS/DFS)   0 Salir       │
└──────────────────────────────────────────────────────────────────────────┘
```

## Flujo de una consulta

### Buscar por título (TP3)

```text
Terminal.__init__
      │  inserta cada película del catálogo
      ▼
ArbolCatalogo.insertar()  (BST ordenado por título)

Opción 1: Terminal._buscar_titulo(texto)
      │
      ├──► ArbolCatalogo.buscar_exacto()  O(log n) promedio
      │         coincidencia exacta, va primero
      │
      └──► Catalogo.buscar()  O(n)
                coincidencias parciales, sin repetir la exacta
      ▼
List<Pelicula> (exacta primero, luego el resto)
```

### Top 10 (TP6)

```text
Catalogo.listar()
      │
      ▼
RankingPeliculas.cargar()  ──►  HeapMax.desde_elementos()  O(n)
      │
      ▼
RankingPeliculas.top(10)  ──►  HeapMax.top_n(10)  O(n + k log n)
      │
      ▼
List<Pelicula> ordenada por rating descendente
```

### Películas relacionadas (TP7)

```text
Catalogo.listar()
      │
      ▼
GrafoPeliculas.cargar()
      │  compara cada par de películas
      ▼
Grafo.insertar_vertice() / insertar_arista()
      │
      ▼
GrafoPeliculas.relacionadas(pelicula)
      │  recorre la lista de adyacencia del vértice
      ▼
Vecinos ordenados por afinidad y rating
```

### Camino más corto (BFS)

```text
GrafoPeliculas.camino(origen, destino)
      │
      ▼
Grafo.camino_mas_corto()
      │  cola FIFO + mapa de padres
      ▼
List<Pelicula> con la secuencia de relaciones
```

### Explorar la red (DFS)

```text
GrafoPeliculas.explorar(pelicula)
      │
      ▼
Grafo.dfs()
      │  recursión sobre la lista de adyacencia
      ▼
List<Pelicula> en orden de profundidad
```

## Complejidades principales

| Operación | Estructura | Complejidad |
| --- | --- | --- |
| Buscar por título (parcial, "contiene") en el catálogo | Lista | O(n) |
| Buscar título exacto en BST (opción 1) | BST | O(log n) promedio, O(n) si se desbalancea |
| Buscar título exacto en AVL | Árbol AVL | O(log n) siempre |
| Insertar en la heap | Heap | O(log n) |
| Ver el máximo | Heap | O(1) |
| Top-N | Heap | O(n + k log n) |
| Construir el grafo | Grafo | Se comparan los pares de películas |
| Recorrer el grafo (BFS/DFS) | Grafo | O(V + E) |
| Camino más corto sin pesos | Grafo + BFS | O(V + E) |
