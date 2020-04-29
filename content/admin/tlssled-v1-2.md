Title: TLSSLed v1.2
Date: 2011-10-23 15:45
Author: Nacho Cano
Tags: openssl, script, ssl, tlssled
Slug: tlssled-v1-2
Related: configurar-apache-para-servir-conexiones-seguras,sa-nostra-y-ssl

[TLSSLed][] es un _script_ cuya finalidad es evaluar la seguridad de
SSL/TLS de un servidor web. Se basa en el escáner de SSL/TLS, `sslscan`,
el cual a su vez se basa en la librería `openssl`, y en el comando
openssl s_client. Entre las comprobaciones que realiza se incluyen
comprobar si el servidor soporta SSLv2, cifrado NULL, cifrados débiles
por la longitud de su clave (40 ó 56 bits), la disponibilidad de
cifrados fuertes, como AES, si el certificado está firmado con MD5 y si
permite la renegociación de SSL/TLS.

(Ya está disponible la [versión 1.3][])

Un ejemplo de uso:

    $ TLSSLed_v1.2.sh 127.0.0.1 443
    ------------------------------------------------------
     TLSSLed - (1.2) based on sslscan and openssl
                     by Raul Siles (www.taddong.com)
    ------------------------------------------------------
    + openssl version: OpenSSL 1.0.0e 6 Sep 2011
    + sslscan version 1.8.2
    ------------------------------------------------------

    [-] Analyzing SSL/TLS on 127.0.0.1:443 ..

    [*] The target service 127.0.0.1:443 seems to speak SSL/TLS...


    [-] Running sslscan on 127.0.0.1:443...

    [*] Testing for SSLv2 ...

    [*] Testing for NULL cipher ...

    [*] Testing for weak ciphers (based on key length) ...


    [*] Testing for strong ciphers (AES) ...
        Accepted  SSLv3  256 bits  DHE-RSA-AES256-SHA
        Accepted  SSLv3  256 bits  AES256-SHA
        Accepted  SSLv3  128 bits  DHE-RSA-AES128-SHA
        Accepted  SSLv3  128 bits  AES128-SHA
        Accepted  TLSv1  256 bits  DHE-RSA-AES256-SHA
        Accepted  TLSv1  256 bits  AES256-SHA
        Accepted  TLSv1  128 bits  DHE-RSA-AES128-SHA
        Accepted  TLSv1  128 bits  AES128-SHA

    [*] Testing for MD5 signed certificate ...

    [*] Testing for certificate public key length ...
        RSA Public Key: (2048 bit)

    [*] Testing for certificate subject ...
        Subject: /C=ES/ST=IB/L=Palma de Mallorca/O=Localhost/CN=Localhost/emailAddress=karpoke@localhost

    [*] Testing for certificate CA issuer ...
        Issuer: /C=ES/ST=IB/O=Localhost CA/CN=Localhost/emailAddress=karpoke@localhost

    [*] Testing for certificate validity period ...
        Today: dom oct 23 13:21:35 UTC 2011
        Not valid before: Jun 14 11:26:10 2011 GMT
        Not valid after: Jun 13 11:26:10 2012 GMT

    [*] Checking preferred server ciphers ...
      Prefered Server Cipher(s):
        SSLv3  256 bits  DHE-RSA-AES256-SHA
        TLSv1  256 bits  DHE-RSA-AES256-SHA



    [-] Testing for SSLv3/TLSv1 renegotiation vuln. (CVE-2009-3555) ...

    [*] Testing for secure renegotiation ...
    Secure Renegotiation IS supported


    [-] Testing for TLS v1.1 and v1.2 (CVE-2011-3389 aka BEAST) ...

    [*] Testing for SSLv3 and TLSv1 support first ...
        Accepted  SSLv3  256 bits  DHE-RSA-AES256-SHA
        Accepted  SSLv3  256 bits  AES256-SHA
        Accepted  SSLv3  168 bits  EDH-RSA-DES-CBC3-SHA
        Accepted  SSLv3  168 bits  DES-CBC3-SHA
        Accepted  SSLv3  128 bits  DHE-RSA-AES128-SHA
        Accepted  SSLv3  128 bits  AES128-SHA
        Accepted  SSLv3  128 bits  RC4-SHA
        Accepted  SSLv3  128 bits  RC4-MD5
        Accepted  TLSv1  256 bits  DHE-RSA-AES256-SHA
        Accepted  TLSv1  256 bits  AES256-SHA
        Accepted  TLSv1  168 bits  EDH-RSA-DES-CBC3-SHA
        Accepted  TLSv1  168 bits  DES-CBC3-SHA
        Accepted  TLSv1  128 bits  DHE-RSA-AES128-SHA
        Accepted  TLSv1  128 bits  AES128-SHA
        Accepted  TLSv1  128 bits  RC4-SHA
        Accepted  TLSv1  128 bits  RC4-MD5

    [*] Testing for TLS v1.1 support ...
    The local openssl version does NOT support TLS v1.1

    [*] Testing for TLS v1.2 support ...
    The local openssl version does NOT support TLS v1.2


    [-] Testing for SSL/TLS HTTPS security headers ...

    [*] Testing for Strict-Transport-Security (STS) header ...

    [*] Testing for cookies with the secure flag ...

    [*] Testing for cookies without the secure flag ...


    [-] New files created:
    -rw-rw-r-- 1 karpoke karpoke 9223 2011-10-23 15:21 sslscan_127.0.0.1_443_2011-10-23_151957.log
    -rw-rw-r-- 1 karpoke karpoke 2796 2011-10-23 15:21 openssl_HEAD_127.0.0.1_443_2011-10-23_151957.log
    -rw-rw-r-- 1 karpoke karpoke 2511 2011-10-23 15:19 openssl_RENEG_127.0.0.1_443_2011-10-23_151957.log
    -rw-rw-r-- 1 karpoke karpoke 688 2011-10-23 15:19 openssl_RENEG_127.0.0.1_443_2011-10-23_151957.err
    -rw-rw-r-- 1 karpoke karpoke 582 2011-10-23 15:21 openssl_HEAD_127.0.0.1_443_2011-10-23_151957.err


    [-] done

Via [L’home dibuixat][].

  [TLSSLed]: http://www.taddong.com/en/lab.html#TLSSLED
    "TLSSLed"
  [versión 1.3]: http://www.taddong.com/tools/TLSSLed_v1.3.sh
    "TLSSLed 1.3"
  [L’home dibuixat]: http://caballe.cat/wp/eina-tlssled-v12/
    "L’home dibuixat"
