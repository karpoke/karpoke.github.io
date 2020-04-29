Title: Solucionado el error "Tcl/Tk not found" al instalar OMNeT++ en Ubuntu
Date: 2011-02-21 14:37
Author: Nacho Cano
Tags: 10.10, configure, make, omnetpp, simulador de redes, ssh, tck/tk, ubuntu maverick meerkat
Slug: solucionado-el-error-tcltk-not-found-al-instalar-omnet-en-ubuntu

[OMNeT++][] es un entorno de desarrollo modular y extensible
desarrollado en C++, y gratuito pasa uso no comercial, especialmente
pensado para construir simuladores de redes de eventos discretos en el
sentido más amplio: redes de comunicaciones alámbricas, inalámbricas,
redes de colas, etc. El soporte para dominios específicos tales como
redes de sensores, redes inalámbricas _ad-hoc_, protocolos de Internet,
modelado del rendimiento, etc, viene dado por proyectos desarrollados de
forma independiente. OMNeT++ ofrece un IDE basado en eclipse, un entorno
de ejecución gráfico y otras herramientas. Hay extensiones para
simulación en tiempo real, emulación de redes, lenguages de programación
alternativos (Java, C\#), integración con bases de datos, etc.

![Onmetpp]({static}/images/omnetpp-300x224.png)

Para instalarlo en Ubuntu, nos bajamos el [código fuente][] y lo
descomprimimos, por ejemplo, en nuestro directorio personal:

    $ tar xvfz 2217-omnet-41-source--ide-tgz -C ~

Instalamos los paquetes necesarios:

    $ sudo aptitude install build-essential gcc g++ bison flex perl tcl-dev tk-dev blt
    libxml2-dev zlib1g-dev openjdk-6-jre doxygen graphviz openmpi-bin
    libopenmpi-dev libpcap-dev

Ejecutamos las siguientes líneas y también las añadimos a nuestro
`~/.bashrc`:

    # omnet++4.1
    export PATH=$PATH:$HOME/omnetpp-4.1/bin
    export TCL_LIBRARY=/usr/share/tcltk/tcl8.4

Ya podemos proceder con la instalación:

    $ ./configure

Si al ejecutar este comando termina con el siguiente error:

    checking for Tcl/Tk with CFLAGS="-I/usr/include/tcl8.4 -fwritable-strings" LIBS="-L/usr/share/tcltk -ltk8.4 -ltcl8.4"... no
    configure: error: Tcl/Tk not found, needed for all GUI parts. Version 8.4.0+ and devel package required. Check config.log for more info!

se debe a que no encuentra las librerías Tcl/Tk. Para solucionarlo,
deberemos modificar el archivo de configuración
`~/omnet-4.1/configure.user` para que las encuentre. La solución del
[manual de instalación][] no me ha ido del todo bien dado que las
librerías Tcl/Tk en Ubuntu no se encuentran por defecto donde el
programa espera. Así que editamos ese fichero, y allí donde nos sugiere
que modifiquemos estas variables, añadimos las siguientes líneas:

    TK_CFLAGS="-I/usr/include/tcl8.4 -I/usr/include/tk8.4"
    TK_LIBS="-L/usr/share/tcltk/tcl8.4 -L/usr/share/tcltk/tk8.4 -ltk8.4 -ltcl8.4"

* * * * *

#### Actualizado el 20 de junio de 2012

La variable `TK_CFLAGS` debe contener los directorios donde se
encuentran los ficheros `tcl.h` y `tk.h`. Si se encuentran en
directorios distintos, se debe incluir ambos, precedidos del argumento
`-I`.

La variable `TK_LIBS` debe contener los directorios donde se encuentran
las librerías cuyo nombre comienza por `libtcl` y `libtk`, por ejemplo,
`libtcl84.so`, `libtk8.4.a`, etc. El argumento `-l` contiene el nombre de
las librerías (que debe coincidir con el nombre de los ficheros
anteriores, quitan el prefijo `lib` y los sufijos `.so` y `.a`). Podría
ser necesario enlazar con las librerías `X11`, por lo que se debería
añadir `-lX11`, aunque esto último no me hizo falta.

* * * * *

Ahora ya podemos ejecutar el comando:

    $ ./configure

Y compilar con el `make`, pero aprovechando que tengo un procesador con
dos núcleos y que el programa puede optimizarse para el número de
núcleos, le pasaremos el argumento `-j`:

    $ make -j2

Si modificamos algún parámetro de `configure.user`, deberemos hacer una
limpieza y volver a compilar:

    $ make cleanall
    $ make -j2

Si queremos ejecutar el programa sin entorno gráfico, por ejemplo, si lo
vamos a utilizar a través de una sesión remota por `ssh`, y queremos
decirle que que no tenga en cuenta las librerías Tcl/Tk a la hora de
compilar, usaremos el siguiente comando:

    $ NO_TCL=yes ./configure

Podemos ver y probar algunos de los ejemplos que trae el programa
ejecutando:

    $ ~/omnetpp-4.1/samples/rundemo

  [OMNeT++]: http://www.omnetpp.org/ "omnet++"
    "OMNeT++"
  [código fuente]: http://www.omnetpp.org/omnetpp/doc_details/2217-omnet-41-source--ide-tgz
    "código fuente"
  [manual de instalación]: http://omnetpp.org/doc/omnetpp41/InstallGuide.pdf
    "manual de instalación"
    "manual de instalación de omnet++"
