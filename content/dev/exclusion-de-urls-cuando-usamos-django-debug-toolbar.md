Title: Exclusión de URLs cuando usamos django-debug-toolbar
Date: 2014-05-15 20:10
Author: Nacho Cano
Tags: django, django-debug-toolbar
Slug: exclusion-de-urls-cuando-usamos-django-debug-toolbar

[django-debug-toolbar][] es una aplicación para Django que nos muestra
información de depuración acerca de las diferentes peticiones y
respuestas que se llevan a cabo en el servidor: variables de contexto,
cabeceras, peticiones SQL, etc.

Sin embargo, hay algunas URLs para las cuales nos puede interesar que no
se analicen, como por ejemplo, peticiones que se hagan por Ajax o URLs
relativas a diversas aplicaciones instaladas, como el panel de
administración, Rosetta, etc.

Una forma sencilla de lograr esto es utilizando la variable de
configuración [SHOW_TOOLBAR_CALLBACK][], la cual debe apuntar a la
función que determine si se debe mostrar la barra o no (por defecto, se
comprueba el valor de la variable DEBUG).

Por ejemplo, si no queremos mostrar la barra para diferentes URLs, hasta
la versión 1.0, podemos hacer lo siguiente:

```python
def show_toolbar(request):
    for url in DEBUG_TOOLBAR_CONFIG["IGNORE_URIS"]:
        if re.search(url, request.path):
            return False
    return True

DEBUG_TOOLBAR_CONFIG = {
    'IGNORE_URIS': (
        '^/admin',
        '^/rosetta',
    ),
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}
```

[A partir de la versión 1.0][], el nombre de la función se debe
especificar como una ruta separada por puntos:

```bash
    'SHOW_TOOLBAR_CALLBACK': 'projectname.settings.show_toolbar',
```

  [django-debug-toolbar]: http://github.com/django-debug-toolbar/django-debug-toolbar
    "django-debug-toolbar"
  [SHOW_TOOLBAR_CALLBACK]: http://django-debug-toolbar.readthedocs.org/en/1.2/configuration.html
    "SHOW_TOOLBAR_CALLBACK"
  [A partir de la versión 1.0]: http://stackoverflow.com/questions/20726257/django-v1-6-debug-toolbar-middleware-error-no-rsplit/20727979#20727979
    "A partir de la versión 1.0"
