Title: Asignar la IP que queramos a un dominio de DynDNS
Date: 2010-12-30 19:12
Author: Nacho Cano
Tags: dyndns, inadyn, ip dinámica, nc, netcat, python, servidor http
Slug: asignar-la-ip-que-queramos-a-un-dominio-de-dyndns
Related: iniciar-sesion-en-dyndns-desde-el-terminal

Con el comando `inadyn` podemos actualizar la IP de nuestro dominio, o
[dominios][], en DynDNS, pero la IP no se pasa como argumento sino que
se hace una consulta a un servidor que devuelve la IP pública que
tenemos en ese momento. Por defecto, el servidor es
`checkip.dyndns.org:80`.

Podemos hacer que el dominio apunte a la IP que queramos utilizando el
argumento `--ip_server_name` para especificar un servidor controlado por
nosotros y que devuelva la IP que queramos.

Una manera sencilla de montar un servidor HTTP temporal es utilizar el
comando `nc`. Antes de ejecutarlo, crearemos un fichero `index.html` con
el siguiente contenido, modificando la IP por la que nosotros queramos:

```html
Current IP Check
Current IP Address: 209.85.146.106
```

Lanzamos el servidor:

```python
$ cat index.html | nc -l 8000
```

Y actualizamos nuestro dominio con la IP que pusimos en el archivo
`index.html`:

```bash
$ /usr/sbin/inadyn -u user -p pass --iterations 1 --dyndns_system custom@dyndns.org
 --ip_server_name localhost:8000 / -a anacreonte.homelinux.com
```

Ojo, no es recomendable ir escribiendo nuestras contraseñas en la línea
de comandos.

Bueno, después de hacer algunas pruebas más, he visto que no hace falta
crear un fichero HTML, basta con que nuestro servidor devuelva la IP que
queremos asignar:

```bash
$ echo 209.85.146.106 | nc -l 8000
```

Otra manera sería utilizar un Apache, en el cual el fichero no tiene
porqué estar en la raíz del dominio. En tal caso, la petición sería algo
como:

```bash
$ /usr/sbin/inadyn -u user -p pass --iterations 1 --dyndns_system custom@dyndns.org
 --ip_server_name smyrno.homelinux.com:8000 /path/ip.html -a anacreonte.homelinux.com
```

donde el fichero `ip.html` es el que contiene la IP y se encuentra en el
subdirectorio `/path/`.

Por último, también he probado con Python, ejecutando:

```python
$ python -m SimpleHTTPServer 8000
```

pero esto no acaba de funcionar. `inadyn` una vez conectado al servidor
realiza una petición que siempre recibe un error 404, dado que el
archivo solicitado no se encuentra.

Para mostrar este comportamiento, lazamos el servidor:

```bash
$ python -m SimpleHTTPServer 8000
```

y en otra consola intentamos realizar la actualización:

```bash
$ /usr/sbin/inadyn -u user -p pass --iterations 1 --dyndns_system custom@dyndns.org
 --ip_server_name localhost:8000 / -a anacreonte.homelinux.com  --verbose 5
```

```bash
INADYN: Started 'INADYN version 1.96.2' - dynamic DNS updater.
The request for IP server:
GET http://localhost:8000/ HTTP/1.0


DYNDNS: IP server response: HTTP/1.0 404 File not found
Server: SimpleHTTP/0.6 Python/2.6.6
Date: Thu, 30 Dec 2010 16:43:31 GMT
Content-Type: text/html
Connection: close


Error response


Error response
Error code 404.
Message: File not found.
Error code explanation: 404 = Nothing matches the given URI.


W:'RC_DYNDNS_INVALID_RSP_FROM_IP_SERVER' (0x42) updating the IPs. (it 0)
```

Este es el registro que muestra el servidor:

```bash
Serving HTTP on 0.0.0.0 port 8000 ...
localhost.localdomain - - [30/Dec/2010 17:43:31] code 404, message File not found
localhost.localdomain - - [30/Dec/2010 17:43:31] "GET http://localhost:8000/ HTTP/1.0" 404 -
```

Sin embargo, si abrimos un navegador y vamos a la direccion
`localhost:8000`, en el navegador nos aparece la IP y esto es lo que
muestra el servidor:

```bash
localhost.localdomain - - [30/Dec/2010 17:51:15] "GET / HTTP/1.1" 200 -
```

* * * * *

#### Actualizado el 10 de junio de 2013

Actualmente, es posible [actualizar el dominio con la IP que
queramos][], simplemente haciendo una petición como la siguiente:

```bash
$ USERNAME=username
$ PASSWORD=password
$ DOMAIN=example.homelinux.com
$ IP=1.2.3.4
$ curl https://$USERNAME:$PASSWORD@members.dyndns.org/nic/update?hostname=$DOMAIN&myip=$IP&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG
```

Debido a un cambio en la política de uso de las cuentas gratuitas, es
necesario [iniciar sesión][] mínimo una vez al mes para mantener los
dominios.

* * * * *

  [dominios]: {filename}/admin/dyndns-e-inadyn.md
    "dyndns e inadyn"
  [actualizar el dominio con la IP que queramos]: http://dyn.com/support/developers/api/perform-update/
    "actualizar el dominio con la IP que queramos"
  [iniciar sesión]: {filename}/admin/iniciar-sesion-en-dyndns-desde-el-terminal.md
    "iniciar sesión"
