Title: Solucionado el error "Fontconfig warning: reading configurations from ~/.fonts.conf is deprecated." en Ubuntu
Date: 2012-12-23 13:51
Author: Nacho Cano
Tags: 12.10, deprecated, fontconfig, quantal quetzal, ubuntu, warning
Slug: solucionado-el-error-fontconfig-warning-reading-configurations-from-fonts-conf-is-deprecated-en-ubuntu

En Ubuntu, si tenemos el archivo de configuración `~./fonts.conf` y
lanzamos una aplicación que lo utilice, es posible que nos aparezca un
error como el siguiente:

    Fontconfig warning: "/etc/fonts/conf.d/50-user.conf", line 9: reading configurations from ~/.fonts.conf is deprecated.

El motivo, [tal como apunta Githlar en este foro][], es que
`~/.fonts.conf` será eliminado en el futuro. La solución pasa por mover
el fichero a su nuevo emplazamiento (es posible que necesitemos primero
crear el directorio destino):

    $ mkdir -p .config/fontconfig
    $ mv -i ~/.fonts.conf ~/.config/fontconfig/fonts.conf

Referencias
-----------

» [Fontconfig warning][]
» [better \~/.fonts.conf deprecation warning][tal como apunta Githlar
en este foro]

  [tal como apunta Githlar en este foro]: http://askubuntu.com/questions/206271/fontconfig-warning
    "tal como apunta Githlar en este foro"
  [Fontconfig warning]: https://bugs.launchpad.net/ubuntu/+source/fontconfig/+bug/1068549
    "Fontconfig warning"
