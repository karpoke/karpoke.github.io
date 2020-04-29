Title: Control de concurrencia optimista en Django
Date: 2010-11-05 18:11
Author: Nacho Cano
Tags: condición de carrera, control de concurrencia optimista, django, métodos perezosos
Slug: control-de-concurrencia-optimista-en-django

Si tenemos una aplicación multiusuario, podría darse el caso de que dos
usuarios accediesen simultáneamente al mismo registro para editarlo. Si
no controlamos este evento, sucederá que el primero que guarde, que no
tiene porqué ser el primero que comenzó a editar, perderá los cambios, y
lo que es peor, sin enterarse.

Una solución sería utilizar [transacciones][] [1], pero éstas deberían
abarcar varias peticiones HTTP, desde que se empieza a editar hasta que
se guarda satisfactoriamente (o no), con lo que la solución idónea se
complica. Una solución más sencilla, pero efectiva en la inmensa mayoría
de casos, es utilizar el [control de concurrencia optimista][] (también
comentado en [slashdot][]).

El control de concurrencia optimista se basa en el hecho de que es
bastante improbable que la edición concurrente se dé, por lo que la
solución más sencilla pasa por detectarla y avisar al usuario en caso de
que ocurra, obligándole a repetir el proceso de edición. La simplicidad
de la solución unida a la baja probabilidad de que suceda hacen de ella
una solución interesante y práctica. Lo de la baja probabilidad es
importante, ya que si los usuarios tuvieran que estar constantemente
repitiendo el proceso de edición dejaría de ser una solución práctica.

Para implementarla, necesitamos conocer si el registro que estamos
editando ha sido modificado desde la última vez que accedimos a él.
Podemos lograr esto incluyendo un campo que contenga un número de
versión, que se incrementa con cada edición. Si a la hora de guardar, el
número de versión no es el mismo que había cuando nosotros accedimos al
registro, es que alguien se nos ha adelantado. En lugar de un número de
versión, también podemos utilizar un campo _timestamp_. La ventaja de
éste último es que podemos definir el campo con la opción
`auto_now=True` y nos olvidamos de tener que actualizarlo, ya que ya lo
hacer Django por nosotros.

El siguiente ejemplo, proporcionado por Andrei Savu, muestra la idea:

    updated = Entry.objects.filter(Q(id=e.id) && Q(version=e.version))
             .update(updated_field=new_value, version=e.version+1)
    if not updated:
        raise ConcurrentModificationException()

La operación se realiza de forma atómica, ya que `filter` es un [método
_perezoso_][], es decir, no implica un operación de base de datos
inmediatamente.

[Otra solución][] propuesta consiste en sobreescribir el método `save`
para comprobar si el registro ha sido modificado justo antes de
guardarlo (en lugar de filtrar y actualizar):

    def save(self):
        if(self.id):
            foo = Foo.objects.get(pk=self.id)
            if(foo.timestamp > self.timestamp):
                raise Exception, "trying to save outdated Foo"
        super(Foo, self).save()

Sin embargo, esta solución presenta un problema de condición de carrera.
La operación de consultar el último valor y la operación de guardar no
se realizan de forma atómica, por lo que podría darse el caso de que
ambos guardasen a la vez y el sistema ejecutara las instrucciones de tal
manera (alternativamente, para ser más concretos) que cada uno pensaría
que había sido el último en guardar, por lo que el segundo
sobreescribiría al primero, pero sin que a éste se le notificara.

[1] Existe una aplicación para Django, [django-locking][], que nos
brinda el control de concurrencia, permitiendo, además, que los usuarios
sepan si un registro ha sido bloqueado, e incluso que les permita
acceder en modo de sólo lectura.

  [transacciones]: http://docs.djangoproject.com/en/dev/topics/db/transactions/
    "transacciones"
  [control de concurrencia optimista]: http://stackoverflow.com/questions/320096/django-how-can-i-protect-against-concurrent-modification-of-data-base-entries
    "control de concurrencia optimista"
  [slashdot]: http://hardware.slashdot.org/comments.pl?sid=1381511&cid=29536367
    "slashdot"
  [método _perezoso_]: http://docs.djangoproject.com/en/dev/topics/db/queries/
    "método _perezoso_"
  [Otra solución]: http://stackoverflow.com/questions/1645269/concurrency-control-in-django-model
    "Otra solución"
  [django-locking]: http://stdbrouw.github.com/django-locking/
    "django-locking"
