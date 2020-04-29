Title: De pantallas bloqueadas, capturas de pantalla y David Hasselhoff
Date: 2010-10-06 18:36
Author: Nacho Cano
Tags: ataque Hasselhoff, captura de pantalla, chvt, fondo de pantalla, gconftool-2, import, sleep, terminal bloqueado
Slug: de-pantallas-bloqueadas-capturas-de-pantalla-y-david-hasselhoff

El [ataque David Hasselhof][] es una de las técnicas de guerrilla de
oficina con la mejor relación coste/humillación ^_[cita\\ requerida]_^,
basta encontrarse una sesión de usuario abierta (y no protegida contra
este "ataque") y, ¡zas!, en toda la boca.

No sé si un [aviso disuasorio][] como medida de prevención contra este
tipo de ataque será efectivo, pero me ha hecho preguntarme cómo
podríamos incluirlo en Gnome.


Capturas de pantalla
--------------------

Curiosamente, lo primero que he encontrado sobre la ventana de
desbloquear la pantalla es que no se puede realizar una captura de
pantalla de la misma pulsando la tecla `Impr Pant`; pruébalo!

Esto no significa que no se pueda realizar, y no hablo de recurrir a
métodos como un escritorio remoto o una máquina virtual, sino desde la
consola:

    $ sleep 5; import -window root screenshot.png

Tras escribir estos comandos en una consola, tendremos 5 segundos para
que se realice una captura de pantalla, con el comando `import`, y que
se guardará como `screenshot.png`.

Para que la captura se realice de la pantalla de desbloqueo, primero
debemos bloquear la sesión. Vamos al menú de sesión, bloquear la
pantalla y una vez bloqueada, movemos el ratón o pulsamos alguna tecla
para que aparezca la ventana de desbloqueo. También podemos bloquear la
sesión pulsando la combinación de teclas `Ctrl+Alt+L`.

![Lock Screen]({static}/images/lock-screen1-300x119.png)

Ya puestos, si queremos realizar una captura de pantalla en un ordenador
remoto, estando conectados a través de `ssh`, debemos, además de
inicializar la variable de entorno `DISPLAY`, cambiar previamente al
terminal gráfico, `/dev/tty7`, con el comando `chvt`, más o menos lo que
haríamos con la combinación de teclas `Ctrl+Alt+F7` si fuese en local:

    $ chvt 7; sleep 5; DISPLAY=:0.0 import -window root screenshot.png

Ventana de desbloqueo
---------------------

Para añadir el mensaje disuasorio, debemos fijarnos en el fichero
`/usr/share/gnome-screensaver/lock-dialog-default.ui`. En ese fichero se
define el contenido de la ventana de desbloqueo, es decir, cosas como:

-   `auth-realname-label`, el nombre real del usuario,
-   `auth-username-label`, el nombre de usuario y el del equpo,
-   `auth-status-label`, el mensaje de estado

El mensaje de estado se utiliza, cuando es necesario, para mostrar
mensajes como que se está comprobando la contraseña o que ésta es
incorrecta. Utilizaremos este campo para mostrar inicialmente el aviso
disuasorio. Para esto, modificamos la propiedad `label` del objeto con
el `id=auth-status-label`:


   AVISO: Terminal protegida contra ataques 'Hasselhoff'.
   En caso de ser detectado, se tomarán represalias.

![Lock Screen Aviso]({static}/images/lock-screen-aviso1-300x108.png)

El ataque David Hasselhoff
--------------------------

Receta para Ubuntu:

1.  Descargar una imagen de David Hasselhoff como [esta][]
2.  Abrirla con el visor de imágenes de Gnome (EOG, _Eye of Gnome_)
3.  Menú Imagen > Establecer como fondo de escritorio, o `Ctrl+F8`

También lo podríamos hacer de forma remota, pero aquí tiene menos
gracia, ya que, o bien tenemos acceso a la cuenta de usuario o bien
tenemos privilegios de administrador. Aún así, es difícil resistirse.

1.  Descargamos la imagen:
    `wget http://www.una-web.com/la/imagen/de/david.jpg`
2.  Ponemos la imagen de fondo:
    `gconftool-2 -t str --set /desktop/gnome/background/picture_filename /ruta/aboluta/a/la/imagen/david.jpg`

- más sobre el ataque Hasselhoff en [el lado del mal][]

  [ataque David Hasselhof]: http://windowstips.wordpress.com/2008/06/08/el-caso-del-hacker-de-la-oficina/
    "ataque David Hasselhof"
  [aviso disuasorio]: http://www.seguridadapple.com/2010/10/mostrar-avisos-disuasorios-en-la.html
    "aviso disuasorio"
  [esta]: http://www.periodistadigital.com/imagenes/2009/12/01/david-hasselhoff.jpg
    "esta"
  [el lado del mal]: http://www.google.es/search?q=ataque+david+hasselhoff+site:elladodelmal.com
    "el lado del mal"
