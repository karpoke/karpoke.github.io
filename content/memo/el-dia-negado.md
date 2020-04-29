Title: El día negado
Date: 2013-03-14 02:03
Author: Nacho Cano
Tags: año bisiesto, cal
Slug: el-dia-negado
Related: de-aqui-al-2038

Leyendo el [espejo lúdico][], me encuentro con estas dos preguntas:

> ¿Hay algún día de la semana en el que nunca puede empezar un siglo?
>  Por el contrario, ¿cuál es el día de la semana que puede ser inicio y
> final de un siglo?

que pueden quedar contestadas rápidamente ejecutando el siguiente
comando:

    $ for year in `seq 2001 100 3001`; do cal 1 $year | grep -A2 $year; done | grep --color -B2 " 1 "
         Enero 2001
    do lu ma mi ju vi sá
        1  2  3  4  5  6
         Enero 2101
    do lu ma mi ju vi sá
                       1
         Enero 2201
    do lu ma mi ju vi sá
                 1  2  3
         Enero 2301
    do lu ma mi ju vi sá
           1  2  3  4  5
         Enero 2401
    do lu ma mi ju vi sá
        1  2  3  4  5  6
         Enero 2501
    do lu ma mi ju vi sá
                       1
         Enero 2601
    do lu ma mi ju vi sá
                 1  2  3
         Enero 2701
    do lu ma mi ju vi sá
           1  2  3  4  5
         Enero 2801
    do lu ma mi ju vi sá
        1  2  3  4  5  6
         Enero 2901
    do lu ma mi ju vi sá
                       1
         Enero 3001
    do lu ma mi ju vi sá
                 1  2  3

Los años divisibles por 100 no son bisiestos, a no ser que sean
divisible por 400:

    $ cal 2 2000
        Febrero 2000
    do lu ma mi ju vi sá
           1  2  3  4  5
     6  7  8  9 10 11 12
    13 14 15 16 17 18 19
    20 21 22 23 24 25 26
    27 28 29

    $ cal 2 2100
        Febrero 2100
    do lu ma mi ju vi sá
        1  2  3  4  5  6
     7  8  9 10 11 12 13
    14 15 16 17 18 19 20
    21 22 23 24 25 26 27
    28

Por lo que, volviendo a las preguntas, los siglos no pueden comenzar en
miércoles, viernes ni domingo. El lunes es él único día que puede ser
comienzo y final de siglo. Por ejemplo, en 2001:

    $ cal 1 2001
         Enero 2001
    do lu ma mi ju vi sá
        1  2  3  4  5  6
     7  8  9 10 11 12 13
    14 15 16 17 18 19 20
    21 22 23 24 25 26 27
    28 29 30 31

    $ cal 12 2001
       Diciembre 2001
    do lu ma mi ju vi sá
                       1
     2  3  4  5  6  7  8
     9 10 11 12 13 14 15
    16 17 18 19 20 21 22
    23 24 25 26 27 28 29
    30 31

  [espejo lúdico]: http://espejo-ludico.blogspot.com.es/2013/03/el-dia-negado.html
    "espejo lúdico"
