Title: Instalar Spotify en Ubuntu 16.04
Date: 2016-12-15 07:58
Author: Ignacio Cano
Tags: Spotify, Ubuntu, Xenial Xerus, 16.04, apt-key, sources.list, apt, PPA
Slug: instalar-spotify-en-ubuntu-16-04

Si queremos instalar el cliente de Spotify en Ubuntu Xenial Xerus, tan sólo
tenemos que instalar la clave:

```bash
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys BBEBDCB318AD50EC6865090613B00F1FD2C19886
Executing: /tmp/tmp.imoQkQ9ZVV/gpg.1.sh --keyserver
hkp://keyserver.ubuntu.com:80
--recv-keys
BBEBDCB318AD50EC6865090613B00F1FD2C19886
gpg: solicitando clave D2C19886 de hkp servidor keyserver.ubuntu.com
gpg: clave D2C19886: clave pública "Spotify Public Repository Signing Key <operations@spotify.com>" importada
gpg: Cantidad total procesada: 1
gpg:               importadas: 1  (RSA: 1)
```

Añadimos el PPA oficial:

```bash
$ echo "deb http://repository.spotify.com stable non-free" |
  sudo tee /etc/apt/sources.list.d/spotify.list
```

Actualizamos e instalamos:

```bash
$ sudo apt update
# sudo apt install spotify-client
```

Referencias
-----------

- [spotify.com][]

  [spotify.com]: https://www.spotify.com/es/download/linux/
    "Spotify for Linux"
