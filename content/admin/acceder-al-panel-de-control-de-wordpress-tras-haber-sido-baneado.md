Title: Acceder al panel de control de Wordpress tras haber sido baneado
Date: 2011-04-20 01:46
Author: Nacho Cano
Tags: ban, fail2ban, lockdown, login, mysql, ssh, unban, wordpress
Slug: acceder-al-panel-de-control-de-wordpress-tras-haber-sido-baneado

De forma similar a [`fail2ban` para `ssh`][fail2ban para ssh], existe un
complemento para Wordpress, [Login LockDown][], que controla el número de
intentos de acceso al panel de control, y si se falla en 3 intentos, _banea_
dicha IP durante una hora. Estos parámetros, y alguno más, son configurables
desde la página de configuración del complemento.

El problema es que si compartimos la misma IP pública con más gente, ya sea
porque estamos en un lugar público o en casa de unos amigos, y alguien en esta
misma red realiza más intentos de los permitidos, también nosotros quedamos
_baneados_.

Si tenemos acceso por `ssh` al servidor donde se encuentra la base de datos,
podemos hacer lo siguiente para desbanearnos:

```bash
$ mysql -u wordpress -p wordpress
mysql> select * from wp_lockdowns;
+-------------+---------+---------------------+---------------------+--------------+
| lockdown_ID | user_id | lockdown_date       | release_date        | lockdown_IP  |
+-------------+---------+---------------------+---------------------+--------------+
|           1 |       1 | 2011-04-19 18:58:05 | 2011-04-19 19:58:05 | 80.58.0.33 |
+-------------+---------+---------------------+---------------------+--------------+
1 row in set (0.00 sec)
mysql> delete from wp_lockdowns where lockdown_ID=1;
Query OK, 1 row affected (0.00 sec)
```

  [fail2ban para ssh]: {filename}/admin/detectando-intrusos-en-ubuntu-maverick-meerkat.md
    "detectando intrusos en ubuntu maverick meerkat"
  [Login LockDown]: http://wordpress.org/extend/plugins/login-lockdown/
    "Login LockDown"
