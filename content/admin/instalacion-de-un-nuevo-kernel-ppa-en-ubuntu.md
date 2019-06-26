Title: Instalación de un nuevo kernel PPA en Ubuntu
Date: 2012-01-26 12:19
Author: Nacho Cano
Tags: deb, kernel, module-init-tools, pae, ppa, precompilado, script, ubuntu
Slug: instalacion-de-un-nuevo-kernel-ppa-en-ubuntu

Esta receta muestra como [instalar un nuevo kernel precompilado][] en
Ubuntu.

Antes de continuar, cabe avisar de que si tenemos módulos del kernel que
no sean libres, por ejemplo, módulos de ATI, [Broadcom][] o
[Virtualbox][], es posible que nos surja algún problema que deberemos
resolver en cada caso. En algunos casos, volver a reinstalar las
aplicaciones o los controladores puede funcionar.

Instalamos `module-init-tools`, una herramienta para gestionar módulos
del kernel que se encuentra en los repositorios, que puede evitar que
nos aparezcan algunos errores y avisos.

El kernel lo podemos descargar de [kernel.ubuntu.com][]. En este caso
vamos a descargar la versión 3.2.1 Precise PAE de 32 bits, así que
descargamos los paquetes.

-   linux-headers-all
-   linux-headers-generic-pae_i386
-   linux-image-generic-pae_i386

```bash
$ mkdir ~/Downloads/kernel-v3.2.1-precise
$ wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.2.1-precise/linux-headers-3.2.1-030201_3.2.1-030201.201201121644_all.deb
$ wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.2.1-precise/linux-headers-3.2.1-030201-generic-pae_3.2.1-030201.201201121644_i386.deb
$ wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.2.1-precise/linux-image-3.2.1-030201-generic-pae_3.2.1-030201.201201121644_i386.deb
```

Los instalamos en ese mismo orden:

```bash
$ sudo dpkg -i linux-headers-3.2.1-030201_3.2.1-030201.201201121644_all.deb
$ sudo dpkg -i linux-headers-3.2.1-030201-generic-pae_3.2.1-030201.201201121644_i386.deb
$ sudo dpkg -i linux-image-3.2.1-030201-generic-pae_3.2.1-030201.201201121644_i386.deb
```

Sólo queda reiniciar para poder probar el nuevo kernel.

* * * * *

#### Actualizado el 13 de marzo de 2012

He subido un pequeño _script_ que permite [automatizar este proceso][].
Comprueba la versión del kernel que tenemos instalada y si hay una nueva
versión, la descarga y, si así lo queremos, la instala.

Un ejemplo:

```bash
$ install-new-kernel.sh
[+] Checking 'http://kernel.ubuntu.com/~kernel-ppa/mainline/' for a new version...
[+] New version 3.2.11 available.
[+] Checking 'http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.2.11-precise/' for packages...
[+] Downloading 'linux-headers-3.2.11-030211_3.2.11-030211.201203131335_all.deb'...
[+] Downloading 'linux-headers-3.2.11-030211-generic-pae_3.2.11-030211.201203131335_i386.deb'...
[+] Downloading 'linux-image-3.2.11-030211-generic-pae_3.2.11-030211.201203131335_i386.deb'...
[+] Do you want to install them now? (y/n) y
```

* * * * *

  [instalar un nuevo kernel precompilado]: http://www.howopensource.com/2011/08/how-to-install-linux-kernel-3-1-rc2-oneiric-in-ubuntu-11-04-10-10-and-10-04/
    "instalar un nuevo kernel precompilado"
  [Broadcom]: http://www.ultimateeditionoz.com/forum/viewtopic.php?t=2504
    "Broadcom"
  [Virtualbox]: http://unix.stackexchange.com/questions/10962/i-am-failing-to-build-virtualbox-driver-for-linux-2-6-38
    "Virtualbox"
  [kernel.ubuntu.com]: http://kernel.ubuntu.com/~kernel-ppa/mainline/
    "kernel.ubuntu.com"
  [automatizar este proceso]: http://terminus.ignaciocano.com/wp-uploads/linked/install-new-kernel.sh
    "instalación de nuevo kernel PPA en ubuntu"
