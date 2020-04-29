Title: Extraer un archivo de un archivo comprimido, desde el terminal
Date: 2011-06-30 20:36
Author: Nacho Cano
Tags: copia de seguridad, ssh, sudo, tar, tee, vim, wtf
Slug: extraer-un-archivo-de-un-archivo-comprimido-desde-el-terminal

Un día estás editando un archivo en un servidor remoto, [por `ssh`][por ssh],
y, a la hora de guardar, te das cuenta de que has editado el fichero sin
tener los privilegios suficientes, por lo que `vim` se queja:

    E505: "app.config" is read-only (add ! to override)

La solución es sencilla, para guardarlo como `root` escribes:

    :w !sudo tee %

O eso creías. De repente, te das cuenta de que eso no es lo que has
escrito, porque `vim` se ha puesto en modo _inferno_, y cada tecla que
pulsas le da vida propia, porque hace exactamente lo que le dices que
haga y no lo que realmente quieres que haga, y cuando pasa la tormenta y
vuelves a editar el fichero, sólo contiene:

    :wq

WTF!

No pasa nada, tienes copias de seguridad. Una vez que encuentras la
copia, `backup.tgz`, quieres buscar el fichero en cuestión:

    $ tar tvf backup.tgz | grep app.config
    -rw-r--r-- user/user          10458 2011-06-30 13:11 home/user/projects/django/projectname/myapp/app.config

Para descomprimir únicamente ese fichero:

    $ tar xvzf backup.tgz home/user/projects/django/projectname/myapp/app.config
    home/user/projects/django/projectname/myapp/app.config

Si no queremos que nos cree todos esos directorios intermedios, podemos
usar el argumento `-O`, que vuelca el contenido a la salida estándar:

    $ tar xvzf backup.tgz home/user/projects/django/projectname/myapp/app.config -O | tee app.config

  [por ssh]: {filename}/admin/compartiendo-una-conexion-por-ssh.md
    "compartiendo una conexión por ssh"
