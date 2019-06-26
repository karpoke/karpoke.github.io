Title: fwknop: Single Packet Authorization y port knocking
Date: 2011-09-18 00:49
Author: Nacho Cano
Tags: cifrado, cifrado asimétrico, clave pública, dsa, fwknop, fwknop-client, fwknop-server, generar entropía, gnupg, gnupg-agent, gpg, iptables, port knocking, random, Rijndael, rng-tools, rsa, scp, single packet authorization, spa, ssh, ubuntu, ufw
Slug: fwknop-single-packet-authorization-y-port-knocking
Related: mejorando-la-seguridad-de-apache-con-varnish,servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal,compartiendo-una-conexion-por-ssh,conectarse-por-ssh-utilizando-expect,conectarse-por-ssh-solo-usando-la-clave,sslh-compartiendo-el-puerto-443,ssh-over-http-proxy

`fwknop` implementa un esquema de autorización llamado *Single Packet
Authorization (SPA)*. Mediante SPA necesita un único paquete cifrado
para abrir puertos en el cortafuegos o llevar a cabo acciones en el
sistema. Se utiliza en conjunción con un cortafuegos que impide la
conexión a los puertos de los servicios que queremos proteger. De esta
forma, se logra una capa extra de seguridad, ya que los hace permanecer
invisibles, descartando silenciosamente los paquetes que llegan a dicho
puerto. Para poder tener acceso a los servicios protegidos, la parte
servidor de `fwknop` esnifa pasivamente los paquetes que llegan al
servidor usando `libpcap` y, en caso de recibir de parte del cliente de
`fwknop` un paquete cifrado válido que no ha sido recibido antes, se
permite el acceso a través del cortafuegos.

SPA tiene los beneficios del _port knocking_, es decir, la protección
de un servicio tras un filtro que descarta los paquetes por defecto,
pero con las siguientes ventajas:

-   puede utilizar cifrado asimétrico. _Port knocking_ utiliza
    únicamente las cabeceras de los paquetes, las cuales no suelen ser
    suficientes para guardar una clave de cifrado asimétrico, que suelen
    tener una longitud mayor que la de una clave de cifrado simétrico
-   los paquetes no se pueden reenviar. En _port knocking_ hay
    estrategias para reducir el riesgo de reutilizar un paquete, pero no
    son fácilmente escalables cuando se tienen muchos usuarios.
-   SPA no se puede romper con ataques triviales para averiguar la
    secuencia. Un atacante monitorizando la red podría averiguar la
    secuencia utilizada por _port knocking_, simplemente encontrando un
    paquete duplicado (que venga de una secuencia real) a un puerto
    anterior de la secuencia
-   SPA sólo envía un paquete, por lo que es más rápido y para alguien
    que estuviera monitorizando no aparece como un escaneo de puertos.
    _Port knocking_ necesita un retardo de tiempo entre paquetes
    sucesivos porque la entrega en orden no está garantizada

Instalación de `fwknop` en Ubuntu
---------------------------------

### En el servidor

Instalamos `fwknop-server` y `libpcap` en el servidor:

```bash
$ sudo aptitude install fwknop-server libpcap-dev
```

Nos hará unas preguntas:

```bash
Configure fwknop to protect the SSH port? Yes
Sniffing interface: eth0
Encryption key to use: __********__
```

### Utilizando claves GPG

Esta clave que nos pide es para usar el algoritmo simétrico Rijndael, o
AES. Si queremos utilizar cifrado asimétrico, podemos utilizar GnuPG.

Para crear las claves GnuPG, lo hacemos directamente como el usuario
`root`, no con `sudo`:

```bash
$ sudo su
# gpg --gen-key
- RSA y RSA    # RSA para firmar y cifrar
- 2048 bits    # longitud de la clave
- 1y           # la clave caducará en un año
```

Cuando terminen de crearse el par de claves, mostrará algo como lo
siguiente:

```bash
pub   2048R/4A064F2A 2011-09-17 [[caduca: 2012-09-16]]
      Huella de clave = 0CCD D9F5 1F77 E316 2B2B  0062 0C6E B0E6 4A06 4F2A
uid                  Server
sub   2048R/38F4A4A8 2011-09-17 [[caduca: 2012-09-16]]
```

Exportamos la clave a un fichero:

```bash
# gpg -a --export 4A064F2A > fwknop-server.asc
```

### Generando entropía

Si nos aparece el mensaje:

```bash
Es necesario generar muchos bytes aleatorios. Es una buena idea realizar
alguna otra tarea (trabajar en otra ventana/consola, mover el ratón, usar
la red y los discos) durante la generación de números primos. Esto da al
generador de números aleatorios mayor oportunidad de recoger suficiente
entropía.

No hay suficientes bytes aleatorios disponibles. Por favor, haga algún
otro trabajo para que el sistema pueda recolectar más entropía
(se necesitan 92 bytes más).
```

Poniendo a trabajar el servidor podría servir para crear entropía. Algo
como:

```bash
# ls -lRh /
# find / -name \*
```

El paquete `rng-tools` ayuda a [generar entropía][]. Una vez instalado
desde los respositorios, modificamos el fichero `/etc/default/rng-tools`
para que contenga:

```bash
HRNGDEVICE=/dev/urandom
```

Y reiniciamos el servicio:

```bash
$ sudo service rng-tools restart
```

### En el cliente

Si vamos a utilizar cifrado asimétrico, también deberemos generar el par
de claves en el cliente:

```bash
$ gpg --gen-key

pub   2048R/723B172D 2011-09-17 [[caduca: 2012-09-16]]
      Huella de clave = 7EB6 CFC6 6617 6354 A2A1  2BBF FD15 D606 723B 172D
uid                  Client
sub   2048R/3482560E 2011-09-17 [[caduca: 2012-09-16]]
```

Exportamos la clave:

```bash
$ gpg -a --export 723B172D > fwknop-client.asc
```

Copiamos la clave que hemos exportado en el servidor al cliente, para
firmar la clave del cliente con la del servidor.

```bash
$ scp remotehost:~/fwknop-server.asc .
```

Importamos la clave del servidor:

```bash
$ gpg --import fwknop-server.asc
gpg: clave 4A064F2A: clave pública "Server " importada
gpg: Cantidad total procesada: 1
gpg:               importadas: 1  (RSA: 1)
```

Y la firmamos con la nuestra. Nos pedirá la contraseña:

```bash
$ gpg --sign-key server@localhost
pub  2048R/4A064F2A  creado: 2011-09-17  [caduca: 2012-09-16]  uso: SC
                     confianza: desconocido   validez: desconocido
sub  2048R/38F4A4A8  creado: 2011-09-17  [caduca: 2012-09-16]  uso: E
desconocido (1). Server


pub  2048R/4A064F2A  creado: 2011-09-17  [caduca: 2012-09-16]  uso: SC
                     confianza: desconocido   validez: desconocido
 Huella de clave primaria: 0CCD D9F5 1F77 E316 2B2B  0062 0C6E B0E6 4A06 4F2A

     Server

Esta clave expirará el 2012-09-16.
¿Está realmente seguro de querer firmar esta clave
con su clave: "Client " (723B172D)?

¿Firmar de verdad? (s/N) s

Necesita una frase contraseña para desbloquear la clave secreta
del usuario: "Client "
clave RSA de 2048 bits, ID 723B172D, creada el 2011-09-17
```

Ahora lo haremos a la inversa. Copiamos nuestra clave (cliente) al
servidor, para poder firmarla después con la del servidor.

```bash
$ scp fwknop-client.asc remotehost:~
```

### `fwknop` con claves GPG

Estando en el servidor, y habiendo copiado la clave desde el cliente, la
importamos. Una vez más, nos pedirá la contraseña:

```bash
# gpg --import fwknop-client.asc
gpg: clave 723B172D: clave pública "Client " importada
gpg: Cantidad total procesada: 1
gpg:               importadas: 1  (RSA: 1)
```

Firmamos la clave del cliente con la del servidor:

```bash
# gpg --sign-key client@localhost
pub  2048R/723B172D  creado: 2011-09-17  [caduca: 2012-09-16]  uso: SC
                     confianza: desconocido   validez: desconocido
sub  2048R/3482560E  creado: 2011-09-17  [caduca: 2012-09-16]  uso: E
desconocido (1). Client


pub  2048R/723B172D  creado: 2011-09-17  [caduca: 2012-09-16]  uso: SC
                     confianza: desconocido   validez: desconocido
 Huella de clave primaria: 7EB6 CFC6 6617 6354 A2A1  2BBF FD15 D606 723B 172D

     Client

Esta clave expirará el 2012-09-16.
¿Está realmente seguro de querer firmar esta clave
con su clave: "Server " (4A064F2A)?

¿Firmar de verdad? (s/N) s

Necesita una frase contraseña para desbloquear la clave secreta
del usuario: "Server "
clave RSA de 2048 bits, ID 4A064F2A, creada el 2011-09-17
```

#### gpg: el agente gpg no esta disponible en esta sesión

El agente gpg es un programa que se encarga de gestionar un almacén
temporal de claves seguro. Sirve para no tener que introducir la frase
de paso para la clave privada cada vez que la queramos utilizar en la
misma sesión. Si no queremos que nos vuelva a salir ese aviso, o si no
lo vamos a usar, podemos desinstalarlo:

```bash
$ sudo aptitude purge gnupg-agent
```

Ahora sólo queda modificar la configuración de acceso en el fichero
`/etc/fwknop/access.conf`:

```bash
SOURCE: ANY;
OPEN_PORTS: tcp/22;
DATA_COLLECT_MODE: PCAP;
# si no queremos utilizar cifrado simétrico, comentamos la siguiente línea
#KEY: myPassword
GPG_HOME_DIR: /root/.gnupg;
GPG_DECRYPT_ID: 4A064F2A;
GPG_DECRYPT_PW: password para la clave;
GPG_REMOTE_ID: 723B172D;
FW_ACCESS_TIMEOUT: 30;
```

Y reiniciamos el servicio:

```bash
$ sudo service fwknop-service restart
```

### Otra vez al cliente

Instalamos `fwknop-client` en el cliente:

```bash
$ sudo aptitude install fwknop-client
```

Ya podemos probar a conectarnos. Primero, probamos la conexión por
cifrado simétrico:

```bash
$ fwknop -A 'tcp/22' -s -D 192.168.0.30

[+] Starting fwknop client (SPA mode)...
[+] Enter an encryption key. This key must match a key in the file
    /etc/fwknop/access.conf on the remote system.

Encryption Key:

[+] Building encrypted Single Packet Authorization (SPA) message...
[+] Packet fields:

        Random data:    8324045518684247
        Username:       karpoke
        Timestamp:      1316296897
        Version:        1.9.12
        Type:           1   (access mode)
        Access:         0.0.0.0,tcp/22
        SHA256 digest:  Lk3XUmw7PUd3OEOAb7mzb1kB+0CTTNzDyMrNdYK0YVo

[+] Sending 182 byte message to 192.168.0.30 over udp/62201...
```

En el servidor, en los ficheros de log, por ejemplo en
`/var/log/messages`, veremos algo como:

```bash
Sep 18 00:01:37 server fwknopd: received valid Rijndael encrypted packet from: 192.168.0.100, remote user: karpoke, client version: 1.9.12 (SOURCE line num: 26)
Sep 18 00:01:37 server fwknopd: add FWKNOP_INPUT 192.168.0.100 -> 0.0.0.0/0(tcp/22) ACCEPT rule 30 sec
Sep 18 00:02:08 server fwknop(knoptm): removed iptables FWKNOP_INPUT ACCEPT rule for 192.168.0.100 -> 0.0.0.0/0(tcp/22), 30 sec timeout exceeded
```

Si queremos utilizar la autenticación mediante la clave GPG:

```bash
$ fwknop -A 'tcp/22' -s -D 192.168.0.30 --gpg-recip 4A064F2A --gpg-sign 723B172D
```

Para conectarnos desde fuera de la red, debemos utilizar el argumento `-w`.
Con este flag, el comando realiza una petición a `whatismyip.com` y
utiliza esa IP. De lo contrario, estaríamos enviado nuestra IP interna y
sería esa IP la que se utilizaría para crear la regla en el cortafuegos
del servidor:

```bash
$ fwknop -A 'tcp/22' -s -w -D 192.168.0.30 --gpg-recip 4A064F2A --gpg-sign 723B172D
```

O podemos enviar la IP mediante el argumento `-a`:

```bash
$ fwknop -A 'tcp/22' -s -a 1.2.3.4 -D 192.168.0.30 --gpg-recip 4A064F2A --gpg-sign 723B172D
```

El cortafuegos
--------------

Después de 30 segundos se elimina la regla que permite la conexión con
el puerto. Si sucede que la conexión se corta cuando `fwknop` elimina la
regla, podemos añadir una nueva regla que mantenga las conexiones que ya
estuvieran establecidas:

```bash
$ sudo iptables -A INPUT -p tcp -i eth0 -m state --state ESTABLISHED, RELATED -j ACCEPT
```

Más información
---------------

- `fwknop`
- [Single Packet Authorization][]
- [Single Packet Authorization in Ubuntu][]
- [GPG Howto][]
- [fwknopping your way to success with single packet authorisation][]
- [SPA, Single Packet Authorization][]
- [_Port knocking_, ofuscación o capa de seguridad?][]

  [generar entropía]: http://dajul.com/2010/12/18/generar-mas-entropia/
    "generar entropía"
  [Single Packet Authorization]: http://help.ubuntu.com/community/SinglePacketAuthorization
    "Single Packet Authorization"
  [Single Packet Authorization in Ubuntu]: http://savvyadmin.com/fwknop-single-packet-authorization-in-ubuntu/
    "Single Packet Authorization in Ubuntu"
  [GPG Howto]: http://www.cipherdyne.org/fwknop/docs/gpghowto.html
    "GPG Howto"
  [fwknopping your way to success with single packet authorisation]: http://www.thelinuxsociety.org.uk/content/fwknopping-your-way-to-success-with-single-packet-authorisation
    "fwknopping your way to success with single packet authorisation"
  [SPA, Single Packet Authorization]: http://rafasec.blogspot.com/2008/03/spa-single-packet-authorization.html
    "SPA, Single Packet Authorization"
  [_Port knocking_, ofuscación o capa de seguridad?]: http://www.hispasec.com/unaaldia/3382
    "_Port knocking_, ofuscación o capa de seguridad?"
