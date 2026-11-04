# Casos de Uso

## Caso de Uso 1: Buscar pelicula por título

* **Quien lo usa:** El usuario.
* **Para que sirve:** Para buscar peluculas escribiendo el nombre completo o solo una parte sin tener que poner el título completo.
* **Que se necesita antes:** Que las peliculas esten cargadas en el sistema.

### Pasos
1. Pones el numero **1** en el menu.
2. Escribis una palabra (por ejemplo: `"El"` o `"batalla"`).
3. El programa se fija cuales peliculas tienen esa palabra en el nombre y junta todas las que encuentra.
4. Te muestra la lista de esas peliculas en la pantalla.
5. Vuelve al menu principal.

### Si algo sale distinto
* **No encuentra nada:** Si la palabra que pusiste no este en ninguna pelicula, te avisa con un mensaje y te devuelve al menu.

---

## Caso de Uso 2: Mostrar todas las peluculas

* **Quien lo usa:** El usuario.
* **Para qué sirve:** Para ver la lista completa de peliculas que hay guardadas.
* **Que se necesita antes:** Tener la aplicacion abierta.

### Pasos
1. Pones el numero **2** en el menu.
2. El programa busca todo el listado de peliculas.
3. Te las va mostrando una por una en la pantalla.
4. Vuelve al mene principal.

---

## Caso de Uso 3: Filttrar por categoria

* **Quien lo usa:** El usuario.
* **Para que sirve:** Para ver unicamente las peluculas de un tipo o genero (como Accion o Fantasia).
* **Que se necesita antes:** Que existan peliculas guardadas en el sistema.

### Pasos
1. Pones el número **3** en el menú.
2. Escribis el tipo de pelicula que queres ver.
3. El programa lo arregla si te olvidaste de ponerle tilde a la palabra (como escribir `"accion"` sin acento) y busca las que coinciden.
4. Te muestra en pantalla las peliculas de ese tipo.
5. Vuelve al menu principal.

### Si algo sale distinto
* **Categoría sin películas:** Si escribis un género que no tiene peliculas, te dice que no hay nada en esa categoria y te manda al menu.

---

## Caso de Uso 4: Explorar categorías

* **Quien lo usa:** El usuario.
* **Para que sirve:** Para ver la jerarquía de géneros y elegir una categoría
  sin tener que escribir el nombre exacto de memoria.
* **Que se necesita antes:** Que las películas estén cargadas y el árbol de
  categorías construido.

### Pasos
1. Pones el número **4** en el menú.
2. El programa muestra el árbol general de categorías.
3. Escribís un género de la lista (o presionás Enter para volver).
4. El programa busca la categoría en el árbol y muestra sus películas.
5. Vuelve al menú principal.

### Si algo sale distinto
* **Categoría inexistente:** Si el nombre no está en el árbol, avisa que no se
  encontró y vuelve al menú.

---

## Caso de Uso 5: Ver el Top 10

* **Quien lo usa:** El usuario.
* **Para que sirve:** Para ver rápidamente las 10 películas mejor rankeadas
  según su rating.
* **Que se necesita antes:** Que el catálogo esté cargado.

### Pasos
1. Pones el número **5** en el menú.
2. El programa consulta el ranking construido con la heap.
3. Muestra las 10 películas de mayor rating, con medallas para las tres
   primeras.
4. Vuelve al menú principal.

### Si algo sale distinto
* **Catálogo vacío:** Si no hay películas, avisa que no se puede armar el
  ranking.
* **Ratings empatados:** Las películas con el mismo rating salen en el orden
  en que fueron cargadas (criterio FIFO).

---

## Caso de Uso 6: Ver películas relacionadas

* **Quien lo usa:** El usuario.
* **Para que sirve:** Para descubrir películas parecidas a una que le gustó.
* **Que se necesita antes:** Que el grafo de relaciones esté construido.

### Pasos
1. Pones el número **6** en el menú.
2. Escribís el título de una película (o parte de él).
3. Si hay varias coincidencias, elegís una por número.
4. El programa muestra hasta 5 películas relacionadas, ordenadas por
   afinidad y rating, con el motivo de cada relación.
5. Vuelve al menú principal.

### Si algo sale distinto
* **Sin relaciones:** Si la película no comparte género, director ni actores
  con otra, avisa que no tiene relaciones cargadas.
* **Título inexistente:** Avisa que no se encontraron coincidencias.

---

## Caso de Uso 7: Buscar el camino entre dos películas

* **Quien lo usa:** El usuario.
* **Para que sirve:** Para ver cómo se conectan dos películas a través de
  relaciones, usando el camino con menos saltos.
* **Que se necesita antes:** Que el grafo esté construido.

### Pasos
1. Pones el número **7** en el menú.
2. Escribís la película de origen.
3. Escribís la película de destino.
4. El programa ejecuta BFS y muestra la secuencia de películas conectadas.
5. Vuelve al menú principal.

### Si algo sale distinto
* **No hay camino:** Avisa que las películas no están conectadas.
* **Mismo origen y destino:** Informa que es la misma película y no ejecuta
  la búsqueda.

---

## Caso de Uso 8: Explorar la red

* **Quien lo usa:** El usuario.
* **Para que sirve:** Para ver todas las películas alcanzables desde una
  película y comparar el orden de los recorridos BFS y DFS.
* **Que se necesita antes:** Que el grafo esté construido.

### Pasos
1. Pones el número **8** en el menú.
2. Escribís la película de inicio.
3. El programa muestra el recorrido BFS (por niveles) y el recorrido DFS
   (en profundidad).
4. Vuelve al menú principal.

### Si algo sale distinto
* **Película aislada:** BFS y DFS muestran solamente la película de inicio.
* **Título inexistente:** Avisa que no se encontraron coincidencias.

