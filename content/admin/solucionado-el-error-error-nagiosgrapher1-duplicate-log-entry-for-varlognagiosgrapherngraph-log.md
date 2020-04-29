Title: Solucionado el error «error: nagiosgrapher:1 duplicate log entry for /var/log/nagiosgrapher/ngraph.log»
Date: 2013-03-20 21:08
Author: Nacho Cano
Tags: 12.04, error, logrotate, nagios, nagiosgrapher, quantal, quetzal, ubuntu
Slug: solucionado-el-error-error-nagiosgrapher1-duplicate-log-entry-for-varlognagiosgrapherngraph-log

`nagiosgrapher` es un programa que recoge la información de Nagios y
crea una serie de gráficos a partir de ella.

En Ubuntu 12.04.2, la versión instalada desde los repositorios, 1.7.1-3,
tiene un pequeño fallo, de tal manera que
[`logrotate` arroja el siguiente error][logrotate arroja el siguiente error]:

    error: nagiosgrapher:1 duplicate log entry for /var/log/nagiosgrapher/ngraph.log
    error: found error in /var/log/nagiosgrapher/ngraph.log , skipping

El fallo está corregido a partir de la versión 1.7.2.

Podemos confirmar el fallo si vemos que `nagiosgrapher` instala dos
archivos como los siguientes en el directorio de `logrotate`:

    $ dpkg -L nagiosgrapher | grep logrotate
    /etc/logrotate.d
    /etc/logrotate.d/nagiosgrapher
    /etc/logrotate.d/nagios_grapher

    $ ls /etc/logrotate.d | grep nagios
    nagiosgrapher
    nagios_grapher

Uno de ellos, `nagios_grapher`, hace referencia a un archivo que no
existe, `/usr/bin/nagios_grapher`. Basta con eliminar, o mover a un
directorio de _backup_, este archivo para que ya nos avise del error.

  [logrotate arroja el siguiente error]: https://bugs.launchpad.net/ubuntu/+source/nagiosgrapher/+bug/466671
    "logrotate arroja el siguiente error"
