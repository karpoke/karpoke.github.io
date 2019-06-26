Title: De usuarios en WordPress
Date: 2012-08-02 13:45
Author: Nacho Cano
Tags: administrador, fingerprinting, mysql, privilegios, root, usuarios, wordpress
Slug: de-usuarios-en-wordpress
Related: recuperar-la-direccion-de-wordpress,acceder-al-panel-de-control-de-wordpress-tras-haber-sido-baneado,with-great-power-comes-great-responsibility

Uno de los peores hábitos, en cuanto a seguridad en informática se
refiere, es utilizar la cuenta de administrador de forma compulsiva para
todo, sin importar que la tarea que estemos haciendo requiera
privilegios de administrador o no. Esto se puede aplicar tanto a la
cuenta de `root` en un sistema GNU/Linux como al usuario administrador
en WordPress. Lo ideal sería utilizar una cuenta con el mínimo nivel de
privilegios posible que nos permita llevar a cabo nuestra tarea.

En WordPress hay varios [niveles de privilegios][], desde suscriptor que
sólo puede modificar su perfil, hasta super administrador, pasando por
diferentes niveles según se permita la creación, edición o eliminación
de artículos.

Si ya teníamos artículos publicados, por ejemplo con el usuario
administrador, y queremos pasarlos a otro usuario, por ejemplo con
perfil autor, podemos hacerlo, utilizando la cuenta de administrador,
uno a uno. Si teníamos muchos artículos, mejor hacerlo directamente
sobre la base de datos.

Nos conectamos a la base de datos de WordPress.

```bash
$ mysql -uwpuser -p wpdb
```

Las tablas que vamos a utilizar son `wp_posts` y `wp_users`. Podemos ver
información relativa a ellas con el comando `desc`:

```bash
mysql> desc wp_users;
+---------------------+---------------------+------+-----+---------------------+----------------+
| Field               | Type                | Null | Key | Default             | Extra          |
+---------------------+---------------------+------+-----+---------------------+----------------+
| ID                  | bigint(20) unsigned | NO   | PRI | NULL                | auto_increment |
| user_login          | varchar(60)         | NO   | MUL |                     |                |
| user_pass           | varchar(64)         | NO   |     |                     |                |
| user_nicename       | varchar(50)         | NO   | MUL |                     |                |
| user_email          | varchar(100)        | NO   |     |                     |                |
| user_url            | varchar(100)        | NO   |     |                     |                |
| user_registered     | datetime            | NO   |     | 0000-00-00 00:00:00 |                |
| user_activation_key | varchar(60)         | NO   |     |                     |                |
| user_status         | int(11)             | NO   |     | 0                   |                |
| display_name        | varchar(250)        | NO   |     |                     |                |
+---------------------+---------------------+------+-----+---------------------+----------------+
```

```bash
mysql> desc wp_posts;
+-----------------------+---------------------+------+-----+---------------------+----------------+
| Field                 | Type                | Null | Key | Default             | Extra          |
+-----------------------+---------------------+------+-----+---------------------+----------------+
| ID                    | bigint(20) unsigned | NO   | PRI | NULL                | auto_increment |
| post_author           | bigint(20) unsigned | NO   | MUL | 0                   |                |
| post_date             | datetime            | NO   |     | 0000-00-00 00:00:00 |                |
| post_date_gmt         | datetime            | NO   |     | 0000-00-00 00:00:00 |                |
| post_content          | longtext            | NO   | MUL | NULL                |                |
| post_title            | text                | NO   | MUL | NULL                |                |
| post_excerpt          | text                | NO   |     | NULL                |                |
| post_status           | varchar(20)         | NO   |     | publish             |                |
| comment_status        | varchar(20)         | NO   |     | open                |                |
| ping_status           | varchar(20)         | NO   |     | open                |                |
| post_password         | varchar(20)         | NO   |     |                     |                |
| post_name             | varchar(200)        | NO   | MUL |                     |                |
| to_ping               | text                | NO   |     | NULL                |                |
| pinged                | text                | NO   |     | NULL                |                |
| post_modified         | datetime            | NO   |     | 0000-00-00 00:00:00 |                |
| post_modified_gmt     | datetime            | NO   |     | 0000-00-00 00:00:00 |                |
| post_content_filtered | longtext            | NO   |     | NULL                |                |
| post_parent           | bigint(20) unsigned | NO   | MUL | 0                   |                |
| guid                  | varchar(255)        | NO   |     |                     |                |
| menu_order            | int(11)             | NO   |     | 0                   |                |
| post_type             | varchar(20)         | NO   | MUL | post                |                |
| post_mime_type        | varchar(100)        | NO   |     |                     |                |
| comment_count         | bigint(20)          | NO   |     | 0                   |                |
+-----------------------+---------------------+------+-----+---------------------+----------------+
```

Necesitamos conocer los identificadores del usuario origen y usuario
destino. Por ejemplo:

```bash
mysql> select ID, user_login from wp_users;
+----+------------+
| ID | user_login |
+----+------------+
|  1 | admin      |
|  2 | user       |
+----+------------+
```

Cambiamos los artículos del viejo usuario (con identificador 1) al nuevo
usuario (con identificador 2):

```bash
mysql> update wp_posts set post_author=2 where post_author=1;
```

Y listos.

Cambiar el nombre de usuario
----------------------------

Cambiar el nombre de usuario que se utiliza para iniciar sesión, una vez
creado el usuario, es algo que no se puede hacer desde el panel de
administración de WordPress, pero podemos cambiarlo desde la consola
MySQL. Por ejemplo, para cambiar el usuario `admin` por `newlogin`:

```bash
$ update wp_users set user_login="newlogin" where user_login="admin";
```

* * * * *

#### Actualizado el 12 de enero de 2014

Enumeración de usuarios
-----------------------

WordPress permite mostrar un listado de los artículos de cada usuario
mediante una URL como `http://www.example.com/author/username/`. El
problema es que, por defecto, este nombre de usuario coincide con el
nombre de usuario que se utiliza para iniciar sesión en el panel de
administración. Encontrar este nombre de usuario no es difícil, ya que
los enlaces del tipo `http://www.example.com/?author=1` redirigen a un
enlace como el anterior, pero con el nombre del usuario que se
corresponde con el identificador utilizado, en este ejemplo el 1, que
además suele ser el usuario administrador.

Afortunadamente, se pueden tener [nombres de usuario diferentes para
iniciar sesión y para mostrar los artículos de un usuario][] a través el
campo `user_nicename`. Podemos modificar el nuestro mediante:

```bash
mysql> update wp_users set user_nicename="nick" where user_login="username";
```

* * * * *

#### Actualizado el 15 de agosto de 2012

Cambiar la información del autor de los comentarios
---------------------------------------------------

Los comentarios en WordPress también tienen asociado un usuario. Primero
veamos los campos que tiene la tabla `wp_comments`:

```bash
mysql> desc wp_comments;
+----------------------+---------------------+------+-----+---------------------+----------------+
| Field                | Type                | Null | Key | Default             | Extra          |
+----------------------+---------------------+------+-----+---------------------+----------------+
| comment_ID           | bigint(20) unsigned | NO   | PRI | NULL                | auto_increment |
| comment_post_ID      | bigint(20) unsigned | NO   | MUL | 0                   |                |
| comment_author       | tinytext            | NO   |     | NULL                |                |
| comment_author_email | varchar(100)        | NO   |     |                     |                |
| comment_author_url   | varchar(200)        | NO   |     |                     |                |
| comment_author_IP    | varchar(100)        | NO   |     |                     |                |
| comment_date         | datetime            | NO   |     | 0000-00-00 00:00:00 |                |
| comment_date_gmt     | datetime            | NO   | MUL | 0000-00-00 00:00:00 |                |
| comment_content      | text                | NO   |     | NULL                |                |
| comment_karma        | int(11)             | NO   |     | 0                   |                |
| comment_approved     | varchar(20)         | NO   | MUL | 1                   |                |
| comment_agent        | varchar(255)        | NO   |     |                     |                |
| comment_type         | varchar(20)         | NO   |     |                     |                |
| comment_parent       | bigint(20) unsigned | NO   | MUL | 0                   |                |
| user_id              | bigint(20) unsigned | NO   |     | 0                   |                |
+----------------------+---------------------+------+-----+---------------------+----------------+
```

Si el usuario está registrado, el campo `user_id` tiene el identificador
del usuario, sino le asigna un 0. Sin embargo, el nombre, la URL y el
correo electrónico, que queda registrado aunque no se muestre, son los
que tuviera el usuario en el momento de hacer el comentario, por lo que
si el usuario los modifica posteriormente, los cambios no quedan
reflejados en los comentarios anteriores.

Para ver los comentarios de usuarios registrados podemos ejecutar:

```bash
mysql> select comment_author, comment_author_url, comment_author_email, comment_author_IP, user_id from wp_comments where user_id != 0;
```

Si queremos cambiar el autor de los comentarios de un usuario concreto y
actualizar la información asociada, por ejemplo cambiar el autor de los
comentarios del usuario con identificador 1 al que tiene el 2, no
tenemos más que ejecutar:

```bash
mysql> update wp_comments c, wp_users u
       set c.comment_author=u.user_nicename, c.comment_author_url=u.user_url, c.comment_author_email=u.user_email, c.user_id=u.ID
       where u.ID=2 and c.user_id=1;
```

Dependiendo de la configuración de MySQL, es posible que nos aparezca el
siguiente error:

```bash
ERROR 1175 (HY000): You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column
```

Si están activadas las [actualizaciones seguras][], no se permite
ejecutar ninguna sentencia de actualización o borrado si no se utiliza
un campo clave en el WHERE o no se utiliza la cláusula LIMIT. En este
caso no estamos seleccionando los comentarios por ningún campo clave, de
ahí que aparezca el error.

Podemos desactivar las actualizaciones seguras ejecutando:

```bash
mysql> set SQL_SAFE_UPDATES=0;
```

Y ahora ya sí que nos dejará ejecutar la actualización. Si queremos
volver a activar las actualizaciones seguras, no tenemos más que
asignarle un valor de 1.

* * * * *

  [niveles de privilegios]: http://codex.wordpress.org/Roles_and_Capabilities
    "niveles de privilegios"
  [nombres de usuario diferentes para iniciar sesión y para mostrar los artículos de un usuario]: http://www.authorsure.com/827/wordpress-username-security
    "nombres de usuario diferentes para iniciar sesión y para mostrar los artículos de un usuario"
  [actualizaciones seguras]: http://dev.mysql.com/doc/refman/5.5/en/mysql-tips.html#safe-updates
    "actualizaciones seguras"
