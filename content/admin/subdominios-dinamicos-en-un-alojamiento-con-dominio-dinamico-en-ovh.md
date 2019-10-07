Title: Subdominios dinámicos en un alojamiento con dominio dinámico en OVH
Date: 2012-12-15 01:05
Author: Nacho Cano
Tags: apache, apache2, certificado, cname, dns, dominio dinámico, dyndns, dynhost, https, mod_rewrite, nginx, no-ip, ovh, ssl, tls, vhost_alias, wildcard
Slug: subdominios-dinamicos-en-un-alojamiento-con-dominio-dinamico-en-ovh
Related: forzar-el-uso-de-sslhttps-de-un-directorio-en-apache2-mediante-htaccess-y-mod_rewrite,obteniendo-la-ip-publica-la-ip-privada-y-la-direccion-mac-en-bash,asignar-la-ip-que-queramos-a-un-dominio-de-dyndns

Lo que se pretende es conseguir una manera rápida y sencilla de poner
sitios web _online_. Una vez configurado el servidor web y el servidor
DNS, lo único que tendremos que hacer para tener accesible un nuevo
sitio web será colocarlo en un directorio concreto del servidor y
podremos acceder a él a través del subdominio con el nombre del
directorio. Por ejemplo, si creamos la web `web1`, automáticamente será
accesible desde `web1.example.com`.

En mi caso concreto, dado que el dominio que apuntará al servidor será
un dominio dinámico (`sub.ignaciocano.com`), los sitios web serán
accesibles a través de un subdominio de éste. Por ejemplo,
`web1.sub.ignaciocano.com`.


Configurar el servidor DNS
--------------------------

Se puede utilizar cualquier servidor DNS que permita comodines
(_wildcards_) para los subdominios de un dominio. Podemos utilizar el
servidor DNS de nuestro dominio principal, o un servidor DNS propio. No
sé si debe quedar algún servicio gratuito de dominios dinámicos, ya que
servicios como DynDNS o No-IP creo recordar que sólo permiten los
comodines en su versión de pago. En mi caso, he configurado el servidor
DNS de OVH.

En tres sencillos pasos lo tendremos todo listo.

Primero, creamos un nuevo dominio tipo DynHOST. Para ello, vamos a
Inicio > Hosting > Dominios & DNS > Zona DNS > campo DynHOST:

-   Subdominio: sub
-   IP de destino: Ponemos la IP del servidor
-   Dejamos marcada la casilla para crear un identificador DynHOST

Tras validar el primer paso, vamos a crear el identificador DynHOST:

-   Identificador: ignaciocano-identificadordeldominio
-   Subdominio: sub.ignaciocano.com
-   Contraseña: __***************__

Validamos y ya sólo quedará un último paso. Para que el este DynHOST
permita subdominios, deberemos crear un registro CNAME. Vamos a
Inicio > Hosting > Dominios & DNS > Zona DNS > campo CNAME:

-   Subdominio: *.sub.ignaciocano.com
-   Destino: sub.ignaciocano.com

Validamos y listo.

Configurar el servidor web
--------------------------

Todos los proyectos estarán ubicados a partir de un directorio común:
`/home/projects/subdomains`. Lo que tenemos que hacer es que el servidor
utilice el prefijo del dominio para utilizar la raíz del sitio correcta.

### Nginx

Configurar Nginx para que cualquier subdominio apunte a un directorio
concreto es sencillo. Creamos un fichero de configuración para el
dominio `/etc/nginx/sites-available/sub.ignaciocano.com`:

```bash
server {
    listen 80;
    server_name
        sub.ignaciocano.com
        ~^([^.]+)\.sub\.ignaciocano\.com
        ;
    access_log /var/log/nginx/access.sub.ignaciocano.com.log;
    if ($host ~* ^([^.]+)\.sub\.ignaciocano\.com$) {
        set $subdomain $1;
    }
    root /home/projects/subdomains/$subdomain/;
}
```

Sólo resta activar el sitio y reiniciar el servidor.

### Apache

Hacer lo propio en Apache es también sencillo. Podemos utilizar
`mod_rewrite`:

```bash
ServerName sub.ignaciocano.com
ServerAlias *.sub.ignaciocano.com

RewriteEngine On
RewriteCond %{HTTP_HOST} ^([^\.]+)\.sub\.ignaciocano\.com
RewriteCond /home/projects/subdomains/%1 -d
RewriteRule ^(.*) /%1/$1 [L]
```

O bien [`vhost_alias`][vhost_alias], el cual lo simplifica aún más:

```bash
ServerName sub.ignaciocano.com
ServerAlias *.sub.ignaciocano.com

VirtualDocumentRoot /home/projects/subdomains/%1
```

* * * * *

#### Actualizado el 14 de febrero de 2015

Si queremos que [las conexiones a estos subdominios sean seguras][], una
opción es crear un certificado con _wildcard_ pero en lugar de hacerlo
para el dominio principal, lo debemos hacer para el primer subdominio.
En este caso, al crear la petición de firmado, en el campo `Common Name`
deberemos poner `*.sub.ignaciocano.com`.

Hay que tener en cuenta que un certificado con _wildcard_ para el
dominio de primer nivel (_\*.ignaciocano.com_), [no se puede utilizar
para estos subdominios de un subdominio][], o de lo contrario el
navegador nos avisará de que el dominio no coincide con el del
certificado:

> Matching is performed using the matching rules specified by
>  [RFC2459]. If more than one identity of a given type is present in
>  the certificate (e.g., more than one dNSName name, a match in any
> one
>  of the set is considered acceptable.) Names may contain the wildcard
>  character \* which is considered to match any single domain name
>  component or component fragment. E.g., \*.a.com matches foo.a.com
> but
>  not bar.foo.a.com. f\*.com matches foo.com but not bar.com.

Por último, no estaría demás [forzar el uso de HTTPS][] para estos
subdominios:

```bash
ServerName sub.ignaciocano.com
ServerAlias *.sub.ignaciocano.com

RewriteEngine on
ReWriteCond %{SERVER_PORT} !^443$
RewriteRule ^/(.*) https://%{HTTP_HOST}/$1 [NC,R,L]
```

* * * * *

Referencias
-----------

» [Redirect of wildcard subdomain to subfolder][]
» [Wildcard subdomain directory names][]
» [HTTP over TLS][no se puede utilizar para estos subdominios de un
subdominio]

  [vhost_alias]: http://httpd.apache.org/docs/2.2/mod/mod_vhost_alias.html
    "`vhost_alias`"
  [las conexiones a estos subdominios sean seguras]: {filename}/admin/configurar-apache-para-servir-conexiones-seguras.md
    "Configurar Apache para servir conexiones seguras"
  [no se puede utilizar para estos subdominios de un subdominio]: http://tools.ietf.org/html/rfc2818#section-3.1
    "no se puede utilizar para estos subdominios de un subdominio"
  [forzar el uso de HTTPS]: {filename}/admin/forzar-el-uso-de-sslhttps-de-un-directorio-en-apache2-mediante-htaccess-y-mod_rewrite.md
    "Forzar el uso de SSL/HTTPS de un directorio en Apache2 mediante .htaccess y mod_rewrite"
  [Redirect of wildcard subdomain to subfolder]: http://forum.nginx.org/read.php?9,221859
    "Redirect of wildcard subdomain to subfolder"
  [Wildcard subdomain directory names]: http://serverfault.com/questions/182929/wildcard-subdomain-directory-names/182933#182933
    "Wildcard subdomain directory names"
