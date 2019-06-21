Title: Envenenamiento de cabeceras en Django 1.3 y 1.4
Date: 2012-10-28 12:57
Author: Nacho Cano
Slug: envenenamiento-de-cabeceras-en-django-1-3-y-1-4

> Django, framework de desarrollo web basado en Python ha actualizado
> las ramas 1.3 y 1.4 para dar solución a una vulnerabilidad que podría,
> mediante técnicas de envenenamiento de cabeceras (”Header poisoning”),
> redireccionar a un usuario a un sitio malicioso o incluso el robo de
> credenciales.
>
> Para realizar algunas operaciones, Django extrae el nombre del dominio
> de la cabecera ”Host” enviada. La vulnerabilidad (CVE-2012-4520)
> reside en el parser del método django.http.HttpRequest.get_host(),
> que extrae esta cabecera ”Host” incorrectamente.

- Antonio Sánchez | [unaaldia.hispasec.com][]

  [unaaldia.hispasec.com]: http://unaaldia.hispasec.com/2012/10/envenenamiento-de-cabeceras-en-django.html
    "Envenenamiento de cabeceras en Django 1.3 y 1.4"
