Title: Túnel SSH inverso
Date: 2011-09-30 18:03
Author: Nacho Cano
Tags: 2FA, contraseña de un solo uso, OTP, ssh, túnel inverso, verificación en dos pasos
Slug: tunel-ssh-inverso
Related: sslh-compartiendo-el-puerto-443,compartiendo-una-conexion-por-ssh,conectarse-por-ssh-utilizando-expect,conectarse-por-ssh-solo-usando-la-clave,servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal,fwknop-single-packet-authorization-y-port-knocking,ssh-over-http-proxy,utilizar-ssh-para-establecer-un-servidor-proxy-socks

El escenario es el siguiente. Tenemos un equipo remoto C detrás de un
cortafuegos, _router_ o similar, que no podemos configurar y no permite
conexiones entrantes, de tal manera que el equipo es inaccesible desde
el exterior de la red en la que está. Otro equipo A, el nuestro, también
está detrás de un cortafuegos, en otra red, que tampoco podemos
configurar y tampoco permite conexiones entrantes. La buena noticia es
que tenemos un servidor remoto B en otra red diferente al que sí tenemos
acceso por SSH desde el equipo remoto C y desde el nuestro (el A). Tanto
el equipo remoto C como el servidor B tienen un servidor SSH corriendo.

Una posible solución es abrir un túnel inverso del equipo C al servidor
B, entonces desde nuestro equipo (el A) conectarnos al servidor B y de
ahí al equipo remoto C.

El siguiente comando abre un túnel inverso desde el equipo C al servidor
B, de tal manera que en el servidor B en el puerto 8000 se podrá iniciar
una conexión que será redirigida al servidor SSH del equipo C:

```bash
remoteC$ ssh -f -N -R 8000:localhost:22 userB@remoteB    # remoteC:22    --->    remoteB:8000
hostA$   ssh userB@remoteB
remoteB$ ssh -p8000 userC@localhost
```

Estas dos últimas acciones se pueden combinar en una sola si utilizamos
el argumento `-t` para utilizar el servidor SSH de B como servidor
intermedio para acceder a C (a través de la redirección en el propio
servidor B):

```bash
remoteC$ ssh -f -N -R 8000:localhost:22 userB@remoteB    # remoteC:22    --->    remoteB:8000
hostA$   ssh -t userB@remoteB ssh -p8000 localhost
```

Otra forma es abrir un túnel desde nuestro equipo creando una
redirección local al puerto del servidor B en el cual se ha creado,
previamente, el túnel inverso al equipo remoto C. De esta forma bastará
conectarnos a nuestro propio equipo para tener acceso al equipo remoto
C:

```bash
remoteC$ ssh -f -N -R 8000:localhost:22 userB@remoteB    # remoteC:22    --->    remoteB:8000
hostA$   ssh -f -N -L 8001:localhost:8000 userB@remoteB    # remoteB:8000  --->    hostA:8001
hostA$   ssh -p8000 userC@localhost
```

Sería mejor que los usuarios para conectarnos al servidor B desde el
equipo remoto C y desde el nuestro fuesen distintos:

```bash
remoteC$ ssh -f -N -R 8000:localhost:22 user_1B@remoteB  # remoteC:22    --->    remoteB:8000
hostA$   ssh -f -N -L 8001:localhost:8000 user_2B@remoteB  # hostA:8001    < --    remoteB:8000
hostA$   ssh -p8000 userC@localhost
```

Como último comentario, si vamos a utilizar este sistema para
administrar equipos remotos, quizá sería interesante utilizar algún
sistema de [contraseñas de un solo uso][] en el servidor.

  [contraseñas de un solo uso]: {filename}/admin/servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal.md
    "contraseñas de un solo uso"
