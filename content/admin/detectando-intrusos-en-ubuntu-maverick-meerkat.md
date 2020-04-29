Title: Detectando intrusos en Ubuntu Maverick Meerkat
Date: 2011-03-07 22:11
Author: Nacho Cano
Tags: 10.10, denyhosts, detección de intrusos, fail2ban, firewall, http, https, log, logcheck, logwatch, psad, ssh, tiger, ufw
Slug: detectando-intrusos-en-ubuntu-maverick-meerkat
Related: w00t-w00t,buscando-rootkits-y-troyanos,la-guardiana-de-la-puerta

Un artículo para tener en cuenta algunas de las acciones que podemos
llevar a cabo para [securizar Ubuntu Maverick Meerkat][]. Algunos
programas para facilitar la tarea de controlar los intentos de acceso al
sistema:


ufw
---

`ufw` es una forma sencilla de manejar un cortafuegos. Nada más
instalarlo, lo habilitamos:

    $ sudo ufw enable

Damos de alta los servicios^[1][]^ que queremos que estén disponibles:

    $ sudo ufw allow http
    $ sudo ufw allow https
    $ sudo ufw allow 1234

Si queremos deshacer alguna de estas acciones, por ejemplo, eliminar la
regla para el puerto 1234:

    $ sudo ufw delete 1234

Comprobamos el estado:

    $ sudo ufw status
    Estado: activo
    Hasta                      AcciónDesde
    -----                      ------------------------
    80                         ALLOW       Anywhere
    443                        ALLOW       Anywhere
    1234                       ALLOW       Anywhere`

fail2ban
--------

`fail2ban` busca intentos de acceso por SSH fallidos en
`/var/log/auth.log` y bloquea las IPs de forma temporal. Podemos poner
que se permitan hasta 3 intentos y si se falla se banea la IP durante,
por ejemplo, 10 minutos. En el archivo `/etc/fail2ban/jail.conf`, además
de poder poner un correo electrónico al cual nos lleguen los avisos,
está la configuración para cada servicio que queramos controlar. Por
ejemplo:

    [ssh]
    enabled = true
    port    = 1234
    filter  = sshd
    logpath  = /var/log/auth.log
    maxretry = 3

    [apache]
    enabled = true
    port    = http,https
    filter  = apache-auth
    logpath = /var/log/apache*/*error.log
    maxretry = 3

En el fichero también vienen configuración para Apache, varios
servidores de FTP, de correo y DNS.

Para controlar el estado ejecutamos el cliente, por ejemplo:

    $ sudo fail2ban-client status
    Status
    |- Number of jail:      2
    `- Jail list:           apache, ssh

    $ sudo fail2ban-client status ssh
        Status for the jail: ssh
        |- filter
        |  |- File list:        /var/log/auth.log
        |  |- Currently failed: 0
        |  `- Total failed:     3
        `- action
           |- Currently banned: 0
           |  `- IP list:
           `- Total banned:     0

denyhosts
---------

`denyhosts` es parecido a `fail2ban`. Comprueba los intentos de acceso
por SSH fallidos en `/var/log/auth.log` y añade las IPs al fichero
`/etc/hosts.deny`.

![You are being monitored]({static}/images/you-are-being-monitored1-300x300.jpg)

psad
----

`psad` monitoriza los _logs_ del `iptables` para detectar intentos de
intrusión y tráfico sospechos. Se pueden configurar incontables
parámetros en `/etc/psad/psad.conf`. Para comprobar el estado
ejecutamos:

    $ sudo psad -S
        [+] psadwatchd (pid: 18853)  %CPU: 0.0  %MEM: 0.0
            Running since: Mon Mar  7 19:34:09 2011

        [+] psad (pid: 18851)  %CPU: 0.0  %MEM: 0.4
            Running since: Mon Mar  7 19:34:09 2011
            Command line arguments: [none specified]
            Alert email address(es): karpoke@localhost

        [+] Version: psad v2.1.5

        [+] Top 50 signature matches:
                [NONE]

        [+] Top 25 attackers:
                [NONE]

        [+] Top 20 scanned ports:
                [NONE]

        [+] iptables log prefix counters:
                [NONE]

            Total packet counters: tcp: 0, udp: 0, icmp: 0

        [+] IP Status Detail:
                [NONE]

            Total scan sources: 0
            Total scan destinations: 0

        [+] These results are available in: /var/log/psad/status.out


Tiger
-----

`Tiger` es una herramienta de detección de intrusiones. Para ejecutarlo
(Ojo! el análisis es bastante intenso en términos de CPU):

    $ sudo tiger
        Configuring...

        Will try to check using config for 'i686' running Linux 2.6.32-28-generic...
        --CONFIG-- [con005c] Using configuration files for Linux 2.6.32-28-generic. Using
                   configuration files for generic Linux 2.
        Tiger security scripts *** 3.2.2, 2007.08.28.00.00 *__
        20:38> Beginning security report for terminus.
        20:38> Starting file systems scans in background...
        20:38> Checking password files...
        20:38> Checking group files...
        20:38> Checking user accounts...
        20:40> Checking .rhosts files...
        20:40> Checking .netrc files...
        20:40> Checking ttytab, securetty, and login configuration files...
        20:40> Checking PATH settings...
        20:40> Checking anonymous ftp setup...
        20:40> Checking mail aliases...
        20:40> Checking cron entries...
        20:40> Checking 'inetd' configuration...
        20:40> Checking 'tcpd' configuration...
        20:40> Checking 'services' configuration...
        20:40> Checking NFS export entries...
        20:40> Checking permissions and ownership of system files...
        --CONFIG-- [con010c] Filesystem 'devtmpfs' used by 'none' is not recognised as a valid filesystem
        20:40> Checking for indications of break-in...
        --CONFIG-- [con010c] Filesystem 'devtmpfs' used by 'none' is not recognised as a valid filesystem
        20:40> Performing rootkit checks...
        20:41> Performing system specific checks...
        20:44> Performing root directory checks...
        20:44> Checking for secure backup devices...
        20:44> Checking for the presence of log files...
        20:44> Checking for the setting of user's umask...
        20:44> Checking for listening processes...
        20:44> Checking SSHD's configuration...
        20:44> Checking the printers control file...
        20:44> Checking ftpusers configuration...
        20:44> Checking NTP configuration...
        20:44> Waiting for filesystems scans to complete...
        20:44> Filesystems scans completed...
        20:44> Performing check of embedded pathnames...
        20:45> Security report completed for terminus.
        Security report is in `/var/log/tiger/security.report.terminus.110307-20:38'.

Para [evitar el aviso][]:

    –CONFIG– [con010c] Filesystem 'devtmpfs' used by 'none' is not recognised as a valid filesystem

editamos el fichero de configuración, `/etc/tiger/tigerrc`, y añadimos
el sitema de ficheros `devtmpfs` como válido. Para esto buscamos la
clave `Tiger_FSScan_Local` y la modificamos:

    Tiger_FSScan_Local='devtmpfs'

logwatch
--------

`logwatch` analiza los _logs_ del sistema y nos envía un repote de las
áreas a analizar que le especifiquemos. Se ejecuta diariamente. Podemos
configurar el correo al que envía los reportes dándole un valor a la
variable de entorno `MAILTO`. Añadimos la siguiente línea al fichero
`/etc/bash.bashrc`:

    MAILTO=user@localhost

Para probar el funcionamiento ejecutamos:

    $ /usr/sbin/logwatch --debug 10

logcheck
--------

`logcheck`, otro analizador de _logs_. Es posible que empecemos a
[recibir demasiados mensajes][] debido a la sincronización de `ntp`,
pero podemos configurarlo para que los ignore. El fichero de
configuración está en `/etc/logcheck/logcheck.conf`.

<a name="servicios" title="servicios"></a>
[1] Podemos encontrar una lista de los servicios más comunes en el
fichero `/etc/services`.

  [securizar Ubuntu Maverick Meerkat]: http://dzulkifli.com/index.php?option=com_content&view=article&id=109:securing-maverick-meerkat&catid=35:ubuntu&Itemid=85
    "securizar Ubuntu Maverick Meerkat"
  [1]: #servicios "servicios"
    "1"
  [evitar el aviso]: http://blogs.unbolt.net/index.php/brinley/2010/08/07/filesystem-devtmpfs-used-by-none-is-not-recognised-as-a-valid-filesystem
    "evitar el aviso"
  [recibir demasiados mensajes]: {filename}/admin/kernel-time-sync-status-change.md
    "kernel time sync status change in logcheck"
  [un usuario inicia sesión en el sistema]: {filename}/admin/la-guardiana-de-la-puerta.md
    "enviarnos un correo electrónico cada vez que un usuario inicia sesión"
