# AeroChinquihue

![Imagen de AeroChinquihue](assets/picture.png)

**Vuelos en toda la Región de Los Lagos.**

Este programa es funcional en Python 3.12. No probado en otras versiones.

## Requisitos

En caso de que quieras desarrollar, instala las dependencias necesarias ejecutando:

> $ pip install -r requirements.dev.txt -r requirements.txt

En caso de que solo quieras ejecutar el programa, instala las dependencias
necesarias ejecutando:

> $ pip install -r requirements.txt

## Configuración básica

### Archivo .env

**Copia** el archivo .env.example a .env y configura las variables de entorno.

Ejemplo:

> \# Nombre de aerolínea
>
> BRANDING=AeroChinquihue
>
> \# Nombre del archivo de la base de datos
>
> DATABASE_FILENAME=database.db
>
> \# Eslogan que aparece en la vista principal
>
> SLOGAN=Vuelos en toda la Región de Los Lagos.

### Base de datos

Debes tener [SQLite](https://www.sqlite.org/index.html) instalado en tu sistema
**para crear** la base de datos inicial de acuerdo al archivo sql/createDatabase.sql.

Ejemplo:

> $ sqlite3 database.db < sql/createDatabase.sql

### Creación de usuarios (opcional)

El script create_user.py es usado para esto.

Ejemplo:

> $ python create_user.py *nombre* *RUT* *contraseña*

Las contraseñas están sujetas a hashing mediante el uso de [yescrypt](
https://en.wikipedia.org/wiki/Yescrypt), por lo tanto, no se guardan en texto
plano en la base de datos.

### Ejecutando el programa

Basta con solo ejecutar el archivo main.py.

Ejemplo:

> $ python main.py

## Estructura de archivos

### Carpeta principal

* create_user.py: Script para crear usuarios.

* main.py: Script principal.

### Carpeta assets

Contiene recursos tales como imágenes usadas en el programa.

### Carpeta package

Contiene un paquete principalmente relacionado con el patrón de arquitectura
[Modelo–vista–modelo de vista](https://es.wikipedia.org/wiki/Modelo%E2%80%93vista%E2%80%93modelo_de_vista).

* \_\_init__.py: Provee las clases necesarias (Identification, Model, View, ViewModel).

* identification.py: Clase Identification utilizada para manipular RUTs.

* model.py: **Modelo**. Contiene funcionalidad relacionada con la base de datos (SQLite).

* view.py: **Vista**. Interfaz de usuario (PySide).

* viewmodel.py: **Modelo de vista**. Maneja las interacciones entre modelo y vista.

### Carpeta sql

* createDatabase.sql: Crea una base de datos inicial con la información requerida.

### Carpeta ui

El nombre de un archivo .ui corresponde a la interfaz de una clase del mismo
nombre (sin la extensión) ubicada en el archivo package/view.py.

## Software necesario

### Desarrollo

* [Git](https://git-scm.com/)

### Uso

* [Python](https://www.python.org/)

## Software recomendado

* [PyCharm](https://www.jetbrains.com/pycharm/): IDE para programar en Python

## Créditos

* [https://github.com/Bombadil-Tom/pyqt-mvvm-example](https://github.com/Bombadil-Tom/pyqt-mvvm-example)

## Licencia

* El repositorio está licenciado bajo la licencia MIT, la cual puede verse [aquí](https://github.com/esteuwu/AeroChinquihue/blob/master/LICENSE).

## To-do

Solo para uso interno.

### Necesario

* [X] OK: Documentar el código hasta el commit c2f40c1 o aplicable (Esteban)

* [X] OK: Descuento de 10% para clientes frecuentes (más de 10 vuelos, 50%
implementado; implementado en Model y ViewModel con la función
get_flight_count(), falta implementarlo en View)

* [ ] Pendiente: Agregar límites de pasajeros y peso para cada avión y agregar validaciones
correspondientes

* [X] OK: Mostrar una fecha de entrega para encomiendas al confirmar la reserva

* [ ] Pendiente: Agregar opción de obviar pago utilizando credenciales de
gerente en vista de empleados (agregar callback functions)

* [X] OK: Permitir la modificación de valores en la vista de gerente y agregar
validaciones correspondientes

* [ ] Pendiente: Agregar algoritmo de hora de salida

* [X] OK: Convertir los valores como tal antes de mostrarlos en la tabla de gerente

### No necesario

* [ ] Agregar sistema de localización (borrar strings localizadas del código)

* [ ] Bloquear el tamaño de la ventana

* [ ] Hacer que todo ocurra en una sola ventana (puede chocar con n.º 3)

* [ ] Avisar de que solo se puede seleccionar una entrada para Gerente,
posiblemente usando QTableWidget.selectedRanges() (dificultad: media)
