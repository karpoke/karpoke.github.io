Title: Recuperando archivos del USB
Date: 2010-10-27 11:57
Author: Nacho Cano
Tags: dd, file, icat, ils, informática forense, pérdida de información, recuperación de información, sleuthkit
Slug: recuperando-archivos-del-usb

Tengo la mala costumbre de borrar archivos utilizando la combinación
`shift+del`, para borrarlos directamente sin pasar por la papelera.
Llegará el momento en que borre algo que no debería o algo que
necesitaré más tarde.

![Sushi USB2]({static}/images/sushi_usb_2-300x190.jpg)

Si esto sucediese, lo mejor podría ser:

1.  Desmontar el USB para evitar males mayores

    $ sudo umount /media/miusb # 'miusb' es el nombre del volumen del USB

2.  Hacer una copia del USB con `dd`

    $ dd if=/dev/sdb1 of=/tmp/miusb.dd # sdb1 es la unidad donde se monta el USB

3.  Podemos listar los archivos borrados con `ils`

    $ ils -r /tmp/miusb.dd

    class|host|device|start_time
    ils|anacreonte||1288172460
    st_ino|st_alloc|st_uid|st_gid|st_mtime|st_atime|st_ctime|st_crtime|st_mode|st_nlink|st_size
    8|f|0|0|1263329350|1265842800|0|1263329350|777|0|33076
    12|f|0|0|1265738134|1288130400|0|1265738134|777|0|31609
    14|f|0|0|1263325690|1288130400|0|1263325690|777|0|28946
    16|f|0|0|1263326438|1288130400|0|1263326438|777|0|2305751
    19|f|0|0|1263327386|1288130400|0|1263327386|777|0|91028

4.  Creamos un directorio para tener todos los archivos que se puedan
    recuperar

    $ mkdir /tmp/miusb_tmp

5.  Recuperamos los archivos con `icat`

    $ for i in $(ils -r /tmp/miusb.dd | awk '{print $1}' FS="|" | sed 1,3d); do
    icat -r /tmp/miusb.dd $i > /tmp/miusb_tmp/$i
    echo $i
    done

6.  Comprobamos el tipo de archivos recuperados

    $ file /tmp/miusb_tmp/*

    8:  OpenDocument Text
    12: PDF document, version 1.2
    14: PDF document, version 1.3
    16: PDF document, version 1.4
    19: PDF document, version 1.2

`ils` y `icat` vienen incluidos en el paquete `sleuthkit`, que se
encuentra en los repositorios. También existe `autopsy`, que es una
interfaz web para `sleuthkit`.
