Title: Symfony en Ubuntu Lucid Lynx 10.04
Date: 2012-06-03 03:59
Author: Nacho Cano
Tags: 10.04, apache, csrf, framework, lampp, mvc, mysql, php, symfony, ubuntu lucid lynx, xss
Slug: symfony-en-ubuntu-lucid-lynx-10-04
Related: mejorando-la-seguridad-de-apache-con-varnish

[Symfony][] es una _framework_ MVC escrito en PHP para el desarrollo
rápido de páginas web. Además, ofrece un conjunto de buenas prácticas
para desarrollar páginas más seguras y con un coste de mantenimiento
menor.

Para que la instalación sea más segura, los ficheros de Symfony debería
estar fuera del `DocumentRoot`.


Requisitos
----------

Symfony se basa en entorno LAMPP, por lo que suponemos que ya tenemos
configurado Apache, MySQL y PHP versión 5.2.4 o superior. Para comprobar
si todo está correctamente configurado y que cumplimos los
requerimientos para Symfony, descargamos siguiente _script_ y lo
ejecutamos, pasando como parámetro la ruta al archivo `php.ini` que
utiliza apache (por defecto, al ejecutarlo desde el terminal en lugar
del navegador, utiliza otro archivo `php.ini`):

```bash
$ wget http://sf-to.org/1.4/check.php
$ php --php-ini /etc/php5/apache2/php.ini check.php
__****************************__
_                              _
_  symfony requirements check  _
_                              _
__****************************__

php.ini used by PHP: /etc/php5/apache2/php.ini

__ WARNING __
*  The PHP CLI can use a different php.ini file
*  than the one used with your web server.
*  If this is the case, please launch this
*  utility from your web server.
__ WARNING __

__ Mandatory requirements __

  OK        PHP version is at least 5.2.4 (5.3.2-1ubuntu4.15)

__ Optional checks __

  OK        PDO is installed
  OK        PDO has some drivers installed: mysql, sqlite, sqlite2
  OK        PHP-XML module is installed
  OK        XSL module is installed
  OK        The token_get_all() function is available
  OK        The mb_strlen() function is available
  OK        The iconv() function is available
  OK        The utf8_decode() is available
  OK        The posix_isatty() is available
  OK        A PHP accelerator is installed
  OK        php.ini has short_open_tag set to off
  OK        php.ini has magic_quotes_gpc set to off
  OK        php.ini has register_globals set to off
  OK        php.ini has session.auto_start set to off
  OK        PHP version is not 5.2.9
```

Corregimos los errores que nos dé, si es que ya sea editando la
configuración de `php.ini` o instalando paquetes que nos pudieran faltar
(como, por ejemplo, `php-xml-parser`, `php5-xsl` o `php-apc`).

Si queremos, podemos copiar el archivo al `DocumentRoot` y abrirlo
mediante el navegador, para estar seguros de que no hay ningún problema,
y acto seguido lo borramos.

Instalación
-----------

Como hemos comentado al principio, colocaremos los ficheros de Symfony
fuera del `DocumentRoot`. Crearemos el directorio para alojar los
proyectos y, dentro de él, el directorio para el primer proyecto:

```bash
$ mkdir -p /home/sfprojects/sfproject
$ cd /home/sfprojects/sfproject
```

Hay dos versiones principales de Symfony, la 1.4, versión estable con
soporte hasta finales de este año, y la 2.0, que será la próxima versión
principal. Utilizaremos la 1.4.

A la hora de instalar Symfony, podemos hacerlo de forma global, para
todo el sistema, o local, independiente para cada proyecto. La segunda
es más recomendable, sobre todo si vamos a tener varios proyectos. De
esta forma, la actualización de uno no afectará al resto.

Se considera una buena práctica instalar Symfony en el directorio
`lib/vendor` dentro del directorio raíz del proyecto, así que lo creamos
primero:

```bash
$ mkdir -p lib/vendor
```

Instalaremos la versión estable actual de Symfony desde el repositorio
subversion:

```bash
$ svn checkout http://svn.symfony-project.com/tags/RELEASE_1_4_18 symfony
```

Cuando salga una nueva versión, podremos actualizar cambiando
simplemente la URL del repositorio. También podríamos utilizar la
versión en desarrollo, con lo que incluiríamos las correcciones de
errores con sólo actualizar la copia de trabajo.

Creación de un proyecto
-----------------------

Desde el directorio que habíamos creado para el proyecto,
`/home/sfprojects/sfproject`, creamos el proyecto con Symfony, de nombre
sfproject, mediante la tarea `generate:project`:

```bash
$ cd /home/sfprojects/sfproject
$ php lib/vendor/symfony/data/bin/symfony generate:project sfproject
```

Esta tarea crea la estructura de directorios:

```bash
apps/       Contiene las aplicaciones del proyecto
cache/      Ficheros cacheados
config/     Ficheros de configuración del proyecto
data/       Ficheros con datos iniciales (fixtures)
lib/        Bibliotecas y clases del proyecto
log/        Ficheros de log
plugins/    Plugins instalados
test/       Ficheros con los tests unitarios y funcionales
web/        El directorio raíz de la página web
```

Cambiamos los permisos para los directorios `cache` y `log`. Estos son
los únicos directorios en los que necesita escribir Symfony para
comenzar:

```bash
$ chmod 777 cache log
```

La tarea, además, crea un acceso directo a
`lib/vendor/symfony/data/bin/symfony` en el directorio del proyecto,
para que sea más sencillo y rápido llamar al fichero.

Para comprobar que la instalación es correcta, ejecutamos:

```bash
$ ./symfony -V
symfony version 1.4.18 (/home/sfproject/lib/vendor/symfony/lib)
```

Nos aseguramos que en el archivo de configuración del proyecto,
`config/ProjectConfiguration.class.php`, no hay una ruta absoluta sino
relativa, con lo que podremos mover de lugar el directorio del proyecto
sin que nada deje de funcionar:

```bash
require_once dirname(__FILE__).'/../lib/vendor/symfony/lib/autoload/sfCoreAutoload.class.php';
```

Podemos ver una lista de opciones que nos ofrece el comando `symfony`,
ejecutándolo sin ningún parámetro.

Base de datos
-------------

Antes de continuar, crearemos una base de datos específica para este
proyecto y un usuario con privilegios únicamente para esta base de
datos. Por ejemplo, si utilizamos MySQL:

```bash
$ mysql -uroot -p
mysql> CREATE DATABASE sfproject;
mysql> CREATE USER 'sfproject'@'localhost' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON sfproject.* TO 'sfproject'@'localhost';
mysql> FLUSH PRIVILEGES;
```

Symfony puede trabajar con diferentes bases de datos gracias a PDO
(extensión para la abstracción de acceso a los datos). Para trabajar con
PDO puede utilizaz dos herramientas: Doctrine, por defecto cuando
creamos un proyecto, y Propel.

Para configurar la base de datos ejecutamos:

```bash
$ ./symfony configure:database "mysql:host=localhost;dbname=sfproject" sfproject password
```

Si no queremos escribir la contraseña en el terminal, para que no quede
registrada en el historial, podemos omitirla y luego editar el fichero
`config/databases.yml`. Una razón para tener el directorio del proyecto
fuera del `DocumentRoot` es evitar que este archivo llegue a ser
accesible.

Creación de una aplicación
--------------------------

Para crear la aplicación _frontend_ utilizaremos la tarea
`generate:app`, desde el directorio raíz del proyecto:

```bash
$ ./symfony generate:app frontend
```

Esta tarea crea la siguiente estructura dentro del directorio
`apps/frontend`:

```bash
config/    Contiene los ficheros de configuración de la aplicación
lib/       Contiene las bibliotecas y las clases de la aplicación
modules/   Contiene el código de la aplicación (MVC)
templates/ Contiene las plantillas globales
```

Por defecto, Symfony nos protege de dos de las vulnerabilidades más
extendidas en la web: XSS, escapando el contenido mostrado, y CSRF,
creando un código CSRF aleatorio.

Configuración del servidor
--------------------------

En el `DocumentRoot` sólo deberían estar los ficheros que deban poder
ser accedidos por el servidor web, como imágenes, hojas de estilo y
Javascripts.

Creamos el fichero de configuración del sitio,
`/etc/apache2/sites-available/sfproject.domain.tld`:

```bash

  ServerName sfproject.domain.tld
  DocumentRoot "/home/sfprojects/sfproject/web"
  DirectoryIndex index.php

    AllowOverride All
    Allow from All


  Alias /sf /home/sfprojects/sfproject/lib/vendor/symfony/data/web/sf

    AllowOverride All
    Allow from All

```

Si no tenemos configurado el dominio sfproject.domain.tld, podemos crear
un alias en el fichero `/etc/hosts`:

```bash
127.0.0.1  sfproject.domain.tld
```

El alias `sf` sirve para acceder a las imágenes, hojas de estilo y
Javascripts de Symfony, necesarios para mostrar correctamente las
páginas por defecto.

Activamos el sitio y reiniciamos apache:

```bash
$ sudo a2ensite sfproject.domain.tld
$ sudo apache2ctl restart
```

Si todo ha ido bien, introducimos
`http://sfproject.domain.tld/index.php/` en el navegador y veremos el
mensaje de bienvenido. Si tenemos activado `mod_rewrite` no será
necesario poner `index.php`. Para acceder al entorno de desarrollo dela
aplicación que hemos creado ponemos
`http://sfproject.domain.tld/frontend_dev.php/`.

Entornos
--------

Dentro del directorio `web/` hay dos ficheros PHP, `index.php` y
`frontend_dev.php`. A estos ficheros se les llama _front controllers_.
Todas las peticiones a la aplicación se hacen a través de ellos. Ambos
apuntan a la misma aplicación, pero en diferentes entornos.

Cuando se desarrolla una aplicación se necesitan varios entornos:

-   desarrollo: utilizado por los programadores para añadir
    características, arreglar fallos, etc
-   test: utilizado para realizar los tests de forma automática
-   _staging_: utilizado por el cliente para probar la aplicación y
    reportar fallos o características que falten
-   producción: utilizado por los usuarios finales

Cada entorno tiene características diferentes. El de desarrollo está
enfocado a los programadores, la aplicación registra todo tipo de
detalles para facilitar la depuración, se deshabilita la caché para que
los cambios tengan efecto de forma inmediata, cuando ocurre un error,
Symfony muestra información detallada, etc. En producción, la caché está
activada, se personalizan los mensajes de error y se optimiza para
mejorar la experiencia de usuario.

Referencias
-----------

» [Symfony: getting started][]

  [Symfony]: http://www.symfony-project.org/
    "Symfony"
  [Symfony: getting started]: http://www.symfony-project.org/getting-started/1_4/en/
    "Symfony: getting started"
