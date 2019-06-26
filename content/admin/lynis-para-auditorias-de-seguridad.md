Title: Lynis para auditorías de seguridad
Date: 2012-07-14 19:23
Modified: 2016-12-03 19:17
Author: Nacho Cano
Tags: auditoría, Basel II, cron, escáner de vulnerabilidades, GLBA, HIPAA, malware, PCI DSS, SOX, wget, apt-key
Slug: lynis-para-auditorias-de-seguridad

[Lynis][] es una herramienta para realizar auditorías en sistemas Unix.
Escanea el sistema en busca de vulnerabilidades y fallos de seguridad.
También muestra información general del sistema, paquetes instalados y
errores de configuración.

Su objetivo es ayudar en el proceso de auditoría, actualización del
software y escaneo de vulnerabilidades y _malware_ en sistemas Unix. Se
puede ejecutar sin necesidad de instalación.

Se puede utilizar en auditorías Basel II, GLBA, HIPAA, PCI DSS y SOX
(Sabarnes-Oxley). La [documentación][] está disponible en línea.

Si queremos probarlo, no tenemos más que descargarlo de su página, ahora
mismo la última versión estable es la 1.3.0, descomprimirlo y
ejecutarlo:

```bash
$ wget http://www.rootkit.nl/files/lynis-1.3.0.tar.gz
$ shasum lynis-1.3.0.tar.gz
b60921420277a969cf862b0e0166fe36451057b9  lynis-1.3.0.tar.gz
$ tar xvzf lynis-1.3.0.tar.gz
$ cd lynis-1.3.0
```

Algunas opciones:

```bash
  Scan options:
    --auditor ""            : Auditor name
    --check-all (-c)              : Check system
    --no-log                      : Don’t create a log file
    --profile            : Scan the system with the given profile file
    --quick (-Q)                  : Quick mode, don’t wait for user input
    --tests ""             : Run only tests defined by
    --tests-category "" : Run only tests defined by

  Layout options:
    --no-colors                   : Don’t use colors in output
    --quiet (-q)                  : No output, except warnings
    --reverse-colors              : Optimize color display for light backgrounds

  Misc options:
    --check-update                : Check for updates
    --view-manpage (--man)        : View man page
    --version (-V)                : Display version number and quit
```

Por ejemplo:

```bash
$ sudo ./lynis -Q
```

Si queremos que realice un reporte automático, por ejemplo diario,
podemos incluir una línea como la siguiente en el `cron`:

```bash
$ sudo crontab -e
23 7 * * * /path/to/lynis-1.3.0/lynis --auditor "automated" --cronjob
```

El argumento `--cronjob` equivale a `-c -Q`, es decir, todos los tests y
sin intervención del usuario.

O crear el fichero `/etc/cron.daily/lynis` con el siguiente contenido:

```bash
#!/bin/sh

LYNIS=/path/to/lynis-1.3.0/lynis
NICE=0
MAILTO="root@localhost"

test -x $LYNIS || exit 0

OUTFILE=`mktemp` || exit 1

cd $(dirname $LYNIS)
/usr/bin/nice -n $NICE $LYNIS --cronjob --auditor "automated" > $OUTFILE
if [ -s "$OUTFILE" ]; then
    SUBJECT="Subject: [lynis] $(hostname -f) - Daily report"
    cat $OUTFILE | mail -s $SUBJECT $MAILTO
fi
rm -f $OUTFILE
```

* * * * *

#### Actualizado el 3 de diciembre de 2016

La forma más sencilla de mantener `lynis` actualizado es utilizar el
[repositorio oficial] y seguir lo siguientes pasos.

Si lo habíamos instalado desde los repositorios de Ubuntu, lo desinstalamos:

```bash
$ sudo apt remove lynis
```

Descargamos la clave desde el servidor central de claves de Ubuntu:

```bash
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C80E383C3DE9F082E01391A0366C67DE91CA5D5F
```

En su defecto, también podríamos descargarla e importarla del servidor oficial de la aplicación:

```bash
$ wget -O - http://packages.cisofy.com/keys/cisofy-software-public.key | sudo apt-key add -
```

Añadimos el repostorio:

```bash
$ echo "deb https://packages.cisofy.com/community/lynis/deb/ trusty main" | sudo tee -a /etc/apt/sources.list.d/cisofy-lynis.list
```

Actualizamos los paquetes y reinstalamos:

```bash
$ sudo apt update
$ sudo apt install lynis
```

* * * * *

  [Lynis]: http://www.rootkit.nl/projects/lynis.html
    "Lynis"
  [documentación]: http://www.rootkit.nl/files/lynis-documentation.html
    "documentación"
  [repositorio oficial]: https://packages.cisofy.com/#debian-ubuntu
    "repositorio oficial"
