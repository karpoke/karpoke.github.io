Title: Instalar el controlador libre para Broadcom BCM4312 en Ubuntu Trusty Thar
Date: 2014-11-07 19:28
Author: Nacho Cano
Tags: 14.04, b43, bcm4312, broadcom, controladores libres, lspci, ubuntu trusty thar, wifi, wireless
Slug: instalar-el-controlador-libre-para-broadcom-bcm4312-en-ubuntu-trusty-thar
Related: cambiar-el-firmware-del-router-comtrend-ar-5381u-por-uno-libre

Al actualizar Ubuntu 14.04 de 32 a 64 bits, se eliminaron los
controladores de la tarjeta de red inalámbrica. Reinstalar el
controlador libre es sencillo. Antes que nada, necesitamos saber qué
chipset tiene, el identificador y qué módulo carga el kernel (si es que
tenemos algún controlador en uso):

    $ lspci -vvnn | grep -A 9 Network
    04:00.0 Network controller [0280]: Broadcom Corporation BCM4312 802.11b/g LP-PHY [14e4:4315] (rev 01)
    Subsystem: Dell Wireless 1397 WLAN Mini-Card [1028:000c]
    Control: I/O- Mem+ BusMaster+ SpecCycle- MemWINV- VGASnoop- ParErr- Stepping- SERR+ FastB2B- DisINTx-
    Status: Cap+ 66MHz- UDF- FastB2B- ParErr- DEVSEL=fast >TAbort- SERR-

-   **Chipset:** BCM4312
-   **PCI ID:** 14e4:4315
-   **Controlador en uso:** Ninguno (no aparece la línea que lo debería
    indicar)

Instalamos el paquete necesario (si no tenemos conexión, deberemos
conectarnos por cable o bien descargarlo desde otro equipo; más
información en el enlace al final):

    $ sudo aptitude install firmware-b43-installer

Al cabo de unos segundos, ya deberíamos poder usar la red inalámbrica.

### deauthenticating from 00:00:00:11:22:33 by local (reason=3)

Si nos encontramos con que no tenermina de conectar y en los logs
aparece algo como:

    [  123.456789] wlan0: deauthenticating from 00:00:00:11:22:33 by local choice (reason=3)

podría ser debido a que el controlador que estábamos usando [no se ha
descargado correctamente][]. En principio, tras reiniciar ya no
deberíamos tener este problema.

Referencias
-----------

» [Community Help Wiki | WifiDocs/Driver/bcm43xx][]
» [b43 and b43legacy][]

  [no se ha descargado correctamente]: https://bbs.archlinux.org/viewtopic.php?pid=1276722#p1276722
    "no se ha descargado correctamente"
  [Community Help Wiki | WifiDocs/Driver/bcm43xx]: https://help.ubuntu.com/community/WifiDocs/Driver/bcm43xx
    "Community Help Wiki | WifiDocs/Driver/bcm43xx"
  [b43 and b43legacy]: http://wireless.kernel.org/en/users/Drivers/b43
    "b43 and b43legacy"
