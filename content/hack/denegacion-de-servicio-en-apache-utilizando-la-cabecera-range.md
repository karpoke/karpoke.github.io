Title: Denegación de servicio en Apache utilizando la cabecera Range
Date: 2011-08-31 14:19
Author: Nacho Cano
Tags: 2.2.17, apache, cabeceras HTTP, denegación de servicio, dos, mod_headers, mod_rewrite, perl, range, requestheader, script, telnet
Slug: denegacion-de-servicio-en-apache-utilizando-la-cabecera-range

Una [vulnerabilidad descubierta por _kingcope_][] permite que los
servidores Apache vulnerables sean susceptibles de sufrir una denegación
de servicio.

La vulnerabilidad se encuentra en el uso de la cabecera `Range`. Esta
cabecera se utiliza para obtener sólo una parte de la página. Si se
solicitan varias partes además de pedir que la respuesta se comprima,
mediante la cabecera `Accept-Encoding: gzip`, se dispara el consumo de
procesador y memoria.

Existe un [_script_][] que permite comprobar si el servidor es
vulnerable y, si es el caso, explotar dicha vulnerabilidad.

Para comprobar si un servidor es vulnerable, podemos ejecutar:

```bash
$ telnet 127.0.0.1 80
HEAD / HTTP/1.1
Host: 127.0.0.1
Range: bytes=0-5
Accept-Encoding: gzip
Connection: close
```

Si la respuesta es un código `206 Partial Content` el servidor es
vulnerable:

```bash
HTTP/1.1 206 Partial Content
Date: Wed, 31 Aug 2011 11:52:13 GMT
Server: Apache/2.2.17 (Ubuntu)
Vary: Accept-Encoding
Content-Encoding: gzip
Content-Range: bytes 0-5/20
Content-Length: 6
Connection: close
Content-Type: text/html;charset=UTF-8
```

Protección
----------

Si tenemos un servidor vulnerable, podemos adoptar alguna de las
siguientes medidas de protección.

-   Podemos [deshabilitar la cabecera `Range`][deshabilitar la cabecera Range] mediante la directiva
    `RequestHeader`, usando el módulo `mod_headers`:

    ```bash
     RequestHeader unset Range
    ```

» [Limitar el número de intervalos][] mediante `mod_rewrite`:

    ```bash
     RewriteEngine On
    RewriteCond %{HTTP:Range} ([0-9]_-[0-9]_)(\s*,\s*[0-9]_-[0-9]_)+
    RewriteRule .* - [NS,L,F]
    ```

» [Deshabilitar el módulo `mod_deflate`][Deshabilitar el módulo mod_deflate]:

    ```bash
$ sudo a2dismod deflate
    ```

  [vulnerabilidad descubierta por _kingcope_]: http://issues.apache.org/bugzilla/show_bug.cgi?id=51714
    "vulnerabilidad descubierta por _kingcope_"
  [_script_]: http://seclists.org/fulldisclosure/2011/Aug/att-175/killapache_pl.bin
    "_script_"
  [deshabilitar la cabecera Range]: http://www.securityartwork.es/2011/08/25/denegacion-de-servicio-en-apache/
    "deshabilitar la cabecera `Range`"
  [Limitar el número de intervalos]: http://seclists.org/fulldisclosure/2011/Aug/257
    "Limitar el número de intervalos"
  [Deshabilitar el módulo mod_deflate]: http://www.daboweb.com/2011/08/24/vulnerabilidad-0-day-y-ataques-dos-en-apache-2-0-2-2-y-1-3-medidas-para-paliarlo/
    "Deshabilitar el módulo `mod_deflate`"
