Title: USB Dumping
Date: 2010-10-27 19:44
Author: Nacho Cano
Tags: cp, dd, mount, script, sysfs, udev, usb dumping
Slug: usb-dumping

El [USB Dumping][] consiste en copiar el [contenido de un USB][]
introducido en un ordenador, sin que la víctima se entere.

En Ubuntu, podemos conseguir que se ejecute el _script_ que llevará a
cabo el robo de información, cuando se conecte un dispositivo USB. Para
ello, deberemos crear alguna [regla de `udev`][regla de udev].


`udev` y `sysfs`
----------------

`udev` se encarga de crear los nodos en `/dev` para los dispositivos
presentes en el sistema. Para ello, se basa en la información
prorcionada por `sysfs` y una serie de reglas proporcionadas por el
usuario. `sysfs` devuelve información de los dispositivos conectados al
sistema, y `udev` lo utiliza para crear los nodos `/dev`.

Reglas
------

Las reglas se guardan en ficheros de configuración dentro del directorio
`/etc/udev/rules.d`. Los nombres de los ficheros pueden tener un número
al comienzo, en función de la prioridad y de algunos privilegios que les
queramos otorgar. En el archivo README que hay en ese directorio hay una
pequeña explicación de esto. A nosotros nos basta con saber que, como no
nos importa el orden, nuestro fichero de reglas no necesita llevar
prefijo numérico. Podría llamarse, por ejemplo:
`/etc/udev/rules.d/usb-dumping.rules`.

Las reglas podrán ser aplicadas inmediatamente después de haber guardado
el fichero, ya que no es necesario reiniciar el demonio.

Para nuestro caso, la regla sería:

```bash
KERNEL=="sd[b-d]1", ACTION=="add", RUN+="/home/karpoke/usb-dumping.sh %k"
```

donde

-   `KERNEL=="sd[b-d]1"`, especifica que la regla se debe ejecutar cada
    vez que el kernel asigne un nombre como `sdb1`, `sdc1` ó `sdd1`.
    Evitamos el `/dev/sda` porque es donde está montado el sistema.
    También hemos evitado interesarnos por otras particiones que pudiera
    haber en el disco: `sdb2`, `sdb5`, etc...
-   `ACTION=="add"`, especifica que la regla se debe ejecutar cuando se
    conecte el dispositivo. Lo contrario sería _remove_.
-   `RUN+="..."`, especifica el _script_ que hay que ejecutar cuando se
    cumplen las condiciones.
-   `%k`, es el nombre que le asigna el kernel al dispositivo y se lo
    pasamos al _script_ como parámetro.

En el fichero `/var/log/messages`, podremos obtener información útil
acerca de los dispositivos conectados y de si no encuentra nuestro
_script_ o no puede ejecutarlo, pero, ¡ojo!, no saldrá nada si nuestro
_script_ no hace lo que toca o si tiene algún error de sintaxis.

Volcado
-------

### `dd`

El _script_, que se ejecuta como `root`, es importante que esté marcado
como ejecutable y contenga el _shebang_ en la primera línea, ya que
`udev` no lo ejecutará en un terminal ni en una consola. Podría ser algo
tan sencillo como:

```bash
#!/bin/sh
devname="$1" # p.ej: sdb1
dd if=/dev/$devname of=/tmp/$devname.dd &
```

Debemos utilizar el `&` para asegurarnos de que la ejecución del
_script_ continúa en segundo plano. La ventaja de usar `dd` es que no
bloquea el dispositivo, por lo que si la víctima lo retira no pasará
nada. Otra ventaja es que se podrían copiar archivos que la víctima haya
[eliminado de su USB][]. El principal inconveniente es que se creará un
fichero del mismo tamaño que el USB entero, aunque éste estuviera vacío,
con el tiempo que eso puede conllevar. *[haciendo pruebas, me ha tardado
1 minuto y 15 segundos para un USB de 1 GByte]*

Para recuperar la información del archivo volcado, deberemos montarlo en
un directorio:

```bash
$ mkdir ~/usb_fs
$ sudo mount -o loop,ro,noexec,nodev /tmp/sdb1.dd ~/usb_fs
```

La opción `noexec` para el `mount` es importante, ya que no nos gustaría
que ese USB estuviera infectado y programado para ejecutar algún tipo de
_script_ al montarse.

### `cp`

En lugar de usar `dd` podríamos utilizar `cp`, con la ventaja de que
sólo copia los ficheros y directorios existentes en el USB. En este
caso, el inconveniente es que se bloquea el USB, y no dejará que el
dispositivo se expulse de forma segura hasta que haya terminado la
copia.

Hay que tener en cuenta que no podemos utilizar `cp` directamente con
`/dev/sdb1`, sino que primero deberemos montar el dispositivo.

```bash
#!/bin/sh
devname="$1" # p.ej: sdb1
mkdir /mnt/$devname
mount /dev/$devname /mnt/$devname
cp -fr /mnt/$devname /tmp &
```

Sin embargo, esto tiene otro problema, y es que al haber montado el
dispositivo, Ubuntu no lo vuelve a montar y, por tanto, no se muestra al
usuario. Podríamos abrir el directorio en un ventana de Gnome con algo
como:

```bash
export DISPLAY=:0.0
nautilus /mnt/$devname
```

Por otro lado, si lo hacemos así, el directorio de montaje no se llamará
como el nombre del volumen del USB, cosa que podría llamar la atención
del usuario.

Además, deberíamos asegurarnos de eliminar el directorio recién creado y
desmontar el dispositivo cuando éste se extraiga. Esto lo podríamos
hacer con otra regla en nuestro fichero de reglas para `udev`:

```bash
KERNEL=="sd?1", ACTION=="remove", RUN+="/home/karpoke/usb-dumping-umount.sh '%k'"
```

y en este _script_ para demontar la unidad tendríamos algo como:

```bash
umount /dev/$devname
rm -fr /mnt/$devname
```

¿Y si pudiéramos matar el proceso de copia del primer _script_ desde
este último _script_, con un `pkill`, por ejemplo? No sirve, ya que este
_script_ se ejecuta cuando el dispositivo ya ha sido desconectado, y en
el caso de que utilicemos la opción con `cp` y el usuario no podrá sacar
el USB de forma segura antes de que la copia haya terminado.

Protección
----------

La única solución que se me ocurre para protegernos de una forma segura
de este tipo de ataques es, o bien no utilizar nuestro USB en ningún
otro ordenador, cosa harto improbable si lo que queremos con el USB es
tener nuestros archivos independientemente del ordenador en el que
estemos, o bien cifrar el contenido del USB, en todo o en parte.

  [USB Dumping]: http://www.seguridadapple.com/2010/10/usb-dumping-en-mac-os-x.html
    "seguridad apple"
  [contenido de un USB]: {filename}/admin/recuperando-archivos-del-usb.md
    "contenido de un USB"
  [regla de udev]: http://www.reactivated.net/writing_udev_rules.html
    "udev rules"
  [eliminado de su USB]: {filename}/admin/recuperando-archivos-del-usb.md
    "recuperando archivos eliminados"
