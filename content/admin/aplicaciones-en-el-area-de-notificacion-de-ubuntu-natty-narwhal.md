Title: Aplicaciones en el área de notificación de Ubuntu Natty Narwhal
Date: 2011-05-12 11:57
Author: Nacho Cano
Tags: 11.04, 11.10, área de notificación, dropbox, gsettings, ubuntu natty narwhal, ubuntu oneiric ocelot, unity
Slug: aplicaciones-en-el-area-de-notificacion-de-ubuntu-natty-narwhal

Con la llegada de la nueva Ubuntu, se ha cambiado el área de
notificación por una [nueva API][]. Para las aplicaciones que todavía no
se han adaptado, se ha habilitado una lista blanca de aplicaciones que
pueden utilizar la antigua área de notificación, hasta que se
actualicen.

Para ver qué aplicaciones hay en la lista:

```bash
$ gsettings get com.canonical.Unity.Panel systray-whitelist
['JavaEmbeddedFrame', 'Mumble', 'Wine', 'Skype', 'hp-systray', 'scp-dbus-service']
```

Para añadir una aplicación, por ejemplo, `dropbox`:

```bash
$ gsettings get com.canonical.Unity.Panel systray-whitelist ['JavaEmbeddedFrame', 'Mumble', 'Wine', 'Skype', 'hp-systray', 'scp-dbus-service', 'dropbox']
```

Para volver a los valores originales:

```bash
$ gsettings reset com.canonical.Unity.Panel systray-whitelist
```

* * * * *

#### Actualizado el 4 de febrero de 2012

El truco sigue funcionando en Ubuntu Oneiric Ocelot (11.10). Si queremos
que el icono de Dropbox aparezca sin tener que cerrar la sesión, podemos
matar el proceso y volverlo a arrancar:

```bash
$ killall dropbox
$ /usr/bin/dropbox
```

Si estamos [utilizando múltiples cuentas de Dropbox][], podemos hacer lo
mismo, pero lanzando el _script_, en lugar del comando `dropbox`
directamente:

```bash
$ killall dropbox
$ MultipleDropboxInstances.sh
```

* * * * *

  [nueva API]: http://pricklytech.wordpress.com/2011/04/30/ubuntu-11-4-natty-customizing-the-notification-area-in-unity/
    "nueva API"
  [utilizando múltiples cuentas de Dropbox]: {filename}/admin/multiples-cuentas-de-dropbox-en-ubuntu-maverick-meerkat.md
    "utilizando múltiples cuentas de Dropbox"
