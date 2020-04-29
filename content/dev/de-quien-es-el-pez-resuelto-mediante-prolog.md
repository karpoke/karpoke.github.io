Title: «¿De quién es el pez?», resuelto mediante Prolog
Date: 2015-12-26 19:02
Author: Nacho Cano
Tags: acertijo lógico, Einstein, problemas de matemáticas, prolog, swipl
Slug: de-quien-es-el-pez-resuelto-mediante-prolog

Éste es un viejo [acertijo lógico][], atribuido a Einstein:

1. El inglés vive en la casa roja.
2. El sueco tiene perro.
3. El danés toma té.
4. El noruego vive en la primera casa.
5. El Alemán fuma Prince.
6. La casa verde queda inmediatamente a la izquierda de la blanca.
7. El dueño de la casa verde toma café.
8. La persona que fuma Pall Mall cría pájaros.
9. El dueño de la casa amarilla fuma Dunhill.
10. El hombre que vive en la casa del centro toma leche.
11. El hombre que fuma Blends vive al lado del que tiene un gato.
12. El hombre que tiene un caballo vive al lado del que fuma Dunhill.
13. El hombre que fuma Bluemaster toma cerveza.
14. El hombre que fuma Blends es vecino del que toma agua.
15. El noruego vive al lado de la casa azul.

Ante estas afirmaciones, la pregunta es: ¿de quién es el pez?

Veamos una manera de resolverlo utilizando Prolog:

    insertar(E, L, [E|L]).
    insertar(E, [X|Y], [X|Z]):-insertar(E, Y, Z).

    permutacion([], []).
    permutacion([X|Y], Z):-permutacion(Y, L), insertar(X, L, Z).

    posicion(X, [X|L], 1).
    posicion(Y, [X|L], Z):-posicion(Y, L, R), Z is R+1.

    izquierda(X1, X2, L):-posicion(X1, L, P1), posicion(X2, L, P2), P2 is P1+1.

    vecinos(P1, P2):-P1 is P2+1;P2 is P1+1.

    escribir(A, B, C, D, E):-writeln(A), writeln(B), writeln(C), writeln(D), writeln(E).

    de-quien-es-el-pez(L1, L2, L3, L4, L5):-
        permutacion([ingles, sueco, danes, noruego, aleman],  L1),
        permutacion([roja, blanca, verde, amarilla, azul],  L2),

        /_ 1.  El inglés vive en la casa roja. _/
        posicion(ingles, L1, P1),  posicion(roja, L2, P1),

        permutacion([perro, pajaros, gato, caballo, pez],  L3),

        /_ 2.  El sueco tiene perro. _/
        posicion(sueco, L1, P2),  posicion(perro, L3, P2),

        permutacion([te, cafe, leche, cerveza, agua],  L4),

        /_ 3.  El danés toma té. _/
        posicion(danes, L1, P3),  posicion(te, L4, P3),

        /_ 4.  El noruego vive en la primera casa. _/
        posicion(noruego, L1, P4), P4 is 1,

        permutacion([prince, pallmall, dunhill, blends, bluemaster],  L5),

        /_ 5.  El Alemán fuma Prince. _/
        posicion(aleman, L1, P5),  posicion(prince, L5, P5),

        /_ 6.  La casa verde queda inmediatamente a la izquierda de la blanca. _/
        izquierda(verde, blanca, L2),

        /_ 7.  El dueño de la casa verde toma café. _/
        posicion(verde, L2, P6),  posicion(cafe, L4, P6),

        /_ 8.  La persona que fuma Pall Mall cría pájaros. _/
        posicion(pallmall, L5, P7),  posicion(pajaros, L3, P7),

        /_ 9.  El dueño de la casa amarilla fuma Dunhill. _/
        posicion(amarilla, L2, P8),  posicion(dunhill, L5, P8),

        /_ 10. El hombre que vive en la casa del centro toma leche. _/
        posicion(leche, L4, P9), P9 is 3,

        /_ 11. El hombre que fuma Blends vive al lado del que tiene un gato. _/
        posicion(blends, L5, P10),  posicion(gato, L3, P11),  vecinos(P10, P11),

        /_ 12. El hombre que tiene un caballo vive al lado del que fuma Dunhill. _/
        posicion(caballo, L3, P12),  vecinos(P8, P12),

        /_ 13. El hombre que fuma Bluemaster toma cerveza. _/
        posicion(bluemaster, L5, P13),  posicion(cerveza, L4, P13),

        /_ 14. El hombre que fuma Blends es vecino del que toma agua. _/
        posicion(agua, L4, P14),  vecinos(P10, P14),

        /_ 15. El noruego vive al lado de la casa azul. _/
        posicion(azul, L2, P15),  vecinos(P1, P15).

    main:-
        de-quien-es-el-pez(L1, L2, L3, L4, L5),
        escribir(L1, L2, L3, L4, L5).

    main.

Y la solución:

    [noruego,danes,ingles,aleman,sueco]
    [amarilla,azul,roja,verde,blanca]
    [gato,caballo,pajaros,pez,perro]
    [agua,te,leche,cafe,cerveza]
    [dunhill,blends,pallmall,prince,bluemaster]

  [acertijo lógico]: http://hipertextual.com/2015/12/acertijo-de-einstein
    "acertijo lógico"
