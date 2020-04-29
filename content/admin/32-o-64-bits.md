Title: 32 ó 64 bits
Date: 2011-01-18 15:41
Author: Nacho Cano
Tags: arch, dpkg-architecture, flags, getconf, lm, uname, lshw
Slug: 32-o-64-bits

Para saber si el procesador es de 64 bits, ejecutamos el siguiente
comando:

    $ grep flags /proc/cpuinfo | grep -Eo " lm " && echo "64" || echo "32"
    32

Otro comando que nos dirá si la arquitectura es de 32 ó 64 bits es `lshw`:

    $ sudo lshw -C CPU | grep width
    width: 32 bits

Para saber si el sistema operativo es de 32 ó 64 bits ejecutamos el
siguiente comando:

    $ getconf LONG_BIT
    32

    $ uname -m
    i686

    $ arch  # es lo mismo que la anterior
    i6868

Otro comando útil es `dpkg-architecture`:

    $ dpkg-architecture
    DEB_BUILD_ARCH=i386
    DEB_BUILD_ARCH_BITS=32
    DEB_BUILD_ARCH_CPU=i386
    DEB_BUILD_ARCH_ENDIAN=little
    DEB_BUILD_ARCH_OS=linux
    DEB_BUILD_GNU_CPU=i686
    DEB_BUILD_GNU_SYSTEM=linux-gnu
    DEB_BUILD_GNU_TYPE=i686-linux-gnu
    DEB_BUILD_MULTIARCH=i386-linux-gnu
    DEB_HOST_ARCH=i386
    DEB_HOST_ARCH_BITS=32
    DEB_HOST_ARCH_CPU=i386
    DEB_HOST_ARCH_ENDIAN=little
    DEB_HOST_ARCH_OS=linux
    DEB_HOST_GNU_CPU=i686
    DEB_HOST_GNU_SYSTEM=linux-gnu
    DEB_HOST_GNU_TYPE=i686-linux-gnu
    DEB_HOST_MULTIARCH=i386-linux-gnu
