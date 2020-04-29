Title: Salvapantallas con el código fuente del kernel
Date: 2011-07-28 12:42
Author: Nacho Cano
Tags: aleatoriedad, código fuente, kernel, linux, phosphor, protector de pantalla, salvapantallas, script, sed, uname
Slug: salvapantallas-con-el-codigo-fuente-del-kernel

Si queremos que cada vez que aparezca el salvapantallas, lo haga
mostrando algunas líneas del código fuente del _kernel_ por pantalla,
sólo necesitamos configurar el salvapantallas `phosphor`.

![Phosphor]({static}/images/phosphor-300x178.png)

Lo primero es instalar el código fuente del `kernel`:

    $ sudo apt-get source linux-source-$(uname -r)

El comando `uname` muestra información acerca del sistema operativo
instalado, la versión del kernel, la familia del procesador, el nombre
de la máquina o la plataforma. En mi caso, uso un kernel PAE, porque
tengo una Ubuntu de 32 bits y 4 GB de RAM, por lo que el comando
anterior no me ha ido del todo bien:

    $ uname -r
    2.6.38-10-generic-pae

Así que, en su lugar, he utilizado:

    $ sudo apt-get source linux-2.6.38

Una vez descargado el código fuente del kernel, configuraremos
`phosphor` para que muestre el contenido de algún fichero. Si no tenemos
instalado `phosphor`, habrá que instalar el paquete
`xscreensaver-data-extra`.

El fichero de configuración de `phosphor` está en
`/usr/share/applications/screensavers/phosphor.desktop`:

    [Desktop Entry]
    Name=Phosphor
    Exec=/usr/lib/xscreensaver/phosphor -root
    TryExec=/usr/lib/xscreensaver/phosphor
    Comment=Draws a simulation of an old terminal, with large pixels and long-sustain phosphor. On X11 systems, This program is also a fully-functional VT100 emulator! Written by Jamie Zawinski.
    StartupNotify=false
    Terminal=false
    Type=Application
    Categories=Screensaver;
    OnlyShowIn=GNOME;

Para probarlo podemos ejecutar:

    $ /usr/lib/xscreensaver/phosphor -program fortune
    $ /usr/lib/xscreensaver/phosphor -scale 2 -delay 40000 -ticks 10 -geom '1680x1050' -program 'od -txC -w6 /dev/random'

Podemos pasarle diferentes opciones, tales como el tipo, el tamaño o la
escala de la fuente a utilizar, la velocidad a la que escribe, el
programa del cual debe recoger el texto, etc.

Crearemos un pequeño _script_, [`random-lines-of-code.sh`][random-lines-of-code.sh], que
permita seleccionar un trozo [aleatorio][] de un fichero aleatorio del
código fuente del kernel;

    function randint() {
       cat /proc/interrupts | md5sum | sed -r 's/[a-f]//g; s/^0+//; s/.{3}$//'
    }

    # random file
    f=$(ls /usr/src/linux-2.6.38/_/_.{c,h} | shuf -n1)

    # number of lines
    declare -i nol=$(wc -l $f | awk '{print $1}')

    # choose a random first line
    declare -i first=$( echo $(randint) % $nol | bc )

    # choose a random bunch of lines
    declare -i offset=$( echo $(randint) % \($nol-$first\) | bc )

    # first line doesn't start at 0
    first=$(( first+1 ))

    # last line
    declare -i last=$(( first+offset ))

    # show the lines of the file
    cat $f | sed -n ${first},${last}p

Guardamos el _script_, le damos permisos de ejecución y modificamos el
fichero de configuración de `phosphor` para que lo ejecute. Cambiamos la
línea del `Exec`:

    Exec=/usr/lib/xscreensaver/phosphor -root -scale 2 -program '/home/user/random-lines-of-code.sh'

En el menú `Sistema > Preferencias > Salvapantallas` seleccionamos
`Phosphor`, y listos.

  [random-lines-of-code.sh]: http://terminus.ignaciocano.com/wp-uploads/linked/random-lines-of-code.sh
    "random-lines-of-code.sh"
  [aleatorio]: {filename}/dev/random-bash.md
    "aleatorio"
