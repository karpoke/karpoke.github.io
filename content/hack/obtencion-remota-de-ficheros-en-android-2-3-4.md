Title: Obtención remota de ficheros en Android < 2.3.4
Date: 2011-11-28 14:54
Author: Nacho Cano
Tags: android, base64, exploit, robo de información, script
Slug: obtencion-remota-de-ficheros-en-android-2-3-4

Hoy se ha hecho pública la [prueba de concepto][] de Thomas Cannon que
permite [obtener ficheros de los dispositivos con Android][] con versiones
anteriores a la 2.3.4.

En la demostración se ha utilizado un HTC Desire (UK version) con
Android 2.2. Yo lo he probado con un HTC Wildfire con Android 2.2.1 y
también funciona.

La vulnerabilidad permite que un sitio malicioso obtenga cualquier
fichero guardado en la tarjeta SD, e incluso algunos ficheros e
información guardados en el teléfono. No se puede acceder a ficheros del
sistema, ya que se ejecuta dentro de la _sandbox_.

El navegador de Android no pide confirmación al usuario para descargar
el fichero, por ejemplo `poc.html`, y lo descarga de forma automática en
el directorio `/sdcard/download/poc.html`. Mediante javascript es
posible abrir automáticamente el fichero descargado, forzando al
navegador a enviar los ficheros locales, sin pedir confirmación al
usuario.

El principal impedimento es que el atacante debe conocer la ruta y el
nombre de los ficheros que quiere obtener. Sin embargo, algunas
aplicaciones utilizan nombres concretos para guardar sus ficheros en la
tarjeta SD o nombres que siguen una pauta concreta.

Un ejemplo del resultado de la [prueba de concepto][1] es el siguiente:

    Array
    (
        [filename0] => L3Byb2MvdmVyc2lvbg==
        [data0] => TGludXggdmVyc2lvbiAyLjYuMzIuMjEtZzZjNTVlZTQgKGh0Yy1rZXJuZWxAYW5kMTgtMikgKGdjYyB2ZXJzaW9uIDQuNC4wIChHQ0MpICkgIzEgUFJFRU1QVCBUaHUgRGVjIDIgMTY6NTk6MjcgQ1NUIDIwMTAK
    )

El contenido está en base 64. Si lo decodificamos:

    $ base64 -d <<< "L3Byb2MvdmVyc2lvbg=="
    /proc/version
    $ base64 -d <<< "TGludXggdmVyc2lvbiAyLjYuMzIuMjEtZzZjNTVlZTQgKGh0Yy1rZXJuZWxAYW5kMTgtMikgKGdjYyB2ZXJzaW9uIDQuNC4wIChHQ0MpICkgIzEgUFJFRU1QVCBUaHUgRGVjIDIgMTY6NTk6MjcgQ1NUIDIwMTAK"
    Linux version 2.6.32.21-g6c55ee4 (htc-kernel@and18-2) (gcc version 4.4.0 (GCC) ) #1 PREEMPT Thu Dec 2 16:59:27 CST 2010

Referencias
-----------

Via [@hackplayers][]
Prueba de concepto en [exploit-db.com][prueba de concepto]
Blog de [Thomas Cannon][obtener ficheros de los dispositivos con Android]

  [prueba de concepto]: http://www.exploit-db.com/exploits/18164/
    "prueba de concepto"
  [obtener ficheros de los dispositivos con Android]: http://thomascannon.net/blog/2010/11/android-data-stealing-vulnerability/
    "obtener ficheros de los dispositivos con Android"
  [1]: http://terminus.ignaciocano.com/index/android-content.php
    "prueba de concepto de obtención de ficheros en android < 2.3.4"
  [@hackplayers]: http://twitter.com/#!/hackplayers/status/141105359132700672
    "@hackplayers"
