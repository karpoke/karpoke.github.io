Title: Solucionado el error "$MFTMirr does not match $MFT (record 0)." al montar una partición NTFS
Date: 2012-09-06 12:46
Author: Nacho Cano
Tags: $MFT, $MFTMirr, NTFS, ntfsfix, ntfsprogs, Windows
Slug: solucionado-el-error-mftmirr-does-not-match-mft-record-0-al-montar-una-particion-ntfs

Si intentamos montar un disco o partición en NTFS, el formato que
utiliza Windows, que no ha sido desconectada "de forma segura", es
posible que no podamos montarla y que recibamos el siguiente error:

```bash
$ sudo mount -t ntfs-3g /dev/sdb1 /media/ntfs
$MFTMirr does not match $MFT (record 0).
    Failed to mount '/dev/sdb1': Error de entrada/salida
    NTFS is either inconsistent, or there is a hardware fault, or it’s a
    SoftRAID/FakeRAID hardware. In the first case run chkdsk /f on Windows
    then reboot into Windows twice. The usage of the /f parameter is very
    important! If the device is a SoftRAID/FakeRAID then first activate
    it and mount a different device under the /dev/mapper/ directory, (e.g.
    /dev/mapper/nvidia_eahaabcc1). Please see the 'dmraid' documentation
    for more details.
```

Incluso si utilizamos el parámetro `-o force` nos sigue devolviendo el
mismo error.

Afortunadamente, existe el paquete `ntfsprogs`, disponible en los
repositorios, que incluye una herramienta con la que podemos
solucionarlo:

```bash
$ sudo ntfsfix /dev/sdb1
    Mounting volume... $MFTMirr does not match $MFT (record 0).
    FAILED
    Attempting to correct errors...
    Processing $MFT and $MFTMirr...
    Reading $MFT... OK
    Reading $MFTMirr... OK
    Comparing $MFTMirr to $MFT... FAILED
    Correcting differences in $MFTMirr record 0...OK
    Processing of $MFT and $MFTMirr completed successfully.
    Setting required flags on partition... OK
    Going to empty the journal ($LogFile)... OK
    Checking the alternate boot sector... FIXED
    NTFS volume version is 3.1.
    NTFS partition /dev/sdb1 was processed successfully.
```

Y ahora ya sí podremos montarla normalmente.

El paquete `ntfsprogs` incluye, además, herramientas para realizar todo
tipo de acciones sobre volúmenes NTFS: crear, clonar, comparar,
comprobar, redimensionar, desfragmentar, mostrar información de
ficheros, listar directorios, deshacer el borrado de ficheros, etc.

Referencias
-----------

- [How to fix '$MFTMirr does not match $MFT (record 0)'][]

  [How to fix '$MFTMirr does not match $MFT (record 0)']: https://wmarkito.wordpress.com/2010/12/29/how-to-fix-mftmirr-does-not-match-mft-record-0/
    "How to fix '$MFTMirr does not match $MFT (record 0)'"
