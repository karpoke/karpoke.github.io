Title: Configurar sSMTP para enviar correo mediante GMail desde el terminal
Date: 2012-01-14 13:50
Author: Nacho Cano
Tags: bsd-mailx, cabeceras SMTP, gmail, mail, sendmail, sSMTP
Slug: configurar-ssmtp-para-enviar-correo-mediante-gmail-desde-el-terminal
Related: copia-de-seguridad-de-gmail-con-getmail

Con esta receta, podremos enviar correos electrónicos desde el terminal
sin necesidad de tener instalado un servidor de correo, simplemente
utilizando una cuenta de GMail y  sSMTP, que se encuentra en los
repositorios. Esta opción puede estar bien para enviar correos desde un
sistema que utilizamos sólo nosotros, pero no es un sustituto de un
servidor de correo como Sendmail, Exim o Postfix.

Para configurarlo, editamos el fichero `/etc/ssmtp/ssmtp.conf` y
añadimos las siguientes líneas al final del mismo:

    AuthUser=johndoe@gmail.com
    AuthPass=SGsA97wdhA92Dd
    FromLineOverride=YES
    mailhub=smtp.gmail.com:587
    UseSTARTTLS=YES
    UseTLS=YES

Hay que tener en cuenta que nuestra contraseña está escrita en texto
plano, y que cualquier persona con privilegios de administrador, o que
esté usando nuestra cuenta, tendría acceso a ella.

Lo siguiente será parar `sendmail`, deshabilitarlo y sustituirlo por
`ssmtp`:

    $ sudo service sendmail stop
    $ sudo chkconfig sendmail off
    $ sudo mv /usr/sbin/sendmail{,.bak}
    $ sudo ln -s /usr/sbin/ssmtp /usr/sbin/sendmail

Si quisiéramos recuperar `sendmail`, deberemos realizar los pasos en
orden inverso:

    $ sudo mv /usr/bin/sendmail{.bak,}
    $ sudo chkconfig sendmail on
    $ sudo service sendmail start

Para probarlo, basta ejecutar:

    $ echo "Lorem ipsum" | mail -s "Lorem" johndoe@gmail.com

Si nos sale que no reconoce el comando `mail`, podemos instalar el
paquete `bsd-mailx`.

Si tenemos alguna aplicación que nos envía un correo local, a un usuario
del sistema, éste no será accesible y la cuenta de GMail desde la que
enviamos el correo recibirá un notificación de envío fallido.

GMail incluye en los mensajes las siguiente cabeceras:

    Received: by 10.216.138.89 with SMTP id z67mr1808982wei.10.1328051201592;
           Tue, 31 Jan 2012 15:06:41 -0800 (PST)
    Return-Path:
    Received: from myhostname (21.48.29.25.dynamic.ip.es. [25.29.48.21])
           by mx.google.com with ESMTPS id n5sm67537993wiw.7.2012.01.31.15.06.38
           (version=TLSv1/SSLv3 cipher=OTHER);
           Tue, 31 Jan 2012 15:06:40 -0800 (PST)
    Message-ID: <4f287400.e54cb40a.54de.ffff801c@mx.google.com>
    Received: by myhostname (sSMTP sendmail emulation); Wed, 01 Feb 2012 00:06:36 +0100

Podemos ver que en las cabeceras `Received` se incluye el nombre de
nuestro equipo, la IP que teníamos y el nombre del MTA que hemos
utilizado, `sSMTP`, por lo que el receptor tiene información acerca de
quién envió el correo.

Referencias
-----------

» [How To Use Gmail Account To Relay Email From a Shell Prompt][] | Via
[L'home dibuixat][]

  [How To Use Gmail Account To Relay Email From a Shell Prompt]: http://www.cyberciti.biz/tips/linux-use-gmail-as-a-smarthost.html
    "How To Use Gmail Account To Relay Email From a Shell Prompt"
  [L'home dibuixat]: http://caballe.cat/wp/truc-configurar-linux-per-enviar-els-missatges-directament-via-gmail/
    "L'home dibuixat"
