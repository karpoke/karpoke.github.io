Title: Instalando MySQL Workbench desde el código fuente en Ubuntu Oneiric Ocelot
Date: 2012-01-10 16:16
Author: Nacho Cano
Tags: 11.10, código fuente, msql workbench, ubuntu oneiric ocelot
Slug: instalando-mysql-workbench-desde-el-codigo-fuente-en-ubuntu-oneiric-ocelot

[MySQL Workbench][] es una herramienta que permite diseñar y administrar
una base de datos MySQL y proporciona herramientas para la configuración
del servidor y la administración de los usuarios.

MySQL Workbench no se encuentra en los repositorios de Ubuntu, y desde
la [página de descargas][] todavía no hay un paquete para Ubuntu Oneiric
Ocelot (11.10).


Instalación
-----------

Para instalar MySQL Workbench, primero nos bajamos el código fuente.
Ahora mismo, la última versión es la 5.2.37.

    $ wget http://dev.mysql.com/get/Downloads/MySQLGUITools/mysql-workbench-gpl-5.2.37-src.tar.gz/from/ftp://ftp.inria.fr/pub/MySQL/

Comprobamos el fichero:

    $ md5sum mysql-workbench-gpl-5.2.37-src.tar.gz
    c7301f078834512538353ee3ce2cf460  mysql-workbench-gpl-5.2.37-src.tar.gz

Los descomprimimos:

    $ tar xvzf mysql-workbench-gpl-5.2.37-src.tar.gz
    $ cd mysql-workbench-gpl-5.2.37-src

Configuramos el paquete:

    $ ./configure

Esto, además de configurar el paquete, nos avisará de cualquier
dependencia requerida que no tengamos instalada. En este caso:

    $ sudo aptitude install libzip-dev libgtkmm-2.4-dev libsqlite3-dev uuid-dev liblua5.1-0-dev libctemplate-dev

Una vez terminado sin errores, ya podemos compilar:

    $ make

Antes de instalarlo, podemos realizar una comprobación:

    $ make check

Y ya podemos instalarlo:

    $ sudo make install

  [MySQL Workbench]: http://www.mysql.com/products/workbench/
    "MySQL Workbench"
  [página de descargas]: http://dev.mysql.com/downloads/workbench#downloads
    "página de descargas"
