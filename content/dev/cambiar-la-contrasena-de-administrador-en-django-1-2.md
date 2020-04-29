Title: Cambiar la contraseña de administrador en Django 1.2
Date: 2011-02-16 14:11
Author: Nacho Cano
Tags: changepassword, check_passwd, django, manage.py, set_passwd
Slug: cambiar-la-contrasena-de-administrador-en-django-1-2

A partir de [Django 1.2][] se ha añadido el comando
`manage.py changepassword`.

    $ ./manage.py changepassword ['username']

Si no proporcionamos un nombre de usuario se intentará cambiar el nombre
de usuario que concuerde con el del usuario que ha iniciado sesión. Este
comando nos ahorra escribir lo siguiente:

    >>> from django.contrib.auth.models import User
    >>> u = User.objects.get(username__exact='john')
    >>> u.set_password('new password')
    >>> u.save()

![Django Admin Login]({static}/images/django-admin-login-300x171.png)

El usuario administrador es el primer usuario del sistema por lo que
podemos escribir:

    >>> from django.contrib.auth.models import User
    >>> u = User.objects.get(pk=1)
    >>> u.is_superuser
    True
    >>> u.username
    'bofh'
    >>> u.set_password('new password')
    >>> u.save()

Es importante usar `set_password` y no asignar la contraseña
directamente, ya que la contraseña se guarda con un formato que
`set_password`, y también `check_password`, gestiona correctamente. La
contraseña se guarda junto con el tipo de _hash_ y la _sal_, una cadena
aleatoria utilizada junto con la contraseña para crear el _hash_. Por
ejemplo,

    `sha1$a1976$a36cc8cbf81742a8fb52e221aaeab48ed7f58ab4`

  [Django 1.2]: https://pythonhosted.org/django_simple_feedback/topics/auth.html#changing-passwords
    "Nuevo comando changepassword en Django 1.2"
