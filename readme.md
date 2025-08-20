# Gestor de Biblioteca

Este proyecto es  un sistema de gestión de biblioteca en Python, utilizando programación orientada a objetos (POO) y persistencia de datos en un archivo (`biblioteca.txt`). Está enfocado en literatura japonesa.

## Características

- Clases `Libro` y `LibroDigital` (acá hay herencia y polimorfismo).
- Clase `Biblioteca` gestiona una lista de libros.
- Las Funciones que hay son para:
  - Agregar libros (físicos o digitales).
  - Eliminar libros.
  - Listar todos los libros.
  - Buscar un libro por título.
  - Marcar un libro como prestado.
  - Devolver un libro prestado.
- Manejo de excepciones (ej. intentar prestar un libro ya prestado).
- Persistencia en archivo `biblioteca.txt`:
  - Al iniciar: se cargan los libros guardados o se inicializa con una Biblioteca japonesa precargada.
  - Al modificar: se guardan automáticamente los cambios.
- Menú interactivo por consola.

## Archivos del proyecto

- `gestor_biblioteca.py`: código principal del sistema.
- `biblioteca.txt`: archivo JSON con los libros almacenados.
- `README.md`: este documento.

## ▶️ Ejecución

1. Asegúrate de tener **Python 3.10+** instalado.
2. Abre una terminal en la carpeta del proyecto.
3. Ejecuta:

   ```bash
   python gestor_biblioteca.py

--- Gestor de Biblioteca ---
1. Agregar libro
2. Eliminar libro
3. Ver todos los libros
4. Buscar libro
5. Marcar libro como prestado
6. Devolver libro
7. Salir
Elige una opción:
