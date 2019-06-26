Title: Identificando los plugins de WordPress instalados
Date: 2011-06-20 20:47
Author: Nacho Cano
Tags: 404, apache, escáner de vulnerabilidades, fingerprint, http-wp-plugins, nmap, plugin, script, seguridad por oscuridad, wordpress, wpfinger
Slug: identificando-los-plugins-de-wordpress-instalados

Hay un _script_ para `nmap`, [http-wp-plugins][], que permite [detectar
los complementos instalados en WordPress][].

Dicho _script_ intenta acceder a los directorios de los complementos en
`wp-content/plugins/` con la ayuda de un [diccionario][]. Si la
respuesta no es un error 404 interpreta que el directorio, y por tanto
el complemento, existe. La lista de complementos para WordPress es extensa,
casi 13405 entradas, y podría llevar bastante tiempo analizarlas todas,
por lo que las entradas están ordenadas por popularidad y por defecto
sólo se escanean las 100 primeras.


Instalación y uso
-----------------

Después de bajarnos el [diccionario][], lo descomprimimos en el
directorio `/usr/share/nmap/nselib/data`, o en el directorio
`nselib/data` relativo a donde tengamos instalado `nmap`, y ya podemos
probar el complemento:

```bash
$ nmap -p80 --script=http-wp-plugins --script-arg http-wp-plugins.root="/blog/",http-wp-plugins.search=500 mydomain.com
PORT   STATE SERVICE
80/tcp open  http
| http-wp-plugins:
| search amongst the 500 most popular plugins
|   all-in-one-seo-pack
|   akismet
|   si-contact-form
|   wp-super-cache
|   google-sitemap-generator
|   yet-another-related-posts-plugin
|   google-analytics-for-wordpress
|   maintenance-mode
|   broken-link-checker
|   feedburner-plugin
|   exploit-scanner
|_  secure-wordpress
```

Mediante la opción `http-wp-plugins.root="/blog/"` le decimos al
complemento que la ruta relativa al WordPress es `/blog/`, es decir,
`mydomain.com/blog/`, y con `http-wp-plugins.search=500` que busque los
500 primeros complementos de la lista. Si quisiéramos que los buscase
todos, pondríamos `all`.

Cómo "protegernos"
------------------

Una medida para evitar que un atacante pueda recabar información de los
complementos que tenemos instalados es añadir al archivo de configuración
del sitio de Apache, `/usr/share/wordpress/wp-content`, las siguientes
directivas:

```apache

    Order Deny,Allow
    Deny from All
    Options FollowSymLinks
    AllowOverride None
```

Y reiniciamos el servicio.

Después de estos cambios, el resultado será que que, para el _script_,
todos los complementos están instalados, ya que el acceso a estos
directorios está prohibido (error 403).

```bash
$ nmap -p80 --script=http-wp-plugins --script-arg http-wp-plugins.root="/blog/",http-wp-plugins.search=10 mydomain.com
PORT   STATE SERVICE
80/tcp open  http
| http-wp-plugins:
| search amongst the 10 most popular plugins
|   gtranslate
|   all-in-one-seo-pack
|   contact-form-7
|   google-analyticator
|   akismet
|   wptouch
|   si-contact-form
|   wp-super-cache
|   add-to-any
|_  sexybookmarks
```

Éstos se corresponden justamente con las 10 primeras entradas del
diccionario:

```bash
$ head /usr/share/nmap/nselib/data/wp-plugins.lst
gtranslate
all-in-one-seo-pack
contact-form-7
google-analyticator
akismet
wptouch
si-contact-form
wp-super-cache
add-to-any
sexybookmarks
```

Sin embargo, esta medida no llega a ser una medida realmente efectiva ya
que:

-   algunos complementos dejarán de funcionar de forma correcta. Los que
    incluyan archivos estáticos tales como CSS o Javascript dentro de
    sus directorios no podrán cargarlos, por lo que no se verán como
    estaba pensado o dejarán de funcionar correctamente
-   no deja de ser una medida de seguridad por oscuridad, ya que ocultar
    lo que tenemos no nos hace más seguros, sino más confiados, y
    seguramente se pueden seguir identificando algunos de los complementos
    que tenemos instalados inspeccionando el código fuente de la página.

Lo mejor sería tener nuestro [WordPress actualizado][], utilizar
complementos de fuentes fiables y que se actualicen regularmente.

Usando `wpfinger`
-----------------

[wpfinger][] es una herramienta que analiza el repositorio de complementos
de WordPress y genera firmas basadas en las diferencias entre cada
versión de cada complemento. Mediante estas firmas puede detectar la
presencia de cualquier complemento del repositorio, y probablemente la
versión concreta, en una página web.

Para instalarlo desde el repositorio Git:

```bash
$ git clone https://code.google.com/p/wpfinger/
```

Para realizar un escaneo:

```bash
$ ./wpfinger.py http://localhost/wordpress/
Detected 404 as default response code.
Installed plugins:
google-analytics-for-wordpress: trunk
si-contact-form: 2.9.7.1
add-to-any: 0.9.9.9.4 - trunk
all-in-one-seo-pack: trunk
wp-super-cache: 0.9.9.4
yet-another-related-posts-plugin: 3.3.1
akismet: trunk
google-sitemap-generator: trunk
broken-link-checker: trunk
maintenance-mode: trunk
secure-wordpress: 2.0.1
feedburner-plugin: trunk
post-plugin-library: 2.5.0.5
exploit-scanner: 1.0.5 - trunk
wp-syntax: trunk
login-lockdown: 1.5 - trunk
wp-jquery-lightbox: 1.2.1
nktagcloud: 0.99.5 - trunk
wp-paginate: trunk
```

Usando `wpscan`
---------------

[WPScan][] es un escáner de vulnerabilidades que comprueba la seguridad
de una instalación de WordPress utilizando un enfoque de caja negra.
Puede listar usuarios, romper claves débiles, mostrar la versión de
WordPress instalada, mostrar los complementos instalados y las
vulnerabilidades que puedan tener, además de otra información.

Antes de descargar el código del repositorio SVN, necesitaremos instalar
las dependencias:

```bash
$ sudo aptitude install libcurl4-gnutls-dev libxml-simple-ruby
$ sudo gem install typhoeus
$ svn checkout http://wpscan.googlecode.com/svn/trunk/ wpscan-read-only
```

Si queremos realizar una comprobación no intrusiva que muestre la
versión de WordPress y el tema instalado:

```bash
$ ruby wpscan-read-only/wpscan.rb --url http://localhost/wordpress
____________________________________________________
 __          _______   _____
 \ \        / /  __ \ / ____|
  \ \  /\  / /| |__) | (___   ___  __ _ _ __
   \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
    \  /\  /  | |     ____) | (__| (_| | | | |
     \/  \/   |_|    |_____/ \___|\__,_|_| |_| v1.1

  WordPress Security Scanner by ethicalhack3r.co.uk
 Sponsored by the RandomStorm Open Source Initiative
_____________________________________________________

# Copyright (C) 2011 Ryan Dewhurst
# This program comes with ABSOLUTELY NO WARRANTY.
# This is free software, and you are welcome to redistribute it
# under certain conditions. See GNU GPLv3.

| URL: http://localhost/wordpress
| Started on Sun Sep 18 18:00:35 2011

[+] The WordPress theme in use is called minimalism
[+] WordPress version/s "3.2.1" identified from advanced fingerprinting.

[+] Finished at Sun Sep 18 18:00:40 2011
```

Si queremos que nos muestre los complementos instalados:

```bash
$ ruby wpscan-read-only/wpscan.rb --enumerate p --url http://localhost/wordpress
____________________________________________________
 __          _______   _____
 \ \        / /  __ \ / ____|
  \ \  /\  / /| |__) | (___   ___  __ _ _ __
   \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
    \  /\  /  | |     ____) | (__| (_| | | | |
     \/  \/   |_|    |_____/ \___|\__,_|_| |_| v1.1

  WordPress Security Scanner by ethicalhack3r.co.uk
 Sponsored by the RandomStorm Open Source Initiative
_____________________________________________________

# Copyright (C) 2011 Ryan Dewhurst
# This program comes with ABSOLUTELY NO WARRANTY.
# This is free software, and you are welcome to redistribute it
# under certain conditions. See GNU GPLv3.

| URL: http://localhost/wordpress
| Started on Sun Sep 18 18:09:31 2011

[+] The WordPress theme in use is called minimalism
[+] WordPress version/s "3.2.1" identified from advanced fingerprinting.

[+] Enumerating installed plugins...

Checking for 2162 total plugins... 1% complete.
```

  [http-wp-plugins]: http://seclists.org/nmap-dev/2011/q1/att-806/http-wp-plugins.nse
    "http-wp-plugins"
  [detectar los complementos instalados en WordPress]: http://blog.alexos.com.br/?p=2302
    "detectar los complementos instalados en WordPress"
  [diccionario]: http://seclists.org/nmap-dev/2011/q1/att-806/wp-plugins_lst_tar.gz
    "diccionario"
  [WordPress actualizado]: {filename}/admin/la-infame-actualizacion-de-wordpress-en-15-segundos.md
    "la infame actualización de wordpress en 15 segundos"
  [wpfinger]: http://code.google.com/p/wpfinger/
    "wpfinger"
  [WPScan]: http://code.google.com/p/wpscan/
    "WPScan"
