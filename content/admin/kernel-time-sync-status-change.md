Title: kernel time sync status change
Date: 2011-01-07 06:04
Author: Nacho Cano
Tags: logcheck, ntp
Slug: kernel-time-sync-status-change

Tras instalar `logcheck`, un programa que escanea los ficheros de _log_
del sistema en busca de "líneas interesantes", comencé a recibir
demasiados avisos del tipo:

    Jan  7 02:04:38 terminus ntpd[1117]: kernel time sync status change 6001
    "1117"
    Jan  7 02:21:44 terminus ntpd[1117]: kernel time sync status change 2001
    "1117"

[Estos cambios son debidos][] a que `ntp` cambia [dinámicamente][] entre
los modo `FLL` y el `PLL`, lo que le permite tener en cuenta la latencia
de la red o el _jitter_ a la hora de actualizar el reloj del sistema.

Por lo tanto, los mensajes son inofensivos, y si queremos que no nos
lleguen más, deberemos [cambiar una regla][] que se encuentra en el
fichero `/etc/logcheck/ignore.d.server/ntp` (si el modo en que trabaja
`logcheck` es `server` y así está especificado en el fichero
`/etc/logcheck/logcheck.conf`).

Cambiaremos:

    ^\w{3} [ :0-9]{11} [._[:alnum:]-]+ ntpd\[[0-9]+\]: kernel time sync (disabled|enabled) [0-9]+$
    " :0-9]{11} [._[:alnum:]-]+ ntpd\[[0-9]+\"

por:

    ^\w{3} [ :0-9]{11} [._[:alnum:]-]+ ntpd\[[0-9]+\]: kernel time sync (disabled|enabled|status change) [0-9]+$
    " :0-9]{11} [._[:alnum:]-]+ ntpd\[[0-9]+\"

  [Estos cambios son debidos]: http://lists.freebsd.org/pipermail/freebsd-stable/2005-April/013404.html
    "Estos cambios son debidos"
  [dinámicamente]: http://www.eecis.udel.edu/~mills/database/papers/allan.pdf
    "dinámicamente"
  [cambiar una regla]: http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=498992
    "cambiar una regla"
