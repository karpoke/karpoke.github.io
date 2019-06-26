Title: etckeeper, control de versiones del directorio /etc
Date: 2012-12-21 16:41
Author: Nacho Cano
Tags: aptitude, bazaar, bzr, control de versiones, cvs, etc, etckeeper, rkhunter
Slug: etckeeper-control-de-versiones-del-directorio-etc
Related: hphosts-evitando-la-navegacion-por-dominios-maliciosos

`etckeeper` permite utilizar una herramienta de control de versiones
para registrar los cambios hechos en los ficheros del directorio `/etc`.
Se pueden utilizar varias herramientas de control de versiones, como
Bazaar, Git, Mercurial o Darcs.

Aunque puede ser de gran ayuda tener un historial de los cambios en los
ficheros del directorio `/etc`, no debemos olvidar que puede que se
estén copiando ficheros que deberían permanecer secretos, como por
ejemplo `/etc/shadow`. Al repositorio sólo puede acceder el
administrador del sistema, pero deberemos tener en cuenta esto si, por
ejemplo, copiamos el repositorio.


Instalación
-----------

En este caso, utilizaremos Bazaar. Instalamos los paquetes necesarios:

```bash
$ sudo aptitude install etckeeper bzr
```

Configuración
-------------

Editamos el fichero `/etc/etckeeper/etckeeper.conf` y comprobamos que la
siguiente línea no está comentada:

```bash
VCS="bzr"
```

Si utilizamos `aptitude`, también podemos modificar el valor de
`HIGHLEVEL_PACKAGE_MANAGER`:

```bash
HIGHLEVEL_PACKAGE_MANAGER=aptitude
```

Inicialización
--------------

Lo primero que hay que hacer antes que nada es inicializar el
repositorio. Ejecutamos:

```bash
$ sudo etckeeper init
```

Del mismo modo, podemos dejar de usar el control de versiones y borrar
toda la información guardada ejecutando:

```bash
$ sudo etckeeper uninit
```

Uso
---

Supongamos que acabamos de [actualizar el fichero `/etc/hosts`][actualizar el fichero /etc/hosts].
Para comprobar los archivos modificados ejecutamos:

```bash
$ sudo bzr status /etc
modified:
  hosts
unknown:
  X11/core
```

Para registrar (_commit_) los cambios ejecutamos:

```bash
$ sudo etckeeper commit "Updated hphosts"
Committing to: /etc/
modificado hosts
Committed revision 2.
```

Comprobar el historial de cambios, podemos especiar un directorio o un
fichero concreto:

```bash
$ sudo bzr log /etc/hosts
------------------------------------------------------------
revno: 2
committer: karpoke
branch nick: localhost /etc repository
timestamp: Fri 2012-12-21 15:28:08 +0100
message:
  Updated hphosts
------------------------------------------------------------
revno: 1
committer: karpoke
branch nick: localhost /etc repository
timestamp: Fri 2012-12-21 15:13:09 +0100
message:
  Initial commit
```

Si queremos revertir los cambios, debemos especificar el número de
versión al que queremos volver. También podemos especificar un
directorio o un fichero:

```bash
$ sudo bzr revert --revision 2 /etc/hosts
```

### Alertas y mensajes de error

`etckeeper` está configurado por defecto para ejecutarse automáticamente
una vez al día y tras cada actualización, instalación o borrado de
paquetes del sistema. En este caso, es posible que, si no hay ningún
cambio en los ficheros de `/etc`, nos aparezca un mensaje de error como
el siguiente:

```bash
bzr: ERROR: No changes to commit. Please 'bzr add' the files you want to commit, or use --unchanged to force an empty commit.
```

Si queremos evitarlo, basta editar la siguiente línea en el fichero de
configuración:

```bash
BZR_COMMIT_OPTIONS="--unchanged"
```

### Avisos de rkhunter

Si tenemos instalado [rkhunter][], podemos añadir las siguientes líneas
al fichero de configuración para evitar que nos lleguen avisos de los
ficheros y directorios utilizados por etckeeper:

```bash
ALLOWHIDDENDIR="/etc/.bzr"
ALLOWHIDDENFILE="/etc/.etckeeper"
ALLOWHIDDENFILE="/etc/.bzrignore"
```

Referencias
-----------

- [Using Version Control For Your /etc Directory With etckeeper And
Bazaar On Debian Squeeze][]

  [actualizar el fichero /etc/hosts]: {filename}/admin/hphosts-evitando-la-navegacion-por-dominios-maliciosos.md
    "hpHosts, evitando la navegación por dominios maliciosos"
  [rkhunter]: {filename}/admin/buscando-rootkits-y-troyanos.md
    "rkhunter"
  [Using Version Control For Your /etc Directory With etckeeper And Bazaar On Debian Squeeze]: http://www.howtoforge.com/using-version-control-for-your-etc-directory-with-etckeeper-and-bazaar-on-debian-squeeze
    "Using Version Control For Your /etc Directory With etckeeper And Bazaar On Debian Squeeze"
