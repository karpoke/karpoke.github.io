Title: Descifrando al César en Bash
Date: 2011-02-16 04:26
Author: Nacho Cano
Tags: cifrado césar, rot13, rot47, sed, tr, bsdgames
Slug: descifrando-al-cesar-en-bash

Después de ver cómo se [descifra al César en Python][], me he encontrado
con un par de maneras elegantes de hacerlo desde Bash.


Cifrado César
-------------

Con `tr`:

```bash
$ echo "lorem ipsum dolor sit amet" | tr 'a-z' 'd-za-c'
oruhp lsvxp groru vlw dphw
$ echo "oruhp lsvxp groru vlw dphw" | tr 'd-za-c' 'a-z'
lorem ipsum dolor sit amet
```

Con `sed` también se puede conseguir, aunque es bastante más laborioso:

```bash
$ echo "lorem ipsum dolor sit amet" | sed -e "y/abcdefghijklmnopqrstuvwxyz/defghijklmnopqrstuvwxyzabc/"
oruhp lsvxp groru vlw dphw
$ echo "oruhp lsvxp groru vlw dphw" | sed -e "y/abcdefghijklmnopqrstuvwxyz/defghijklmnopqrstuvwxyzabc/"
lorem ipsum dolor sit amet
```

ROT13
-----

Con `tr`:

```bash
$ echo "lorem ipsum dolor sit amet" | tr 'a-zA-Z' 'n-za-mN-ZA-M'
yberz vcfhz qbybe fvg nzrg
$ echo "yberz vcfhz qbybe fvg nzrg" | tr 'n-za-mN-ZA-M' 'a-zA-Z'
lorem ipsum dolor sit amet
```

Por supuesto, con `rot13`, incluido en el paquete `bsdgames`:

```bash
$ rot13 "lorem ipsum dolor sit amet"
yberz vcfhz qbybe fvg nzrg
$ rot13 "yberz vcfhz qbybe fvg nzrg"
lorem ipsum dolor sit amet
```

ROT47
-----

Con `tr`:

```bash
$ echo "lorem ipsum dolor sit amet" | tr '!-~' 'P-~!-O'
=@C6> :ADF> 5@=@C D:E 2>6E
$ echo "=@C6> :ADF> 5@=@C D:E 2>6E" | tr 'P-~!-O' '!-~'
lorem ipsum dolor sit amet
```

  [descifra al César en Python]: {filename}/dev/descifrando-al-cesar-en-python.md
    "descifra al César en Python"
