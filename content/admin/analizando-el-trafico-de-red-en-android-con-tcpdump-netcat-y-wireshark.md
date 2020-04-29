Title: Analizando el tráfico de red en Android con tcpdump, netcat y Wireshark
Date: 2012-08-20 01:55
Author: Nacho Cano
Tags: adb, adb wifi, android, arm, http, nc, netcat, tcpdump, tcpdump-arm, tráfico de red, wireshark
Slug: analizando-el-trafico-de-red-en-android-con-tcpdump-netcat-y-wireshark

Si necesitamos analizar el tráfico de red de nuestro Android, ya sea
para depurar una aplicación o para ver qué uso de la red hacen las
aplicaciones instaladas en el terminal, podemos recurrir a herramientas
bien conocidas como `tcpdump`, `netcat` y Wireshark.


Antes de empezar
----------------

Antes de continuar, deberemos tener instaladas las [herramientas de
desarrollo para Android][]. Descargamos el paquete y lo descomprimimos:

    $ wget http://dl.google.com/android/android-sdk_r20.0.3-linux.tgz
    $ tar xvzf android-sdk_r20.0.3-linux.tgz

Añadimos los directorios `tools` y `platform-tools` al `PATH`.
Ejecutamos las siguientes líneas, y las añadimos también en el fichero
`~/.bashrc`, para incluirlas en el PATH del sistema:

    export ANDROID_HOME=$HOME/android-sdk-linux
    export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

Abrimos el gestor de paquetes ejecutando:

    $ android sdk

Instalaremos las SDK Tools y las SDK Platform-tools.

Instalando tcpdump en Android
-----------------------------

Utilizaremos una versión de `tcpdump` que ha sido compilada para ARM. La
podemos descargar de aquí [tcpdump-arm][]:

    $ wget http://www.eecs.umich.edu/~timuralp/tcpdump-arm

Ahora activaremos el modo depuración. En Android 4.0.3 se encuentra en
el menú Ajustes > Opciones del desarrollador > Depuración de USB. En
otras versiones puede variar ligeramente. Si no nos aparece esta opción,
podemos probar pulsando 7 veces en el campo _Build_ del menú Ajustes >
Información. Acto seguido, conectamos el móvil a nuestro equipo mediante
el cable USB.

Si todo ha ido bien, podremos listar los dispositivos conectados
ejecutando:

    $ adb devices
    List of devices attached
    192B32A8955D29F device

Enviamos la versión de tcpdump que hemos descargado al móvil y le
cambiamos los permisos:

    $ adb push tcpdump-arm /data/local
    $ adb shell
    shell@android:/ $ cd /data/local
    shell@android:/data/local $ chmod 777 tcpdump-arm
    shell@android:/data/local $ su
    1|shell@android:/data/local # ./tcpdump-arm -h
    tcpdump-arm version 4.0.0
    libpcap version 1.0.0
    Usage: tcpdump-arm [-aAdDefIKlLnNOpqRStuUvxX] [ -B size ] [ -c count ]
            [ -C file_size ] [ -E algo:secret ] [ -F file ] [ -G seconds ]
            [ -i interface ] [ -M secret ] [ -r file ]
            [ -s snaplen ] [ -T type ] [ -w file ] [ -W filecount ]
            [ -y datalinktype ] [ -z command ] [ -Z user ]
            [ expression ]

Un ejemplo de captura de tráfico:

    shell@android:/data/local # ./tcpdump-arm -n -i wlan0 -p -s 0 -w out.pcap

El argumento `-n` es para evitar traducir IPs a nombres, `-i` especifica la
interfaz de red, `-p` indica que no sea en modo promiscuo, dado que de
todas formas no iba a funcionar, `-s 0` es para que capture todo el
paquete desde el primer byte y `-w` envía la salida a un fichero.

Cuando queramos parar, matamos el proceso con `^C` y nos traemos el
fichero de la captura, que podremos abrir con Wireshark:

    $ adb pull /data/local/out.pcap

* * * * *

#### Actualizado el 20 de enero de 2014

Me he encontrado algún caso en el que al intentar ejecutar `netcat`, nos
devuelve el siguiente error:

    $ adb shell
    ~ # nc
    /sbin/sh: nc: not found

En este caso, podemos utilizar la versión que trae alguna aplicación,
como por ejemplo SSH Droid:

    ~ # alias nc="/data/data/berserker.android.apps.sshdroid/home/bin/nc"

Otra opción podría ser utilizar BusyBox:

    ~ # find . -name busybox
    ./system/xbin/busybox
    ~ # alias nc="/system/xbin/busybox nc"  # debemos pasar el nombre del comando

* * * * *

Analizar el tráfico en tiempo real
----------------------------------

Guardar el tráfico en un fichero para luego examinarlo puede estar bien
en algunos casos, pero poder analizar en tiempo real también suena
interesante. Lo que haremos será abrir una conexión entre el móvil y
nuestro equipo mediante `netcat`, y pasar la salida de `tcpdump` a
través de ella directamente hacia Wireshark.

    $ adb shell
    shell@android:/ $ su
    shell@android:/ # /data/local/tcpdump-arm -n -s 0 -i wlan0 -w - | nc -l -p 12345

O en un solo comando:

    $ adb shell "su -c '/data/local/tcpdump-arm -n -s 0 -i wlan0 -w - | nc -l -p 12345'"

En nuestro equipo, creamos una redirección de un puerto en el móvil, el
puerto en el que hemos lanzado `netcat` como servidor, a un puerto de
nuestro equipo:

    $ adb forward tcp:12345 tcp:12345

Y utilizando `netcat` como cliente, pasamos su salida a Wireshark:

    $ nc 127.0.0.1 12345 | wireshark -k -S -i -

* * * * *

#### Actualizado el 22 de julio de 2014

Si usamos ADB sobre red no es necesario que conectemos el móvil al
ordenar por USB. Basta activar el modo de depuración y ejecutar:

</p>
    $ adb connect 192.168.1.51:5555

* * * * *

Referencias
-----------

» [Analyzing Android Network Traffic][]
» [Android: Binary solo][]
» [Android Developer Tools][herramientas de desarrollo para Android]
» [Cross Compiling on Linux][]

  [herramientas de desarrollo para Android]: http://developer.android.com/tools/index.html
    "herramientas de desarrollo para Android"
  [tcpdump-arm]: http://www.eecs.umich.edu/~timuralp/tcpdump-arm
    "tcpdump-arm"
  [Analyzing Android Network Traffic]: http://mobile.tutsplus.com/tutorials/android/analyzing-android-network-traffic/
    "Analyzing Android Network Traffic"
  [Android: Binary solo]: http://nerdjusttyped.blogspot.com.es/2009/03/android-binary-solo.html
    "Android: Binary solo"
  [Cross Compiling on Linux]: http://wiki.neurostechnology.com/index.php/Cross_Compiling_on_Linux
    "Cross Compiling on Linux"
