Title: Reiniciar el router desde el terminal
Date: 2012-02-09 21:36
Author: Nacho Cano
Tags: comtrend, expect, ip, router, script, telnet, vr-3025u, yad
Slug: reiniciar-el-router-desde-bash
Related: conectarse-por-ssh-utilizando-expect,obteniendo-la-ip-publica-la-ip-privada-y-la-direccion-mac-en-bash

De vez en cuando, necesitamos reiniciar nuestro _router_. Por ejemplo,
para provocar un cambio de IP, si tenemos IP dinámica. Podemos acceder
al panel de administración del _router_ mediante el navegador,
normalmente en el puerto 80 u 8080, aunque también es posible hacerlo a
través de telnet, en el puerto 22.

Para hacer más sencillo este trámite, utilizaremos un _script_ que se
conecta por telnet al _router_, introduce el usuario y la contraseña y
lo reinicia mediante el comando `reboot`. Esto dependerá de cada modelo
de _router_ en concreto, pero creo que funciona para un gran número. En
principio, no es posible apagarlo, sólo reiniciarlo.

El siguiente _script_, `router.sh`, permite ejecutar un comando en el
_router_ utilizando `expect`:

```bash
#!/usr/bin/expect -f
set timeout 20
set username "admin"
set password "admin"
set ip "192.168.1.1"

# Read command as arg to this script
set cmd [lindex $argv 0]

spawn telnet $ip

expect "Login:"
send -- "$username\r"
expect "Password:"
send -- "$password\r"

expect " > "
send -- "$cmd\r"

expect " > "
send -- "^D"
```

Para reiniciarlo, ejecutamos:

```bash
$ router.sh reboot
```

Para obtener un listado de comandos disponibles, en este caso en un
Comtrend:

```bash
$ router.sh help
spawn telnet 192.168.1.1
Trying 192.168.1.1...
Connected to 192.168.1.1.
Escape character is '^]'.
BCM96328 Broadband Router
Login: admin
Password:
 > help
?
help
logout
exit
quit
reboot
adsl
xdslctl
xtm
brctl
cat
loglevel
logdest
virtualserver
ddns
df
dumpcfg
dumpmdm
meminfo
psp
kill
dnsproxy
syslog
echo
ifconfig
ping
ps
pwd
sntp
sysinfo
tftp
wlctl
arp
defaultgateway
dhcpserver
dns
lan
lanhosts
passwd
ppp
restoredefault
route
save
swversion
cfgupdate
swupdate
exitOnIdle
wan
build
version
```

Mejorando el _script_
---------------------

Un inconveniente es que los datos de conexión, usuario, contraseña e IP,
están escritos directamente en el _script_. Podemos modificar el
_script_ para que nos pida los datos, o pasárselos como parámetros, pero
si lo hacemos así, prácticamente no ganamos nada respecto a conectarnos
directamente por telnet al _router_.

Mediante `yad` (_yet another dialog_, un _fork_ mejorado de `zenity`),
crearemos una sencilla interfaz gráfica que nos pida los parámetros
previamente.

Básicamente, consiste en mostrar una pantalla con 3 campos y los botones
de aceptar y cancelar. La IP del _router_ se obtiene de la salida del
comando `route`. Una vez que se haya reiniciado el _router_, nos
aparecerá una ventana mostrándonos la nueva IP.

```bash
action=$(yad
   --title "Router Reboot"
   --image=gnome-shutdown
   --form
   --field=Username
   --field=Password:H
   --field=Gateway
   --separator=" "
   --button="gtk-ok:0"
   --button="gtk-cancel:1"
$username $password $gateway)
ret=$?
```

![Router reboot]({static}/images/router-reboot-300x179.png)

Si le damos a aceptar, la variable `$action` contendrá el valor de las
variables `$username`, `$password` y `$gateway` separados por un
espacio, y `$ret` contendrá el valor del botón pulsado, 0 para aceptar y
1 para cancelar.

```bash
$ echo $action
admin admin 192.168.1.1
$ echo $ret
0
```

Enlace al _script_ `router-reboot`.

* * * * *

#### Actualizado el 26 de mayo de 2013

Ha caído en mis manos el _router_ Comtred VR-3025u de Jazztel, que
permite renovar la IP sin tener que reiniciar el router, por lo que el
cambio es mucho más rápido que esperar a que reinicie.

He encontrado el siguiente _script_ en un [foro de Banda Ancha][] para
llevar a cabo la renovación de la IP:

```bash
#!/bin/sh

# vr3025u
IFACE=ppp1.1

# vr3025un
#IFACE=ppp1

USER=admin
PASS=admin
IP=192.168.1.1

( sleep 3
  echo $USER
  sleep 1
  echo $PASS
  sleep 1
  echo ppp config $IFACE down
  sleep 5
  echo ppp config $IFACE up
  sleep 1
  echo exit ) | telnet $IP
```

* * * * *

Referencias
-----------

» [Shell script to reboot DSL/ADSL router][]
» [yad examples][]
» [Script cambio IP Comtrend VR-3025un (para JDownloader)][foro de Banda Ancha]

  [foro de Banda Ancha]: http://bandaancha.eu/foros/script-cambio-ip-comtrend-vr-3025un-1681948
    "foro de Banda Ancha"
  [Shell script to reboot DSL/ADSL router]: http://www.cyberciti.biz/tips/shell-script-to-reboot-dsladsl-router.html
    "Shell script to reboot DSL/ADSL router"
  [yad examples]: http://code.google.com/p/yad/wiki/Examples
    "yad examples"
