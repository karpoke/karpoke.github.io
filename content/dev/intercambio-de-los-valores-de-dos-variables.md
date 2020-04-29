Title: Intercambio de los valores de dos variables
Date: 2010-12-03 21:01
Author: Nacho Cano
Tags: bash, intercambio de valores, python
Slug: intercambio-de-los-valores-de-dos-variables

![Teleporter]({static}/images/teleporter-300x299.jpg)

En algunos lenguajes, intercambiar el valor de la variable `a` por el de
la variable `b` implica, explícitamente, utilizar una variable temporal:

    t = a;
    a = b;
    b = t;

En Python:

    a, b = b, a

Pero esperen, aún hay más:

    a, b, c, d = d, c, b, a

* * * * *

#### Actualizado el 31 de julio de 2011

En [Bash][]:

    $ read a b c <<< $(echo $c $b $a)

[Otra manera][]:

    $ read a b c <<(echo $c $b $a)

* * * * *

#### Actualizado el 23 de junio de 2016

Si los valores son numéricos, podemos recurrir a sumas y restas:

    In [1]: a, b = 3, 5
    In [2]: a = a + b
    In [3]: b = a - b
    In [4]: a = a - b
    In [5]: a, b
    Out[5]: (5, 3)

O multiplicaciones y divisiones:

    In [1]: a, b = 3.2, 5.7
    In [2]: a = a * b
    In [3]: b = a / b
    In [4]: a = a / b
    In [5]: a, b
    Out[5]: (5.7, 3.2)

* * * * *

  [Bash]: http://www.commandlinefu.com/commands/view/8937/multiple-variable-assignments-from-command-output-in-bash
    "Bash"
  [Otra manera]: http://www.commandlinefu.com/commands/view/8943/multiple-variable-assignments-from-command-output-in-bash
    "Otra manera"
