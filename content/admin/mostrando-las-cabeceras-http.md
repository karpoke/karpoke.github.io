Title: Mostrando las cabeceras HTTP
Date: 2010-10-07 10:35
Author: Nacho Cano
Tags: cabeceras HTTP, curl, HEAD, lynx, netcat, telnet, w3m, wget
Slug: mostrando-las-cabeceras-http

Leyendo el artículo de [análisis de cabeceras][] de SbD y, en
particular, lo relacionado con las cabeceras no estándar, es decir, las
que comienzan por `X-`, se me ha ocurrido que estaría bien ver qué debe
haber por el mundo:

![HTTP Header]({static}/images/http_header.jpg)

Suponiendo que el archivo [sites.txt][] contiene un listado de los
sitios que queremos comprobar:

```bash
$ for url in $(cat sites.txt); do
>   echo $url
>   curl -sI $url | grep "^X-"
>   done > headers.txt
```

Es cierto que se podría haber realizado de otras formas:

```bash
$ HEAD barrapunto.com
```

```bash
$ nc barrapunto.com 80
GET / HTTP/1.1
```

```bash
$ telnet barrapunto.com 80
GET / HTTP/1.1
Host:barrapunto.com
```

```bash
$ wget -qS barrapunto.com
```

```bash
$ w3m -dump_head barrapunto.com
```

```bash
$ lynx -head -dump "http://barrapunto.com"
```

  [análisis de cabeceras]: http://www.securitybydefault.com/2010/08/analizando-cabeceras-http-just-for-fun.html
    "análisis de cabeceras"
  [sites.txt]: http://terminus.ignaciocano.com/wp-uploads/linked/sites.txt
    "sites.txt"
