# Tp Integrador - Recomendador de Películas

**Trabajo práctico integrador de la cátedra ESTRUCTURA DE DATOS de la carrera TÉCNICATURA EN PROGRAMACIÓN de la UNIVERSIDAD NACIONAL GUILLERMO BROWN**

## Integrantes de la comisión 2:

- **Matias Jesus Bermudez**
- **Joaquin Rafael Rodiguez**
- **Fernando Daniel Groba**

## Profesores:

- **Ing. Maximiliano Zorzoli**
- **Lic Angel Leonardo Bianco**

## Recomendador de películas:

**Este tp consiste en un sistema que recomnienda al usuario que peliculas ver como así tambien generar una lista para guardas peliculas del interes del usuario**

## Estructura del Proyecto

├── algoritmos/ # Módulo para algoritmos específicos
├── data/
│ └── data.json # El archivo con todas las películas guardadas
├── docs/
│ ├── capturas/ # Evidencias de funcionamiento y pruebas
│ │ ├── Busqued_por_titulo.png
│ │ ├── filtrar_por_genero.png
│ │ ├── listar_peliculas.png
│ │ ├── menu.png
│ │ ├── prueba_UnitTest_tp1.png
│ │ └── salida.png
│ ├── 01_requerimientos.md # Especificación de requisitos del sistema
│ ├── 02_casos_de_uso.md # Paso a paso de cómo el usuario usa el programa
│ ├── 03_diagrama_de_clases.md # Arquitectura de clases (Mermaid)
│ ├── 04_diagrama_de_datos.md # Estructura del archivo JSON
│ ├── 05_gestion_proyecto.md # Organización y roles del equipo
│ └── Propuesta.md # La idea inicial que presentamos del TP
├── estructuras/ # Módulo para estructuras de datos
├── models/
│ ├── **init**.py
│ └── pelicula.py # La clase que define la entidad Película
├── services/
│ ├── **init**.py
│ └── catalogo.py # Catálogo para buscar y filtrar las películas
├── tests/
│ ├── **init**.py
│ └── test_catalogo.py # Pruebas unitarias del catálogo
├── UI/
│ ├── **init**.py
│ └── terminal.py # El menú y las pantallas que se ven en la consola
├── main.py # El archivo principal para arrancar el sistema
└── README.md # La presentación y explicación general del trabajo
