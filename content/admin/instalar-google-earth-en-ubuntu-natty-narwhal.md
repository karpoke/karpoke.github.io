Title: Instalar Google Earth en Ubuntu Natty Narwhal
Date: 2011-07-15 15:46
Author: Nacho Cano
Tags: 11.04, asco de vida, dpkg, gdebi, google, google earth, googleearth-package, GoogleEarthLinux.bin, make-googleearth-package, microsoft, natty narwhal, ubuntu, wget
Slug: instalar-google-earth-en-ubuntu-natty-narwhal

Ésta es la única manera en que me ha funcionado. Nada de [bajar el `.deb`][bajar el .deb]
de su página—además de que, ahora mismo, baja el fichero
[GoogleEarthLinux.bin][]—, ni [googleearth-package][], ni
[gdebi][], ni [nada][].

![Google Earth]({static}/images/google-earth-300x178.png)

[Bajamos el paquete estable][] y lo instalamos:

```bash
$ wget https://dl-ssl.google.com/linux/direct/google-earth-stable_current_i386.deb
$ sudo dpkg -i google-earth-stable_current_i386.deb
```


Es posible que necesitemos el paquete `lsb-core`:

```bash
$ sudo aptitude install lsb-core
```

Si las fuentes de la interfaz gráfica se ven realmente mal, instalamos
las fuentes de Microsoft (ADV).

```bash
$ sudo aptitude install ttf-mscorefonts-installer
```

Deberemos cerrar la sesión de usuario y volver a entrar para que los
cambios en las fuentes tengan efecto.

  [bajar el .deb]: http://www.google.com/earth/download/ge/agree.html
    "bajar el .deb"
  [GoogleEarthLinux.bin]: http://mizaq.blogspot.com/2011/07/instalar-google-earth-en-ubuntu-1010.html
    "GoogleEarthLinux.bin"
  [googleearth-package]: http://help.ubuntu.com/community/GoogleEarth#Using%20make-googleearth-package
    "googleearth-package"
  [gdebi]: http://help.ubuntu.com/community/GoogleEarth#Installing%20the%20.deb%20file%20downloaded%20from%20the%20Google%20Earth%20Website
    "gdebi"
  [nada]: http://www.google.com/support/forum/p/earth/thread?tid=6f59e15bf811d4e2&hl=en
    "nada"
  [bajamos el paquete estable]: http://blogs.udp.cl/instalar-google-earth-6012032-beta-en-ubuntu-1010-maverick
    "bajamos el paquete estable"
