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
