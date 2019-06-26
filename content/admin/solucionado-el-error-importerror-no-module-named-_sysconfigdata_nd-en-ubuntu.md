Title: Solucionado el error «ImportError: No module named _sysconfigdata_nd» en Ubuntu
Date: 2014-11-13 22:32
Author: Nacho Cano
Tags: _sysconfigdata_nd.py, ImportError, python2.7, virtualenv
Slug: solucionado-el-error-importerror-no-module-named-_sysconfigdata_nd-en-ubuntu

Si estando en un entorno virtual, nos encontramos con el error:

```bash
ImportError: No module named _sysconfigdata_nd
```

Es debido a un [conocido error en Ubuntu][], por el cual dicho fichero
se encuentra en otra ubicación, en lugar de `/usr/lib/python2.7`.

En 32 bits:

```bash
$ dpkg -S _sysconfigdata_nd.py
libpython2.7-minimal:i386: /usr/lib/python2.7/plat-i386-linux-gnu/_sysconfigdata_nd.py
```

En 64 bits:

```bash

$ dpkg -S _sysconfigdata_nd.py
libpython2.7-minimal:amd64: /usr/lib/python2.7/plat-x86_64-linux-gnu/_sysconfigdata_nd.py
```

Una manera de evitarlo es crear un enlace simbólico:

```bash
$ cd /usr/lib/python2.7
$ sudo ln -s plat-*/_sysconfigdata_nd.py .
```

  [conocido error en Ubuntu]: https://bugs.launchpad.net/ubuntu/+source/python2.7/+bug/1115466
    "conocido error en Ubuntu"
