Title: Descifrando al César en Python
Date: 2011-02-16 03:40
Author: Nacho Cano
Tags: ASCII, cifrado césar, maketrans, python, rot13, rot47, translate, vigenere
Slug: descifrando-al-cesar-en-python

Si lo que pretendemos es, dada una cadena, sustituir una serie de
caracteres por otra, en Python es tan sencillo como pasarle al método
`maketrans` una cadena con los caracteres que queremos cambiar y otra
con los caracteres a utilizar en su lugar. Ambas cadenas deberán tener
la misma longitud. Este método devuelve una tabla de traducción, un
objeto susceptible de ser usado por el método `translate` el cual se
aplica sobre un _string_, como veremos.


Cifrado César
-------------

En pocas palabras, el [cifrado César][] se basa en sustituir cada letra
de un mensaje, una cadena de texto, por la que le sigue 3 puestos más
allá en el alfabeto, es decir, la A por la D, la B por la E, y así
sucesivamente, hasta las tres últimas letras que se cambiarán por las
tres primeras letras, respectivamente. Para descifrar un mensaje cifrado
con este sistema sólo tenemos que llevar a cabo el proceso inverso,
cambiar la A por la X, la B por la Y, la C por la Z, y a partir de la D
por la letra 3 puestos antes en el alfabeto. No tiene en cuenta
mayúsculas o minúsculas, por lo que por ahora no nos preocuparemos de
eso.

    from string import maketrans

    sfrom = "abcdefghijklmnopqrstuvwxyz"
    sto = "xyzabcdefghijklmnopqrstuvw"
    trantab = maketrans(sfrom, sto)

    "sbwkrq".translate(trantab)

Con esto en mente, podemos escribir un [método][] que nos permita
cualquier tipo de traslación, tanto en un sentido como en otro:

    from string import maketrans, translate, ascii_lowercase as al
    def caesar(text, offset=3):
       return translate(text, maketrans(al, al[offset:] + al[:offset]))

    >>> caesar("python")
    'sbwkrq'
    >>> caesar("sbwkrq", -3)
    'python'
    >>> caesar("python", 13)
    'clguba'

Los métodos de cifrado basados en traslaciones hace mucho tiempo que
quedaron obsoletos, ya que es sencillo obtener una distribución de las
frecuencias de letras de un texto cifrado y compararlas con la
[frecuencia de aparición de letras][] para un idioma concreto.

ROT13
-----

[RTO13][] está basado en el cifrado César, sólo que en lugar de 3
posiciones, hace la sustitución por el carácter que está 13 puestos
hacia adelante en el alfabeto, conservando, además, si es mayúscula o
minúscula.

    from string import maketrans, translate, ascii_lowercase as al, ascii_uppercase as au
    def rot13(text, offset=13):
       sfrom = au + al
       sto = au[offset:] + au[:offset] + al[offset:] + al[:offset]
       return translate(text, maketrans(sfrom, sto))

    >>> rot13("ABCXYZabcxyz")
    'NOPKLMnopklm'

ROT47
-----

Este es un ROT13 que utiliza un conjunto mayor que el de las letras, ya
que utiliza el conjunto de los caracteres ASCII del "!" (33) al "\~"
(126), y realiza la sustitución por el carácter que está 47 puestos
hacia adelante. Crearemos la lista de caracteres ASCII necesarios a
partir de las listas de caracteres del módulo `string`. Para
conseguirlo, buscaremos los índices de los caracteres de puntuación
entre los cuales insertaremos las listas de dígitos y letras mayúsculas
y minúsculas.

Este es el código ASCII:

      30 40 50 60 70 80 90 100 110 120
     ---------------------------------
    0:    (  2  < F  P  Z  d   n   x
    1:    )  3  =  G  Q  [  e   o   y
    2:    *  4  >  H  R  \  f   p   z
    3: !  +  5  ?  I  S  ]  g   q   {
    4: "  ,  6  @  J  T  ^  h   r   |
    5: #  -  7  A  K  U  _  i   s   }
    6: $  .  8  B  L  V  `  j   t   ~
    7: %  /  9  C  M  W  a  k   u  DEL
    8: &  0  :  D  N  X  b  l   v
    9: ;’  1  ;  E  O  Y  c  m   w

Y este es el contenido de la lista de signos de puntuación:

    >>> string.punctuation
    '!"#$%&\'()*+,-./:;< =>?@[\\]^_`{|}~'

Debemos colocar los números entre "/" y ":", las letras mayúsculas entre
"@" y "[", y las letras minúsculas entre "\`" y "{":

    from string import punctuation as p, digits as d, ascii_lowercase as al, ascii_uppercase as au

    ix = p.find(":")
    iu = p.find("[")
    il = p.find("{")
    ascii = p[:ix] + d + p[ix:iu] + au + p[iu:il] + al + p[il:]

    >>> print ascii
    '!"#$%&\'()*+,-./0123456789:;< =>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    >>> len(ascii)
    94

Ya podemos crear una función `rot47`:

    from string import maketrans, translate
    def rot47(text, offset=47):
       # ascii contiene los caracteres ASCII del "!" (33) al "~" (126)
       return translate(text, maketrans(ascii, ascii[offset:] + ascii[:offset]))

    >>> print rot47("Cómo se puede distinguir a un extrovertido de un")
    ró>@ D6 AF656 5:DE:?8F:C 2 F? 6IEC@G6CE:5@ 56 F?

Vigenëre
--------

[Vigenëre][] es un cifrado César por grupos, donde cada letra del grupo
sufre una traslación diferente. La longitud de la palabra clave
determina el tamaño de los grupos, y cada letra especifica la traslación
para cada letra del grupo. No distingue entre mayúsculas y minúsculas.

    from string import ascii_lowercase as al
    def vigenere_crypt(text, key, decrypt=0):
       prefix = -1 if decrypt else 1
       len_t = len(text)
       len_k = len(key)
       ak = [ al.find(c) for c in key ]
       return "".join([caesar(text[i], prefix*ak[i%len_k]) for i in range(len_t)])

    >>> vigenere_crypt("parisvautbienunemesse", "loup")
    'aolxdjujepctyihtxsmhp'

    >>> vigenere_crypt("aolxdjujepctyihtxsmhp", "loup", -1)
    'parisvautbienunemesse'

Este cifrado también quedó obsoleto después de que se descubriera el
[método Kasiski][], que consiste en buscar palabras repetidas en el
texto cifrado. Es casi seguro que dichas palabras no sólo eran la misma
antes del cifrado sino que además la clave coincidió en la misma
posición en ambas ocurrencias. La distancia entre palabras repetidas es
múltiplo de la longitud de la clave, por lo que si tenemos diferentes
palabras que se repiten, obtenemos el máximo común divisor de las
longitudes y la longitud de la clave debe ser, o dicho mcd, o un factor
primo de éste. Una vez encontrada la longitud de la clave, se aplica la
misma técnica estadística que para el cifrado César.

  [cifrado César]: http://es.wikipedia.org/wiki/Cifrado_C%C3%A9sar
    "cifrado César"
  [método]: http://techyoyo.com/2009/08/encrypt-message-python-programming-language/#comments
    "método"
  [frecuencia de aparición de letras]: http://es.wikipedia.org/wiki/Frecuencia_de_aparici%C3%B3n_de_letras
    "frecuencia de aparición de letras"
  [RTO13]: http://es.wikipedia.org/wiki/ROT13
    "RTO13"
  [Vigenëre]: http://es.wikipedia.org/wiki/Cifrado_de_Vigen%C3%A8re
    "Vigenëre"
  [método Kasiski]: http://es.wikipedia.org/wiki/M%C3%A9todo_Kasiski
    "método Kasiski"
