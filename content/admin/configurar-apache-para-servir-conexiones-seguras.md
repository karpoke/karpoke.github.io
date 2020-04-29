Title: Configurar Apache para servir conexiones seguras
Date: 2011-06-14 14:13
Author: Nacho Cano
Tags: apache, autoridad certificadora, beast, ca, certificado, clave pública, des3, https, openssl, renovación del certificado, rsa, ssl
Slug: configurar-apache-para-servir-conexiones-seguras

Si tenemos Apache, y queremos configurarlo para que se pueda navegar de
forma segura por nuestro sitio utilizando el protocolo HTTPS,
necesitamos:

-   crear las claves que se utilizarán para cifrar la conexión,
-   configurar `mod_ssl`, el módulo de Apache para usar conexiones
    seguras,
-   y permitir la conexión por el puerto 443.


Crear las claves de cifrado
---------------------------

Vamos a generar un par de claves RSA triple DES de 2048 bits en el
directorio `/etc/ssl`:

    $ cd /etc/ssl
    $ sudo openssl genrsa -des3 -out server.key 2048

Nos pedirá una contraseña y al terminar nos habrá creado la clave
`server.key` que será la que utilizará Apache. Le cambiamos los
permisos:

    $ sudo chmod 700 server.key

y guardamos una copia en un lugar seguro. Si pensamos utilizar más de un
`VirtualHost` podría ser interesante utilizar el dominio para el nombre
de la clave en lugar de `server.key`.

Cada vez que se inicie Apache nos pedirá la contraseña que acabamos de
dar. Si [no queremos que nos vuelva a pedir la contraseña][], ejecutamos
lo siguiente, y utilizamos la nueva clave obtenida:

    $ sudo openssl rsa -in server.key -out new.server.key

Nuestra clave necesita estar avalada por _alguien_, por lo que creamos
una petición de firmado de nuestra clave. Que no se nos pase poner la
dirección de nuestra web en `Common Name`.

    $ sudo openssl req -new -key server.key -out server.csr
    Country Name (2 letter code) [AU]:ES
    State or Province Name (full name) [Some-State]:IB
    Locality Name (eg, city) []:Palma de Mallorca
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:Terminus
    Common Name (eg, YOUR name) []:terminus.ignaciocano.com
    Email Address []:karpoke@spamme.com

* * * * *

#### Actualizado el 22 de mayo de 2015

Podemos usar la opción `-subj` para pasarle esta información
directamente al comando `openssl`:

    $ sudo openssl req -new -key server.key -out server.csr -subj '/C=ES/ST=IB/L=Palma de Mallorca/O=Terminus/CN=terminus.ignaciocano.com/emailAddress=karpoke@spamme.com'

También podemos consultar esta información del fichero de petición con
la opción `-subject`:

    $ openssl req -in server.csr -noout -subject
    subject=/C=ES/ST=IB/L=Palma de Mallorca/O=Terminus/CN=terminus.ignaciocano.com/emailAddress=karpoke@spamme.com

* * * * *

Si queremos crear un certificado _wildcard_, válido para todos los
subdominios de un dominio, en `Common Name` bastará que pongamos algo
como por ejemplo `*.ignaciocano.com`.

Después de ejecutar el comando, se habrá creado el fichero con la
petición de firmado de nuestra clave, `server.csr`.

Ahora deberíamos entregar esta petición a una entidad certificadora para
que nuestro certificado esté avalado por una CA como Verisign o Thawte,
y así evitar que un usuario que acceda a nuestra web le salga el aviso
de que el certificado del sitio no puede ser validado. Pero si estamos
haciendo pruebas, tenemos dos opciones para nuestra petición, o
autofirmarla, o crear una autoridad certificadora (CA) y firmarla.

### Autofirmar la petición

Crearemos un certificado autofirmado, `server.crt`, con una validez de
un año:

    $ sudo openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
    Country Name (2 letter code) [AU]:ES
    State or Province Name (full name) [Some-State]:IB
    Locality Name (eg, city) []:Palma de Mallorca
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:Terminus
    Common Name (eg, YOUR name) []:terminus.ignaciocano.com
    Email Address []:karpoke@spamme.com

### Crear una autoridad certificadora y firmar el certificado

En lugar de autofirmar el certificado, podemos crear una autoridad
certificadora utilizando un pequeño _script_ incluido con `openssl`.

    $ sudo /usr/lib/ssl/misc/CA.sh -newca
    Country Name (2 letter code) [AU]:ES
    State or Province Name (full name) [Some-State]:IB
    Locality Name (eg, city) []:Palma de Mallorca
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:Terminus CA
    Organizational Unit Name (eg, section) []:
    Common Name (eg, YOUR name) []:terminus.ignaciocano.com
    Email Address []:karpoke@spamme.com

Nos pedirá una contraseña para el certificado de nuestra CA. Una vez que
termine, se habrá creado el directorio `/etc/ssl/demoCA`, que contiene
el certificado de nuestra CA.

Algunos programas tienen problemas con los certificados que no son DER,
por lo que convertiremos el nuestro:

    $ sudo openssl x509 -in demoCA/cacert.pem -out demoCA/cacert.der -outform DER

Renombramos el fichero del certificado, ya que así lo exige el script
que utilizaremos para firmar:

    $ sudo mv server.csr newreq.pem

Y firmamos el certificado. Nos pedirá la contraseña que le dimos al
certificado de la CA y nos pedirá confirmación para firmar la petición:

    $ sudo /usr/lib/ssl/misc/CA.sh -signreq

Volvemos a renombrar el certificado firmado:

    $ sudo mv newcert.pem server.crt

Configurar Apache para que use el certificado
---------------------------------------------

Movemos el certificado y la clave del servidor a los siguientes
directorios:

    $ sudo mv server.crt /etc/ssl/certs/
    $ sudo mv server.key /etc/ssl/private/

Activamos el módulo `mod_ssl` de Apache:

    $ sudo a2enmod ssl

Editamos la configuración del sitio por defecto para `SSL`, en el
fichero `/etc/apache2/sites-available/default-ssl` para que incluya:

    SSLEngine on
    SSLOptions +FakeBasicAuth +ExportCertData +StrictRequire
    SSLCertificateFile /etc/ssl/certs/server.crt
    SSLCertificateKeyFile /etc/ssl/private/server.key

El significado de las `SSLOptions` es el siguiente:

-   `FakeBasicAuth`, permite utilizar los métodos estándar Auth/DBMAuth
    para controlar el acceso,
-   `ExportCertData`, exporta las variables de entorno `SSL_CLIENT_CERT`
    y `SSL_SERVER_CERT`,
-   `StrictRequire`, deniega el acceso cuando se utilice `SSLRequireSSL`
    o `SSLRequire`

Activamos la configuración para que el sitio use `SSL`:

    $ sudo a2ensite default-ssl

Escuchando en el puerto 443
---------------------------

Debemos asegurarnos de que Apache está configurado para escuchar en el
puerto 443, el puerto bien definido para HTTPS, por lo que en el fichero
`/etc/apache2/ports.conf`, debería haber algo como:


        # If you add NameVirtualHost *:443 here, you will also have to change
        # the VirtualHost statement in /etc/apache2/sites-available/default-ssl
        # to
        # Server Name Indication for SSL named virtual hosts is currently not
        # supported by MSIE on Windows XP.
        Listen 443

Sólo queda reiniciar el servicio:

    $ sudo apache2ctl graceful

Y asegurarnos de que la NAT del _router_ está configurada correctamente,
si es que la usamos, o de que [el cortafuegos deja pasar las
peticiones][] por el puerto 443.

* * * * *

#### Actualización el día 24 de marzo de 2013

Cuando se haya pasado un año, deberemos renovar el certificado.

Primero, generamos, de nuevo, una petición de certificación de un año,
tal como hicimos al crear el certificado. El nombre del fichero debe ser
`newreq.pem`:

    $ sudo openssl req -new -key /etc/ssl/private/server.key -out /etc/ssl/newreq.pem

Firmamos el certificado:

    $ sudo /usr/lib/ssl/misc/CA.sh -signreq

Renombramos el certificado firmado y lo movemos al directorio correspondiente:

    $ sudo mv /etc/ssl/{newcert.pem,certs/server.crt}

Y ya sólo queda reiniciar Apache.

    $ sudo apache2ctl graceful

Podemos [comprobar las fechas de validez del certificado][] ejecutando:

    $ sudo openssl x509 -noout -dates -in /etc/ssl/certs/server.crt
    notBefore=Mar 24 11:52:07 2013 GMT
    notAfter=Mar 24 11:52:07 2014 GMT

O podemos obtenerlo directamente del servidor web:

    $ openssl s_client -showcerts -connect terminus.ignaciocano.com:443

* * * * *

Bonus
-----

Para comprobar [la calidad de una conexión segura][], podemos usar
nuevamente el comando `openssl`.

Siguiendo los criterios del artículo enlazado, comprobamos que no dé
soporte a SSL v2, ya que se puede considerar obsoleto:

    $ openssl s_client -ssl2 -connect localhost:443
    CONNECTED(00000003)
    19609:error:1407F0E5:SSL routines:SSL2_WRITE:ssl handshake failure:s2_pkt.c:428

Vemos que no cumplimos con la validación extendida en el certificado,
pero es que hemos usado nuestra propia autoridad certificadora.

Comprobamos que la longitud de la clave es la mínima aceptable:

    $ openssl s_client -connect localhost:443
    Server public key is 2048 bit

Por último, comprobamos que no admita algoritmos débiles, cuya longitud
de clave sea de 56 ó 64 bits:

    $ openssl s_client  -cipher LOW:EXP -connect localhost:443
    CONNECTED(00000003)
    1433:error:14077410:SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake failure:s23_clnt.c:596:

* * * * *

#### Actualización el día 24 de marzo de 2013

También podemos utilizar un servicio externo, como [SSL Server Test, de
Qualys SSL Labs][].

Si nos aparece que nuestro certificado es vulnerable al ataque BEAST,
podemos mitigarlo utilizando las siguientes directivas en la
configuración de Apache:

    SSLHonorCipherOrder On
    SSLCipherSuite ECDHE-RSA-AES128-SHA256:AES128-GCM-SHA256:RC4:HIGH:!MD5:!aNULL:!EDH

Más información:

» ivanr [Mitigating the BEAST attack on TLS][]
» ivanr [RC4 in TLS is Broken: Now What?][]

* * * * *

#### Actualizado el día 25 de enero de 2015

Dado que SHA1 va quedando obsoleto, es conveniente ir actualizando el
certificado. Creamos la petición de firmado del certificado:

    $ sudo openssl req -new -sha256 -key /etc/ssl/private/server.key -out /etc/ssl/newreq.pem

Confirmamos la información de la petición:

    $ sudo openssl req -in /etc/ssl/newreq.pem -text -noout

Firmamos la petición:

    $ sudo /usr/lib/ssl/misc/CA.sh -signreq

Movemos el certificado al directorio correspondiente:

    $ sudo mv /etc/ssl/{newcert.pem,certs/server.crt}

Reiniciamos `apache`:

    $ sudo apache2ctl restart

* * * * *

Utilidades
----------

Algunas utilidades para analizar la configuración SSL del servidor:

» [TLSSLed][]
» [SSLyze][]

* * * * *

  [no queremos que nos vuelva a pedir la contraseña]: http://www.madboa.com/geek/openssl/#key-removepass
    "no queremos que nos vuelva a pedir la contraseña"
  [el cortafuegos deja pasar las peticiones]: {filename}/admin/detectando-intrusos-en-ubuntu-maverick-meerkat.md
    "detectando intrusos en ubuntu maverick meerkat"
  [comprobar las fechas de validez del certificado]: http://systemadmin.es/2013/03/ver-las-fechas-de-validez-de-un-certificado
    "comprobar las fechas de validez del certificado"
  [la calidad de una conexión segura]: http://www.securitybydefault.com/2010/10/bancos-y-ssl-quien-aprueba.html
    "bancos y ssl quien aprueba"
  [SSL Server Test, de Qualys SSL Labs]: https://www.ssllabs.com/ssltest/analyze.html
    "SSL Server Test, de Qualys SSL Labs"
  [Mitigating the BEAST attack on TLS]: https://community.qualys.com/blogs/securitylabs/2011/10/17/mitigating-the-beast-attack-on-tls
    "Mitigating the BEAST attack on TLS"
  [RC4 in TLS is Broken: Now What?]: https://community.qualys.com/blogs/securitylabs/2013/03/19/rc4-in-tls-is-broken-now-what
    "RC4 in TLS is Broken: Now What?"
  [TLSSLed]: {filename}/admin/tlssled-v1-2.md
    "TLSSLed"
  [SSLyze]: {filename}/admin/sslyze.md
    "SSLyze"
