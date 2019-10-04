Title: De aquí al 2038
Date: 2010-10-07 13:27
Author: Nacho Cano
Tags: cadenas, cal, y2k38
Slug: de-aqui-al-2038

Como bien dice el agente Smith, es cuestión de contrastar un poco.
[Octubres][] con 5 viernes, 5 sábados y 5 domingos, de aquí al [2038][],
si es que llegamos:

```bash
$ for ((i=2011; i < 2039; i++)); do cal 10 $i; done |
grep -B2 -A4  "             1  2  3"
```

```bash
    Octubre 2021
lu ma mi ju vi sá do
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30 31
--
    Octubre 2027
lu ma mi ju vi sá do
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30 31
--
    Octubre 2032
lu ma mi ju vi sá do
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30 31
--
    Octubre 2038
lu ma mi ju vi sá do
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30 31
```

  [Octubres]: http://rinzewind.org/archives/2010/10/07/5-viernes-5-sabados-5-domingos/
    "Octubres"
  [2038]: http://es.wikipedia.org/wiki/Problema_del_a%C3%B1o_2038
    "2038"
