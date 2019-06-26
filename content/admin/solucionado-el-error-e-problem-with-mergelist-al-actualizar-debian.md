Title: Solucionado el error "E: Problem with MergeList" al actualizar Debian
Date: 2011-03-17 11:11
Author: Nacho Cano
Tags: almacén de paquetes, aptitude, debian, mergelist, sid, update, wheezy
Slug: solucionado-el-error-e-problem-with-mergelist-al-actualizar-debian

Tras realizar una actualización rutinaria, `aptitude update`, me
encuentro con el siguiente error:

```bash
E: Encountered a section with no Package: header
E: Problem with MergeList /var/lib/apt/lists/ftp.caliu.cat_debian_dists_testing_main_binary-i386_Packages
E: No se pudieron analizar o abrir las listas de paquetes o el archivo de estado.
E: No se pudo reconstruir el almacén de paquetes
```

![Deb packages]({static}/images/icono-paquete-deb.png)

La [solución][] para resolver el conflicto, que parece ser debido a una
corrupción en las listas, pasa por borrarlas, y ya podremos actualizar
normalmente:

```bash
$ sudo rm -fr /var/lib/apt/lists/*
```

  [solución]: http://ubuntuforums.org/archive/index.php/t-863742.html
    "solución"
