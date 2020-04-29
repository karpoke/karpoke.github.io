Title: Controlando la actividad de los usuarios conectados
Date: 2011-08-01 12:51
Author: Nacho Cano
Tags: bofh, byobu, DISPLAY, finger, fingerprint, id, last, lastlog, screen, tac, terminales virtuales, w, whatch, who, whoami, whowatch
Slug: controlando-la-actividad-de-los-usuarios-conectados
Related: limitando-el-numero-de-procesos-por-usuario

Podemos utilizar varios comandos para saber qué [usuarios están
conectados al sistema][], desde cuando y qué están haciendo. También
podemos saber cuando se han conectado anteriormente.

También podríamos interactuar con los usuarios, enviarles mensajes,
matarles procesos, echarlos del sistema, etc, pero ahora nos vamos a
centrar en saber cuando entran, cuando salen y qué están haciendo.


`w`
---

Con `w` podemos saber que usuarios están conectados ahora mismo y que
procesos están ejecutando.

    $ w
     11:54:16 up  4:04,  3 users,  load average: 0,34, 0,12, 0,12
    USER     TTY      FROM              LOGIN@   IDLE   JCPU   PCPU WHAT
    karpoke  tty1                      08:58    9.00s  0.62s  0.50s -bash
    karpoke  tty7     :0               07:51    3:04m  7:08   0.28s gnome-session --session=2d-gnome
    karpoke  pts/0    :0.0             07:51   54.00s  1.18s  0.69s ssh 192.168.50.2
    karpoke  pts/1    :0.0             08:14    0.00s  1.67s  0.00s w
    karpoke  pts/2    192.168.50.10:S. 08:27    0.00s  0.53s  0.00s /bin/bash
    karpoke  pts/3    192.168.50.10:S. 08:42    3:19   0.28s  0.28s /bin/bash

En la cabecera muestra la hora actual, el tiempo que lleva encendida la
máquina, el número de usuarios en el sistema y la carga media del último
minuto, los últimos 5 minutos y los últimos 15 minutos. Después, para
cada conexión de usuario, muestra el nombre de usuario, el terminal al
que está conectado, la máquina remota, el tiempo que hace que está
conectado, el tiempo que ha estado sin hacer nada, el tiempo usado por
los procesos en ejecución, incluyendo procesos en segundo plano, y el
tiempo utilizado por el proceso en ejecución, que es el que aparece en
la última columna.

El terminal al que está conectado el usuario puede ser:

-   un terminal en modo texto, como `tty1`. Desde la sesión gráfica
    podemos cambiar a este tipo de terminal utilizando la combinación de
    teclas `Ctrl+Alt+F<1-6>`
-   una terminal gráfico, como `tty7`. Es el terminal por defecto cuando
    iniciamos sesión en Gnome o KDE
-   un emulador de terminal, como `pts/0`. Cuando nos conectamos usando
    `gnome-terminal`, por ejemplo.

Cuando el usuario se conecta desde la propia máquina, en la columna
correspondiente a la máquina desde la cual se conecta el usuario aparece
el contenido de [la variable DISPLAY][], si es que está definida. Esta
variable está controlada por el servidor de las X y consiste en un
nombre de _host_, que no aparece cuando se refiere a la propia máquina,
seguido de dos puntos ":" y un número de secuencia, que suele ser 0 pero
puede variar si hay varias sesiones gráficas conectadas a la misma
máquina. Si continua con un punto seguido de un número, se refiere al
número de pantalla dentro de la misma sesión gráfica.

En el último caso, cuando aparece una IP seguida de dos puntos y una S,
quiere decir que el usuario está utilizando `screen` (o, como en este
caso, `byobu`). En este caso, la longitud de la IP corta el contenido,
ya que después de la S viene una secuencia que indica cada una de las
"ventanas" abiertas con `screen`, por ejemplo: `192.168.50.10:S.1`.

Podemos [iniciar otra sesión gráfica][] ejecutando en un terminal,
debemos ir a un terminal en modo texto libre, por ejemplo, `tty1`,
pulsando `Ctrl+Alt+F1`, iniciamos sesión, y ejecutamos:

    $ startx -- :1 # importante: hay un espacio antes y después de los dos guiones

Para acceder a esta nueva sesión gráfica, pulsamos `Ctrl+Alt+F8`.

Sólo puede haber una sesión gráfica por terminal, por lo que si
quisiéramos una más, deberíamos ir `tty2`, pulsando `Ctrl+Alt+F2`, y
ejecutar:

    $ startx -- :2

Para acceder a esta sesión gráfica, pulsamos `Ctrl+Alt+F9`.

`who`
-----

Con `who` también podemos saber quién está conectado.

    $ who -a
               Sistema de arranque 2011-07-27 07:50
               `run-level' 2 2011-07-27 07:50
    LOGIN      tty4         2011-07-27 07:50              1250 id=4
    LOGIN      tty5         2011-07-27 07:50              1254 id=5
    LOGIN      tty2         2011-07-27 07:50              1288 id=2
    LOGIN      tty3         2011-07-27 07:50              1289 id=3
    LOGIN      tty6         2011-07-27 07:50              1291 id=6
    karpoke  - tty1         2011-07-27 11:58 00:19       14171
    karpoke  + tty7         2011-07-27 07:51  antig       3723 (:0)
    karpoke  + pts/0        2011-07-27 07:51 00:01        5965 (:0.0)
    karpoke  + pts/1        2011-07-27 08:14   .          5965 (:0.0)
               pts/2        2011-07-27 11:07                 0 id=/2    term=0 salida=0

Nos muestra la fecha y hora del último arranque del sistema y el nivel
de ejecución. Después, en la primera columna, muestra los procesos de
_login_, marcados con la palabra LOGIN, los usuarios que han iniciado
sesión y, si no aparece nada, se refiere a los procesos muertos, por
ejemplo, si abrimos un terminal y lo cerramos. También muestra el PID
del proceso en ejecución y la máquina remota o el DISPLAY
correspondiente.

El comando tiene varias opciones para mostrar esta información por
partes, por ejemplo, el número de usuarios conectados:

    $ who -q
    karpoke karpoke karpoke karpoke
    # usuarios=4

`whoami`
--------

Con `whoami` podemos saber, [única y exclusivamente][], cual es nuestro
usuario:

    $ whoami
    karpoke

Es equivalente a ejecutar:

    $ id -un

`id`
----

`id` muestra información de los identificadores de usuarios y grupos:

    $ id
    uid=1000(user) gid=1000(user) grupos=1000(user),4(adm),7(lp),20(dialout),24(cdrom),29(audio),44(video),46(plugdev),103(fuse),104(lpadmin),112(netdev),115(admin),120(sambashare)

Tiene varios argumentos que permiten mostrar sólo cierta información y de
diferentes maneras.

`whowatch`
----------

`whowatch` es un monitor interactivo por consola de procesos y usuarios.
Muestra información de los usuarios conectados al sistema en tiempo
real. Además de la información habitual, como el nombre de usuario, el
terminal, la máquina remota o el tipo de conexión, se puede visualizar
el árbol de procesos del usuario, e incluso enviarle señales, como
SIGINT o SIGKILL, a dichos procesos.

Soporta el uso de complementos, hasta 3, que amplíen la información acerca
del sistema, de un usuario o de un proceso.

    $ whowatch
    3 users: (2 local, 0 telnet, 0 ssh, 1 other)             load: 0.06, 0.08, 0.31
    (gdm-session-w karpoke   tty7   :0                  -
    (init)         karpoke   pts/0  :0.0                -
    (init)         karpoke   pts/1  :0.0                -
    [F1]Help [F9]Menu [ENT]proc all[t]ree [i]dle/cmd [c]md [d]etails [s]ysinfo

Pulsando Intro en el usuario conectado que queramos nos muestra
información de los procesos que está ejecutando:

    3 users: (2 local, 0 telnet, 0 ssh, 1 other)             load: 0.03, 0.07, 0.30
    (init)         karpoke   pts/1  :0.0
     6056   - gnome-terminal
     6105    |- bash
     3135    | `- ssh 192.168.50.10
     6062    |- gnome-pty-helper
     2982    `- bash
     3845 R    `- whowatch

    [ENT]users [c]md all[t]ree [d]etails [o]wner [s]ysinfo sig[l]ist ^[K]ILL

Podemos ver detalles de un proceso concreto:

    
    START: Mon Aug  1 09:11:00 2011                   
    EXE: /usr/bin/ssh                                 
    ROOT: /                                           
    CWD: /home/karpoke                                
                                                      
    STATUS:                                           
    Uid:    1000    1000    1000    1000              
    Gid:    1000    1000    1000    1000              
    FDSize: 256                                       
    Groups: 4 7 20 24 29 44 46 103 104 112 115 120 100
    VmPeak:     7460 kB                               
    VmSize:     7460 kB                               
    VmLck:         0 kB                               
     < - -> [a]up, [z]down '

Y enviarle una señal:

     PID 3135 - choose signal and press 'y' to send 
    ->1  HUP Hangup detected on controlling terminal  
      2  INT Interrupt from keyboard                  
      3  QUIT Quit from keyboard                      
      4  ILL Illegal Instruction                      
      6  ABRT Abort signal from abort(3)              
      8  FPE Floating point exception                 
      9  KILL Kill signal                             
      11  SEGV Invalid memory reference               
      13  PIPE Broken pipe: write to pipe with no read
      14  ALRM Timer signal from alarm(2)             
      15  TERM Termination signal                     
                                                      
                                                      
     < - -> [a]up, [z]down '

También podemos consultar información del sistema:

    
    BOOT TIME: Mon Aug  1 08:30:18 2011               
    CPU: 3.6% user 2.1% sys 1.0% nice 93.2% idle      
    MEMORY:                                           
    MemTotal:        4081788 kB                       
    MemFree:          436656 kB                       
    Buffers:          530624 kB                       
    Cached:          1825612 kB                       
    SwapCached:            0 kB                       
    Active:          1777952 kB                       
    Inactive:        1396896 kB                       
    Active(anon):     709296 kB                       
    Inactive(anon):   115352 kB                       
    Active(file):    1068656 kB                       |
     < - -> [a]up, [z]down '

`finger`
--------

`finger` muestra información acerca de los usuarios del sistema, tal
como el nombre de usuario, el nombre real, el terminal al que está
conectado y si tiene permisos de escritura, la hora de inicio de sesión,
tiempo que ha estado ocioso, información de contacto, si tiene correo y
cuando fue la última vez que lo consultó, etc.

    $ finger
    Login     Name       Tty      Idle  Login Time   Office     Office Phone
    karpoke   karpoke    tty7       26  Aug  1 08:31 (:0)
    karpoke   karpoke    pts/0          Aug  1 08:32 (:0.0)

    $ finger karpoke
    Login: karpoke                  Name: karpoke
    Directory: /home/karpoke                Shell: /bin/bash
    On since Mon Aug  1 08:31 (CEST) on tty7 from :0
        27 minutes 18 seconds idle
    On since Mon Aug  1 08:32 (CEST) on pts/0 from :0.0
    Mail last read Sat Jul 30 14:40 2011 (CEST)
    No Plan.

Antiguamente, se podía acceder a la información de un usuario de forma
remota. Hoy en día, el servicio de `finger` no suele utilizarse, por lo
que se limita a mostrar información de nuestra propia máquina.

Hay una serie de ficheros que se mostrarán si se encuentran en el
directorio del usuario: `.plan`, `.project` y `.gpgkey`. Además, si el
fichero `~/.nofinger` existe, `finger` no mostrará información del
usuario a ninguna petición remota.

`last`
------

`last` muestra los último usuarios conectados. Por defecto, busca la
información en el fichero `/var/log/wtmp`. La información se limpia a
principios de cada mes.

    $ last
    karpoke  pts/1        192.168.50.10     Mon Aug  1 09:11   still logged in
    wtmp begins Mon Aug  1 09:11:04 2011

Cuando tengamos muchas entradas, una opción interesante sería mostrar el
listado en orden inverso:

    $ last | tac
    wtmp begins Mon Aug  1 09:11:04 2011
    karpoke  pts/1        192.168.50.10     Mon Aug  1 09:11   still logged in

`lastlog`
---------

`lastlog` muestra la última conexión de los usuario del sistema. Permite
especificar un rango de fechas o un usuario concreto. El orden es el
mismo en el que aparecen en `/etc/passwd`.

    $ lastlog -t 1000
    Username         Port     From             Latest
    root             tty2                      dom nov  1 13:40:34 +0100 2009
    karpoke          pts/1    192.168.50.10    lun ago  1 09:11:04 +0200 2011

El contenido lo lee del fichero binario `/var/log/lastlog`.

`acct`
------

`acct` muestra el tiempo de conexión en horas basándose en el fichero
`/var/log/wtmp`. Permite múltiples opciones, como el tiempo total por
día o por usuario. También muestra el total global.

    $ ac -d
    Today   total        0.24

    $ ac -p
    karpoke                              0.25
    total        0.25

El tiempo se expresa en horas en formato decimal, pero podemos
[convertirlo fácilmente a sexagesimal][]:

    $ ac -d | awk '{h=int($NF); m=($NF-h)*60; s=int((m-int(m))*60); m=int(m); print $0" = "h"h "m"m "s"s "}'
    Today   total        0.31 = 0h 18m 36s

  [usuarios están conectados al sistema]: {filename}/admin/la-guardiana-de-la-puerta.md
    "recibir un aviso cuando un usuario se conecta"
  [la variable DISPLAY]: http://linux-faq.blogspot.com/2008/05/display-variable.html
    "la variable DISPLAY"
  [iniciar otra sesión gráfica]: http://usuariodebian.blogspot.com/2007/08/varias-sesiones-la-misma-vez.html
    "iniciar otra sesión gráfica"
  [única y exclusivamente]: {filename}/memo/true.md
    "No hay nada como hacer sólo una cosa, pero hacerla bien..."
  [convertirlo fácilmente a sexagesimal]: http://www.commandlinefu.com/commands/view/5908/print-statistics-about-users-connect-time
    "convertirlo fácilmente a sexagesimal"
