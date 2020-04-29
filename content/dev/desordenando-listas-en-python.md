Title: Desordenando listas en Python
Date: 2011-03-29 20:00
Author: Nacho Cano
Tags: algoritmo de Sattolo, intercambio de valores, permutación, python, shuffle
Slug: desordenando-listas-en-python
Related: intercambio-de-los-valores-de-dos-variables,mystery

Si tenemos una lista de elementos, por ejemplo:

    >>> l = [ 2, 3, 5, 7, 11, 13, 17, 19 ]

![Deck Card Shuffler]({static}/images/deck_card_shuffler-300x213.jpg)

Y queremos desordenarla, pero con la condición de que ningún elemento
ocupe la misma posición que ocupaba originalmente, podemos aplicar el
[algoritmo de Sottolo][]:

    >>> from random import randrange
    >>> def sattoloCycle(items):
    ...     i = len(items)
    ...     while i > 1:
    ...         i = i - 1
    ...         j = randrange(i)  # 0 < = j <= i-1
    ...         items[j], items[i] = items[i], items[j]
    ...     return

    >>> sattoloCycle(l)
    >>> print l
    [5, 17, 3, 2, 7, 11, 13]

  [algoritmo de Sottolo]: http://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle#Sattolo.27s_algorithm
    "algoritmo de Sottolo"
