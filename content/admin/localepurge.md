Title: localepurge
Date: 2011-05-25 10:44
Author: Nacho Cano
Tags: apt, apt-config, localepurge, optimización, ubuntu, uso de disco
Slug: localepurge

`localepurge` es una herramienta que elimina los archivos de traducción
que no necesitemos. Después de instalarlo, nos pedirá que [seleccionemos
qué idiomas queremos conservar][]:

-   en_US
-   en_US.ISO-8859-15
-   en_US.UTF-8
-   es
-   es_ES
-   es_ES@euro
-   es_ES.UTF-8

Después de instalarlo, lo ejecutamos:

    $ sudo localepurge
    Total disk space freed by localepurge: 26552 KiB

Cada vez que instalemos un nuevo paquete de los respositorios se
ejecutará automáticamente, por lo que no tendremos que volver a
preocuparnos.

* * * * *

#### Actualización a 17 de marzo de 2013

Acabo de encontrar una anotación interesante en el blog del [crysol][].
En lugar de eliminar las traducciones que no nos interesan, podemos,
directamente, evitar descargarlas. Editamos el fichero
`/etc/apt/apt.conf.d/99Translations`, y añadimos lo que necesitemos, por
ejemplo:

    Acquire::Languages:: "es";
    Acquire::Languages:: "es_ES";

O, mejor aún, si no queremos bajar ninguna traducción:

    Acquire::Languages:: "none";

Podemos ver la configuración con el comando `apt-config`:

    $ apt-config dump | grep Lang
    Acquire::Languages "";

A partir de ahora, las actualizaciones deberían ir algo más rápidas.

* * * * *

  [seleccionemos qué idiomas queremos conservar]: http://www.guia-ubuntu.org/index.php?title=Localepurge
    "seleccionemos qué idiomas queremos conservar"
  [crysol]: http://crysol.org/es/node/1696
    "crysol"
