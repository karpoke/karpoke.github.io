Title: Últimos paquetes instalados
Date: 2011-08-27 18:14
Author: Nacho Cano
Tags: dpkg
Slug: ultimos-paquetes-instalados

En el fichero `/var/log/dpkg.log` se registran las operaciones sobre los
paquetes que tenemos en el sistema: instalaciones, actualizaciones,
eliminaciones, etc. Para obtener una lista de los [últimos paquetes
instalados][] ejecutamos:

    $ cat /var/log/dpkg.log* | grep " install " | sort
    ...
    2011-08-24 12:11:04 install linux-image-2.6.38-11-generic-pae < ninguna> 2.6.38-11.48
    2011-08-24 12:11:27 install linux-headers-2.6.38-11 < ninguna> 2.6.38-11.48
    2011-08-24 12:11:33 install linux-headers-2.6.38-11-generic-pae < ninguna> 2.6.38-11.48
    2011-08-26 18:25:40 install libcgal5 < ninguna> 3.6.1-2ubuntu2
    2011-08-26 18:25:41 install libopencsg1 < ninguna> 1.3.1-4
    2011-08-26 18:25:42 install openscad < ninguna> 2011.06-1+natty1

  [últimos paquetes instalados]: http://distilledb.com/blog/archives/date/2009/06/30/getting-a-list-of-recently-installed-packages-in-ubuntu.page
    "últimos paquetes instalados"
