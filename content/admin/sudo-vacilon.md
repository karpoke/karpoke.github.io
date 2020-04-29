Title: sudo vacilón
Date: 2011-08-04 13:32
Author: Nacho Cano
Tags: sudo, sudo rm -fr, visudo
Slug: sudo-vacilon

    $ sudo passwd
    [sudo] password for user:
    Are you on drugs?
    [sudo] password for user:
    Maybe if you used more than just two fingers...
    [sudo] password for user:
    I’ve seen penguins that can type better than that.
    sudo: 3 incorrect password attempts

Si te gustaría recibir un piropo cada vez que [escribes mal la
contraseña de `sudo`][escribes mal la contraseña de sudo], no
tienes más que editar el archivo de configuración de [`sudo`][sudo],
`/etc/sudoers`, mediante el comando `visudo`:

    $ sudo visudo

Y añadir la opción `insults`:

    Defaults        env_reset,insults

  [escribes mal la contraseña de sudo]: http://usemoslinux.blogspot.com/2011/08/sudo-no-me-insultes-el-terminal-se.html
    "escribes mal la contraseña de sudo"
  [sudo]: {filename}/memo/with-great-power-comes-great-responsibility.md
    "un gran poder conlleva una gran responsabilidad"
