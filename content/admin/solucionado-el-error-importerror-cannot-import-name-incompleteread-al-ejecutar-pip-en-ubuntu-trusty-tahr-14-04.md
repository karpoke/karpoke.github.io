Title: Solucionado el error «ImportError: cannot import name IncompleteRead» al ejecutar pip en Ubuntu Trusty Tahr 14.04
Date: 2015-01-02 13:02
Author: Nacho Cano
Tags: 14.04, IncompleteRead, pip, requests, ubuntu trusty tahr
Slug: solucionado-el-error-importerror-cannot-import-name-incompleteread-al-ejecutar-pip-en-ubuntu-trusty-tahr-14-04

Si al ejecutar `pip` nos encontramos con el siguiente error:

```bash
Traceback (most recent call last):
  File "/usr/bin/pip", line 9, in
    load_entry_point('pip==1.5.4', 'console_scripts', 'pip')()
  File "/usr/local/lib/python2.7/dist-packages/pkg_resources.py", line 352, in load_entry_point
    return get_distribution(dist).load_entry_point(group, name)
  File "/usr/local/lib/python2.7/dist-packages/pkg_resources.py", line 2307, in load_entry_point
    return ep.load()
  File "/usr/local/lib/python2.7/dist-packages/pkg_resources.py", line 2021, in load
    entry = __import__(self.module_name, globals(),globals(), ['__name__'])
  File "/usr/lib/python2.7/dist-packages/pip/__init__.py", line 11, in
    from pip.vcs import git, mercurial, subversion, bazaar # noqa
  File "/usr/lib/python2.7/dist-packages/pip/vcs/mercurial.py", line 9, in
    from pip.download import path_to_url
  File "/usr/lib/python2.7/dist-packages/pip/download.py", line 25, in
    from requests.compat import IncompleteRead
ImportError: cannot import name IncompleteRead
```

Parece ser debido a un [problema entre el paquete `requests` y `pip`][problema entre el paquete requests y pip].
A partir de las [versión 2.4.0][] de `requests` se eliminó
`requests.compat.IncompleteRead`. Sin embargo, las versiones de `pip`
anteriores a [julio de 2014][] aún utilizan `IncompleteRead`.

En la vesión actual de `pip` ya no ocurre este problema por lo que la
solución pasa por [actualizarlo][]:

```bash
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python get-pip.py
```

  [problema entre el paquete requests y pip]: http://stackoverflow.com/a/27341847
    "problema entre el paquete `requests` y `pip`"
  [versión 2.4.0]: https://github.com/tweepy/tweepy/issues/501
    "versión 2.4.0"
  [julio de 2014]: https://github.com/pypa/pip/blob/0dedf2b6f5adefcc29d3d295318a7ebc916fc822/pip/download.py
    "julio de 2014"
  [actualizarlo]: https://pip.pypa.io/en/latest/installing.html
    "actualizarlo"
