Title: SSLyze
Date: 2013-03-29 22:54
Author: Nacho Cano
Tags: ssl, sslyze
Slug: sslyze
Related: configurar-apache-para-servir-conexiones-seguras,tlssled-v1-2

[SSLyze][] es una herramienta para analizar la configuración SSL de un
servidor, diseñada para ser rápida y exhaustiva.

Un ejemplo de uso:

```bash
$ python sslyze --regular localhost:443


 REGISTERING AVAILABLE PLUGINS
 -----------------------------

  PluginCertInfo
  PluginSessionRenegotiation
  PluginCompression
  PluginSessionResumption
  PluginOpenSSLCipherSuites



 CHECKING HOST(S) AVAILABILITY
 -----------------------------

   localhost:443        => 127.0.0.1:443



 SCAN RESULTS FOR LOCALHOST:443 - 127.0.0.1:443
 -----------------------------------------------------------------

  * Compression :
        Compression Support:      Disabled

  * Session Renegotiation :
      Client-initiated Renegotiations:    Rejected
      Secure Renegotiation:               Supported

  * Certificate :
      Validation w/ Mozilla's CA Store:  Certificate is NOT Trusted: self signed certificate in certificate chain
      Hostname Validation:               OK - Common Name Matches
      SHA1 Fingerprint:                  12C4EC1C16807D8654269FBE5E0A8DBFBF1244CC

      Common Name:                       localhost
      Issuer:                            /C=ES/ST=IB/O=Localhost CA/CN=localhost/emailAddress=postmaster@localhost
      Serial Number:                     F525610B96987DAE
      Not Before:                        Mar 20 10:31:07 2013 GMT
      Not After:                         Mar 20 10:31:07 2014 GMT
      Signature Algorithm:               sha1WithRSAEncryption
      Key Size:                          2048

Unhandled exception when processing --sslv2:
utils.ctSSL.errors.ctSSLFeatureNotAvailable - SSLv2 disabled.

  * Session Resumption :
      With Session IDs:           Supported (5 successful, 0 failed, 0 errors, 5 total attempts).
      With TLS Session Tickets:   Supported

  * TLSV1_1 Cipher Suites :

      Rejected Cipher Suite(s): Hidden

      Preferred Cipher Suite:
        RC4-SHA                  128 bits      HTTP 302 Found - /

      Accepted Cipher Suite(s):
        CAMELLIA256-SHA          256 bits      HTTP 302 Found - /
        AES256-SHA               256 bits      HTTP 302 Found - /
        DES-CBC3-SHA             168 bits      HTTP 302 Found - /
        RC4-SHA                  128 bits      HTTP 302 Found - /
        CAMELLIA128-SHA          128 bits      HTTP 302 Found - /
        AES128-SHA               128 bits      HTTP 302 Found - /

      Undefined - An unexpected error happened: None

  * TLSV1_2 Cipher Suites :

      Rejected Cipher Suite(s): Hidden

      Preferred Cipher Suite:
        AES128-GCM-SHA256        128 bits      HTTP 302 Found - /

      Accepted Cipher Suite(s):
        CAMELLIA256-SHA          256 bits      HTTP 302 Found - /
        AES256-SHA256            256 bits      HTTP 302 Found - /
        AES256-SHA               256 bits      HTTP 302 Found - /
        AES256-GCM-SHA384        256 bits      HTTP 302 Found - /
        DES-CBC3-SHA             168 bits      HTTP 302 Found - /
        RC4-SHA                  128 bits      HTTP 302 Found - /
        CAMELLIA128-SHA          128 bits      HTTP 302 Found - /
        AES128-SHA256            128 bits      HTTP 302 Found - /
        AES128-SHA               128 bits      HTTP 302 Found - /
        AES128-GCM-SHA256        128 bits      HTTP 302 Found - /

      Undefined - An unexpected error happened: None

  * SSLV3 Cipher Suites :

      Rejected Cipher Suite(s): Hidden

      Preferred Cipher Suite:
        RC4-SHA                  128 bits      HTTP 302 Found - /

      Accepted Cipher Suite(s):
        CAMELLIA256-SHA          256 bits      HTTP 302 Found - /
        AES256-SHA               256 bits      HTTP 302 Found - /
        DES-CBC3-SHA             168 bits      HTTP 302 Found - /
        RC4-SHA                  128 bits      HTTP 302 Found - /
        CAMELLIA128-SHA          128 bits      HTTP 302 Found - /
        AES128-SHA               128 bits      HTTP 302 Found - /

      Undefined - An unexpected error happened: None

  * TLSV1 Cipher Suites :

      Rejected Cipher Suite(s): Hidden

      Preferred Cipher Suite:
        RC4-SHA                  128 bits      HTTP 302 Found - /

      Accepted Cipher Suite(s):
        CAMELLIA256-SHA          256 bits      HTTP 302 Found - /
        AES256-SHA               256 bits      HTTP 302 Found - /
        DES-CBC3-SHA             168 bits      HTTP 302 Found - /
        RC4-SHA                  128 bits      HTTP 302 Found - /
        CAMELLIA128-SHA          128 bits      HTTP 302 Found - /
        AES128-SHA               128 bits      HTTP 302 Found - /

      Undefined - An unexpected error happened: None



 SCAN COMPLETED IN 16.95 S
 -------------------------
```

  [SSLyze]: https://github.com/iSECPartners/sslyze
    "SSLyze"
