Title: Saltar a una entrada aleatoria en WordPress
Date: 2012-07-27 00:20
Author: Nacho Cano
Tags: aleatoriedad, página aleatoria, php, wordpress
Slug: saltar-a-una-entrada-aleatoria-en-wordpress

Si queremos añadir un enlace que nos permita saltar a una entrada
aleatoria de un blog en WordPress, basta crear un archivo que contenga
lo siguiente:

```php
<?php
require('wp-blog-header.php');
query_posts(array('orderby' => 'rand', 'showposts' => 1));
if (have_posts()) : the_post();
$url = get_permalink($post->id);
        header("Location: " . $url);
endif;
wp_reset_query();
?>
```

Guardamos el archivo en una ruta accesible, por ejemplo en la raíz del
blog.

Sólo queda añadir el enlace para que nos lleve a una [entrada
aleatoria][].

PS: Recordando una vieja entrada en [Microsiervos][].

* * * * *

#### Actualizado el 28 de septiembre de 2012

WordPress puede utilizar URLs claras para enlazar a los artículos,
categorías, etiquetas, páginas o archivos. Si queremos que el enlace al
_script_ sea del mismo tipo, podemos añadir las siguientes líneas al
fichero `.htaccess` de la raíz del sitio:

```bash
RewriteEngine On
RewriteBase /blog/
RewriteRule ^salta/$ salta.php
```

* * * * *

Referencias
-----------

- [Function Reference/query posts][]
- [The Loop][]
- [Template Tags/get posts][]

  [Microsiervos]: http://www.microsiervos.com/archivo/general/salta.html
    "Microsiervos"
  [entrada aleatoria]: /salta/
    "Salta a una entrada aleatoria"
  [Function Reference/query posts]: http://codex.wordpress.org/Function_Reference/query_posts
    "Function Reference/query posts"
  [The Loop]: http://codex.wordpress.org/The_Loop
    "The Loop"
  [Template Tags/get posts]: https://codex.wordpress.org/Function_Reference/get_posts
    "Template Tags/get posts"
