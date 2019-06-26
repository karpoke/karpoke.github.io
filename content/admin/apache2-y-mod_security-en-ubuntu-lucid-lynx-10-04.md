Title: Apache2 y mod_security en Ubuntu Lucid Lynx 10.04
Date: 2012-04-12 22:34
Author: Nacho Cano
Tags: 10.04, 12.04, 2.2.5, apache2, core rules set, crs, mod_security, OWASP, reglas, rules-updater.pl, ubuntu lucid lynx
Slug: apache2-y-mod_security-en-ubuntu-lucid-lynx-10-04
Related: cabeceras-http-personalizadas-en-apache2,cabeceras-http-personalizadas-en-apache2,ocultando-cabeceras,configurar-apache-para-servir-conexiones-seguras,mejorando-la-seguridad-de-apache-con-varnish,detectando-intrusos-en-ubuntu-maverick-meerkat

`mod_security` es un módulo de Apache que actua como cortafuegos,
protegiendo contra diversos tipos de ataque, y permitiendo monitorizar
el tráfico HTTP en tiempo real.

Por sí solo, el módulo no provee la protección, sino que deben añadirse
reglas. Afortunadamente, existen conjuntos de reglas predefinidos, como
el OWASP ModSecurity Core Rule Set Project, que nos facilitan la tarea.
Al contrario que los sistemas de detección de intrusos, basados en
firmas de vulnerabilidades conocidas, este conjunto de reglas protege
contra vulnerabilidades desconocidas que pueda haber en las aplicaciones
web.


Instalación de `mod_security`
-----------------------------

Podemos descargarnos el código desde su web, desde su repositorio de
versiones o desde el repositorio de paquetes de la distribución. Para
descargarlo desde el repositorio de Ubuntu:

```bash
$ sudo aptitude install libxml2 libxml2-dev libxml2-utils libaprutil1 libaprutil1-dev
$ sudo aptitude install libapache-mod-security
```

La versión que se instala es la 2.5.11-1. Aunque la última versión
estable en su web es la 2.6.2, esta vez utilizaremos la del repositorio
de Ubuntu.

Para activar el módulo:

```bash
$ sudo a2enmod mod-security
```

Y reiniciamos Apache:

```bash
$ sudo apache2ctl restart
```

### Configuración inicial

Podemos crear un archivo donde configuremos algunas directivas en
`/etc/apache2/conf.d/modsecurity.conf`. Por ejemplo, donde se encuentra
el fichero de _log_:

```bash
SecAuditLog /var/log/apache2/mod-security.log
```

Reiniciamos Apache para que los cambios tengan efecto:

```bash
$ sudo apache2ctl restart
```

Reglas OWASP
------------

Descargamos la última versión de las reglas (2.2.4) y lo descomprimimos
en el directorio `/etc/apache2`. Para evitar problemas, las
descargaremos en el directorio `/etc/apache2`:

```bash
$ cd /etc/apache2
$ sudo wget http://downloads.sourceforge.net/project/mod-security/modsecurity-crs/0-CURRENT/modsecurity-crs_2.2.4.tar.gz
$ sudo tar xvzf modsecurity-crs_2.2.4.tar.gz
$ sudo chown -R root:root modsecurity-crs_2.2.4
$ sudo mv modsecurity-crs_2.2.4 modsecurity-crs
```

Hay cinco directorios de reglas con diferentes tipos de regla:

-   `activated_rules`
-   `base_rules`
-   `experimental_rules`
-   `optional_rules`
-   `slr_rules`

### Configuración básica

Empezaremos con la configuración básica que viene de ejemplo. Copiamos
el archivo de configuración:

```bash
$ cd /etc/apache2/modsecurity-crs
$ sudo cp modsecurity_crs_10_config.conf.example modsecurity_crs_10_config.conf
```

Para que se tengan en cuenta las reglas, añadiremos al final del fichero
`/etc/apache2/apache2.conf`:

```bash

    Include modsecurity-crs/modsecurity_crs_10_config.conf
    Include modsecurity-crs/base_rules/*.conf
```

Deberemos reiniciar Apache.

```bash
$ sudo apache2ctl restart
```

#### Error creating rule: Unknown variable: REQBODY_ERROR

Si al reiniciar el Apache nos aparece este error, se debe a que esta
versión de las reglas es para `mod_security` versión 2.6 o superior. Sin
embargo, basta [renombrar esta variable por su valor anterior][] en el
fichero
`modsecurity-crs/base_rules/modsecurity_crs_20_protocol_violations.conf`,
para que se solucione el error:

```bash
$ cd /etc/apache2/modsecurity-crs/base_rules
$ sudo sed -i 's/^SecRule REQBODY_ERROR/SecRule REQBODY_PROCESSOR_ERROR/' modsecurity_crs_20_protocol_violations.conf
```

### Más reglas

Podemos crear una configuración personalizada, utilizando el directorio
`activated_rules` para incluir enlaces simbólicos a las reglas que
queremos activar. En el fichero `README` hay una explicación detallada
de cada regla.

Primero, modificaremos el archivo `/etc/apache2/apache2.conf` para que
contenga:

```bash

    Include modsecurity-crs/modsecurity_crs_10_config.conf
    Include modsecurity-crs/activated_rules/*.conf
```

Por ejemplo, para incluir las reglas básicas:

```bash
$ cd /etc/apache2/modsecurity-crs/activated-rules
$ for f in $(ls /etc/apache2/modsecurity-crs/base_rules); do
     sudo ln -s ../base_rules/$f $f
  done
```

Para incluir las reglas de _spam_:

```bash
$ cd /etc/apache2/modsecurity-crs/activated_rules
$ for f in $(ls /etc/apache2/modsecurity-crs/optional_rules | grep comment_spam); do
     sudo ln -s ../optional_rules/$f $f
  done
```

Para incluir todas las reglas opcionales:

```bash
$ cd /etc/apache2/modsecurity-crs/activated_rules
$ for f in $(ls /etc/apache2/modsecurity-crs/optional_rules); do
     sudo ln -s ../optional_rules/$f $f
  done
```

Reiniciamos Apache:

```bash
$ sudo apache2ctl restart
```

### Actualización de las reglas

Si ya tenemos las reglas instaladas y queremos comprobar si hay
actualizaciones, en el directorio `modsecurity-crs/util` hay un _script_
que facilita el proceso. Para comprobar si hay reglas nuevas:

```bash
$ ./rules-updater.pl -rhttps://www.modsecurity.org/autoupdate/repository/ -l
Could not load GnuPG module - cannot verify ruleset signatures

Repository: https://www.modsecurity.org/autoupdate/repository

modsecurity-crs {
          2.0.0: modsecurity-crs_2.0.0.zip
          2.0.1: modsecurity-crs_2.0.1.zip
          2.0.2: modsecurity-crs_2.0.2.zip
          2.0.3: modsecurity-crs_2.0.3.zip
          2.0.4: modsecurity-crs_2.0.4.zip
          2.0.5: modsecurity-crs_2.0.5.zip
          2.0.6: modsecurity-crs_2.0.6.zip
          2.0.7: modsecurity-crs_2.0.7.zip
          2.0.8: modsecurity-crs_2.0.8.zip
          2.0.9: modsecurity-crs_2.0.9.zip
         2.0.10: modsecurity-crs_2.0.10.zip
          2.1.0: modsecurity-crs_2.1.0.zip
          2.1.1: modsecurity-crs_2.1.1.zip
          2.1.2: modsecurity-crs_2.1.2.zip
          2.2.0: modsecurity-crs_2.2.0.zip
          2.2.1: modsecurity-crs_2.2.1.zip
          2.2.2: modsecurity-crs_2.2.2.zip
          2.2.3: modsecurity-crs_2.2.3.zip
          2.2.4: modsecurity-crs_2.2.4.zip
}
```

Para actualizar a la última versión, primero crearemos un directorio
donde se van a descargar y después las descargamos:

```bash
$ cd /tmp
$ mkdir crs
$ ./rules-updater.pl -rhttp://www.modsecurity.org/autoupdate/repository/ -pcrs -Smodsecurity-crs
```

Esto nos descarga el fichero con las últimas reglas, en este caso
`modsecurity-crs_2.2.4.zip`.

* * * * *

#### Actualización a 2 de junio de 2013

Parece ser que, actualmente, al intentar actualizar las reglas, nos
encontremos con un error 404:

```bash
$ sudo ./rules-updater.pl -rhttp://www.modsecurity.org/autoupdate/repository/ -pcrs -Smodsecurity-crs
Could not load GnuPG module - cannot verify ruleset signatures
Fetching: modsecurity-crs/modsecurity-crs_2.2.5.zip ...
Failed to retrieve ruleset modsecurity-crs/modsecurity-crs_2.2.5.zip: 404 Not Found
```

Podemos encontrar el fichero de reglas para la última versión de
`mod_security`, la 2.2.7, en el [repostorio en GitHub][]. Pero si
queremos descargar una versión anterior, podemos recurrir al paquete
[modsecurity-crs en Launchpad][].

```bash
$ wget https://launchpad.net/ubuntu/+archive/primary/+files/modsecurity-crs_2.2.5.orig.tar.gz
$ md5sum modsecurity-crs_2.2.5.orig.tar.gz
aaeaa1124e8efc39eeb064fb47cfc0aa  modsecurity-crs_2.2.5.orig.tar.gz
$ tar xvzf modsecurity-crs_2.2.5.orig.tar.gz
$ sudo cp -R modsecurity-crs_2.2.5 /etc/apache2/
$ sudo rm /etc/apache2/modsecurity-crs
$ cd /etc/apache2
$ sudo ln -s modsecurity-crs_2.2.5 modsecurity-crs
```

Después de copiarlo al directorio de apache, deberemos crear un fichero
de configuración, por ejemplo a partir del fichero de ejemplo que viene
tal como hicimos al instalarlo sólo que ahora tiene un nombre diferente,
y reiniciar apache para que los cambios tengan efecto:

```bash
$ cd /etc/apache2/modsecurity-crs
$ sudo cp modsecurity_crs_10_setup.conf.example modsecurity_crs_10_setup.conf
```

Si utilizamos la nueva nomenclatura para el fichero, deberemos
actualizar el fichero `/etc/apache2/apache2.conf`:

```bash

    Include modsecurity-crs/modsecurity_crs_10_setup.conf
    Include modsecurity-crs/base_rules/*.conf
```

Una vez más, deberemos reiniciar Apache.

* * * * *

#### Crypt::SSLeay or IO::Socket::SSL not installed

Si nos aparece este error, es que nos faltan módulos:

```bash
$ sudo aptitude install libcrypt-ssleay-perl libio-socket-ssl-perl
```

<h2servertokens < h2>

Mediante `mod_security` se puede cambiar el valor de la cabecera
`Server`.

Lo primero será asegurarnos de que en el fichero
`/etc/apache2/conf.d/security` contiene el valor:

```bash
ServerTokens Full
```

Añadimos al fichero `/etc/apache2/conf.d/modsecurity.conf`:

```bash
SecServerSignature "incognito"
```

Desactivamos y volvemos a activar el módulo, para que se cree el enlace
simbólico a nuestro archivo de configuración, y reiniciamos Apache:

```bash
$ sudo a2dismod mod-security
$ sudo a2enmod mod-security
$ sudo apache2ctl restart
```

Ya podemos comprobar cómo la cabecera `Server` ha cambiado:

```bash
$ curl -sI localhost/k/ | grep ^Server
Server: incognito
```

Referencias
-----------

- [mod_security][]
- [mod_security wiki][]
- [mod_security on Apache][]
- [Howto: Mod_security][]
- [OWASP ModSecurity Core Rule Set Project][]

  [renombrar esta variable por su valor anterior]: http://comments.gmane.org/gmane.comp.apache.mod-security.owasp-crs/410
    "renombrar esta variable por su valor anterior"
  [repostorio en GitHub]: https://github.com/SpiderLabs/owasp-modsecurity-crs/
    "repostorio en GitHub"
  [modsecurity-crs en Launchpad]: https://launchpad.net/ubuntu/+source/modsecurity-crs/
    "modsecurity-crs en Launchpad"
  [mod_security]: http://modsecurity.org/index.html
    "mod_security"
  [mod_security wiki]: http://sourceforge.net/apps/mediawiki/mod-security/index.php?title=Main_Page
    "mod_security wiki"
  [mod_security on Apache]: http://library.linode.com/web-servers/apache/mod-security
    "mod_security on Apache"
  [Howto: Mod_security]: http://wiki.engardelinux.org/index.php/Mod_security
    "Howto: Mod_security"
  [OWASP ModSecurity Core Rule Set Project]: http://www.owasp.org/index.php/Category:OWASP_ModSecurity_Core_Rule_Set_Project
    "OWASP ModSecurity Core Rule Set Project"
