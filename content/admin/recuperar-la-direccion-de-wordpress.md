Title: Recuperar la dirección de WordPress
Date: 2012-04-05 14:46
Author: Nacho Cano
Tags: dirección de wordpress, dirección del sitio, home, mysql, siteurl, url, wordpress
Slug: recuperar-la-direccion-de-wordpress

En el panel de administración de WordPress, en Ajustes > Generales,
podemos cambiar la dirección del blog o la dirección donde está
instalado Wordpress.

Tenemos que tener cuidado si cambiamos la dirección de WordPress, ya que
podemos dejar el sitio, y en especial el panel de control, inaccesible.
O puede que lo que nos interese sea actualizar el dominio antiguo por el
nuevo.

En ambas situaciones, si sólo se debe modificar el dominio, sin que se
deba cambiar ninguna ruta relativa de acceso al blog, podemos lograr
acceso al panel de administración incluyendo el nuevo dominio al archivo
`/etc/hosts`, y desde ahí modificar cualquier variable que necesitemos.

Pero si hemos cambiado la ruta relativa necesitaremos cambiar el valor
en la base de datos. Podemos acceder a través de PhpMyAdmin o, si
tenemos acceso al terminal, con un cliente de MySQL. Por ejemplo, si
queremos asignar la dirección de WordPress a `http://www.example.com`:

    $ mysql -uuser -p wordpress
    mysql> update wp_options set option_value = "http://www.example.com" where option_name = "siteurl";

Si queremos modificar el valor de la dirección del sitio:

    mysql> update wp_options set option_value = "http://www.example.com" where option_name = "home";

Para modificar la URL de los archivos subidos:

    mysql> update wp_options set option_value = "http://www.example.com/wp-uploads" where option_name = "upload_url_path";

Si queremos hacer un cambio masivo, como cambiar una dirección que
aparezca en el contenido de los artículos o de los comentarios:

    mysql> update wp_posts set post_content = replace(post_content, 'example.com', 'new-domain.com'), guid = replace(guid, 'example.com', 'new-domain.com');
    mysql> update wp_comments set comment_author_url = replace(comment_author_url, 'example.com', 'new-domain.com');

En el caso de los plugins, dependerá de cada caso. Por ejemplo:

    mysql> update wp_randomtext set text = replace(text, 'example.com', 'new-domain.com');

Dos sentencias útiles, una nos muestra las tablas que tenemos y la otra
la información de una tabla concreta:

    mysql> show tables;
    mysql> desc wp_posts;

Por último, si hemos actualizado la dirección de WordPress y estamos
usando alguna [técnica _anti-hotlinking_][], deberíamos revisar el
archivo `.htaccess`, por si debiéramos actualizarlo.

  [técnica _anti-hotlinking_]: {filename}/admin/evitando-el-hotlinking.md
    "Evitando el hotlinking"
