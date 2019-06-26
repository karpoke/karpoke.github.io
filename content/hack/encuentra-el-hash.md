Title: Encuentra el hash
Date: 2011-09-30 00:27
Author: Nacho Cano
Tags: cisco7, cracking, cut, hash, lm, md4, md5, md5sum, mysql, ntlm, open source, python, rmd160, script, sha1, sha256
Slug: encuentra-el-hash

Existen herramientas que permiten romper un _hash_, aunque a veces puede
ahorrar tiempo y recursos [buscar si el _hash_ ya ha sido encontrado][].
Ni siquiera hace falta una _rainbow table_.

`findmyhash` es un _script_ escrito en Python que puede buscar
diferentes tipos de _hash_ en diferentes servicios de _cracking online_.
Los algoritmos soportados son los siguientes:

-   MD4
-   MD5
-   SHA1
-   SHA256
-   RMD160
-   MYSQL
-   CISCO7
-   LM
-   NTLM

Un ejemplo sencillo. Si no encuentra el _hash_, también lo buscará en
Google:

```bash
$ hash=$(echo 123456 | md5sum | cut -f1 -d" ")
$ echo $hash
f447b20a7fcbf53a5d5be013ea0b15af
$ ./findmyhash.py MD5 -h $hash -g
[...]
Analyzing with noisette.ch (http://md5.noisette.ch)...

__*** HASH CRACKED!! ***__
The original string is: 123456



The following hashes were cracked:
----------------------------------

f447b20a7fcbf53a5d5be013ea0b15af -> 123456
```

Otro ejemplo, esta vez con [las 20 contraseñas más utilizadas][]:

```bash
$ HASH_FILE=$(mktemp)
$ passwords=(
     123456
     12345
     123456789
     Password
     iloveyou
     princess
     rockyou
     1234567
     12345678
     abc123
     Nicole
     Daniel
     babygirl
     monkey
     Jessica
     Lovely
     michael
     Ashley
     654321
     Qwerty
 )
$ for p in ${passwords[*]}; do
     hash=$(echo $p | md5sum | cut -f1 -d" ")
     echo $hash >> $HASH_FILE
done
$ python findmyhash.py MD5 -f $HASH_FILE > hash_results.txt
```

Después de un rato, casi una hora, ha sido capaz de encontrar 6
contraseñas:

```bash
$ grep "The original string" hash_results.txt
The original string is: 123456
The original string is: 12345
The original string is: 12345678
The original string is: abc123
The original string is: Jessica
The original string is: michael
```

La opción para buscar en Google, en caso de no encuentrar el _hash_ en
ninguno de esos servicios _online_, sólo está disponible si buscamos un
único _hash_, así que modificaremos ligeramente el _script_ anterior
para que, en lugar de pasarle un fichero con los _hashes_, vayamos
llamando al _script_ de uno en uno:

```bash
$ passwords=(
     123456
     12345
     123456789
     Password
     iloveyou
     princess
     rockyou
     1234567
     12345678
     abc123
     Nicole
     Daniel
     babygirl
     monkey
     Jessica
     Lovely
     michael
     Ashley
     654321
     Qwerty
 )
$ > hash_results.txt
$ for p in ${passwords[*]}; do
     hash=$(echo $p | md5sum | cut -f1 -d" ")
     python findmyhash.py MD5 -h $hash -g >> hash_results.txt
done
```

La diferencia respecto al caso anterior es que, para los _hashes_ que no
ha encontrado en ningún servicio, realiza una búsqueda en Google y
muestra los primeros enlaces. Por ejemplo, el _hash_ para la contraseña
654321 no ha sido capaz de encontrarlo, pero la búsqueda en Google,
entre otras, ha proporcionado la URL http://paste2.org/p/1360449, que sí
la contiene.

  [buscar si el _hash_ ya ha sido encontrado]: http://www.pentestit.com/findmyhash/
    "buscar si el _hash_ ya ha sido encontrado"
  [las 20 contraseñas más utilizadas]: http://blog.zonealarm.com/2011/01/securing-yourself-from-a-world-of-hackers.html
    "las 20 contraseñas más utilizadas"
