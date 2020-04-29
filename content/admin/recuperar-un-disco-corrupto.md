Title: Recuperar un disco corrupto
Date: 2018-01-30 20:36
Author: Nacho Cano
Tags: copia de seguridad, recuperación de datos, dd, pv, ddrescue, gddrescue
Slug: recuperar-un-disco-corrupto

Un par de comandos útiles para recuperar datos de un disco problemático.

Para copiar el disco, mostrando una barra de progeso:

    dd if=/dev/sda | pv | dd of=/dev/sdb conv=noerror,sync

Lanzamos `ddrescue`:
    ddrescue -d -r3 /dev/sda /dev/sdb output.log
