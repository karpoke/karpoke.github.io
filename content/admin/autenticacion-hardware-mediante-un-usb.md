Title: Autenticación hardware mediante un USB
Date: 2012-09-30 13:06
Author: Nacho Cano
Tags: 12.04, 2FA, autenticación, doble autenticación, token, ubuntu precise pangolin, verificación en dos pasos
Slug: autenticacion-hardware-mediante-un-usb
Related: servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal,conectarse-por-ssh-solo-usando-la-clave,conectarse-por-ssh-utilizando-expect

[pam_usb][] es un módulo que permite añadir autenticación hardware
utilizando unidades de almacenamiento extraíbles "normales", como
memorias USB, tarjetas SD/MMC, etc. Mediante `pamusb` podemos
especificar que se ejecuten diversas acciones cuando reconoce el
dispositivo conectado, como por ejemplo iniciar sesión sin tener que
introducir la contraseña o desactivar el salvapantallas, por lo que se
puede utilizar para implantar un [sistema de autenticación en dos pasos
(2FA)][].

Sirve cualquier USB, ya que el módulo no modifica su contenido, sino que
comprueba el UUID, el número de serie, el fabricante y el modelo, por lo
que, aunque se copie, no se podrá suplantar fácilmente.

Instalación
-----------

Instalamos el módulo:

```bash
$ api libpam-usb  pamusb-tools
```

Configuración
-------------

### USBs

Una vez conectado el USB que pensamos utilizar, aunque no hace falta que
esté montado, lo añadimos al archivo de configuración `/etc/pamusb.conf`
(podemos asignarle cualquier nombre):

```bash
$ sudo pamusb-conf --add-device myusb
Please select the device you wish to add.
* Using "Kingston Aurum (136C0932618F)" (only option)

Which volume would you like to use for storing data ?
* Using "/dev/sdb1 (UUID: 37AD-8A2F)" (only option)

Name        : myusb
Vendor      : Kingston
Model       : Aurum
Serial      : 136C0932618F
UUID        : 37AD-8A2F

Save to /etc/pamusb.conf ?
[Y/n] Y
Done.
```

Deberemos repetir el proceso para cada USB que queramos utilizar.

### Usuarios

El siguiente paso es configurar los usuarios que queremos que se
autentiquen:

```bash
$ sudo pamusb-conf --add-user myuser
Which device would you like to use for authentication ?
* Using "myusb" (only option)

User        : myuser
Device      : myusb

Save to /etc/pamusb.conf ?
[Y/n] Y
Done.
```

### Comprobación

Comprobamos la configuración, todavía con el USB conectado:

```bash
$ sudo pamusb-check myuser
* Authentication request for user "m" (pamusb-check)
* Device "myusb" is connected (good).
* Performing one time pad verification...
* Regenerating new pads...
* Access granted.
```

Si desconectamos el USB y volvemos a probar:

```bash
$ sudo pamusb-check myuser
* Authentication request for user "myuser" (pamusb-check)
* Device "myusb" is not connected.
* Access denied.
```

Módulo PAM
----------

Para incluir `pam_usb` en el proceso de autenticación del sistema,
deberemos editar el fichero `/etc/pam.d/common-auth` y añadir la
siguiente linea:

```bash
auth    sufficient      pam_usb.so
```

antes de la línea:

```bash
auth    required        pam_unix.so nullok_secure
```

La opción `sufficient` permite autenticar al usuario si el USB conectado
es correcto, y si no lo es continúa con el proceso de autenticación, es
decir, pide la contraseña. Si en su lugar ponemos `required` se
necesitarán ambos, USB y contraseña, para acceder al sistema.

Si sólo queremos utilizar este sistema de autenticación para algún
módulo concreto, en lugar de usar el ficheo `common-auth` editamos el
fichero correspondiente, por ejemplo `lightdm`, `sshd`, `sudo`, etc.

No es necesario reiniciar para que los cambios tengan efecto. Con el USB
desconectamos hacemos la siguiente prueba:

```bash
$ su myuser
* pam_usb v0.5.0
* Authentication request for user "myuser" (su)
* Device "myusb" is not connected.
* Access denied.
Contraseña:
```

Lo conectamos y volvemos a probar:

```bash
$ su myser
* pam_usb v0.5.0
* Authentication request for user "myuser" (su)
* Device "myusb" is connected (good).
* Performing one time pad verification...
* Access granted.
```

Agente
------

Si queremos que se ejecute un comando cuando detecte que se ha conectado
el USB, editamos el fichero `/etc/pamusb.conf`, esta vez mediante un
editor de texto, y añadimos las siguientes líneas en la sección de
configuración de usuario. Hay un ejemplo incluído como el siguiente,
aunque está comentado, y lo que hace es activar o desactivar el
salvapantallas:


```bash
myusb
gnome-screensaver-command --lock
gnome-screensaver-command --deactivate
```

Es posible que necesitemos añadir `pamusb-agent` para que se ejecute al
inicio, aunque con Ubuntu Precise Pangolin no me ha hecho falta. Si
tenemos un entorno de escritorio, podemos incluirlo a través del menú de
Aplicaciones al inicio.

Si queremos hacerlo desde el terminal, dependerá de si usamos `init` o
`upstart`.

### Upstart

Si usamos el sistema `upstart`, para hacer que se ejecute al inicio,
creamos el archivo `/etc/init/pamusb-agent.conf`:

```bash
# pamusb-agent - pam_usb event handler
#
# pamusb-agent is in charge of executing commands upon USB device insertion
# (once authenticated through pam_usb) and removal.

description     "pamusb-agent background daemon"

start on runlevel [2345]
stop on runlevel [!2345]

expect fork
respawn

exec /usr/bin/pamusb-agent
```

Mediante `respawn` especificamos que se reinicie el proceso si termina
de forma inesperada.

Vamos al directorio `/etc/init.d` y creamos el siguiente enlace
simbólico:

```bash
$ sudo ln -s /lib/init/upstart-job pamusb-agent
```

### init

Si utilizamos `init`, añadimos el siguiente _script_ en el directorio
`/etc/init.d`:

```bash
#!/usr/bin/env bash
/usr/bin/pamusb-agent
```

Le damos permisos de ejecución:

```bash
$ sudo chmod +x /etc/init.d/pamusb-agent
```

Lo añadimos al inicio:

```bash
$ sudo update-rc.d pamusb-agent defaults
update-rc.d: warning: /etc/init.d/pamusb-agent missing LSB information
update-rc.d: see
 Adding system startup for /etc/init.d/pamusb-agent ...
   /etc/rc0.d/K20pamusb-agent -> ../init.d/pamusb-agent
   /etc/rc1.d/K20pamusb-agent -> ../init.d/pamusb-agent
   /etc/rc6.d/K20pamusb-agent -> ../init.d/pamusb-agent
   /etc/rc2.d/S20pamusb-agent -> ../init.d/pamusb-agent
   /etc/rc3.d/S20pamusb-agent -> ../init.d/pamusb-agent
   /etc/rc4.d/S20pamusb-agent -> ../init.d/pamusb-agent
   /etc/rc5.d/S20pamusb-agent -> ../init.d/pamusb-agent
```

Para activarlo sin tener que reiniciar, ejecutamos:

```bash
$ sudo service pamusb-agent start
```

Referencias
-----------

- [pam_usb][]
- [Upstart][]

  [pam_usb]: http://pamusb.org/
    "pam_usb"
  [sistema de autenticación en dos pasos (2FA)]: {filename}/admin/servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal.md
    "sistema de autenticación en dos pasos (2FA)"
  [Upstart]: http://upstart.ubuntu.com/wiki/Stanzas
    "Upstart"
