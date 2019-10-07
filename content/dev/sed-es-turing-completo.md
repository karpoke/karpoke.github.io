Title: sed es Turing completo
Date: 2012-04-22 00:32
Author: Nacho Cano
Tags: máquina de turing, sed, turing completo
Slug: sed-es-turing-completo

¿Cómo puede ser un editor de flujo, una utilidad para el tratamiento de
texto, un lenguaje Turing completo? `sed` permite saltos condiciones e
incondicionales y utiliza un _buffer_ temporal, lo que permite
[construir una máquina de Turing con él][], y cualquier lenguaje que
pueda construir una máquina de Turing es Turing completo.

Una implementación de una máquina de Turing con `sed` es [turing.sed][].

Un ejemplo de programa que realiza el incremento de un número binario es
el siguiente:

```bash
| 10010111

# State 0
0  R0
011R1
000R1

# State 1
1  L2
100R1
111R1

# State 2
2 1R3
201R3
210L2

# State 3
3  RF
300R3
311R3
```

En la primera línea se muestra el contenido de la cinta a la derecha del
cursor, marcado por una barra vertical.

Las siguientes líneas del programa son las reglas que definen lo que
debe hacer la máquina de Turing, y tienen la siguiente sintaxis:

```bash
estado_actual símbolo_actual nuevo_símbolo dirección nuevo_estado
```

Para ejecutar el programa:

```bash
$ sed -f turing.sed < increment.tm
(0) | |10010111
(0) |1|0010111
(1) 1|0|010111
(1) 10|0|10111
(1) 100|1|0111
(1) 1001|0|111
(1) 10010|1|11
(1) 100101|1|1
(1) 1001011|1|
(1) 10010111| |
(2) 1001011|1|
(2) 100101|1|0
(2) 10010|1|00
(2) 1001|0|000
(3) 10011|0|00
(3) 100110|0|0
(3) 1001100|0|
(3) 10011000| |
(F) 10011000 | |
Final state F reached... end of processing
```

La salida muestra el estado en el que está la máquina, el contenido de
la cinta y la posición del cursor entre dos barras verticales.

El siguiente programa concatena dos cadenas de unos:

```bash
# concatenate two strings of 1's
| 11011

# State 0
0  R0
000R0
01 R1

# State 1
111R1
100R2

# State 2
200R2
211R3

# State 3
3 1L4
301L4
311R3

# State 4
411L4
400L5

# State 5
5  R7
500L5
511L6

# State 6
6  R0
600R0
611L6

# State 7
700R7
711R8

# state 8
811R8
8  RF
800RF
```

Otros ejemplos:

-   [Tetris][]
-   [Sokoban (juego][]
-   [Calculator][]

Referencias
-----------

» [A proof that Unix utility "sed" is Turing complete][construir una
máquina de Turing con él]
» [Implementation of a Turing Machine as Sed Script][]
» [Turing machine simulator][]

  [construir una máquina de Turing con él]: http://www.catonmat.net/blog/proof-that-sed-is-turing-complete/
    "construir una máquina de Turing con él"
  [turing.sed]: http://www.catonmat.net/ftp/sed/turing.sed
    "turing.sed"
  [Tetris]: http://www.catonmat.net/ftp/sed/sedtris.sed
    "Tetris"
  [Sokoban (juego]: http://www.catonmat.net/ftp/sed/sokoban.sed
    "Sokoban (juego"
  [Calculator]: http://www.catonmat.net/ftp/sed/dc.sed
    "Calculator"
  [Implementation of a Turing Machine as Sed Script]: http://sed.sourceforge.net/grabbag/scripts/turing.txt
    "Implementation of a Turing Machine as Sed Script"
  [Turing machine simulator]: http://morphett.info/turing/turing.html
    "Turing machine simulator"
