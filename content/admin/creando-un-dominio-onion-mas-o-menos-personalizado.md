Title: Creando un dominio .onion (más o menos) personalizado
Date: 2014-11-14 00:29
Author: Nacho Cano
Tags: base32, código fuente, hash, onion, sha1, shallot, tor
Slug: creando-un-dominio-onion-mas-o-menos-personalizado

Hace unos días salió a la luz que Facebook estaba disponible a través de
un [dominio .onion][] en la red Tor.

Las direcciones .onion se crean al aplicar una [codificación base32 a los primeros 80 bytes del hash SHA1 de la clave privada del servidor][].
Sabiendo esto, crear una dirección que contenga palabras clave concretas
es cuestión de fuerza bruta y tiempo.

Un programa que nos servirá para crear dominios que cumplan con nuestros
requisitos es [Shallot][].


Descarga y compilación
----------------------

```bash
$ git clone https://github.com/katmagic/Shallot.git
$ cd Shallot
$ ./configure
$ make
```

Uso
---

Su uso es sencillo:

```bash
$ ./shallot ^test
```

Rendimiento
-----------

Tiempo estimado para generar un dominio con un procesador a 1.5Ghz:

| Caracteres | Tiempo aproximado    |
|------------|----------------------|
| \<4        | menos de 1 segundo   |
| 4          | 2 segundos           |
| 5          | 1 minuto             |
| 6          | 30 minutos           |
| 7          | 1 día                |
| 8          | 25 días              |
| 9          | 1 año                |
| 10         | 40 años              |
| 11         | 640 años             |
| 12         | 10 mil años          |
| 13         | 160 mil años         |
| 14         | 2.6 millones de años |

Referencias
-----------

- [Servicios ocultos en la red Tor][]

  [dominio .onion]: https://lists.torproject.org/pipermail/tor-talk/2014-October/035413.html
    "dominio .onion"
  [codificación base32 a los primeros 80 bytes del hash SHA1 de la clave privada del servidor]: https://gitweb.torproject.org/torspec.git?a=blob_plain;hb=HEAD;f=rend-spec.txt
    "codificación base32 a los primeros 80 bytes del hash SHA1 de la clave privada del servidor"
  [Shallot]: https://github.com/katmagic/Shallot
    "Shallot"
  [Servicios ocultos en la red Tor]: https://www.torproject.org/docs/hidden-services
    "Servicios ocultos en la red Tor"
