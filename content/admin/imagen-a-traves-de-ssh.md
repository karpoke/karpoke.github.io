Title: Imagen a través de SSH
Date: 2011-09-28 20:48
Author: Nacho Cano
Tags: eog, gnome-screensaver, imagemagick, import, pkill, scp, scrot, ssh
Slug: imagen-a-traves-de-ssh
Related: sonido-a-traves-de-ssh,conectarse-por-ssh-solo-usando-la-clave

Si tenemos acceso por SSH a otro ordenador, ambos con entorno gráfico,
podemos redirigir la pantalla, el teclado y el ratón en ambos sentidos,
es decir, podemos conseguir cosas como:

» [aplicaciones remotas que se muestren en nuestro equipo][]
» [aplicaciones remotas que se muestren en el equipo remoto][]
» [aplicaciones locales que se muestren en el equipo remoto][]
» [recibir una captura de pantalla del equipo remoto][]
» [enviar una captura de pantalla de nuestro equipo al equipo
    remoto][]
» [mostrar una imagen remota en nuestro equipo][]
» [mostrar una imagen local en el equipo remoto][]


<a name="aplicaciones-remotas-a-servidor-local"></a>

Aplicaciones remotas en el servidor gráfico local
-------------------------------------------------

Si queremos que un programa de un equipo remoto se ejecute en el
servidor gráfico de nuestro equipo, una de las cosas que podemos hacer
es [configurar el servidor SSH del equipo remoto][] para que acepte el
reenvío X11, o _X11 Forwarding_. De esta forma la conexión va cifrada y,
además, tampoco debemos preocuparnos por el valor de la variable de
entorno `DISPLAY`. Para que el servidor SSH permita el reenvío X11,
deberemos asegurarnos de que en el archivo de configuración
`/etc/ssh/sshd_config` aparece lo siguiente:

```bash
X11Forwarding yes
```

Si no estuviera, lo añadimos y reiniciamos el servicio. Ahora,
iniciaremos una conexión SSH desde el cliente, utilizando el argumento `-X`
de `ssh`:

```bash
$ ssh -C -X user@remotehost
```

El argumento `-X` permite reenviar el terminal gráfico. Se debe utilizar
con cuidado, tal como lo indican en la página del manual. Un usuario del
equipo remoto que pueda saltarse los permisos de archivo (para la base
de datos de usuarios autorizados del servidor X) podría acceder al
terminal gráfico de nuestro equipo a través de la conexión reenviada. Un
atacante podría realizar acciones como por ejemplo monitorizar las
pulsaciones de teclado. Por este motivo, el reenvío X11 está sujeto a
varias restricciones por defecto según la política de seguridad de X11.
Utilizando el argumento `-Y` se confía en el equipo remoto y no se llevan a
cabo los controles ni se aplican estas restricciones.

Cuando ejecutemos una aplicación con interfaz gráfica, ésta se abrirá en
nuestro equipo.

```bash
remotehost$ xeyes &
```

<a name="aplicaciones-remotas-a-servidor-remoto"></a>

Aplicaciones remotas en el servidor gráfico remoto
--------------------------------------------------

Si lo que queremos es abrir un programa con interfaz gráfica del equipo
remoto, pero esta vez [en el servidor gráfico del equipo remoto][], no
es necesario recurrir al reenvío X11. Lo único que hay que hacer, una
vez iniciada la sesión en el equipo remoto, es modificar el valor de la
variable de entorno `DISPLAY`:

```bash
remotehost$ export DISPLAY=:0
```

Cuando lancemos una aplicación con interfaz gráfica instalada en el
equipo remoto, ésta se abrirá en el servidor gráfico del equipo remoto.

En lugar de exportar la variable, podemos definirla únicamente para una
aplicación en concreto:

```bash
$ DISPLAY=:0 xterm
```

<a name="aplicaciones-locales-a-servidor-remoto"></a>

Aplicaciones gráficas locales en el entorno gráfico remoto
----------------------------------------------------------

Podemos utilizar lo visto en los dos casos anteriores para conseguir que
una aplicación de nuestro equipo se ejecute en el servidor gráfico
remoto a través de SSH. Necesitaremos tener un servidor SSH corriendo en
nuestro equipo.

Primero, establecemos un túnel inverso entre nuestro equipo y el equipo
remoto. Esto quiere decir que se creará una redirección en el puerto
8000 del equipo remoto al servidor SSH de nuestro equipo.

```bash
$ ssh -R 8000:localhost:22 remoteuser@remotehost
```

Una vez iniciada esta conexión, modificaremos el valor de la variable
`DISPLAY` y nos conectaremos al puerto local 8000 que redirige a nuestro
equipo:

```bash
remotehost$ DISPLAY=:0 ssh -C -X -p8000 user@localhost
```

Cuando hayamos iniciado sesión en nuestro equipo será como tener otro
terminal abierto, sólo que las aplicaciones que ejecutemos en éste se
mostrarán en el equipo remoto.

En esta página podemos encontrar una comparativa del [consumo de ancho
de banda][] de diferentes programas a través del túnel seguro.

<a name="captura-escritorio-remoto-a-local"></a>

Obtener una captura del escritorio remoto
-----------------------------------------

Si lo que queremos es hacer una captura del escritorio del equipo
remoto, podemos utilizar el comando `import`:

```bash
$ ssh -C user@remotehost "DISPLAY=:0.0 import -window root -format png -" | display -format png -
```

En lugar de visualizarla directamente, podríamos guardarla en el equipo
remoto y luego copiar las capturas con `scp`.

Otro comando sería `scrot`, disponible en los repositorios:

```bash
$ ssh -C user@remotehost "DISPLAY=:0.0 scrot -z - | display -
```

Si está puesto el [protector de pantalla][], por ejemplo, si la captura
sale en negro, deberemos matar el proceso para poder ver el escritorio.

```bash
$ ssh user@remotehost "pkill gnome-screensaver"
```

<a name="captura-escritorio-local-a-servidor-remoto"></a>

Mostrar una captura de nuestro escritorio en el equipo remoto
-------------------------------------------------------------

El caso contrario al anterior.

```bash
$ import -window root -format png - | ssh -C user@remotehost "DISPLAY=:0.0 display -format png -"
```

Otra forma sería guardar la captura en un fichero, enviarlo y luego
abrir una aplicación en el equipo remoto:

```bash
$ import -window root -format png screenshot.png
$ scp screenshot.png user@remotehost:~
$ ssh user@remotehost "DISPLAY=:0 eog screenshot.png"
```

<a name="imagen-servidor-remoto-a-local"></a>

Mostrar imágenes del equipo remoto
----------------------------------

De la misma forma que realizamos una captura, podemos enviarnos una
imagen y visualizarla directamente:

```bash
$ ssh -C user@remotehost "cat screenshot.png" | display -format png -
```

<a name="imagen-local-a-servidor-remoto"></a>

Mostrar imágenes de nuestro equipo en el equipo remoto
------------------------------------------------------

Podemos conseguir que se habrá una aplicación remota que muestre una
imagen de nuestro equipo:

```bash
$ cat screenshot.png | ssh -C user@remotehost "DISPLAY=:0 display -format png -"
```

  [aplicaciones remotas que se muestren en nuestro equipo]: #aplicaciones-remotas-a-servidor-local
    "aplicaciones remotas que se muestren en nuestro equipo"
  [aplicaciones remotas que se muestren en el equipo remoto]: #aplicaciones-remotas-a-servidor-remoto
    "aplicaciones remotas que se muestren en el equipo remoto"
  [aplicaciones locales que se muestren en el equipo remoto]: #aplicaciones-locales-a-servidor-remoto
    "aplicaciones locales que se muestren en el equipo remoto"
  [recibir una captura de pantalla del equipo remoto]: #captura-escritorio-remoto-a-local
    "recibir una captura de pantalla del equipo remoto"
  [enviar una captura de pantalla de nuestro equipo al equipo remoto]: #captura-escritorio-local-a-servidor-remoto
    "enviar una captura de pantalla de nuestro equipo al equipo remoto"
  [mostrar una imagen remota en nuestro equipo]: #imagen-servidor-remoto-a-local
    "Mostrar una imagen remota en nuestro equipo"
  [mostrar una imagen local en el equipo remoto]: #imagen-local-a-servidor-remoto
    "Mostrar una imagen local en el equipo remoto"
  [configurar el servidor SSH del equipo remoto]: http://www.guia-ubuntu.org/index.php?title=Servidor_ssh
    "configurar el servidor SSH del equipo remoto"
  [en el servidor gráfico del equipo remoto]: http://www.carballude.es/blog/2010/05/02/ejecutar-programas-en-la-pantalla-remota-mediante-ssh/
    "en el servidor gráfico del equipo remoto"
  [consumo de ancho de banda]: http://www.vanemery.com/Linux/XoverSSH/X-over-SSH2.html
    "consumo de ancho de banda"
  [protector de pantalla]: {filename}/admin/salvapantallas-con-el-codigo-fuente-del-kernel.md
    "protector de pantalla"
