Title: chmod sin chmod
Date: 2014-11-08 19:54
Author: Nacho Cano
Tags: chmod
Slug: chmod-sin-chmod
Related: ls-sin-ls

Durante la desventura de pasar de 32 a 64 bits, tuve el placer de quedarme sin
poder ejecutar ningún binario, ya que estos se habían sobreescrito por sus
versiones compiladas para la arquitectura de 64 bits mientras aún continuaba
con la de 32.

Ni `ls`, ni `rm`, ni `mv`, ni `cp`, ni `dpkg`... nada. Ni tampoco USB, ni
`ssh`, y no podía reiniciar aún; un entorno idílico, vamos. El tema está en
que, en un momento dado, necesité hacer uso de las versiones compiladas para 32
bits. Pude descargar aquellos binarios que necesitaba, pero no tenían permisos
de ejecución y tampoco podía usar `/bin/chmod`. Por suerte, ya había alguien
que se había imaginado un [escenario sin `chmod`][escenario sin chmod] y había
recopilado toda una serie de alternativas. Ésta es la que yo usé:

```bash
$ /lib/ld-linux.so.2 ~/chmod +x ~/rm
```

En 64 bits, el comando sería ligeramente diferente:

```bash
$ /lib64/ld-linux-x86-64.so.2 /bin/chmod +x /bin/chmod
```

  [escenario sin chmod]: http://www.slideshare.net/cog/chmod-x-chmod
    "escenario sin chmod"
