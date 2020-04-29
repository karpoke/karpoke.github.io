Title: Actualización recursiva de un diccionario en Python
Date: 2010-09-28 13:50
Author: Nacho Cano
Tags: diccionario de datos, django, python, recursividad
Slug: actualizacion-recursiva-de-un-diccionario-en-python

Cuando actualizamos un diccionario con otro en Pyhton, el método `update` copia
las entradas del diccionario fuente en el diccionario destino, sobreescribiendo
las de éste si la entrada existe en ambos diccionarios.

En particular, si un diccionario contiene una entrada que es a su vez otro
diccionario, no se realiza una actualización sobre ésta, por lo que se pierden
los valores que no estuvieran en el diccionario fuente.

Ilustremos este comportamiento con un ejemplo:

    >>> d1 = {'a': 1, 'b': {'c': 3, 'd': 4}}
    >>> d2 = {'a': 11, 'b': {'c': 33}}
    >>> d1.update(d2)
    >>> print d1
    {'a': 11, 'b': {'c': 33}}

`d1` contiene a su vez un diccionario, `d1['b']`, y al realizar la
actualización hemos perdido el valor `d1['b']['d']`.

Nos podría interesar que, en lugar de sobreescribir cada entrada del
diccionario destino, compruebe primero si es un diccionario y realice una
actualización sobre éste.

    >>> def update_dict_r(dst, src):
    ...     """ updates a diccionary recursively, performing an updating on each
    ...          dictionary inside
    ...     """
    ...     for k, v in src.items():
    ...         if k in dst and isinstance(v, dict):
    ...             update_dict_r(dst[k], src[k])
    ...         else:
    ...             dst[k] = src[k]

    >>> d1 = {'a': 1, 'b': {'c': 3, 'd': 4}}
    >>> d2 = {'a': 11, 'b': {'c': 33}}
    >>> update_dict_r(d1, d2)
    >>> print d1
    {'a': 11, 'b': {'c': 33, 'd': 4}}

Ahora ya no no se ha sobreescrito el diccionario `d1['b']`, si no que se ha
realizado una actualización con el diccionario `d2['b']`, con lo que no hemos
perdido el valor de `d1['b']['d']`.

![sluggo recursive]({static}/images/sluggo-recursive-300x225.jpg "sluggo recursive")

Esto podemos utilizarlo, por ejemplo, en Django, para definir un diccionario
con datos por defecto, que sea sobreescrito con aquellos valores que queramos
personalizar.

En el archivo que mapea las direcciones, `urls.py`, tendremos algo como:

    info_dict = {
        'template_name': 'mymodel_paginated_list.html',
        'extra_context':{'paginate_by':2},
    }
    urlpatterns = patterns('',
        url(r'^$', mymodel_list, info_dict, name="myapp_mymodel_list"),
    }

Aquí le estamos pasando a la vista `mymodel_list` (que previsiblemente mostrará
una lista de los elementos de `mymodel`), una variable que queremos utilizar en
la plantilla, `paginate_by`.

Para la realizar la pagínación de una lista de elementos podemos utilizar la
aplicación `django-pagination`, con lo que la gestión de la paginación y la
navegación se vuelve increíblemente sencilla, necesitando únicamente añadir un
par de etiquetas a la plantilla. Una de estas etiquetas es `{% autopaginate
object_list paginate_by %}`, que, opcionalmente, admite como parámetro el
número de elementos por página.  De ahí que pasemos la variable `paginate_by`
en el `extra_context` y no como como parámetro de la vista.

Ahora, si queremos que pasar este valor sea opcional, necesitamos especificar
un valor por defecto, antes de renderizar la plantilla. En la vista, dentro del
fichero `views.py`, tendremos algo como:

    from django.views.generic.list_detail import object_list
    def mymodel_list(request, **info_dict):
        """ Returns a paginated list of the model elements """
        default_dict = {
            'queryset': Mymodel.objects.all(),
            'template_name': 'myapp_list.html',
            'extra_context': {
                'paginate_by': settings.PAGINATE_BY,
                'other': 'other vars',
            }
        }
        default_dict.update(info_dict)
        return object_list(request, **default_dict)

De esta forma, perdemos el valor de `others`, dentro de `extra_context`. Si
además este valor se utiliza, por ejemplo, en un `tag`, obtendremos una bonita
excepción `Caught KeyError while rendering: 'other'`.

Una solución sería utilizar la función que hemos definido antes para actualizar
el diccionario recursivamente, y en lugar de poner:

    default_dict.update(info_dict)

pondremos:

    update_dict_r(default_dict, info_dict)
