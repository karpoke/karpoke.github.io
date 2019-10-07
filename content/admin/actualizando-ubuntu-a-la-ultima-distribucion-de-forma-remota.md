Title: Actualizando Ubuntu a la última distribución de forma remota
Date: 2011-01-07 04:38
Author: Nacho Cano
Tags: 10.04, 10.10, actualización, do-release-upgrade, ubuntu lucid lynx, ubuntu maverick meerkat, update-manager
Slug: actualizando-ubuntu-a-la-ultima-distribucion-de-forma-remota

Instalamos el paquete `update-manager`, si es que no lo teníamos:

```bash
$ sudo aptitude install update-manager
```

Comprobamos que el fichero `/etc/update-manager/release-upgrades`
contiene:

```bash
Prompt=normal
```

Si contiene `Prompt=lts` sólo nos actualizará si hay una [LTS][] nueva.
Si contiene `Prompt=never`... no actualizará nada.

![Ape Man Evolution]({static}/images/ape_man_evolution.png)

Y ejecutamos el comando `do-release-upgrade`:

```bash
$ sudo do-release-upgrade
```

» [ubuntugeek][]

  [LTS]: http://es.wikipedia.org/wiki/Ubuntu
    "LTS"
  [ubuntugeek]: http://www.ubuntugeek.com/how-to-upgrade-from-ubuntu-10-04-lucid-to-ubuntu-10-10-maverick-desktop-and-server.html
    "ubuntugeek"
