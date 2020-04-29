Title: Personalizando el arranque gráfico en Ubuntu Maverirk Meerkat
Date: 2011-01-18 06:55
Author: Nacho Cano
Tags: 10.10, arranque gráfico, grub2 splash, plymouth themes, ubuntu maverick meerkat
Slug: personalizando-el-arranque-grafico-en-ubuntu-maverirk-meerkat

Tras arreglar un par de [problemas que tenía con el arranque][], ya que
estamos, vamos a darle un toque distinto al asunto.

Temas de Plymouth
-----------------

Instalamos algunos de los [temas para Plymouth][]:

    $ sudo apt-get install plymouth-theme-{fade-in,glow,sabily,script,solar,spinfinity,text,ubuntu-logo,text}

Cambiamos por el que queramos:

    $ sudo update-alternatives --config default.plymouth

Y actualizamos el `initramfs`:

    $ sudo update-initramfs -u

Cuando reiciniemos habremos cambiado el tema de Playmouth.

Splashscreen de Grub2
---------------------

Editamos el archivo `/etc/grub.d/05_debian_theme`, y modificamos la
línea:

    WALLPAPER="/usr/share/images/desktop-base/moreblue-orbit-grub.png"

para que apunte a la ruta de la imagen que queramos.

![Gimp Splash BM]({static}/images/gimp_splash_bm-296x300.png)

No hace falta que sea una del directorio `/usr/share/images/grub`,
podemos crearla nosotros, pero debe respetar la resolución que tiene la
pantalla del menú de Grub2, y que está espeficada en el archivo
`/etc/default/grub`.

Actualizamos `grub2`

    $ sudo update-grub2

- imagen de [BlackMooon][]

  [problemas que tenía con el arranque]: {filename}/admin/solucion-de-problemas-con-plymouth-y-ati-en-ubuntu-maverick-meerkat.md
    "solución de problemas con plymouth y ati en ubuntu maverick meerkat"
  [temas para Plymouth]: http://sliceoflinux.com/2010/05/14/cambia-el-tema-plymouth-de-tu-ubuntu-10-04/
    "temas para Plymouth"
  [BlackMooon]: http://blackmoondev.com/official-blackmoons-wallpapers/
    "BlackMooon"
