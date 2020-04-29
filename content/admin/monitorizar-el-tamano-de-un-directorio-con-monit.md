Title: Monitorizar el tamaño de un directorio con monit
Date: 2012-09-22 15:17
Author: Nacho Cano
Tags: monit, script
Slug: monitorizar-el-tamano-de-un-directorio-con-monit

`monit` es un herramienta para monitorizar procesos, ficheros,
directorios y sistemas de ficheros, que permite enviar alertas cuando
suceden eventos tales como que un proceso no arranca, se incrementa la
carga del sistema o el uso de memoria por encima de un umbral
determinado, se modifican ficheros o directorios, etc.

El problema es que, por ahora, no permite controlar que el tamaño de un
directorio, es decir, de los ficheros contenidos en él, supere cierto
valor. Sin embargo, podemos [conseguir este resultado][] utilizando un
_script_ que se ejecute de forma periódica y que modifique la fecha de
un fichero concreto mientras el tamaño del directorio sea correcto. Este
fichero de control nos servirá para saber cuándo se ha superado el
limite.

Por ejemplo, vamos a suponer que queremos monitorizar el directorio
`/var/www/uploads` y que `monit` nos avise si supera los 2 GB. Para
saber el tamaño que ocupa el directorio ejecutamos:

    $ du -s /var/www/uploads | awk '{print $1}' # el tamaño está en KB

Para comprobar si supera el umbral, podemos ejecutar un _script_ como el
siguiente:

    #!/usr/bin/env bash
    # $1: directory
    # $2: size threshold in MB
    # $3: control filename in monit configuration file

    [ $# -lt 3 ] && exit 1
    [ ! -r "$1" ] && exit 1

    declare -i threshold=$(($2*1024))                # MB to KB
    declare -i size=$(du -s "$1" | awk '{print $1}') # KB

    if [ $size -lt $threshold ]; then
        touch "$3";
    fi

Lo ejecutamos y comprobamos que funciona correctamente:

    $ sudo ./test_directory_size.sh /var/www/uploads 2000 /var/tmp/monit_dir_uploads
    $ ls /var/tmp/monit_dir_uploads
    -rw-r--r-- 1 root root 0 2012-07-22 14:48 /var/tmp/monit_dir_uploads

Lo añadimos al `cron`, por ejemplo cada 10 minutos, y le pasamos los
valores adecuados:

    $ sudo crontab -e
    _/10 _ * _ _ /root/scripts/test_directory_size.sh /var/www/uploads 2000 /var/tmp/monit_dir_uploads > /dev/null 2>&1

La frecuencia dependerá de la urgencia que le asignemos a este evento y
las consecuencias que tenga el hecho de que ocurra, así como de otros
factores que limiten su aparición.

Ahora sólo queda añadir la configuración de `monit` en el fichero
`/etc/monit/conf.d/server.conf`. Hay que tener en cuenta el tiempo que
hemos puesto en el `cron` a la hora de comprobar la fecha de
modificación del fichero.

    check file monit_dir_uploads with path /var/tmp/monit_dir_uploads
    if timestamp > 15 minutes then alert

Reiniciamos `monit` para que los cambios tengan efecto.

Cuando ocurra que el tamaño del directorio supere el umbral, y por tanto
el _script_ deje de actualizar el fichero de control, nos llegará un
aviso como el siguiente:

    Timestamp failed Service monit_dir_uploads

    Date: Sun, 22 Jul 2012 15:08:17 +0200
    Action: alert
    Host: localhost
    Description: timestamp test failed for /var/tmp/monit_dir_uploads

    Your faithful employee,
    monit

  [conseguir este resultado]: https://lists.gnu.org/archive/html/monit-general/2009-01/msg00023.html
    "conseguir este resultado"
