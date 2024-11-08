# AeroChinquihue
Este programa es funcional en Python 3.12. No probado en otras versiones.

## Requisitos

Instala las dependencias necesarias ejecutando:
> pip install -r requirements.txt

**Copia** el archivo .env.example a .env y configura el entorno.
> \# Debes colocar el nombre de la base de datos, por ejemplo database.db
>
> DATABASE_FILENAME=

## Estructura de archivos

* main.py: Programa principal.

### Model-View-ViewModel (MVVM)
* mvvmModel.py: Modelo de base de datos (SQLite3).
* mvvmViewModel: Interacciones entre modelo y vista.
* mvvmView: Vista de PyQt.

### Herramientas (carpeta tools)

* createDatabase.py: Crea una database inicial con los datos requeridos.
* vacuumDatabase.py: Reduce el tamaño de la base de datos.

## Limitaciones

* Dado que para la base de datos se utiliza SQLite, **sólo un usuario puede abrir la base de datos a la vez**.

## Software necesario

* [Git](https://git-scm.com/)
* [Python](https://www.python.org/)

## Software recomendado

* [PyCharm](https://www.jetbrains.com/pycharm/): IDE para programar en Python

## Créditos

* https://github.com/Bombadil-Tom/pyqt-mvvm-example
