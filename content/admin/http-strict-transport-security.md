Title: HTTP Strict Transport Security
Date: 2011-09-11 17:37
Author: Nacho Cano
Tags: apache, cabeceras HTTP, hsts, http, https, man in the middle, mitm, mod_headers, robo de sesión, ssl
Slug: http-strict-transport-security
Related: usando-una-conexion-segura-en-el-panel-de-control-de-wordpress,configurar-apache-para-servir-conexiones-seguras,robando-la-identidad-del-vecino

[HTTP Strict Transport Security][] (HSTS) es un mecanismo de seguridad
web donde el servidor exige que las conexiones se realicen únicamente
mediante conexiones seguras. El servidor informa de esta política de
seguridad utilizando la cabecera `Strict-Transport-Security`, en donde
se especifica el periodo durante el cual las conexiones seguras son
obligatorias.

Si una web proporciona acceso seguro (HTTPS) pero accedemos de forma no
segura (HTTP) [podría suceder que nos redirija a la versión segura][],
sin embargo, ya se había iniciado una conversación sin cifrar. Este
comportamiento puede ser explotado por un ataque _Man-In-The-Middle_.

La política de seguridad HSTS pretende evitar este tipo de ataques,
impidiendo que se realice ninguna conexión que no sea segura. La
cabecera no se envía durante una transacción HTTP no cifrada dado que el
User-Agent no sabe si HTTPS está disponible y porque podría haber sido
inyectada por un atacante.


Configuración en Apache
-----------------------

En Apache, además de tener habilitado `mod_headers`, deberemos
introducir la siguiente línea allí [donde configuramos la conexión
SSL][]. Por ejemplo, tras el `DocumentRoot` del `VirtualHost` seguro por
defecto en el archivo `/etc/apache2/sites-enabled/default-ssl`:

```bash
Header add Strict-Transport-Security "max-age=15768000"
```

El atributo `max-age` especifica el tiempo durante el cual las
conexiones seguras serán obligatorias. También se puede añadir el
atributo `includeSubDomains` para incluir todos los subdominios:

```bash
Header add Strict-Transport-Security "max-age=15768000; includeSubDomains"
```

WordPress, por ejemplo, tiene una directiva para conseguir que la
[conexión al panel de control se haga a través de una conexión
segura][]. Pero es posible que en otros casos sigamos necesitando una
redirección hacia la versión segura de la página, que podemos conseguir
mediante `mod_rewrite`:

```bash
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} off
  RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}
</IfModule>
```

  [HTTP Strict Transport Security]: http://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security
    "HTTP Strict Transport Security"
  [podría suceder que nos redirija a la versión segura]: http://hacks.mozilla.org/2010/08/firefox-4-http-strict-transport-security-force-https/
    "podría suceder que nos redirija a la versión segura"
  [donde configuramos la conexión SSL]: http://mikkel.hoegh.org/blog/2010/sep/9/protecting-your-users-phishing-apache-rules-hsts
    "donde configuramos la conexión SSL"
  [conexión al panel de control se haga a través de una conexión segura]: {filename}/admin/usando-una-conexion-segura-en-el-panel-de-control-de-wordpress.md
    "Usando una conexión segura en el panel de control de WordPress"
