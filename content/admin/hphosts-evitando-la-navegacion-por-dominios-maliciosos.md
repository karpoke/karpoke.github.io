Title: hpHosts, evitando la navegación por dominios maliciosos
Date: 2012-06-21 21:03
Author: Nacho Cano
Tags: CRLF, dominios maliciosos, firma, gpg, hosts, pgp, phishing, scammer, spam, tee, tr
Slug: hphosts-evitando-la-navegacion-por-dominios-maliciosos
Related: encontrar-los-dominios-que-comparten-ip-con-otro-dado

Cuando navegamos por Internet, no somos conscientes de muchas de las
conexiones a diferentes dominios que se están llevando a cabo. Desde
páginas web que cargan o envían datos a otros dominios nada más
visitarlas, hasta casos de _phishing_ o conexiones realizadas por virus
o troyanos.

hpHosts es un proyecto que mantiene una recopilación de dominios cuyo
contenido es malicioso, suplanta a otro (_phishing_), busca estafarnos o
está relacionado con _spam_.

Incluyendo esta recopilación en nuestro fichero `/etc/hosts` nos
aseguramos de que si una página quiere acceder a alguno de estos
dominios no lo consiga, ya que se consulta el archivo `/etc/hosts` antes
de hacer una resolución de dominio.

Descargamos el archivo y lo descomprimimos:

```bash
$ wget http://support.it-mate.co.uk/downloads/hphosts.zip
$ md5sum hphosts.zip
85b34ff1f7803bf6e4a314eaa4f02ac8
$ unzip -d hphosts hphosts.zip
$ cd hphosts
```

El fichero comprimido, además del archivo `HOSTS.txt`, contiene la
licencia de usuario, un fichero con información relativa al proyecto y
una firma PGP del fichero `HOSTS.txt`.

Comprobamos la firma:

```bash
$ gpg --verify HOSTS.txt.sig HOSTS.txt
gpg: Firmado el dom 20 may 2012 21:35:05 CEST usando clave DSA ID 155DA479
gpg: Imposible comprobar la firma: Clave pública no encontrada
```

Si no puede comprobar la firma porque no tenemos la clave, la
importamos:

```bash
$ gpg --recv-keys 155DA479
gpg: solicitando clave 155DA479 de hkp servidor keys.gnupg.net
gpg: clave 155DA479: clave pública "Steven Burn " importada
gpg: Cantidad total procesada: 1
gpg:               importadas: 1
```

Volvemos a comprobar la firma del fichero `HOSTS.txt`:

```bash
$ gpg --verify HOSTS.txt.sig HOSTS.txt
gpg: Firmado el dom 20 may 2012 21:35:05 CEST usando clave DSA ID 155DA479
gpg: Firma correcta de ;`Steven Burn ;'
gpg: AVISO: ¡Esta clave no está certificada por una firma de confianza!
gpg:          No hay indicios de que la firma pertenezca al propietario.
Huellas dactilares de la clave primaria: ECF9 1962 5929 2940 0501  1170 D0D4 353E 155D A479
```

Vemos que la firma es correcta, aunque no esté certificada por una firma
de confianza, por lo que no podríamos asegurar que la firma sea de
Steven Burn, pero sí que la firma del fichero pertenece a esa dirección
de correo electrónico.

En la cabecera del fichero podemos ver la fecha de actualización:

```bash
$ head HOSTS.txt
# hpHosts last updated on:      07/06/2012 01:15
# hpHosts last verified by Steven Burn: 01/06/2012 02:00
#
# IMPORTANT:    Rename this file to "HOSTS" (no .txt extension)
#
# Support:  http://mysteryfcm.co.uk/?mode=contact
#       http://forum.hosts-file.net
#
# Download: http://hosts-file.net/?s=Download
# Mirrors:  http://hosts-file.net/?s=Help#dlmirrors
```

Si tenemos curiosidad, podemos ver que en el archivo hay más de 180K
dominios:

```bash
$ grep -c ^127.0.0.1 HOSTS.txt
186434
```

Por último, adjuntamos el contenido del fichero `HOSTS.txt` a nuestro
`/etc/hosts`, eliminando antes los retornos de carro `\r` que contiene
(para que no aparezcan como `^M` cuando lo editamos con `vim`, por
ejemplo):

```bash
$ tr -d '\r' < HOSTS.txt | sudo tee -a /etc/hosts >/dev/null
```

Podemos saber si un sitio ha sido incluido en la lista consultando el
[catálogo][], o utilizando directamente la siguiente URL:
`http://hosts-file.net/?s=URL`, por ejemplo:
<http://hosts-file.net/?s=www.stackoverflow.com>. Y si queremos [saber
el motivo][], en esta otra.

Referencias
-----------

» [http://hosts-file.net][]
» [Protección a nivel local, archivo hosts][]

  [catálogo]: http://hosts-file.net/?s=Browse
    "catálogo"
  [saber el motivo]: http://hosts-file.net/?s=classifications
    "saber el motivo"
  [http://hosts-file.net]: http://hosts-file.net/
    "http://hosts-file.net"
  [Protección a nivel local, archivo hosts]: http://www.flu-project.com/proteccion-a-nivel-local-archivo-hosts.html
    "Protección a nivel local, archivo hosts"
