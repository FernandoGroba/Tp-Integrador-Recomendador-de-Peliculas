# Organización del proyecto

## 1. Forma de trabajo

El proyecto se desarrolló de forma incremental: cada etapa agregó una
estructura de datos y una funcionalidad nueva sobre lo que ya funcionaba. Antes
de cerrar una etapa se verificó que las opciones anteriores siguieran
funcionando y que las pruebas pasaran.

No se usó una metodología formal de gestión. El trabajo se organizó con una
lista de tareas por etapa y una revisión final de cada entrega.

## 2. Organización del código

El código se dividió por responsabilidades:

- `models/`: entidad de dominio (`Pelicula`).
- `estructuras/`: implementación manual de las estructuras (árboles, heap y
  grafo).
- `services/`: lógica que conecta las estructuras con el dominio.
- `UI/`: interacción por terminal.
- `tests/`: pruebas automatizadas.
- `docs/`: documentación de cada etapa.

## 3. Verificación antes de cada entrega

Al finalizar cada etapa se comprobó:

1. Que el programa arranque con `python main.py`.
2. Que las opciones anteriores sigan funcionando.
3. Que las pruebas pasen con `python -m unittest discover -s tests -v`.
4. Que la nueva estructura esté documentada y tenga una funcionalidad real
   dentro de la terminal.
