Title: Dyndns e inadyn
Date: 2010-12-11 03:29
Author: Nacho Cano
Tags: dyndns, inadyn, terminus
Slug: dyndns-e-inadyn

[Dyndns][] no hace mucho que cambió su política de servicios, reduciendo
el número de direcciones gratuitas que se podían gestionar con una
cuenta de usuario de 5 a 2, y reduciendo también el número de dominios
entre los que escoger.

![Karpoke]({static}/extra/favicon.ico)

Sin embargo, si antes de que cambiaran la política ya teníamos más de 2
direcciones o eran de dominios que ya no están disponibles, podremos
seguir conservándolos mientras sigan siendo utilizados, es decir,
mientras se siga actualizando regularmente la IP a la que deben apuntar,
como mínimo una vez al mes. Si actualmente usamos la dirección no hay
problema, ya se encarga el router o el cliente de escritorio de
actualizarla. Pero si tenemos alguna dirección que no estamos utilizando
pero que queremos conservar y tenemos más de 2 direcciones en nuestra
cuenta, corremos el peligro de que se nos pase y la perdamos.

Una forma de evitar esto es utilizar el comando `inadyn`, que permite
actualizar la IP de la dirección que especifiquemos. Para poder
incluirlo en el `cron`, lo mejor será crear un pequeño _script_, de tal
manera que nuestra contraseña no quede registrada en ningún fichero de
_log_ (como sí quedaría si pusíeramos el comando directamente en el
`crontab`):

    /usr/sbin/inadyn -u user -p pass --iterations 1 --dyndns_system custom@dyndns.org -a terminus.ignaciocano.com -a anacreonte.homelinux.com

Podemos añadir tantos subdominios como queramos, o tengamos, precedidos
del argumento `-a`.

  [Dyndns]: http://free.domain.name/
    "Dyndns"
