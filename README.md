# AeroChinquihue

![Imagen de AeroChinquihue](assets/picture.png)

Vuelos en toda la Región de Los Lagos.

Este programa es funcional en Python 3.12. No probado en otras versiones.

## Requisitos

En caso de que quieras desarrollar, instala las dependencias necesarias ejecutando:

> pip install -r requirements.dev.txt -r requirements.txt

En caso de que solo quieras ejecutar el programa, instala las dependencias necesarias ejecutando:

> pip install -r requirements.txt

**Copia** el archivo .env.example a .env y configura las variables de entorno.

> \# Debes colocar el nombre de la base de datos, por ejemplo database.db
>
> DATABASE_FILENAME=
>
> \# Debes colocar el nombre de la imagen de presentación, por ejemplo
> AeroChinquihue.png que viene incluido
>
> PICTURE_FILENAME=

### Creando la base de datos

Debes tener [SQLite](https://www.sqlite.org/index.html) instalado en tu sistema y ejecutar un comando tal como:

> sqlite3 database.db < sql/createDatabase.sql

### Creando un usuario (gerente) en la base de datos

Puedes usar el script create_user.py para esto.

Ejemplo:

> python create_user.py "John Doe" 12.345.678-5 JohnDoe123

Las contraseñas están sujetas a hashing y salting mediante el uso de [yescrypt](https://en.wikipedia.org/wiki/Yescrypt) (sitio web en inglés), por lo tanto, no se guardan en texto plano en la base de datos.

Los usuarios lucen así en la base de datos:

> sqlite> SELECT * FROM users;
>
> John Doe|12345678|DAvEmTm3fQYjWLuqMZ/+aXgQJptxW3idghEJydn3I2c=|b0Q8nnAd5QFlxKgB8ogFAlmOCU7/8BmSkDgWBrTM6Bk=
>
> sqlite>

Los usuarios se guardan de la siguiente manera:

> name|identification|hashed_password|salt

* name: Nombre del usuario.

* identification: RUT del usuario sin dígito verificador.

* hashed_password: Contraseña hasheada junto con la respectiva salt, nuevamente

* salt: Salt de la contraseña codificada en [base64](https://es.wikipedia.org/wiki/Base64). codificada en base64.

## Estructura de archivos

* main.py: Programa principal.

### Paquete mvvm

Contiene código relacionado con el patrón de arquitectura [Modelo–vista–modelo de vista](https://es.wikipedia.org/wiki/Modelo%E2%80%93vista%E2%80%93modelo_de_vista).

* model.py: **Modelo**. Contiene funcionalidad relacionada con la base de datos (SQLite).

* viewmodel.py: **Modelo de vista**. Maneja las interacciones entre modelo y vista.

* view.py: **Vista**. Interfaz de usuario (PySide).

#### Carpeta sql

* createDatabase.sql: Crea una base de datos inicial con la información requerida.

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

## To-do

Solo para uso interno.

### Necesario

* [ ] Documentar el código hasta el commit 693bb7b (Esteban)

* [ ] Descuento de 10% para clientes frecuentes (más de 10 vuelos, 50% implementado; implementado en Model y ViewModel con la función get_flight_count(), falta implementarlo en View)

* [ ] Agregar límites de pasajeros y peso para cada avión y agregar validaciones correspondientes

* [ ] Mostrar una fecha de entrega para encomiendas al confirmar la reserva

* [ ] Agregar opción de obviar pago utilizando credenciales de gerente en vista de empleados (agregar callback functions)

* [ ] Permitir la modificación de valores en la vista de gerente y agregar validaciones correspondientes

* [ ] Agregar algoritmo de hora de salida

### No tan prioritario

* [ ] Agregar sistema de localización (borrar strings localizadas del código)

* [ ] Bloquear el tamaño de la ventana

* [ ] Hacer que todo ocurra en una sola ventana (puede chocar con n.º 3)

* [ ] Avisar de que solo se puede seleccionar una entrada para Gerente, posiblemente usando QTableWidget.selectedRanges() (dificultad: media)
