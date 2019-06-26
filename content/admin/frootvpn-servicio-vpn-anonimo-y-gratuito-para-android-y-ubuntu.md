Title: FrootVPN, servicio VPN anónimo y gratuito para Android y Ubuntu
Date: 2014-11-14 13:02
Author: Nacho Cano
Tags: android, anonimato, frootvpn, https, nameserver, network-manager, openvpn, privacidad, resolv.conf, resolvconf, ubuntu, vpn
Slug: frootvpn-servicio-vpn-anonimo-y-gratuito-para-android-y-ubuntu
Related: sshuttle-la-vpn-de-los-pobres,conectar-de-forma-segura-en-redes-abiertas-con-android-connectbot-y-proxydroid,robando-la-identidad-del-vecino

[FrootVPN][] es un servicio VPN que se anuncia enfocado a preservar la
privacidad y el anonimato, a la par que gratuito. Mediante el uso de un
servicio como éste, podremos conectarnos a Internet de forma segura y
anónima desde sitios que pudieran no serlo, por ejemplo, redes abiertas
que no usan cifrado, servicios que restringen el acceso por país, países
que censuran la libertad de expresión o el acceso a la cultura, etc.

Por supuesto, dado que todo nuestro tráfico irá a través de un tercero,
no estaría demás tomar medidas adicionales como usar HTTPS, o no acceder
en la medida de lo posible a servicios delicados como banca electrónica.

El primer paso antes de configurar nuestro PC o móvil es crear una
cuenta en su web.

Android
-------

[Conectar desde Android][] es tan sencillo como crear una conexión VPN
nueva. Vamos al menú Ajustes > Más > VPN > Añadir, y rellenamos los
datos:

|Parámetro               |Valor                |
|------------------------|---------------------|
|Tipo                    |L2TP/IPSec PSK       |
|Dirección del servidor  |se-vpn.frootvpn.com  |
|Clave compartida        |frootvpnsecret       |

Le damos a conectar e introducimos nuestro usuario y contraseña.

Ubuntu
------

[Conectar desde Ubuntu][] es casi tan sencillo como en Android. Antes
que nada, comprobamos que tenemos instalamos el paquete `openvpn`,
disponible en los repositorios.

Descargarmaos el fichero de configuración desde su página:

```bash
$ wget https://www.frootvpn.com/files/frootvpn.ovpn
$ sudo mv frootvpn.ovpn /etc/openvpn/
```

Y nos conectamos simplemente ejecutando:

```bash
$ sudo openvpn --config /etc/openvpn/frootvpn.ovpn
```

Si tuviéramos problemas al conectar a alguna web, añadir la siguiente
línea en el fichero `/etc/resolv.conf` (o en
`/etc/resolvconf/resolv.conf.d/base` si usamos `resolvconf`) podría
servir:

```bash
nameserver 80.67.0.2
```

### Configurar FrootVPN con Network Manager

Si utilizamos `NetworkManager` y queremos configurar la conexión a
través de él, nos encontraremos que crear la conexión importando el
fichero de configuración que nos hemos descargado no nos funciona.

Si ni siquiera nos aparece la opción de configurar redes VPN, deberemos
instalar el paquete `network-manager-openvpn`.

Para que nos funcione la conexión desde `NetworkManager`, primero
creamos el fichero `/etc/openvpn/frootvpn.crt` y en él copiamos los
certificados que están contenidos en `frootvpn.ovpn`:

```bash
$ sudo su
# cp /etc/openvpn/frootvpn.{ovpn,crt}
# sed -n '/-----BEGIN/,/-----END/p' /etc/openvpn/frootvpn.crt | sponge /etc/openvpn/frootvpn.crt
```

Después, vamos al menú de gestión de redes > Conexiones VPN >
Configurar VPN > Añadir > Importar una configuración VPN guardada, y
seleccionamos el fichero que nos hemos descargado.

En la pantalla de configuración, cambiaremos:

-   el tipo de autenticación: contraseña
-   pondremos nuestro usuario y contraseña
-   en el certificado CA seleccionaremos el fichero
    `/etc/openvpn/frootvpn.crt`

Y ya está.

Referencias
-----------

- [frootvpn.com][FrootVPN]
- Ernesto | [Which VPN services take your anonymity seriously? 2014 edition][]
- [PPTP vs L2TP/IPSEC vs OpenVPN][]

  [FrootVPN]: https://www.frootvpn.com/
    "FrootVPN"
  [Conectar desde Android]: https://www.frootvpn.com/guides/android-20.html
    "Conectar desde Android"
  [Conectar desde Ubuntu]: https://www.frootvpn.com/guides/linuxdebian-19.html
    "Conectar desde Ubuntu"
  [Which VPN services take your anonymity seriously? 2014 edition]: https://torrentfreak.com/which-vpn-services-take-your-anonymity-seriously-2014-edition-140315/
    "Which VPN services take your anonymity seriously? 2014 edition"
  [PPTP vs L2TP/IPSEC vs OpenVPN]: https://www.ivpn.net/pptp-vs-l2tp-vs-openvpn
    "PPTP vs L2TP/IPSEC vs OpenVPN"
