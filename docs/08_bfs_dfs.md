# TP8 — Recorridos de grafos: BFS y DFS

## 1. Objetivo

Usar los dos recorridos clásicos del grafo de películas (TP7) para responder
preguntas reales del dominio y comparar cuándo conviene cada uno.

Código: `estructuras/grafo.py` (`bfs`, `dfs`, `camino_mas_corto`) y
`services/grafo_peliculas.py` (`camino`, `explorar`, `recorrido_amplitud`).

## 2. Qué hace cada algoritmo

| | BFS (amplitud) | DFS (profundidad) |
| --- | --- | --- |
| Estructura auxiliar | Cola FIFO propia (`ColaVertice`) | Pila de llamadas (recursión) |
| Orden de visita | Por niveles: primero los vecinos directos, después los vecinos de los vecinos | Se mete por una rama hasta el final y después retrocede |
| Marca de visitado | `visitado` en cada vértice, reiniciada antes de recorrer | Igual |
| Garantía | La primera vez que llega a un vértice lo hace con la menor cantidad de aristas | Ninguna sobre la distancia |
| Complejidad | O(V + E) | O(V + E) |
| Memoria extra | O(V) por la cola | O(V) por la profundidad de la recursión |

`V` son las películas y `E` las relaciones entre ellas. Con 30 películas hay
191 relaciones.

## 3. Caso de uso 1: relación más cercana (BFS)

**Pregunta:** ¿cuál es el camino más corto entre dos películas?

**Opción 7 del menú.** `Grafo.camino_mas_corto` recorre con BFS y guarda, para
cada vértice, desde cuál se llegó (mapa de padres). Al encontrar el destino
reconstruye el camino yendo hacia atrás y lo invierte.

```text
Camino encontrado (2 saltos):
  Matrix → El Caballero de la Noche → Oppenheimer
```

**Por qué BFS:** el grafo no tiene pesos en los recorridos, así que todas las
relaciones cuestan lo mismo. Como BFS avanza por niveles, el primer camino que
encuentra es el de menos saltos. Además corta apenas encuentra el destino, sin
recorrer el resto del grafo.

## 4. Caso de uso 2: explorar la red (DFS)

**Pregunta:** ¿qué películas se pueden alcanzar a partir de una dada y en qué
orden se recorre una rama completa?

**Opción 8 del menú.** Muestra BFS y DFS desde la misma película para
compararlos. Desde `Matrix`, los dos alcanzan las mismas 29 películas (la
trigésima, `El Bueno, el Malo y el Feo`, no tiene relaciones con ninguna), pero
en distinto orden:

```text
BFS: Matrix → El Caballero de la Noche → Duna: Parte Dos → Spider-Man: Sin Camino a Casa → ...
DFS: Matrix → El Caballero de la Noche → Sueños de libertad → El Padrino → El Padrino: Parte II → ...
```

BFS agota primero las 10 relaciones directas de `Matrix`. DFS sigue la primera
relación de cada película hasta quedarse sin vecinos nuevos y recién ahí
retrocede.

**Por qué DFS:** sirve para explorar a fondo una rama y para saber qué es
alcanzable, y su versión recursiva es corta y fácil de explicar.

## 5. Cuándo conviene cada uno

- **Camino con menos saltos o relación más cercana:** BFS.
- **Todo lo alcanzable a partir de un punto, o seguir una rama hasta el
  final:** DFS.
- **Grafo muy profundo:** BFS, porque el DFS recursivo está limitado por el
  máximo de recursión de Python (cerca de 1.000 niveles).
- **Grafo muy ancho:** DFS, porque la cola de BFS puede crecer mucho.

## 6. Análisis de complejidad

Con la lista de adyacencia, cada vértice se visita una vez y cada arista se
mira una o dos veces (una por cada extremo en un grafo no dirigido), por eso
ambos son **O(V + E)**.

Una matriz de adyacencia los llevaría a O(V²), porque para cada vértice habría
que revisar toda su fila.

Costos extra de esta implementación, que no cambian el orden pero conviene
conocer:

- `buscar_vertice` recorre la lista de vértices: O(V) por cada recorrido que
  empieza desde una película.
- `reiniciar_visitados` recorre todos los vértices antes de cada recorrido:
  O(V).

## 7. Casos borde

- **Película inexistente:** `bfs` y `dfs` devuelven lista vacía.
- **Película sin relaciones** (`El Bueno, el Malo y el Feo`): el recorrido
  devuelve solo esa película y `camino_mas_corto` devuelve `None` hacia ella.
- **Origen igual a destino:** `camino_mas_corto` devuelve una lista con una
  sola película; la terminal lo informa antes de ejecutar nada.
- **Ciclos:** la marca `visitado` evita volver a entrar en una película ya
  recorrida, así que los ciclos no generan bucles infinitos.

## 8. Pruebas

Archivo: `tests/test_grafo.py`. Cubre BFS y DFS con orden esperado, camino
más corto, camino inexistente, película aislada y que BFS y DFS alcancen el
mismo conjunto de películas.

## 9. Conclusión

BFS y DFS recorren el mismo grafo con el mismo costo, O(V + E), pero responden
preguntas distintas. En CineMatch, BFS resuelve "¿qué tan cerca están dos
películas?" y DFS resuelve "¿qué se puede descubrir siguiendo una rama de
relaciones?".
