Title: Jelly Bean con AndroVM en VirtualBox OSE
Date: 2012-12-15 18:40
Author: Nacho Cano
Tags: aceleración gráfica, android, androvm, androvmplayer, hardware opengl, jelly bean, máquina virtual, ova, virtualbox-ose
Slug: jelly-bean-con-androvm-en-virtualbox-ose
Related: analizando-el-trafico-de-red-en-android-con-tcpdump-netcat-y-wireshark,conectar-de-forma-segura-en-redes-abiertas-con-android-connectbot-y-proxydroid,conectar-a-un-servidor-ssh-desde-android-mediante-connectbot-utilizando-claves

[AndroVM][] es una máquina virtual para ejecutar Android. Si queremos
probarla, lo único que tenemos que hacer es [descargarla][] y configurar
VirtualBox OSE para ejecutarla.

![jelly bean]({static}/images/jelly-bean-300x183.png)

Descarga
--------

Desde la página de [descargas][descargarla] nos descargamos el fichero
OVA, por ejemplo, __vbox86tp version with gapps & houdini__ (hay varias
versiones, pero ésta es la más completa), y el reproductor para nuestra
plataforma, por ejemplo __Linux 32-bit__, que emplearemos si queremos
utilizar la aceleración hardware OpenGL.

```bash
$ wget http://androvm.org/Download/androVM_vbox86tp_4.1.1_r4-20121119-gapps-houdini-flash.ova
$ wget http://androvm.org/Download/AndroVMplayer-linux32-20121106.tgz
```

Configuración de VirtualBox OSE
-------------------------------

Vamos a Archivo > Preferencias > Red y creamos un adaptador de red de
tipo "Sólo anfitrión". Habilitamos, también, el servidor DHCP.

Importamos el fichero OVA desde Archivo > Importar servicio
virtualizado.

Habilitamos la interfaz de red de AndroVM, deshabilitada por defecto.
Para ello, vamos a las Preferencias de la máquina virtual > Red >
Adaptador 1 y lo conectamos a "Adaptador sólo anfitrión".

Arranque
--------

Iniciamos la máquina virtual y procedemos con la configuración inicial
de Android.

### Aceleración hardware OpenGL

Si queremos activar la aceleración hardware OpenGL, abrimos la
aplicación AndroVM Configuration, que ya viene instalada, y marcamos la
casilla. Guardamos y reiniciamos cuando nos lo pida.

El otro archivo que nos hemos bajado, AndroVMplayer, se utiliza para
mostrar la máquina virtual y gestionar sus eventos. Reiniciamos la
máquina virtual y mientras tanto, ejecutamos este archivo que puede
tomar tres parámetros: ancho, alto y densidad.

```bash
$ tar xvzf AndroVMplayer-linux32-20121106.tgz
$ cd AndroVMplayer
$ ./AndroVMplayer 1024 600 160
```

Referencias
-----------

» [androvm.org][]

  [AndroVM]: http://androvm.org/
    "AndroVM"
  [descargarla]: http://androvm.org/blog/download/
    "descargarla"
  [androvm.org]: http://androvm.org/blog/blog/2012/11/14/androvm-configuration-tutorial/
    "androvm.org"
