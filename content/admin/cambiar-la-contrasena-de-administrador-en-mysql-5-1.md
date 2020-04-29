Title: Cambiar la contraseña de administrador en MySQL 5.1
Date: 2011-07-08 04:10
Author: Nacho Cano
Tags: apparmor, cambiar contraseña, mysql, mysqld, mysqld_safe, root, syslog, ubuntu
Slug: cambiar-la-contrasena-de-administrador-en-mysql-5-1

Para [cambiar la contraseña de administrador en MySQL][] podemos iniciar
el servicio utilizando los argumentos `--skip-grant-tables`, que permite
iniciar el servicio sin tener en cuenta los privilegios del sistema, por
lo que no es seguro, y el flag `--skip-networing`, que deshabilita las
conexiones remotas pero no se lo impide a las locales, que seguirán
teniendo acceso y lo harán como `root`, por lo que tampoco es seguro.
Antes de ver cómo podemos hacerlo de otra manera, veremos cómo hacerlo
con este método, que funciona siempre.


Método genérico
---------------

Paramos el servicio y lo iniciamos con los mencionados argumentos:

    $ sudo service mysql stop
    $ sudo mysqld --skip-grant-tables --skip-networking &

Lanzamos el cliente de `mysql` y cambiamos la contraseña:

    $ mysql
    mysql> UPDATE mysql.user SET Password=PASSWORD('contraseña') WHERE User='root';
    Query OK, 2 rows affected (0.03 sec)
    Rows matched: 2  Changed: 2  Warnings: 0
    mysql> FLUSH PRIVILEGES;
    Query OK, 0 rows affected (0.00 sec)
    mysql> exit

Reiniciamos el servicio y probamos la nueva contraseña:

    $ sudo service mysql restart
    $ mysql -uroot -p

Método mediante un fichero cargado al iniciar el servicio
---------------------------------------------------------

Por los motivos de seguridad descritos, lo mejor es lanzar el servicio
[indicándole que ejecute un archivo][] que contendrá el código para
cambiar la contraseña:

Paramos el servicio:

    $ sudo service mysqld stop

Creamos un archivo, por ejemplo `~/mysql-init`, que contenga lo
siguiente:

    UPDATE mysql.user SET Password=PASSWORD('contraseña') WHERE User='root';
    FLUSH PRIVILEGES;

Iniciamos el servicio en modo seguro, que carga el archivo que acabamos
de crear y le indicamos que lo haga como el usuario `mysql`. Si no le
indicamos el usuario `mysql`, es posible que se modifique el propietario
de algunos ficheros a `root`, por ejemplo ficheros de _log_, y que esto
cause problemas.

    $ sudo mysqld_safe --init-file=~/mysql-init --user=mysql &

Si todo ha ido bien, podremos conectarnos con la nueva contraseña:

    $ mysql -uroot -p

Ahora, matamos el servicio (sin usar el argumento `-9`) y lo volvemos a
iniciar normalmente:

    $ pgrep mysqld
    25825
    $ sudo kill 25825
    $ sudo service mysql start

Problemas y `apparmor`
----------------------

Si no podemos conectarnos y tenemos una Ubuntu, es posible que sea
[debido a `apparmor`][debido a apparmor]. Lo podremos confirmar sin encontramos algo
parecido a esto en `/var/log/syslog`:

    Jul  8 11:09:26 hostname kernel: [11386.395693] type=1400 audit(1310288966.659:41): apparmor="DENIED" operation="open" parent=8723 profile="/usr/sbin/mysqld" name="/home/user/mysql-init" pid=8837 comm="mysqld" requested_mask="r" denied_mask="r" fsuid=113 ouid=0

Para solucionarlo, editamos el fichero `/etc/apparmor.d/usr.sbin.mysqld`
y añadimos la ruta a nuestro directorio de usuario:

    /home/user/ r,
    /home/user/** rwk,

Reiniciamos `apparmor` para que tenga en cuenta este cambio:

    $ sudo service apparmor restart

Volvemos a probar:

    $ sudo mysqld_safe --init-file=~/mysql-init --user=mysql &

Probamos de nuevo:

    $ mysql -uroot -p

Si todo ha ido bien, ya podemos matar el servicio `mysqld` y arrancarlo
normalmente, eliminar el archivo `~/mysql-init`, eliminar los cambios
hechos en la configuración de `apparmor` y reiniciar éste para que
tengan efecto.

  [cambiar la contraseña de administrador en MySQL]: http://dev.mysql.com/doc/refman/5.1/en/resetting-permissions.html#resetting-permissions-generic
    "cambiar la contraseña de administrador en MySQL"
  [indicándole que ejecute un archivo]: http://dev.mysql.com/doc/refman/5.1/en/resetting-permissions.html#resetting-permissions-unix
    "indicándole que ejecute un archivo"
  [debido a apparmor]: http://www.debianadmin.com/mysql-database-server-installation-and-configuration-in-ubuntu.html/comment-page-1#comment-111
    "debido a `apparmor`"
