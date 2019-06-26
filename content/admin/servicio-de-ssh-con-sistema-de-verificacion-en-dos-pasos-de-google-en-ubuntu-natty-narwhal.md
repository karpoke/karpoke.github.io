Title: Servicio de SSH con sistema de verificación en dos pasos de Google en Ubuntu Natty Narwhal
Date: 2011-08-05 02:21
Author: Nacho Cano
Tags: 10.04, 11.04, 12.04, 2FA, android, blackberry, contraseña de un solo uso, doble autenticación, FreeOTP, google, Google Authenticator, hg, HOTP, iphone, mercurial, OTP, pin, qrcode, qrdecode, scp, ssh, token, TOTP, ubuntu, ubuntu lucid lynx, ubuntu natty narwhal, ubuntu precise pangolin, verificación en dos pasos, wget
Slug: servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal
Related: sslh-compartiendo-el-puerto-443,compartiendo-una-conexion-por-ssh,conectarse-por-ssh-utilizando-expect,conectarse-por-ssh-solo-usando-la-clave

Un sistema de verificación en dos pasos, (_Two Factor Authentication_ o
2FA) consiste en que la autenticación a un servicio se realiza mediante
dos piezas de información, una que conocemos y otra que no. La pieza que
conocemos es nuestra contraseña, que es susceptible de ser sustraída,
mientras que la información que no conocemos es un número de
identificación (PIN) aleatorio que cambia cada 30 segundos y que está
vinculado con un dispositivo hardware. Esto es lo que se conoce como una
contraseña de un solo uso (One Time Password u OTP). De esta forma,
aunque alguien nos robe o averigüe nuestra contraseña, a no ser que
también tenga acceso al dispositivo que crea los PINs, no podrá acceder
al servicio con nuestra cuenta.

Hay que tener en cuenta que, dado que el PIN es de 6 dígitos, si alguien
pudiera probar 1000000 (un millón) de contraseñas en 30 segundos
encontraría la clave, por lo que es necesario añadir algún mecanismo
extra que [impida el acceso por fuerza bruta][] al sistema.

Cuando Google introdujo 2FA en sus aplicaciones, también creó un módulo
PAM para GNU/Linux y una aplicación para el móvil que convierte nuestro
móvil en el dispositivo generador de PINs.

* * * * *

#### Actualizado el 18 de marzo de 2015

Como alternativa a la [aplicación móvil de Google][] (código disponible
en [github][]), podemos usar [FreeOTP][], una aplicación también libre
para [Android][] e iOS, compatible con [HOTP][] y [TOTP][], que servirá
perfectamente para nuestro propósito.

* * * * *

![Google Authenticator Android]({static}/images/google-authenticator-android3-180x300.gif)

<small>_Fuente: [google.com][]_</small>

Antes de comenzar, es necesario remarcar que este sistema es
incompatible con el [uso exclusivo de claves para conectarnos por
SSH][]; se debe poder acceder introduciendo usuario y contraseña.

Requisitos previos
------------------

Para [habilitar 2FA en nuestro servidor][], necesitamos descargar,
compilar e instalar el módulo PAM en nuestra máquina.

Instalación
-----------

Instalamos, previamente, los paquetes necesarios:

```bash
$ sudo aptitude install libpam0g-dev libpam-devperm mercurial
```

[Descargamos][] el módulo PAM:

```bash
$ hg clone https://code.google.com/p/google-authenticator/
```

Realizando la instalación en una Ubuntu Lucid Lynx (10.04) me aparecía
el siguiente error:

```bash
abort: repository [svn]https://zxing.googlecode.com/svn/trunk/ not found!
```

Parece ser que es porque tiene una [versión de `mercurial` un poco
vieja][versión de mercurial un poco vieja].

```bash
$ hg --version
Mercurial Distributed SCM (version 1.4.3)
```

Deberemos instalar una versión de `mercurial` más nueva de la que está
en los repositorios de Lucid, o descargar el código en otro sitio y
copiarlo. Con la versión de `mercurial` en Ubuntu Natty Narwhal no tuve
problemas:

```bash
$ hg --version
Mercurial Distributed SCM (version 1.7.5)
```

Si lo hemos bajado en otra máquina, no hace falta que copiemos el
repositorio entero, únicamente el directorio `libpam`:

```bash
user@otherhost:~$ scp -r google-authentication/libpam/ user@host:~
```

Una vez hecho este paso, lo compilamos en la máquina que lo queremos
instalar, y lo instalamos:

```bash
$ cd libpam/
$ make
```

Como inciso, comentar que, ya que estaba, también lo iba a instalar en
una Ubuntu Natty Narwhal, y me dio el siguiente error:

```bash
google-authenticator.o: In function `displayQRCode':
/home/karpoke/hg-read-only/google-authenticator/libpam/google-authenticator.c:154: undefined reference to `dlopen'
/home/karpoke/hg-read-only/google-authenticator/libpam/google-authenticator.c:166: undefined reference to `dlsym'
/home/karpoke/hg-read-only/google-authenticator/libpam/google-authenticator.c:168: undefined reference to `dlsym'
/home/karpoke/hg-read-only/google-authenticator/libpam/google-authenticator.c:253: undefined reference to `dlclose'
/home/karpoke/hg-read-only/google-authenticator/libpam/google-authenticator.c:156: undefined reference to `dlopen'
```

El problema parece ser que el `Makefile` [no encuentra la librería
`libdl`][no encuentra la librería libdl]—la busca en `/usr/lib/libdl.so`—.
La solución pasa por buscarla nosotros mismos y modificar dicho fichero:

```bash
$ find /usr/lib -name libdl.so
/usr/lib/i386-linux-gnu/libdl.so
$ sed -i 's|/usr/lib/libdl.so|/usr/lib/i386-linux-gnu/libdl.so|g' Makefile
$ make
```

Lo instalamos, por fin:

```bash
$ sudo make install
$ cp pam_google_authenticator.so /lib/security
$ cp google-authenticator /usr/local/bin
```

Configurar el servicio de SSH
-----------------------------

Ahora debemos añadir el módulo recién instalado al final del fichero
`/etc/pam.d/sshd` ^[1][]^:

```bash
# Google 2FA
auth required pam_google_authenticator.so
```

Ejecutamos el siguiente comando __con cada usuario__ con el que queremos
utilizar el 2FA, lo cual nos creará una clave secreta en el directorio
de usuario:

```bash
$ google-authenticator
https://www.google.com/chart?chs=200x200&chld=M|0&cht=qr&chl=otpauth://totp/user@server%3Fsecret%3DSAEP64T5VZAVWAFB
Your new secret key is: SAEP64T5VZAVWAFB
Your verification code is 376046
Your emergency scratch codes are:
  67868696
  26247332
  54815527
  54336661
  71083816

Do you want me to update your "~/.google_authenticator" file (y/n) y

Do you want to disallow multiple uses of the same authentication
token? This restricts you to one login about every 30s, but it increases
your chances to notice or even prevent man-in-the-middle attacks (y/n) y

By default, tokens are good for 30 seconds and in order to compensate for
possible time-skew between the client and the server, we allow an extra
token before and after the current time. If you experience problems with poor
time synchronization, you can increase the window from its default
size of 1:30min to about 4min. Do you want to do so (y/n) n

If the computer that you are logging into isn't hardened against brute-force
login attempts, you can enable rate-limiting for the authentication module.
By default, this limits attackers to no more than 3 login attempts every 30s.
Do you want to enable rate-limiting (y/n) y
```

Deberemos guardar esos códigos celosamente, ya que si perdemos el móvil,
esa será la única manera de poder iniciar sesión de forma remota.

Lo siguiente es abrir en un navegador la URL que nos aparece al
principio y nos aparecerá un QRCode. Utilizamos la aplicación Google
Authenticator para nuestro móvil y lo escaneamos. Si ya teníamos otro
generador, ahora tendremos los dos y los podremos distinguir por el
nombre.

También podemos [leer el código desde el terminal para ver lo que
contiene][]:

```bash
$ wget -O qrcode.png 'https://www.google.com/chart?chs=200x200&chld=M|0&cht=qr&chl=otpauth://totp/user@server%3Fsecret%3DSAEP64T5VZAVWAFB'
$ qrdecode qrcode.png
otpauth://totp/user@server?secret=SAEP64T5VZAVWAFB
```

Es importante que el servidor tenga instalado un servicio de NTP para
actualizar la hora de forma precisa. Si tenemos problemas con esto,
deberíamos permitir un tamaño de ventana más abierto, tal como sugería
`google-authenticator`.

También necesitaremos editar el fichero de configuración de `ssh`,
`/etc/ssh/sshd_config`, para que contenga:

```bash
ChallengeResponseAuthentication yes
UsePAM yes
```

Si usamos las directivas `AllowUsers` o `AllowGroups` debemos acordarnos
de incluir a cada usuario.

Reiniciamos el servicio de SSH pero <bold>no</bold> cerramos la conexión
que tenemos abierta, sino que intentaremos conectarnos iniciando otra
sesión nueva. El motivo es que si tuviéramos algún problema, nos
quedaríamos sin poder acceder a la máquina. Si tenemos las [conexiones
por SSH compartidas][], no bastará con abrir un nuevo terminal,
deberemos conectarnos desde otro usuario o en otra máquina.

```bash
$ ssh user@host
Password:
Verification code:
```

La contraseña es la misma que teníamos y el código de verificación es el
que nos aparezca en el móvil.

Listos. Configurar un sistema de verificación en dos pasos para SSH es
así de sencillo. Por un lado, gracias a Google y por otro, gracias a
tutoriales como el de [TechRepublic][habilitar 2FA en nuestro servidor].

Omitiendo 2FA
-------------

Podemos tener diferentes razones para no querer utilizar este tipo de
autenticación en algunos casos. Por ejemplo, permitir la conexión desde
la propia red o permitir que algunos usuarios no utilicen este sistema.

### Omitiendo 2FA para accesos desde la red interna

Si sólo queremos 2FA para accesos remotos, desde fuera de la red local,
y preferimos omitirlo en [conexiones desde la misma LAN][], deberemos
hacer lo siguiente. Creamos el fichero `/etc/security/access-local.conf`
y ponemos:

```bash
+ : ALL : 192.168.50.0/24
+ : ALL : LOCAL
- : ALL : ALL
```

Modificamos el fichero `/etc/pam.d/sshd` para añadir la siguiente línea
justo antes de la que ya habíamos añadido, quedando así:

```bash
auth [success=1 default=ignore] pam_access.so accessfile=/etc/security/access-local.conf
auth required                   pam_google_authenticator.so
```

Ahora ya podemos reiniciar el servicio `SSH`, y para las conexiones
locales o desde la red 192.168.50.0/24 bastará con proporcionar la
contraseña.

### Omitiendo 2FA para un usuario concreto

Para evitar que determinados usuarios usen este sistema de
autenticación, podemos incluir una línea como la siguiente, al principio
del fichero `/etc/security/access-local.conf`, quedando así:

```bash
+ : username : ALL
+ : ALL : 192.168.50.0/24
+ : ALL : LOCAL
- : ALL : ALL
```

Deberemos reiniciar el servicio SSH para que los cambios tengan efecto.

### Omitiendo 2FA para un grupo concreto

En lugar de ir añadiendo usuarios al fichero
`/etc/security/access-local.conf`, podemos incluir [una nueva regla][]
al fichero `/etc/pam.d/sshd`, justo antes de los cambios que habíamos
acabado de añadir en este fichero, quedando así:

```bash
auth sufficient                 pam_succeed_if.so user ingroup nonotp
auth [success=1 default=ignore] pam_access.so accessfile=/etc/security/access-local.conf
auth required                   pam_google_authenticator.so
```

Los usuarios que pertenezcan al grupo `nonotp` no utilizarán este tipo
de autenticación.

Deberemos reiniciar el servicio SSH para que los cambios tengan efecto.

#### `pam_succeed_if.so`

`pam_succeed_if.so` se emplea para provocar que la autenticación falle o
sea exitosa en función de algunas características del usuario que está
siendo autenticado. Se pueden realizar comprobaciones con los campos:
`user`, `uid`, `gid`, `shell`, `home` y `service`. También se puede
comprobar la pertenencia, o no, de un usuario a un grupo.

* * * * *

#### Actualizado el 7 de abril de 2012

La clave de un solo uso que se genera en un momento dado [depende
únicamente de la clave secreta inicial][] del usuario y del instante en
que se genera dicha clave de un sólo uso. Google Authenticator se basa
en el RFC 4226 (Time based One Time Password) para generar una semilla
inicial de 16 dígitos en base 32 (RFC 4648). En la página anterior se
enlaza a una clase en PHP creada por el autor que muestra como se puede
crear la clave para un momento dado y comprobar si una clave dada es
correcta permitiendo un pequeño desfase entre los relojes de referencia.

En este enlace se muestra una [implementación en Python][], cuyo código
se puede descargar de GitHub.

El proceso de obtención de una clave es el siguiente:

1.  convertir la cadena con la clave a binario
2.  convertir la cadena con el _time stamp_ asociado al intervalo a
    binario
3.  calcular el _hash_ HMAC del _time stamp_ (la parte entera tras
    divirlo entre el tiempo del intervalo, 30 segundos) usando la clave.
    Nos devolverá un _hash_ SHA1 de 20 bytes
4.  en el último byte del _hash_ devuelto se especifica el _offset_ a
    partir del cual se encuentra la contraseña OTP
5.  obtenemos los bytes donde se encuentra la contraseña y los
    convertimos a un entero módulo 1000000

En Python:

```python
def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(h[19]) & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000492246
    return h

def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time())//30)
print get_totp_token('SAEP64T5VZAVWAFB')
492246
```

Un ejemplo de uso del módulo:

```bash
$ git clone https://github.com/tadeck/onetimepass
$ ipython
In [1]: import onetimepass as otp
In [2]: my_secret = 'SAEP64T5VZAVWAFB'
In [3]: otp.get_totp(my_secret)
Out[3]: 453001
In [4]: otp.valid_totp(453001, my_secret)
Out[4]: True
```

* * * * *

#### Actualizado el 1 de marzo de 2015

Desde Ubuntu Precise Pangolin 12.04, el paquete
`libpam-google-authenticator` ya se encuentra en los repositorios.

* * * * *

<a name="2fa-gdm"></a>
[1] Incluso podríamos hacer lo mismo para `/etc/pam.d/gdm` y utilizar
2FA para iniciar sesión en Gnome.

  [impida el acceso por fuerza bruta]: {filename}/admin/detectando-intrusos-en-ubuntu-maverick-meerkat.md
    "Detectando intrusos en Ubuntu"
  [aplicación móvil de Google]: https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2
    "aplicación móvil de Google"
  [github]: https://github.com/google/google-authenticator/wiki
    "github"
  [FreeOTP]: https://fedorahosted.org/freeotp/
    "FreeOTP"
  [Android]: https://play.google.com/store/apps/details?id=org.fedorahosted.freeotp
    "Android"
  [HOTP]: http://www.ietf.org/rfc/rfc4226.txt
    "HOTP"
  [TOTP]: http://www.ietf.org/rfc/rfc6238.txt
    "TOTP"
  [google.com]: http://www.google.com/support/a/bin/answer.py?answer=1037451
    "google.com"
  [uso exclusivo de claves para conectarnos por SSH]: {filename}/admin/conectarse-por-ssh-solo-usando-la-clave.md
    "Conectarse a SSH usando claves"
  [habilitar 2FA en nuestro servidor]: http://m.techrepublic.com/blog/opensource/two-factor-ssh-authentication-via-google-secures-linux-logins/2607
    "habilitar 2FA en nuestro servidor"
  [Descargamos]: http://code.google.com/p/google-authenticator/source/checkout
    "Descargamos"
  [versión de mercurial un poco vieja]: http://code.google.com/p/google-authenticator/issues/detail?id=85
    "versión de mercurial un poco vieja"
  [no encuentra la librería libdl]: http://code.google.com/p/google-authenticator/issues/detail?id=71
    "no encuentra la librería libdl"
  [1]: #2fa-gdm
    "1"
  [leer el código desde el terminal para ver lo que contiene]: {filename}/admin/creando-y-leyendo-codigos-qr-desde-python.md
    "Creando y leyendo códigos QR desde Python"
  [conexiones por SSH compartidas]: {filename}/admin/compartiendo-una-conexion-por-ssh.md
    "Compartiendo una conexión por SSH"
  [conexiones desde la misma LAN]: http://code.google.com/p/google-authenticator/wiki/PamModuleInstructions
    "conexiones desde la misma LAN"
  [una nueva regla]: http://clearimagery.net/blog/2011/03/two-factor-auth-with-pam-google-authenticator.html
    "una nueva regla"
  [depende únicamente de la clave secreta inicial]: http://www.idontplaydarts.com/2011/07/google-totp-two-factor-authentication-for-php/
    "depende únicamente de la clave secreta inicial"
  [implementación en Python]: http://stackoverflow.com/questions/8529265/google-authenticator-implementation-in-python
    "implementación en Python"
