# Biblioteca Django

Una aplicación web de gestión de biblioteca construida con Django y Django REST Framework, con interfaz profesional basada en Bootstrap, roles de usuario, préstamos/devoluciones, autocomplete en búsqueda y despliegue en Heroku.

## Características

* CRUD completo de libros con permisos (administradores vs. usuarios regulares).
* Sistema de préstamo y devolución de libros.
* Autenticación y autorización con roles (`administrador`, `usuario_regular`).
* Interfaz responsiva con Bootstrap 5 y Bootstrap Icons.
* Buscador con autocompletado (typeahead) vía API REST.
* API RESTful (CRUD y acciones personalizadas) documentada y probada con Postman.
* Despliegue fácil en Heroku con Gunicorn y WhiteNoise.

## Requisitos

* Python 3.8+
* pip
* virtualenv (recomendado)
* Git
* Cuenta en Heroku (para despliegue)

## Instalación local

```bash
# 1. Clonar el repositorio
git clone git@github.com:TU_USUARIO/biblioteca-django.git
cd biblioteca-django

# 2. Crear y activar el entorno virtual
python3 -m venv env
source env/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Configuración de variables de entorno

Crea un archivo `.env` en la raíz con:

```ini
# Django
SECRET_KEY=tu_secret_key_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos en producción (Heroku)
DATABASE_URL=postgres://user:pass@host:port/dbname
```

> Usa [python-decouple](https://github.com/henriquebastos/python-decouple) o `django-environ` para cargar estas variables en `settings.py`.

## Migraciones y superusuario

```bash
# Migrar modelos
python manage.py migrate

# Crear superusuario (administrador)
python manage.py createsuperuser
```

## Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Abre [http://127.0.0.1:8000/](http://127.0.0.1:8000/) y accede con tu cuenta.

## Uso de la interfaz

* **Listado de libros**: `/libros/`
* **Detalle**: `/libros/{id}/`
* **Crear/Editar/Borrar** (solo administradores)
* **Préstamo/Devolución** (solo usuarios regulares)
* **Mis prestados**: `/mis-prestados/`
* **Login/Logout**: `/login/`, `/logout/`

## API REST

Base: `/api/libros/`

| Método | Ruta                           | Descripción      | Permisos                         |
| ------ | ------------------------------ | ---------------- | -------------------------------- |
| GET    | `/api/libros/`                 | Listar libros    | Abierto (cualquiera autenticado) |
| GET    | `/api/libros/{id}/`            | Detalle de libro | Abierto                          |
| POST   | `/api/libros/`                 | Crear libro      | Administrador                    |
| PUT    | `/api/libros/{id}/`            | Actualizar libro | Administrador                    |
| DELETE | `/api/libros/{id}/`            | Eliminar libro   | Administrador                    |
| POST   | `/api/libros/{id}/prestamo/`   | Tomar prestado   | Usuario regular                  |
| POST   | `/api/libros/{id}/devolucion/` | Devolver libro   | Usuario regular                  |

> Puedes probarla con la **Browsable API** o importar la colección de Postman (`postman_collection.json`).

## Despliegue en Heroku

1. Añade `Procfile`:

   ```procfile
   web: gunicorn biblioteca.wsgi --log-file -
   ```
2. Configura `settings.py`:

   * `DEBUG=False`
   * `ALLOWED_HOSTS=['tu-app.herokuapp.com']`
   * `STATIC_ROOT` y WhiteNoise
3. Genera `requirements.txt`:

   ```bash
   pip freeze > requirements.txt
   ```
4. Commitea y push:

   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py collectstatic --noinput
   ```
5. Asegura tus **Config Vars** en Heroku: `SECRET_KEY`, `DEBUG=False`, `DATABASE_URL`.

## Pruebas

```bash
python manage.py test
```

## Postman

Importa `postman_collection.json` para probar todos los endpoints.

## License

Este proyecto está bajo la licencia MIT. ¡Contribuciones bienvenidas!
