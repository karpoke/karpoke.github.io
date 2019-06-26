Title: ¿Un keylogger en Ubuntu?
Date: 2011-07-22 04:35
Author: Nacho Cano
Tags: apparmor, c, ixkeylog, keylogger, perl, selinux, ubuntu, xinput
Slug: un-keylogger-en-ubuntu

El comando `xinput` permite configurar y probar dispositivos de entrada
para las XWindow. Podemos obtener un listado de los dispositivos de
entrada:

```bash
$ xinput list
⎡ Virtual core pointer                      id=2    [master pointer  (3)]
⎜   ↳ Virtual core XTEST pointer                id=4    [slave  pointer  (2)]
⎜   ↳ SynPS/2 Synaptics TouchPad                id=15   [slave  pointer  (2)]
⎣ Virtual core keyboard                     id=3    [master keyboard (2)]
    ↳ Virtual core XTEST keyboard               id=5    [slave  keyboard (3)]
    ↳ Power Button                              id=6    [slave  keyboard (3)]
    ↳ Video Bus                                 id=7    [slave  keyboard (3)]
    ↳ Power Button                              id=8    [slave  keyboard (3)]
    ↳ Sleep Button                              id=9    [slave  keyboard (3)]
    ↳ Laptop_Integrated_Webcam_2M               id=10   [slave  keyboard (3)]
    ↳ AT Translated Set 2 keyboard              id=11   [slave  keyboard (3)]
    ↳ Dell WMI hotkeys                          id=13   [slave  keyboard (3)]
```

También podemos obtener más información de algún dispositivo en
concreto, por ejemplo, del teclado, cuyo identificador, en mi caso, es
el 11:

```bash
$ xinput list --long 11
AT Translated Set 2 keyboard                id=11   [slave  keyboard (3)]
    Reporting 1 classes:
        Class originated from: 11
        Keycodes supported: 248
```

También podemos probar el teclado:

```bash
$ xinput test 11
key release 36
key press   45
kkey release 45
key press   38
akey release 38
key press   27
rkey release 27
key press   33
pkey release 33
key press   32
okey release 32
key press   45
kkey release 45
key press   26
ekey release 26
```

Y el _touchpad_:

```bash
$ xinput test 12
motion a[0]=2565 a[1]=3570
motion a[0]=2568 a[1]=3568
motion a[0]=2571 a[1]=3567
motion a[0]=2573 a[1]=3567
motion a[0]=2575 a[1]=3568
```

Todas las teclas que pulsemos, estemos o no en el terminal, aparecen en
el terminal.

[Esto se debe a que][]:

-   XWindows no implementa ningún mecanismo de [aislamiento entre
    aplicaciones][] que pertenecen a la misma sesión X y, por tanto, una
    aplicación con acceso a la sesión puede monitorizar las teclas
    pulsadas, o los movimientos de ratón.
-   En principio, sólo será un problema si algún programa que utilicemos
    está comprometido o es malicioso. Para aprovechar `xinput` como
    _keylogger_ es necesario tener acceso a la sesión X.
-   Utilizando `AppArmor` se puede reducir el riesgo, haciendo más
    difícil instalar un _keylogger_ de forma permanente. Sin embargo, no
    puede evitar que una aplicación registre las pulsaciones de teclado,
    y si ésta tiene acceso a internet, podría enviarlas a un servidor
    remoto.
-   SELinux podría solucionar el problema. Sin embargo, las extensiones
    XSELinux no se cargan por defecto, no todas tienen una madurez para
    incluirlas en un entorno de producción, ni cuales pueden interferir
    negativamente en otras aplicaciones.

Esta [potencial vulnerabilidad][] podría ser aprovechada, por ejemplo,
por:

-   este [_script_ en Perl][script en Perl] ^[[1][]]^, que hace más sencillo reconocer
    qué teclas se están pulsando:

    ```bash
$ perl keylog2.pl
    Keyboard ID: 11
    Watching `xinput test 11`
    k(shift key: 0)
    [45] press: k
    (shift key: 0)
    [45] release: k
    a(shift key: 0)
    [38] press: a
    (shift key: 0)
    [38] release: a
    r(shift key: 0)
    [27] press: r
    (shift key: 0)
    [27] release: r
    p(shift key: 0)
    [33] press: p
    (shift key: 0)
    [33] release: p
    o(shift key: 0)
    [32] press: o
    (shift key: 0)
    [32] release: o
    k(shift key: 0)
    [45] press: k
    (shift key: 0)
    [45] release: k
    e(shift key: 0)
    [26] press: e
    (shift key: 0)
    [26] release: e
    [105] press: {Ctrl}
    ^C
    ```

-   este [programa en C++][],

    ```bash
$ g++ -lX11 keylogger.cpp -o keylogger
$ ./keylogger
    Keylogger started

    Info about X11 connection:
     The display is:::0.0
     Width::1680    Height::1050
     Connection number is 3
     You’ve got a coloured monitor with depth of 24


    Logging started.

    1311301288.99731492996215820312: 36
    k1311301290.27069497108459472656: 45
    1311301290.30860710144042968750: 45
    a1311301290.34145402908325195312: 38
    1311301290.37259697914123535156: 38
    1311301290.40374803543090820312: 27
    1311301290.40377688407897949219: 38
    r1311301290.43391704559326171875: 27
    1311301290.43394398689270019531: 38
    1311301290.46408295631408691406: 27
    1311301290.46410894393920898438: 33
    p1311301290.49424099922180175781: 27
    1311301290.49426794052124023438: 32 33
    o1311301290.52452206611633300781: 32 33
    k1311301290.55576109886169433594: 32 33
    1311301290.55580902099609375000: 45
    1311301290.58594703674316406250: 32
    1311301290.58597397804260253906: 45
    1311301290.61610102653503417969: 45
    e1311301290.67649888992309570312: 26
    1311301290.71751308441162109375: 26
    1311301291.60019397735595703125: 105
    ^C
    ```

-   o este proyecto, [iXKeyLog][programa en C++],

<a name="dependencias"></a>
[1] El _script_ en Perl utiliza el módulo `IO::Pty::Easy`, y para poder
probarlo en Ubuntu, no basta con la librería `libio-pty-perl` que hay en
los respositorios, necesitaremos [instalar el módulo de CPAN][].

  [Esto se debe a que]: http://ubuntuforums.org/archive/index.php/t-1769484.html
    "Esto se debe a que"
  [aislamiento entre aplicaciones]: http://theinvisiblethings.blogspot.com/2011/04/linux-security-circus-on-gui-isolation.html
    "aislamiento entre aplicaciones"
  [potencial vulnerabilidad]: http://answers.launchpad.net/ubuntu/+source/xorg/+question/159596
    "potencial vulnerabilidad"
  [script en Perl]: http://sh.kirsle.net/keylog2
    "_script_ en Perl"
  [1]: #dependencias
    "instalar dependencias para ejecutar el script en Ubuntu"
  [programa en C++]: http://pastebin.com/sk7FZ6AP
    "programa en C++"
  [instalar el módulo de CPAN]: {filename}/admin/instalar-modulos-de-cpan-usando-cpan.md
    "instalar módulos de CPAN usando CPAN"
