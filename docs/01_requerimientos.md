# Requerimientos

## 1. Requerimientos funcionales

| Código | Requerimiento |
| --- | --- |
| RF01 | El sistema debe cargar el catálogo de películas desde un archivo JSON. |
| RF02 | El sistema debe permitir buscar películas por título, aceptando coincidencias parciales e ignorando mayúsculas y tildes. |
| RF03 | El sistema debe listar todas las películas cargadas. |
| RF04 | El sistema debe filtrar películas por género, ignorando mayúsculas y tildes. |
| RF05 | El sistema debe mostrar una jerarquía de categorías y permitir consultar las películas de una categoría. |
| RF06 | El sistema debe mostrar un Top 10 de películas ordenado por rating descendente. |
| RF07 | El sistema debe mostrar películas relacionadas con una película dada, indicando el motivo de la relación. |
| RF08 | El sistema debe encontrar el camino con menos relaciones entre dos películas. |
| RF09 | El sistema debe mostrar los recorridos BFS y DFS desde una película para explorar la red. |
| RF10 | El sistema debe informar de forma clara cuando una búsqueda no devuelve resultados, cuando un título es ambiguo o cuando una película no tiene relaciones. |

## 2. Requerimientos no funcionales

| Código | Requerimiento |
| --- | --- |
| RNF01 | La interfaz debe funcionar por terminal, sin dependencias de interfaz gráfica. |
| RNF02 | El sistema debe ejecutarse con Python 3.10 o superior y no debe requerir librerías externas. |
| RNF03 | Las estructuras de datos pedidas por la cátedra (árboles, heap y grafo) deben estar implementadas por el equipo, sin usar `heapq` ni librerías de grafos. |
| RNF04 | La consulta del Top-N debe resolverse sin ordenar todo el catálogo en cada llamada. |
| RNF05 | Los recorridos del grafo deben ser O(V + E). |
| RNF06 | El código debe estar organizado por responsabilidades (`models`, `estructuras`, `services`, `UI`, `tests`). |
| RNF07 | El sistema debe incluir pruebas automatizadas de las estructuras y de los servicios principales. |
| RNF08 | El sistema debe manejar errores de entrada sin finalizar la ejecución. |
| RNF09 | La documentación debe permitir ejecutar el proyecto y entender las decisiones de diseño. |

## 3. Alcance

### Incluido

- Catálogo de 30 películas cargado desde JSON.
- Búsqueda, listado y filtrado.
- Árbol general de categorías.
- Ranking Top 10 con heap manual.
- Grafo de relaciones con lista de adyacencia.
- Recorridos BFS y DFS.
- Camino más corto sin pesos entre dos películas.
- Interfaz de terminal.
- Pruebas unitarias y documentación.

### Fuera de alcance

- Autenticación de usuarios y perfiles.
- Persistencia de preferencias.
- Interfaz gráfica o web.
- Integración con Telegram.
- Recomendaciones personalizadas por historial.
- Caminos mínimos con pesos (Dijkstra) y ordenamiento topológico.
- Conexión a una base de datos o a una API externa.

## 4. Usuario objetivo

Una persona que quiere elegir qué película ver y no quiere recorrer todo el
catálogo manualmente. Le interesa encontrar rápido una película por título,
ver las mejores valoradas y descubrir opciones parecidas a una que ya vio.
