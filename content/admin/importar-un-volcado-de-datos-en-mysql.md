Title: Importar un volcado de datos en MySQL
Date: 2011-03-27 22:09
Author: Nacho Cano
Tags: mysql, mysqldump, mysqlimport
Slug: importar-un-volcado-de-datos-en-mysql

Para realizar un volcado de datos, podemos ejecutar:

```bash
$ mysqldump -uuser -p --all-databases --host localhost > mysql.sql
```

![MySQL Dump]({static}/images/mysqldump.png )

_<small>Fuente: [luauf.com][]</small>_

Para importar este volcado, existe la herramienta `mysqlimport`:

```bash
$ mysqlimport -uuser -hhost -p --local dbname mysql.sql
```

Sin embargo, no me acaba de ir bien, ya que me devuelve este error:

```bash
mysqlimport: Error: 1146, Table 'dbname.mysql' doesn't exist, when using table: mysql
```

Una forma de conseguir [restaurar el volcado de datos][] es desde el
cliente de `mysql`:

```bash
$ mysql -uuser -p dbname
mysql> source mysql.sql;
mysql> exit;
```

[Otra forma][]:

```bash
$ mysql -uuser -p dbname < mysql.sql
```

  [luauf.com]: http://luauf.com/2008/05/17/mysql-shell-script-backup/
    "luauf.com"
  [restaurar el volcado de datos]: http://forums.mysql.com/read.php?10,269126,269264#msg-269264
    "restaurar el volcado de datos"
  [Otra forma]: http://bookmarks.honewatson.com/2008/05/06/mysqlimport-error-table-databasemydatabase-doesnt-exist/
    "Otra forma"
