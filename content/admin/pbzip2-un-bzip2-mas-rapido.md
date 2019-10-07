Title: pbzip2, un bzip2 más rápido
Date: 2012-06-13 18:43
Author: Nacho Cano
Tags: bzip2, compresión de archivos, pbzip2
Slug: pbzip2-un-bzip2-mas-rapido

`pbzip2`, de _parallel bzip2_, permite aprovechar toda la potencia de
los procesadores con más de un núcleo a la hora de comprimir o
descomprimir, cosa que `bzip2` no hace.

Instalación
-----------

En Ubuntu se encuentra disponible en los repositorios:

```bash
$ sudo aptitude install pbzip2
```

Su uso es idéntico al de `bzip2`, por lo que podemos añadir un _alias_ a
`~/.bash_aliases`:

```bash
alias bzip2=pbzip2
```

Referencias
-----------

» [Speed Up Compression via Parallel BZIP2 (PBZIP2)][]

  [Speed Up Compression via Parallel BZIP2 (PBZIP2)]: http://hackercodex.com/guide/parallel-bzip-compression/
    "Speed Up Compression via Parallel BZIP2 (PBZIP2)"
