Title: Solucionado el error «DistributionNotFound» al usar pip
Date: 2013-07-28 13:52
Author: Nacho Cano
Tags: distributionerror, easy_install, pip
Slug: solucionado-el-error-distributionnotfound-al-usar-pip

Si al ejecutar `pip`, nos aparece el siguiente error:

```bash
$ pip
Traceback (most recent call last):
  File "/usr/local/bin/pip", line 5, in
    from pkg_resources import load_entry_point
  File "/usr/lib/python2.7/dist-packages/pkg_resources.py", line 2707, in
    working_set.require(__requires__)
  File "/usr/lib/python2.7/dist-packages/pkg_resources.py", line 686, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/usr/lib/python2.7/dist-packages/pkg_resources.py", line 584, in resolve
    raise DistributionNotFound(req)
pkg_resources.DistributionNotFound: pip==1.1
```

puede ser debido a que es necesario actualizar el propio `pip`:

```bash
$ sudo easy_install --upgrade pip
Searching for pip
Reading http://pypi.python.org/simple/pip/
Best match: pip 1.4
Downloading https://pypi.python.org/packages/source/p/pip/pip-1.4.tar.gz#md5=ca790be30004937987767eac42cfa44a
Processing pip-1.4.tar.gz
Running pip-1.4/setup.py -q bdist_egg --dist-dir /tmp/easy_install-XSmFvr/pip-1.4/egg-dist-tmp-jmeGZW
warning: no files found matching '*.html' under directory 'docs'
warning: no previously-included files matching '*.rst' found under directory 'docs/_build'
no previously-included directories found matching 'docs/_build/_sources'
Adding pip 1.4 to easy-install.pth file
Installing pip script to /usr/local/bin
Installing pip-2.7 script to /usr/local/bin

Installed /usr/local/lib/python2.7/dist-packages/pip-1.4-py2.7.egg
Processing dependencies for pip
Finished processing dependencies for pip
```

Comprobamos que se ha solucionado:

```bash
$ pip

Usage:
  pip  [options]

Commands:
  install                     Install packages.
  uninstall                   Uninstall packages.
  freeze                      Output installed packages in requirements format.
  list                        List installed packages.
  show                        Show information about installed packages.
  search                      Search PyPI for packages.
  wheel                       Build wheels from your requirements.
  zip                         Zip individual packages.
  unzip                       Unzip individual packages.
  bundle                      Create pybundles.
  help                        Show help for commands.

General Options:
  -h, --help                  Show help.
  -v, --verbose               Give more output. Option is additive, and can be used up to 3 times.
  -V, --version               Show version and exit.
  -q, --quiet                 Give less output.
  --log                 Log file where a complete (maximum verbosity) record will be kept.
  --proxy              Specify a proxy in the form [user:passwd@]proxy.server:port.
  --timeout              Set the socket timeout (default 15 seconds).
  --exists-action     Default action when a path already exists: (s)witch, (i)gnore, (w)ipe, (b)ackup.
  --cert                Path to alternate CA bundle.
```

Referencias
-----------

» [stackoverflow.com][]

  [stackoverflow.com]: http://stackoverflow.com/questions/6200056/pip-broke-how-to-fix-distributionnotfound-error
    "stackoverflow.com"
