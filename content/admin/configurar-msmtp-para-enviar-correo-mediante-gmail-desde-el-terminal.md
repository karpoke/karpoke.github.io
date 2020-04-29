Title: Configurar msmtp para enviar correo mediante GMail desde el terminal
Date: 2014-06-04 23:13
Author: Nacho Cano
Tags: bsd-mailx, gmail, msmtp, mta, sendmail, smtp, ssmtp
Slug: configurar-msmtp-para-enviar-correo-mediante-gmail-desde-el-terminal
Related: configurar-ssmtp-para-enviar-correo-mediante-gmail-desde-el-terminal,copia-de-seguridad-de-gmail-con-getmail

Otra alternativa para enviar correos electrónicos desde el terminal sin
necesidad de tener instalado un servidor de correo. Su configuración es
incluso más sencilla que con [ssmtp][]. Si tenemos instalado `ssmtp`
deberemos desinstalarlo para poder instalar `msmtp`.


Instalamos `mstmp-mta`
----------------------

Instalamos el paquete `msmtp-mta` desde los repositorios y editamos el
fichero de configuración `~/.msmtprc`:

    defaults
    logfile ~/msmtp.log

    account gmail
    auth on
    host smtp.gmail.com
    from example@gmail.com
    auth on
    tls on
    tls_trust_file /usr/share/ca-certificates/mozilla/Equifax_Secure_CA.crt
    user example@gmail.com
    password secret
    port 587

    account default : gmail

Le cambiamos los permisos:

    $ chmod 600 ~/.msmtprc

Instalamos `mailx`
------------------

Utilizaremos el comando `mail` del paquete `bsd-mailx`, también
disponible en los repositorios. (También serviría el comando del mismo
nombre pero del paquete `heirloom-mailx`.)

Ya podemos probarlo:

    echo Lorem impsum dolor | mail -s Subject to@example.com

Referencias
-----------

» [Send Gmail from the Linux Command Line][]

  [ssmtp]: {filename}/admin/configurar-ssmtp-para-enviar-correo-mediante-gmail-desde-el-terminal.md
    "Configurar ssmtp para enviar correo mediante GMail desde el terminal"
  [Send Gmail from the Linux Command Line]: http://tuxtweaks.com/2012/10/send-gmail-from-the-linux-command-line/
    "Send Gmail from the Linux Command Line"
