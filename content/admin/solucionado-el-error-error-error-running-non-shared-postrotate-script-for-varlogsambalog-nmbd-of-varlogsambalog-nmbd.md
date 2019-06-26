Title: Solucionado el error «error: error running non-shared postrotate script for /var/log/samba/log.nmbd of '/var/log/samba/log.nmbd '»
Date: 2013-03-22 21:31
Author: Nacho Cano
Tags: 12.04, error, logrotate, nmbd, quantal, quetzal, samba, smbd, ubuntu
Slug: solucionado-el-error-error-error-running-non-shared-postrotate-script-for-varlogsambalog-nmbd-of-varlogsambalog-nmbd

Si nos encontramos con el siguiente error:

```bash
error: error running non-shared postrotate script for /var/log/samba/log.nmbd of '/var/log/samba/log.nmbd '
```

En Ubuntu 12.04.2, con la versión de `samba` 3.6.3, podría producirse
cuando el [_script_ de `logrotate` para `samba`][script de logrotate para samba]
intenta hacer un `reload` del servicio `nmbd` y éste no está en ejecución.
Necesita un pequeño cambio en los comandos utilizados en la directiva `postrotate`:
deberemos cambiar `reload` por `reload --quiet`, quedando finalmente así
las respectivas líneas en el fichero `/etc/logrorate.d/samba`:

```bash
reload --quiet smbd 2>/dev/null
reload --quiet nmbd 2>/dev/null
```

  [script de logrotate para samba]: http://dev-eole.ac-dijon.fr/issues/4524
    "script de logrotate para samba"
