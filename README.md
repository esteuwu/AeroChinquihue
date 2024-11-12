# AeroChinquihue

Este programa es funcional en Python 3.12. No probado en otras versiones.

## Requisitos

En caso de que quieras desarrollar, instala las dependencias necesarias ejecutando:
> pip install -r requirements.dev.txt -r requirements.txt

En caso de que solo quieras ejecutar el programa,
instala las dependencias necesarias ejecutando:
> pip install -r requirements.txt

**Copia** el archivo .env.example a .env y configura las variables de entorno.
> \# Debes colocar el nombre de la base de datos, por ejemplo database.db
>
> DATABASE_FILENAME=

## Estructura de archivos

* main.py: Programa principal.

### Carpeta mvvm

Contiene archivos relacionados con el patrón de arquitectura
[Modelo–vista–modelo de vista](https://es.wikipedia.org/wiki/Modelo%E2%80%93vista%E2%80%93modelo_de_vista).
* mvvm_model.py: **Modelo**.
Contiene funcionalidad relacionada con la base de datos (SQLite3).
* mvvm_view_model.py: **Modelo de vista**.
Maneja las interacciones entre modelo y vista.
* mvvm_view.py: **Vista**. Interfaz de usuario (PyQt6).

#### Carpeta tools

* createDatabase.py: Crea una base de datos inicial con la información requerida.
* vacuumDatabase.py: Reduce el tamaño de la base de datos ejecutando el comando [VACUUM](https://www.sqlite.org/lang_vacuum.html).

## Software necesario

### Desarrollo

* [Git](https://git-scm.com/)

#### Uso

* [Python](https://www.python.org/)

## Software recomendado

* [PyCharm](https://www.jetbrains.com/pycharm/): IDE para programar en Python

## Créditos

* [https://github.com/Bombadil-Tom/pyqt-mvvm-example](https://github.com/Bombadil-Tom/pyqt-mvvm-example)

## Licencia

* El repositorio está licenciado bajo la licencia MIT, la cual puede verse [aquí](https://github.com/esteuwu/AeroChinquihue/blob/master/LICENSE).
