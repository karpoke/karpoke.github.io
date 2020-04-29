Title: La contraseña del presidente Obama
Date: 2011-12-01 22:28
Author: Nacho Cano
Tags: cracking, findmyhash, hash, md5, md5sum
Slug: la-contrasena-del-presidente-obama
Related: encuentra-el-hash

En un _tweet_ de [@AnonNewsSource][] han publicado el usuario y el
_hash_ de la contraseña de Obama:

> Obama WEB http://whitehouse.gov barack.obama@whitehouse.gov / PASS:
> 6289c5975815012768aefbf9a8d2fd3e / LOGIN: bobama PHONE +1 202-456-1111

Podemos utilizar el _script_ [findmyhash.py][] para ver si encuentra la
contraseña asociada a ese _hash_:

    $ python findmyhash.py md5 -h "6289c5975815012768aefbf9a8d2fd3e" -g

    Cracking hash: 6289c5975815012768aefbf9a8d2fd3e

    Analyzing with joomlaaa (http://joomlaaa.com)...
    ... hash not found in joomlaaa

    Analyzing with md5-lookup (http://md5-lookup.com)...
    ... hash not found in md5-lookup

    Analyzing with md5.com.cn (http://md5.com.cn)...

    __*** HASH CRACKED!! ***__
    The original string is: 80412999


    The following hashes were cracked:
    ----------------------------------

    6289c5975815012768aefbf9a8d2fd3e -> 80412999

Via [segu-info.com.ar][]

  [@AnonNewsSource]: http://twitter.com/#!/AnonNewsSource/status/141733919501467649
    "@AnonNewsSource"
  [findmyhash.py]: {filename}/hack/encuentra-el-hash.md
    "Encuentra el hash"
  [segu-info.com.ar]: http://blog.segu-info.com.ar/2011/12/usuario-y-contrasena-de-barack-obama.html
    "segu-info.com.ar"
