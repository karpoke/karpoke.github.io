Title: La infame actualización de WordPress en 15 segundos
Date: 2010-12-30 04:21
Author: Nacho Cano
Tags: actualización, copia de seguridad, gzip, mysqldump, tar, wordpress
Slug: la-infame-actualizacion-de-wordpress-en-15-segundos

1.  __Copia de respaldo de la base de datos__. Entre el flag `-u` y el
    nombre de usuario no debe haber ningún espacio. Ojo, se bloquearán
    las tablas hasta que termine. Y otro ojo, no es muy recomendable
    escribir la contraseña directamente en la línea de comandos. Si sólo
    ponemos el flag `-p`, se nos pedirá la contraseña para el usuario
    proporcionado.

        $ /usr/bin/mysqldump -uuser -p --all-databases | gzip > mysql-$(date +%F).tgz

2.  __Copia de respaldo de los archivos__. Tanto del directorio
    `wp-uploads` como del directorio `wordpress`.

        $ tar -cvzf wordpress-$(date +%F).tgz /usr/share/wordpress
    $ tar -cvzf wp-uploads-$(date +%F).tgz /var/www/wp-uploads

3.  __Desactivamos todos los *plugins*__ desde el panel de control.
4.  __Eliminamos los subdirectorios__ `wp-admin` y `wp-includes`.

        $ cd /usr/share/wordpress
    $ sudo rm -fr wp-admin wp-includes

5.  __Instalamos__ la última versión.

        $ wget -NP /tmp http://wordpress.org/latest.zip
    $ sudo unzip /tmp/latest.zip -d /usr/share # yes to [A]ll

6.  Comprobamos si se debe __actualizar la base de datos de WordPress__.
    En principio, basta ir al panel de administración y ahí nos
    aparecerá un mensaje diciéndonos que es necesario actualizar la base
    de datos y que visitemos la página `/wp-admin/upgrade.php` para
    realizar dicha actualización.

En una sola línea:

    $ /usr/bin/mysqldump -uuser -p --all-databases | gzip > mysql-$(date +%F).tgz && tar -cvzf wordpress-$(date +%F).tgz /usr/share/wordpress && tar -cvzf wp-uploads-$(date +%F).tgz /var/www/wp-uploads && cd /usr/share/wordpress && sudo rm -fr wp-admin wp-includes && wget -NP /tmp http://wordpress.org/latest.zip && sudo unzip /tmp/latest.zip -d /usr/share

- más info: [Actualizando WordPress][]

* * * * *

#### Actualizado el 31 de diciembre de 2010

5 segundos más para actualizar las traducciones, debemos especificar el número
de versión y el idioma. Por ejemplo:

    $ wget -NP /tmp http://es.wordpress.org/wordpress-3.0.4-es_ES.zip
    $ sudo unzip /tmp/wordpress-3.0.4-es_ES.zip -d /usr/share # yes to [A]ll

* * * * *

  [Actualizando WordPress]: http://codex.wordpress.org/Updating_WordPress
    "Actualizando WordPress"
