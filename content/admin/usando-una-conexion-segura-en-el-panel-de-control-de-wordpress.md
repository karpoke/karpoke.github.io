Title: Usando una conexión segura en el panel de control de Wordpress
Date: 2011-06-14 14:17
Author: Nacho Cano
Tags: apache, https, inicio de sesión, php, plugin, ssl, ssl for logged in users, wordpress
Slug: usando-una-conexion-segura-en-el-panel-de-control-de-wordpress

Si tenemos [instalado un WordPress][] y queremos [iniciar sesión a
través de una conexión segura][], deberemos modificar el fichero
`/usr/share/wordpress/wp-config.php` y añadir:

```php
define('FORCE_SSL_LOGIN', true);
```

Si queremos que se use la conexión segura en todo el panel de control,
en lugar de lo anterior, añadiremos:

```php
define('FORCE_SSL_ADMIN', true);
```

Para que esto funcione, es necesario que [Apache esté configurado para
servir conexiones seguras][].

* * * * *

#### Actualización a 13 de julio de 2013

Si hemos iniciado sesión y navegamos por nuestra página web, deberíamos
asegurarnos de que seguimos usando una conexión segura, ya que estamos
enviando nuestra _cookie_ de sesión y alguien en la misma red podría
llegar a capturarla si no es así.

El complemento [SSL for logged in users][] fuerza que los usuarios que han
iniciado sesión continúen usando una conexión segura en todo el sitio.
Además, con este complemento, ya no será necesario modificar el fichero
`wp-config.php`.

  [instalado un WordPress]: {filename}/admin/la-infame-actualizacion-de-wordpress-en-15-segundos.md
    "la infame actualización de wordpress en 15 segundos"
  [iniciar sesión a través de una conexión segura]: http://rackerhacker.com/2009/07/31/requiring-ssl-encryption-for-wordpress-administration/
    "iniciar sesión a través de una conexión segura"
  [Apache esté configurado para servir conexiones seguras]: {filename}/admin/configurar-apache-para-servir-conexiones-seguras.md
    "configurar apache para servir conexiones seguras"
  [SSL for logged in users]: https://wordpress.org/plugins/ssl-for-logged-in-users/
    "SSL for logged in users"
