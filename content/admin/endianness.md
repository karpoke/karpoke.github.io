Title: Endianness
Date: 2011-07-30 17:34
Author: Nacho Cano
Tags: big-endian, byteorder, c, casting, little-endian, middle-endian, oneliner, pack, perl, python, sys
Slug: endianness

"[Endianicidad][]" designa el formato en el que se almacenan los datos
de más de un byte en un ordenador. El sistema _big-endian_ adoptado por
Motorola entre otros, consiste en representar los bytes en el orden
"natural", así el valor hexadecimal 0x4A3B2C1D se codificaría en memoria
en la secuencia {4A, 3B, 2C, 1D}. En el sistema _little-endian_ adoptado
por Intel, entre otros, el mismo valor se codificaría como {1D, 2C, 3B,
4A}, de manera que de este modo se hace más intuitivo el acceso a datos,
porque se efectúa fácilmente de manera incremental de menos relevante a
más relevante (siempre se opera con incrementos de contador en la
memoria).

Algunas arquitecturas de microprocesador pueden trabajar con ambos
formatos (ARM, PowerPC, DEC Alpha, PA-RISC, Arquitectura MIPS), y a
veces son referidas como sistemas _middle-endian_.


Comprobación en C
-----------------

Una posible forma de comprobar qué sistema utilizamos [mediante un
programa en C][] es con el siguiente código:

    #include
    int main(int argc, char **argv)
    {
       int i = 1;
       char *p = (char *) &i;
       if ( p[0] == 1 )
            printf("Little Endian\n");
       else
            printf("Big Endian\n");
       return 0;
    }

Se obtiene la dirección de memoria de un entero, con un espacio de
almacenamiento de al menos 16 bits, cuyo valor es 1. Leemos el primer
byte y si es 1 es que _little-endian_. Para leer el primer byte del
entero, hacemos una conversión de tipo puntero a carácter.

Comprobación en Bash
--------------------

El siguiente comando [utiliza el caracter ASCII "I"][], cuyo valor en
octal en sistemas _little-endian_ es 000111, mientras que en sistemas
_big-endian_ es 0444000. Basta comprobar el último carácter para conocer
el tipo de sistema. Si es 1 es que utilizamos _little-endian_:

    $ echo -n I | od -to2 | head -n1 | cut -f2 -d" " | cut -c6
    1

También podemos utilizar [`awk`][awk]:

    $ awk 'BEGIN {c="I"; printf "%c",c}' | od | head -n1 | cut -f2 -d" " | cut -c6
    1

Comprobación en Python
----------------------

Utilizando el método [`pack`][pack]:

    $ python -c "from struct import pack;print(int(pack('@h',1)==pack('
    Consultando la propiedad byteorder:
    $ python -c "import sys;print sys.byteorder"
    little
    $ python -c "import sys;print(0 if sys.byteorder=='big' else 1)"
    1

Comprobación en Perl
--------------------

El resultado haciendo [la comprobación en Perl][] es [1234 para
_little-endian_][].

    $ perl -MConfig -e 'print "$Config{byteorder}\n";'
    1234

También se puede utilizar la función [`pack`][1]:

    $ perl -MConfig -e 'print pack("L", 1) ne pack("N", 1);'
    1


  [Endianicidad]: http://secure.wikimedia.org/wikipedia/es/wiki/Endianness
    "Endianicidad"
  [mediante un programa en C]: http://secure.wikimedia.org/wikipedia/es/wiki/Endianness#Ejemplo
    "mediante un programa en C"
  [utiliza el caracter ASCII "I"]: http://serverfault.com/questions/163487/linux-how-to-tell-if-system-is-big-endian-or-little-endian/163493#163493
    "utiliza el caracter ASCII "I""
  [awk]: http://objectmix.com/awk/27127-32-bit-big-endian-integer-values-binary-format-how.html
    "`awk`"
  [pack]: http://serverfault.com/questions/163487/linux-how-to-tell-if-system-is-big-endian-or-little-endian/163505#163505
    "`pack`"
  [la comprobación en Perl]: http://stackoverflow.com/questions/2610849/finding-if-the-system-is-little-endian-or-big-endian-with-perl/2610876#2610876
    "la comprobación en Perl"
  [1234 para _little-endian_]: http://perldoc.perl.org/Config.html#byteorder
    "1234 para _little-endian_"
  [1]: http://stackoverflow.com/questions/2610849/finding-if-the-system-is-little-endian-or-big-endian-with-perl/2610889#2610889
    "1"
