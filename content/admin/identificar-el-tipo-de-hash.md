Title: Identificar el tipo de hash
Date: 2012-05-15 01:29
Author: Nacho Cano
Tags: fingerprinting, hash, hash_id, md5, sha1, sha2
Slug: identificar-el-tipo-de-hash
Related: encuentra-el-hash,la-contrasena-del-presidente-obama

El _script_ `Hash_ID.py`, desarrollado por Zion3R, nos permite
identificar los posibles algoritmos utilizados para crear un _hash_. En
muchas ocasiones no se puede saber qué algoritmo concreto se ha
utilizado, pero nos devolverá una lista de candidatos.

El _script_ compara el _hash_ con el tipo de _hash_ de algoritmos tales
como: ADLER-32, CRC-32, CRC-16, DES(Unix), FCS-16, GHash-32-5, GOST R
34.11-94, Haval-160, Haval-192 110080, Haval-224 114080, Haval-256,
Lineage II C4, Domain Cached Credentials, XOR-32, MD5(Half),
MD5(Middle), MySQL, MD5(phpBB3), MD5(Unix), MD5(Wordpress), MD5(APR),
MD2, MD4, MD5, MD5(HMAC(Wordpress)), NTLM, RAdmin v2.x, RipeMD-128,
SNEFRU-128, Tiger-128, MySQL5 - SHA-1(SHA-1($pass)), MySQL 160bit -
SHA-1(SHA-1($pass)), RipeMD-160, SHA-1, SHA-1(MaNGOS), Tiger-160,
Tiger-192, md5($pass.$salt) - Joomla, SHA-1(Django), SHA-224,
RipeMD-256, SNEFRU-256, md5($pass.$salt) - Joomla, SAM -
(LM_hash:NT_hash), SHA-256(Django), RipeMD-320, SHA-384, SHA-256,
SHA-384(Django), SHA-512, Whirlpool, etc.

Su uso es sencillo:

    $ python Hash_ID.py
       #########################################################################
       #     __  __                     __           ______    _____           #
       #    /\ \/\ \                   /\ \         /\__  _\  /\  _ `\         #
       #    \ \ \_\ \     __      ____ \ \ \___     \/_/\ \/  \ \ \/\ \        #
       #     \ \  _  \  /’__`\   / ,__\ \ \  _ `\      \ \ \   \ \ \ \ \       #
       #      \ \ \ \ \/\ \_\ \_/\__, `\ \ \ \ \ \      \_\ \__ \ \ \_\ \      #
       #       \ \_\ \_\ \___ \_\/\____/  \ \_\ \_\     /\_____\ \ \____/      #
       #        \/_/\/_/\/__/\/_/\/___/    \/_/\/_/     \/_____/  \/___/  v1.1 #
       #                                                             By Zion3R #
       #                                                    www.Blackploit.com #
       #                                                   Root@Blackploit.com #
       #########################################################################

       -------------------------------------------------------------------------
     HASH: 065764eb3fb9c3bcd271ea8a894981c4

    Possible Hashs:
    [+]  MD5
    [+]  Domain Cached Credentials - MD4(MD4(($pass)).(strtolower($username)))

    Least Possible Hashs:
    [+]  RAdmin v2.x
    [+]  NTLM
    [+]  MD4
    [+]  MD2
    [+]  MD5(HMAC)
    [+]  MD4(HMAC)
    [+]  MD2(HMAC)
    [+]  MD5(HMAC(Wordpress))
    [+]  Haval-128
    [+]  Haval-128(HMAC)
    [+]  RipeMD-128
    [+]  RipeMD-128(HMAC)
    [+]  SNEFRU-128
    [+]  SNEFRU-128(HMAC)
    [+]  Tiger-128
    [+]  Tiger-128(HMAC)
    [+]  md5($pass.$salt)
    [+]  md5($salt.$pass)
    [+]  md5($salt.$pass.$salt)
    [+]  md5($salt.$pass.$username)
    [+]  md5($salt.md5($pass))
    [+]  md5($salt.md5($pass))
    [+]  md5($salt.md5($pass.$salt))
    [+]  md5($salt.md5($pass.$salt))
    [+]  md5($salt.md5($salt.$pass))
    [+]  md5($salt.md5(md5($pass).$salt))
    [+]  md5($username.0.$pass)
    [+]  md5($username.LF.$pass)
    [+]  md5($username.md5($pass).$salt)
    [+]  md5(md5($pass))
    [+]  md5(md5($pass).$salt)
    [+]  md5(md5($pass).md5($salt))
    [+]  md5(md5($salt).$pass)
    [+]  md5(md5($salt).md5($pass))
    [+]  md5(md5($username.$pass).$salt)
    [+]  md5(md5(md5($pass)))
    [+]  md5(md5(md5(md5($pass))))
    [+]  md5(md5(md5(md5(md5($pass)))))
    [+]  md5(sha1($pass))
    [+]  md5(sha1(md5($pass)))
    [+]  md5(sha1(md5(sha1($pass))))
    [+]  md5(strtoupper(md5($pass)))

Si tenemos suerte, podemos [encontrar el _hash_ utilizando
`findmyhash.py`][encontrar el hash utilizando findmyhash.py],
un _script_ para buscar _hashes_ en servicios de
_cracking online_.

Referencias
-----------

» [hash-identifier][]

  [encontrar el hash utilizando findmyhash.py]: {filename}/hack/encuentra-el-hash.md
    "encuentra el hash"
  [hash-identifier]: http://code.google.com/p/hash-identifier/
    "hash-identifier"
