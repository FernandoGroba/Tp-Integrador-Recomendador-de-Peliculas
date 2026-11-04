# TP7 — Grafo de relaciones

## 1. Objetivo

Convertir las relaciones entre películas en una **red** que permita responder:

- *"Si me gustó Matrix, ¿qué otras películas puedo ver?"*
- *"¿Qué relación hay entre Matrix y Oppenheimer?"*
- *"¿Qué películas están conectadas con Matrix, directa o indirectamente?"*

## 2. Modelo del grafo

| Elemento | Decisión |
| --- | --- |
| **Vértice** | Una película del catálogo. |
| **Arista** | Dos películas están conectadas si comparten al menos un género, un director o un actor. |
| **Tipo** | **No dirigido**: si A se relaciona con B, entonces B se relaciona con A. |
| **Peso** | **No pesado** para los recorridos. Cada arista guarda un texto con el motivo y un puntaje de afinidad que se usa solo para ordenar las sugerencias. |
| **Representación** | **Lista de adyacencia enlazada**. |

### Justificación de la representación

Con 30 películas, una matriz de adyacencia guardaría todos los pares posibles,
aunque la mayoría no tenga relación. La lista de adyacencia guarda solo las
relaciones que existen y permite recorrer los vecinos de una película sin
revisar todas las demás, que es justo lo que necesitan BFS, DFS y las
recomendaciones.

### Criterio de relación

El servicio `GrafoPeliculas` compara cada par de películas:

1. **Mismo director** → afinidad +3.
2. **Actor en común** → afinidad +2 por actor.
3. **Género en común** → afinidad +1 por género.

Si no comparten ninguno de los tres, no se crea la arista. El texto de la
arista guarda el motivo, por ejemplo:

```text
género en común: Acción, Ciencia Ficción
mismo director (Christopher Nolan)
actor en común: Al Pacino
```

El puntaje de afinidad se usa para ordenar las películas relacionadas; en
empate se ordena por rating descendente y luego por título.

## 3. Estructura implementada

Archivo: `estructuras/grafo.py`.

Se mantienen las clases de TP anteriores (`NodoVertice`, `NodoArista`,
`Arista`, `Grafo`) y se agregaron las operaciones que faltaban:

| Operación | Qué hace | Complejidad |
| --- | --- | --- |
| `insertar_vertice(info)` | Agrega una película al final de la lista de vértices | O(V) por la búsqueda de duplicados |
| `insertar_arista(origen, destino, motivo, peso)` | Conecta dos vértices; si el grafo no es dirigido agrega ambas direcciones | O(V + grado) |
| `buscar_vertice(info)` | Busca un vértice por identidad/igualdad | O(V) |
| `adyacentes(info)` | Devuelve las aristas de salida | O(V + grado) |
| `bfs(inicio)` | Recorrido por amplitud con cola FIFO | O(V + E) |
| `dfs(inicio)` | Recorrido en profundidad recursivo | O(V + E) |
| `camino_mas_corto(origen, destino)` | BFS con mapa de padres | O(V + E) |
| `reiniciar_visitados()` | Limpia las marcas antes de cada recorrido | O(V) |

La cola `ColaVertice` está implementada con nodos enlazados, no con
`collections.deque`, para mantener el mismo enfoque de estructuras manuales
usado en la materia.

## 4. Servicio de dominio

Archivo: `services/grafo_peliculas.py`.

`GrafoPeliculas` recibe el catálogo y construye el grafo una sola vez:

```python
grafo = GrafoPeliculas(catalogo.listar())
matrix = grafo.buscar("Matrix")
relacionadas = grafo.relacionadas(matrix, limite=5)
camino = grafo.camino(matrix, oppenheimer)
recorrido = grafo.explorar(matrix)   # DFS
```

Métodos principales:

- `relacionadas(pelicula, limite)`: vecinos directos ordenados por afinidad y
  rating.
- `camino(origen, destino)`: camino con menos aristas usando BFS.
- `explorar(pelicula)`: recorrido DFS.
- `recorrido_amplitud(pelicula)`: recorrido BFS.
- `grado(pelicula)`: cantidad de relaciones directas.
- `buscar(titulo)`: resuelve una película ignorando mayúsculas y tildes.

## 5. Integración en la terminal

Se agregaron tres opciones al menú:

```text
6 - Ver películas relacionadas (Grafo)
7 - Buscar camino entre películas (BFS)
8 - Explorar la red (BFS / DFS)
```

### Opción 6 — Películas relacionadas

Muestra los 5 vecinos con mayor afinidad y el motivo de cada relación.

```text
Si te gustó «Matrix», quizás te interesen:
  1. Todo en Todas Partes al Mismo Tiempo — ⭐ 5.0 (2022)
     ↳ género en común: Acción, Ciencia Ficción
  2. Máquina de Guerra — ⭐ 4.9 (2026)
     ↳ género en común: Acción, Ciencia Ficción
  ...
```

### Opción 7 — Camino más corto (BFS)

Pide origen y destino y muestra la secuencia de películas relacionadas:

```text
Camino encontrado (2 saltos):
  Matrix → El Caballero de la Noche → Oppenheimer
```

BFS es el algoritmo correcto porque el grafo no tiene pesos y cada arista
representa el mismo costo: una relación.

### Opción 8 — Explorar la red (BFS / DFS)

Muestra los dos recorridos desde una película para comparar el orden de visita:

- **BFS** visita por niveles: primero las relaciones directas, después las
  relaciones de las relaciones.
- **DFS** se mete en una rama hasta el final y después retrocede.

Ambos recorren las mismas películas alcanzables, pero en distinto orden. BFS
sirve para encontrar lo más cercano; DFS sirve para explorar una rama completa.

## 6. Análisis de complejidad

Para `V` películas y `E` relaciones:

- BFS: **O(V + E)**.
- DFS: **O(V + E)**.
- Camino más corto con BFS: **O(V + E)**.
- Consultar los vecinos de una película: **O(V + grado)** por la búsqueda del
  vértice y el recorrido de su lista.

Con 30 películas y 191 relaciones, todas las consultas responden
instantáneamente. Si el catálogo creciera a miles de películas, la construcción
del grafo sería lo más costoso, porque hay que comparar pares de películas; se
podría mejorar indexando por género, director y actor para generar solo las
parejas candidatas.

## 7. Pruebas

Archivo: `tests/test_grafo.py`. Se prueban 16 casos, entre ellos:

- inserción de vértices sin duplicados;
- aristas no dirigidas (A→B y B→A);
- BFS y DFS con orden esperado;
- camino más corto y camino inexistente;
- búsqueda por título con `buscar_titulo_amplitud`;
- todos los vértices del catálogo cargados;
- películas del mismo director relacionadas;
- orden por afinidad y rating;
- película aislada sin relaciones;
- camino entre películas conectadas;
- BFS y DFS alcanzan el mismo conjunto de películas.

Resultado: **todos los tests pasan**.

## 8. Casos borde

- **Película aislada:** `El Bueno, el Malo y el Feo` no comparte género,
  director ni actores con otra película del dataset. La consulta de
  relacionadas devuelve una lista vacía y el camino hacia ella devuelve
  `None`; la terminal lo informa sin romperse.
- **Título ambiguo:** si el usuario escribe una parte de un título que
  coincide con varias películas, la terminal muestra las opciones y pide un
  número.
- **Misma película como origen y destino:** se informa y no se ejecuta BFS.

## 9. Conclusión

El grafo permite pasar de una lista de películas a una red de relaciones y
resolver consultas que con una lista plana requerirían recorrer todo el
catálogo para cada pregunta. La lista de adyacencia y BFS/DFS son adecuados
para el tamaño y la densidad del dominio, y dejan preparado el terreno para
agregar caminos con pesos en el futuro.
