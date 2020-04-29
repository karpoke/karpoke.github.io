Title: Benchmarking de un servidor web
Date: 2012-05-10 19:47
Author: Nacho Cano
Tags: ab, apache, benchmarking, minería de datos
Slug: benchmarking-de-un-servidor-web

Con un sencillo comando podremos saber la carga que soporta nuestro
servidor web. Hay que tener cuidado contra qué servidor lo lanzamos y en
qué momento, porque puede que interfiera o impida el acceso a otros
usuarios.

El comando es `ab`, de _Apache Benchmarking_, y permite multitud de
opciones, entre ellas el número de peticiones concurrentes, con el
argumento `-c`, y la duración de la prueba, con el argumento `-t`:

    $ ab -c 5 -t 60 http://ip-del-servidor
    This is ApacheBench, Version 2.3
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking terminus (be patient)
    Finished 1337 requests


    Server Software:        Incognito
    Server Hostname:        terminus
    Server Port:            80

    Document Path:          /
    Document Length:        73260 bytes

    Concurrency Level:      5
    Time taken for tests:   60.012 seconds
    Complete requests:      1337
    Failed requests:        0
    Write errors:           0
    Total transferred:      98456145 bytes
    HTML transferred:       98020320 bytes
    Requests per second:    22.28 [#/sec] (mean)
    Time per request:       224.428 [ms] (mean)
    Time per request:       44.886 [ms] (mean, across all concurrent requests)
    Transfer rate:          1602.16 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        4   16  12.0     14     261
    Processing:   104  208 122.8    180    3679
    Waiting:        6   23  93.5     16    3273
    Total:        115  224 124.1    196    3688

    Percentage of the requests served within a certain time (ms)
      50%    196
      66%    228
      75%    250
      80%    270
      90%    324
      95%    406
      98%    466
      99%    474
     100%   3688 (longest request)

En este caso, vemos que el servidor soporta algo más de 22 peticiones
por segundo. Es el [viejo servidor][] que aloja esta página, además de
servir para otros menesteres. La página funciona con WordPress y está
instalado el complemento WordPress Super Caché, las páginas cacheadas
cargan más rápido, con lo que eso afecta al valor del resultado, es
decir, es como si todas las visitas las hubiera hecho el mismo usuario,
algo que normalmente no suele darse el caso.

Realmente, la prueba no debería realizarse sobre una única página, sino
que se debería obtener previamente un modelo de la carga del servidor,
segmentado según varios parámetros como podría ser el tipo y el tamaño
de fichero, y realizar las pruebas sobre dicho modelo.

Además, la prueba se ha realizado desde un equipo en la misma red, por
lo que si la prueba se hiciese desde Internet, los resultados serían
algo peores, ya que el ancho de banda es menor.

Por último, comentar que para que el valor sea lo más real posible,
debemos hacer la prueba en un entorno controlado, sin que haya
interferencias de otros usuarios o procesos, tanto en la red como en el
servidor.

  [viejo servidor]: {filename}/memo/the-name-of-the-game.md
    "viejo servidor"
