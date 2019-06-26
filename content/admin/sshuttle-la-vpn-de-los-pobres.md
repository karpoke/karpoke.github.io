Title: sshuttle, la VPN de los pobres
Date: 2013-10-20 21:03
Author: Nacho Cano
Tags: dns, proxy, ssh, sshuttle, tunnel, vpn
Slug: sshuttle-la-vpn-de-los-pobres
Related: saltandonos-el-portal-cautivo-de-una-biblioteca,conectar-de-forma-segura-en-redes-abiertas-con-android-connectbot-y-proxydroid,conectar-a-un-servidor-ssh-desde-android-mediante-connectbot-utilizando-claves,cifrando-el-trafico-dns,utilizar-ssh-para-establecer-un-servidor-proxy-socks,tunel-ssh-inverso,ssh-over-http-proxy

[shuttle][] es una herramienta que nos permite redirigir todo el tráfico
a través de una conexión SSH, incluyendo las peticiones DNS. Está
disponible tanto en los repositorios como en GitHub.

Su uso es sencillo. Para establecer la conexión:

```bash
$ sshuttle --D --pidfile=/tmp/sshuttle.pid -r user@server:1234 --dns 0/0
```

Para terminarla:

```bash
$ kill $(cat /tmp/sshuttle.pid)
```

  [shuttle]: https://github.com/apenwarr/sshuttle
    "shuttle"
