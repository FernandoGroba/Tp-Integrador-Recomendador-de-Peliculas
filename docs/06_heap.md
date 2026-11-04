# TP6 — Cola de prioridades (Heap)

## 1. Objetivo

Agregar al recomendador una consulta de **Top-N de películas** que responda
rápidamente y sin ordenar todo el catálogo cada vez.

La estructura pedida por la cátedra es una **heap binaria implementada a mano**.
No se usa `heapq` ni ninguna otra librería de prioridades.

## 2. Función de prioridad

La prioridad de cada película es su **rating**:

```text
prioridad(película) = película.rating
```

Cuanto mayor es el rating, antes sale la película. Se eligió el rating porque
es el dato que el usuario ya ve en el catálogo y permite responder de forma
directa la pregunta *"¿cuáles son las mejores películas?"*.

### Empates

Hay varias películas con el mismo rating (por ejemplo, seis películas tienen
`5.0`). Para que el ranking sea **determinista** se usa un desempate **FIFO**:
si dos películas tienen la misma prioridad, sale primero la que se insertó
primero. Cada entrada de la heap guarda un número de secuencia creciente:

```text
si prioridad_a != prioridad_b -> gana la prioridad más alta
si prioridad_a == prioridad_b -> gana la secuencia más baja (llegó antes)
```

Esto hace que el resultado coincida con un ordenamiento estable por rating
descendente, que es fácil de verificar en los tests.

## 3. Por qué una heap y no ordenar todo

| Estrategia | Costo de construir | Costo de consultar Top-N | El ranking se conserva |
| --- | --- | --- | --- |
| Ordenar todo con `sorted` | O(n log n) | O(n log n) cada vez | Sí, pero se repite el trabajo |
| Heap manual | O(n) con `desde_elementos` | O(k log n) | Sí, `top_n` trabaja sobre una copia |

La heap conviene porque el sistema consulta el Top-N muchas veces y el
catálogo se carga una sola vez. Además, `insertar` y `extraer_max` son
O(log n), así que el ranking puede actualizarse si cambia un rating sin
reordenar todo.

## 4. Diseño de la estructura

Archivo: `estructuras/heap.py`.

La heap se guarda en un **vector** (`list`). Para el índice `i`:

```text
padre(i)     = (i - 1) // 2
izquierdo(i) = 2 * i + 1
derecho(i)   = 2 * i + 2
```

Es un **max-heap**: la raíz (índice `0`) siempre tiene la mayor prioridad.

### Operaciones implementadas

| Método | Qué hace | Complejidad |
| --- | --- | --- |
| `insertar(dato, prioridad)` / `arribo` | Agrega al final y lo hace flotar | O(log n) |
| `ver_max()` / `frente` | Devuelve la raíz sin extraerla | O(1) |
| `extraer_max()` / `atencion` | Quita la raíz, mueve el último elemento y lo hunde | O(log n) |
| `top_n(n)` | Copia el vector y extrae los `n` mejores | O(n + k log n) |
| `desde_elementos(...)` | Construye la heap con `hundir` desde la mitad | O(n) |
| `cambiar_prioridad(dato, nueva)` | Busca el dato y reacomoda | O(n) |
| `__len__`, `esta_vacia`, `tamanio` | Consultas de estado | O(1) |

### Detalle de las operaciones internas

- **`_flotar(i)`**: mientras el elemento sea mayor que su padre, los
  intercambia. Se usa al insertar.
- **`_hundir(i)`**: compara con sus dos hijos y baja al mayor hasta que la
  propiedad de heap se cumple. Se usa al extraer y al monticulizar.
- **`_monticulizar()`**: recorre desde `n // 2 - 1` hasta `0` aplicando
  `_hundir`. Es O(n), no O(n log n), porque los niveles inferiores tienen
  muchos nodos pero baja altura.
- **`top_n(n)`**: crea una heap copia con `list(self._datos)` y extrae sobre
  la copia. Así el ranking original no se destruye y se puede volver a
  consultar.

## 5. Integración con el proyecto

Archivo: `services/ranking.py`.

La clase `RankingPeliculas` conecta la heap con el dominio:

```python
ranking = RankingPeliculas(catalogo.listar())
mejores = ranking.top(10)      # lista de Pelicula
mejor = ranking.mejor()        # Pelicula con mayor rating
```

- `cargar(peliculas)` reconstruye la heap en O(n) con `desde_elementos`.
- `top(cantidad)` devuelve las mejores sin modificar el ranking.
- `mejor()` usa `ver_max()`.
- `__len__` y `esta_vacio()` delegan en la heap.

La terminal construye el ranking una sola vez en `Terminal.__init__` y lo
consulta en la opción **5 - Ver Top 10 (Heap)**.

Ejemplo de salida real con `data/data.json`:

```text
--- 🏆 TOP 10 MEJOR RANKEADAS ---
🥇 Sueños de libertad — ⭐ 5.0 (1994)
🥈 Tiempos Violentos — ⭐ 5.0 (1994)
🥉 El Señor de los Anillos: La Comunidad del Anillo — ⭐ 5.0 (2001)
 4. Oppenheimer — ⭐ 5.0 (2023)
 5. Todo en Todas Partes al Mismo Tiempo — ⭐ 5.0 (2022)
 6. Matrix — ⭐ 5.0 (1999)
 7. Máquina de Guerra — ⭐ 4.9 (2026)
 8. Duna: Parte Dos — ⭐ 4.8 (2024)
 9. Apex — ⭐ 4.8 (2026)
10. Una batalla tras otra — ⭐ 4.7 (2025)
```

## 6. Pruebas

Archivo: `tests/test_heap.py`. Se prueban 11 casos:

- extracción en orden de prioridad;
- `ver_max` no extrae;
- empate resuelto por FIFO;
- `top_n` no modifica el heap;
- límites de `top_n` (0, más que el tamaño);
- heap vacía;
- construcción O(n) con `desde_elementos`;
- el Top 10 tiene 10 elementos y está ordenado;
- el Top 10 coincide con un ordenamiento estable por rating;
- `mejor()` devuelve el máximo;
- `top()` no vacía el ranking.

Resultado: **todos los tests pasan** (`python -m unittest discover -s tests -v`).

## 7. Conclusión

La heap resuelve el ranking de forma eficiente y se integra con el dominio sin
exponer detalles de la estructura. La decisión clave fue mantener la prioridad
en un solo valor (`rating`) y usar la secuencia de llegada para desempatar,
lo que hace que el Top-N sea reproducible y fácil de testear.
