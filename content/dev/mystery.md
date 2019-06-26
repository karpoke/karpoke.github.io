Title: Mystery
Date: 2011-02-26 00:49
Author: Nacho Cano
Tags: generador, list comprehension, python, yield
Slug: mystery

Casi parece que está escrito en chino, o mejor dicho en _brainfuck_, o
puede que no sea muy _[zen]_, pero no deja de ser _[elegante]_.

```python

def mystery(n):
    a = list(range(n))
    [[(yield i) for a[::i] in [([0]*n)[::i]]] for i in a[2:] if a[i]]

```

El nombre de la función pretende no dar pistas para que intentemos
averiguar qué hace exactamente esta función. He aquí una pista:

![prime numnbers]({static}/images/prime-numbers-300x300.gif "prime-numbers")

Fuente: [www.numberspiral.com]

```python

>>> f = mystery(20)
>>> try:
...     while True:
...         print f.next()
... except StopIteration:
...     pass
2
3
5
7
11
13
17
19

```

  [zen]: {filename}/dev/python-zen.md
    "zen"
  [elegante]: http://blog.garlicsim.org/post/3504711416#comment-156082460
    "elegante"
  [www.numberspiral.com]: http://www.numberspiral.com/
    "www.numberspiral.com"
