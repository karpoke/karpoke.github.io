Title: Sa Nostra y SSL
Date: 2010-10-25 11:50
Author: Nacho Cano
Tags: banca en línea, openssl, ssl
Slug: sa-nostra-y-ssl

Leyendo la comparativa de [SbD][] sobre el uso de SSL por parte de los
bancos online, estos son los resultados de Sa Nostra:

URL: https://linea.sanostra.es

Verificación SSLv2
------------------

Comando:

    $ openssl s_client -ssl2 -connect linea.sanostra.es:443

Bien: no da soporte

Tipo de certificado (Normal/EV)
-------------------------------

Esto lo podemos comprobar a través del navegador.
Mal: Tiene un certificado SSL sin Validación Extendida.

Longitud de la clave RSA del certificado
----------------------------------------

Comando:

    $ openssl s_client -connect linea.sanostra.es:443

Mal: La clave es de 1024 bits.

Soporte de algoritmos débiles
-----------------------------

Comando:

    $ openssl s_client  -cipher LOW:EXP -connect linea.sanostra.es:443

Bien: No admite algoritmos 'débiles', cuya longitud de clave sea de 56 ó
64 bits.

Puntuación final: Aprobado

  [SbD]: http://www.securitybydefault.com/2010/10/bancos-y-ssl-quien-aprueba.html
    "SbD"
    "SbD"
