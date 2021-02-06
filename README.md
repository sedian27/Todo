Este es mi primer proyecto realizado en python.

# Pasos:
## Para inicializar el proyecto primero realiza los siguientes pasos:

***Si usas linux o MAC cambia el set por export***
* ve a la carpeta venv/Scripts y inicializa activate.bat
* regresa al inicio y utiliza los siguientes comandos para la conexion a la base de datos:

```
    set FLASK_DATABASE_HOST=tu servidor.
    set FLASK_DATABASE_PASSWORD=tu contraseña.
    set FLASK_DATABASE_USER='tu usuario'.
    set FLASK_DATABASE=base de datos.
```
* Especificamos a flask que cargaremos nuestro proyecto con:
```
    set FLASK_APP=todo
```
* Para que nos lo ejecute cómo desarrollador tambien le decimos:
```
    set FLASK_ENV=development
```
* Utiliza este comando para la creación de la base de datos:
  
  **¡si ya tienes la base de datos hecha no lo hagas!**
```
    flask init-db
```
* Para iniciar el proyecto debemos ejecutar lo siguiente:
```
    flask run
```