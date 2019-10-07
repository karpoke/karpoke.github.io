Title: Opciones adicionales para trabajar con tablas vinculadas en phpMyAdmin
Date: 2012-05-10 12:26
Author: Nacho Cano
Tags: consultas sql, mysql, phpMyAdmin, pmadb, seguimiento, tablas vinculadas, tracking
Slug: opciones-adicionales-para-trabajar-con-tablas-vinculadas-en-phpmyadmin
Related: cambiar-la-contrasena-de-administrador-en-mysql-5-1,importar-un-volcado-de-datos-en-mysql

![PhpMyAdmin Logo]({static}/images/PhpMyAdmin-Logo-300x212.png)

Puede que alguna vez hayamos visto este mensaje en el panel de
administración de phpMyAdmin:

> Las opciones adicionales para trabajar con tablas vinculadas fueron
> desactivadas. Para saber porqué, dé clic [aquí][].

Si seguimos el enlace, nos lleva a la documentación donde nos explican
que, a partir de la versión 3.3.x, está disponible el sistema de
_tracking_, que es un sistema que permite realizar un seguimiento de las
consultas SQL ejecutadas por phpMyAdmin, tanto sentencias de definición
como de manipulación de datos, pudiendo guardar versiones de las tablas.

Al guardar la versión de una tabla, phpMyAdmin guarda una captura de la
misma, incluyendo su estructura e índices. Posteriormente, phpMyAdmin
guardará todas las órdenes que cambien la estructura de la tabla o los
datos contenidos en ella, y asociará dichas órdenes con el número de
versión. Se podrán visualizar estos cambios en la pestaña de
Seguimiento.

Para permitir esta funcionalidad necesitamos:

-   configurar `pmadb` y el almacenamiento de configuración en
    phpMyAdmin
-   definir el nombre de la tabla en `$cfg['Servers'][$i]['tracking']`

Gracias a este almacenamiento de configuración se puede disfrutar de un
gran variedad de funcionalidades tales como marcadores, comentarios,
histórico de SQL, mecanismo de seguimiento, generación de PDFs,
transformación de los campos de contenido, etc.

Almacenamiento de configuración
-------------------------------

El primero paso será crear las tablas especiales necesarias. En el
fichero `/usr/share/doc/phpmyadmin/examples/create_tables.sql.gz`
tenemos un ejemplo de lo necesario. Posiblemente, ya tengamos creadas
algunas de las tablas que ahí aparecen, si lanzamos el _script_ sólo nos
creará las que no existan:

```bash
$ cp /usr/share/doc/phpmyadmin/examples/create_tables.sql.gz .
$ gunzip create_tables.sql.gz
$ mysql -uroot -p < create_tables.sql
```

Si necesitásemos [recuperar la contraseña de MySQL][] o tuviéramos
problemas [importando los datos][] podemos echarle un ojo a estos
enlaces.

En particular, lo que nos interesa es lo referente a la tabla
`pma_tracking`, y esto es lo que ejecuta el _script_ anterior:

```bash
--
-- Table structure for table `pma_tracking`
--

CREATE TABLE IF NOT EXISTS `pma_tracking` (
  `db_name` varchar(64) collate utf8_bin NOT NULL,
  `table_name` varchar(64) collate utf8_bin NOT NULL,
  `version` int(10) unsigned NOT NULL,
  `date_created` datetime NOT NULL,
  `date_updated` datetime NOT NULL,
  `schema_snapshot` text collate utf8_bin NOT NULL,
  `schema_sql` text collate utf8_bin,
  `data_sql` text collate utf8_bin,
  `tracking` set('UPDATE','REPLACE','INSERT','DELETE','TRUNCATE','CREATE DATABASE','ALTER DATABASE','DROP DATABASE','CREATE TABLE','ALTER TABLE','RENAME TABLE','DROP TABLE','CREATE INDEX','DROP INDEX','CREATE VIEW','ALTER VIEW','DROP VIEW') collate utf8_bin default NULL,
  `tracking_active` int(1) unsigned NOT NULL default '1',
  PRIMARY KEY  (`db_name`,`table_name`,`version`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;
```

Configurar phpMyAdmin
---------------------

Ahora que ya hemos creado las tablas necesarias, deberemos configurar
los parámetros que necesita phpMyAdmin. En Ubuntu, editamos el archivo
`/etc/phpmyadmin/config.inc.php`, y nos aseguramos de que aparecen las
siguientes líneas:

```bash
/_ Optional: User for advanced features _/
$cfg['Servers'][$i]['controluser'] = $dbuser;
$cfg['Servers'][$i]['controlpass'] = $dbpass;

/_ Optional: Advanced phpMyAdmin features _/
$cfg['Servers'][$i]['pmadb'] = $dbname;
$cfg['Servers'][$i]['bookmarktable'] = 'pma_bookmark';
$cfg['Servers'][$i]['relation'] = 'pma_relation';
$cfg['Servers'][$i]['table_info'] = 'pma_table_info';
$cfg['Servers'][$i]['table_coords'] = 'pma_table_coords';
$cfg['Servers'][$i]['pdf_pages'] = 'pma_pdf_pages';
$cfg['Servers'][$i]['column_info'] = 'pma_column_info';
$cfg['Servers'][$i]['history'] = 'pma_history';
$cfg['Servers'][$i]['designer_coords'] = 'pma_designer_coords';
```

Los valores de `controluser`, `controlpass` y `pmadb` se toman del
archivo `/etc/phpmyadmin/config-db.php`.

A continuación de las líneas anteriores, añadimos:

```bash
/_ Optional: Tracking features _/
$cfg['Servers'][$i]['tracking'] = 'pma_tracking';
$cfg['Servers'][$i]['tracking_default_statements'] = 'CREATE TABLE,ALTER TABLE,DROP TABLE,RENAME TABLE,CREATE INDEX,DROP INDEX,INSERT,UPDATE,DELETE,TRUNCATE,REPLACE,CREATE VIEW,ALTER VIEW,DROP VIEW,CREATE DATABASE,ALTER DATABASE,DROP DATABASE';
$cfg['Servers'][$i]['tracking_version_auto_create'] = TRUE;
$cfg['Servers'][$i]['tracking_version_drop_view'] = TRUE;
$cfg['Servers'][$i]['tracking_version_drop_table'] = TRUE;
$cfg['Servers'][$i]['tracking_version_drop_database'] = TRUE;
```

Y ya está. No es necesario reiniciar el servidor, pero es posible que
necesitemos borrar las _cookies_ del navegador para que no volvamos a
ver el mensaje del principio, por ejemplo, cerrando la sesión en
phpMyAdmin y volviendo a entrar, o recargando la caché del navegador
mediante `Ctrl+Shift+r`.

Referencias
-----------

» [phpMyAdmin doc: almacenamiento de configuración para phpMyAdmin][]
» [phpMyAdmin doc: pmadb][]
» [phpMyAdmin doc: tracking][]

  [aquí]: http://www.phpmyadmin.net/localized_docs/es/Documentation.html#tracking
    "aquí"
  [recuperar la contraseña de MySQL]: {filename}/admin/cambiar-la-contrasena-de-administrador-en-mysql-5-1.md
    "Cambiar la contraseña de administrador en MySQL 5.1"
  [importando los datos]: {filename}/admin/importar-un-volcado-de-datos-en-mysql.md
    "Importar un volcado de datos en MySQL"
  [phpMyAdmin doc: almacenamiento de configuración para phpMyAdmin]: http://www.phpmyadmin.net/localized_docs/es/Documentation.html#linked-tables
    "phpMyAdmin doc: almacenamiento de configuración para phpMyAdmin"
  [phpMyAdmin doc: pmadb]: http://www.phpmyadmin.net/localized_docs/es/Documentation.html#pmadb
    "phpMyAdmin doc: pmadb"
  [phpMyAdmin doc: tracking]: http://www.phpmyadmin.net/documentation/#tracking
    "phpMyAdmin doc: tracking"
