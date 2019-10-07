Title: Buscar en todos los campos de un modelo en Django
Date: 2010-11-19 20:49
Author: Nacho Cano
Tags: buscador, django, introspección
Slug: buscar-en-todos-los-campos-de-un-modelo-en-django
Summary: Una acción típica que se va a repetir en, prácticamente, cada listado que mostremos, es la de añadir un buscador.

Una acción típica que se va a repetir en, prácticamente, cada listado
que mostremos, es la de añadir un buscador [1]. Un buscador típico
incluirá un pequeño formulario en la misma página de listado:

```html
<form method="get" action="">
    <input type="text" name="q" value="{{ q }}" />
    <input type="submit" value="Search" />
</form>
```

Nos interesaría no tener que ir copiando y pengando este código en cada
listado. Aunque sea un código que no vaya a cambiar, viola el principio
de DRY.

Una mejor solución pasa por crear un _templatetag_, en el fichero
`my_tags.py` dentro del directorio `templatetags`:

```python
@register.inclusion_tag('search_form.html', takes_context=True)
def display_search_form(context):
    return {
        'q': context['q'],
    }
```

`search_forml.html` es la plantilla HTML que contiene el formulario
mostrado arriba. Mediante el decorador `register.inclusion_tag`
permitimos que a la plantilla HTML le llegue la variable `q` del
contexto, que contiene la búsqueda.

Y luego, en la plantilla del listado, incluimos el _templatetag_

```python
{% load my_tags %}
```

Allá donde queramos que aparezca el buscador incluiremos lo siguiente:

```python
{% display_search_form %}
```

Sólo queda ver el contenido de la vista que muestra el listado. En
particular, deberemos recoger la variable `q` que nos puede llegar por
`GET`. Algo así:

```python
q = request.GET.get("q", "")
```

Antes de modificar la consulta para filtrar los resultados que
concuerden con nuestra búsqueda, hay diferentes aspectos que deberíamos
tener en cuenta referentes a las búsquedas.

Lo primero es sobre qué vamos a buscar, es decir, sobre qué campos del
modelo que vamos a buscar. Pero también podríamos tener una serie de
palabras clave asociadas y guardadas en otro modelo qué también nos
gustaría que se tuvieran en cuenta en la búsqueda. O podríamos buscar,
para cada clave foránea, en los campos de ese modelo.

Lo siguiente es cómo interpretar esa búsqueda. Podríamos buscar una
coincidencia exacta de todo lo que hemos buscado, que debería coincidir
con, o estar contenida en, el contenido de un campo. También podríamos
realizar una búsqueda más elaborada, separando la búsqueda en palabras.
o añadir modificadores, estilo Google, para, por ejemplo, excluir
palabras.

Utilizaremos el [código publicado por Julien Phalip][] para realizar
esta búsqueda de forma que nos sirva para lo que pretendemos. El método
de Julien separa las palabras de la búsqueda para montar un `query` que
utiliza para filtrar el resultado según la lista de campos
proporcionada. Nos basaremos en este método para extender la búsqueda a
todos los campos del modelo y los campos de los modelos referenciados
por las claves foráneas de éste.

```python
def get_full_query(query_string, model):
    """ Returns a query to search in every field of the given model """
    fields = []
    for f in model._meta.fields:
        if not f.rel:
            fields.append(f.name)
        else:
            rel_fields = [ "%s__%s" % (f.name, fr.name) for fr in f.rel.to._meta.fields if not fr.rel ]
            fields.extend(rel_fields)
    return get_query(query_string, fields)
```

`model._meta.fields` devuelve, como su nombre indica, un listado con los
campos del modelo. Cada campo tiene, entre otros, los atributos `name`,
con el nombre del campo, y `rel`, que, en el caso de una clave foránea,
contiene el modelo al que hace referencia.

En la vista del listado tendremos:

```python
queryset = MyTable._default_manager.all() # [2]
if q:
    query = get_full_query(q, MyTable)
    queryset = queryset.filter(query)
```

Este `queryset` contiene el listado que le pasamos a la plantilla:

```python
return render_to_response("my_list.html",
    {
        "object_list": queryset,
        "q": q,
    },
    context_instance=RequestContext(request))
```

» [1] Existen aplicaciones para realizar búsquedas, como [haystack][]
    o `django-sphinx`.
» [2] Según James Bennett, en "Django practical projects", utilizar
    `_default_manager` en lugar de `objects` es una buena práctica, ya
    que podría ser que el modelo tuviera un _manager_ personalizado.
    Utilizar `_default_manager` siempre es seguro.

  [código publicado por Julien Phalip]: http://www.julienphalip.com/blog/2008/08/16/adding-search-django-site-snap/
    "código publicado por Julien Phalip"
  [haystack]: http://haystacksearch.org/
    "haystack"
