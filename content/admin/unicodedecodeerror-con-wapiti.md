Title: UnicodeDecodeError con Wapiti
Date: 2011-05-28 17:32
Author: Nacho Cano
Tags: 11.04, ASCII, crlf injection, cross site scripting, escáner de vulnerabilidades, ldap injection, python, sql injection, ubuntu natty narwhal, uft-8, unicode, wapiti, xpath injection, xss
Slug: unicodedecodeerror-con-wapiti

[Wapiti][] es un escáner de vulnerabilidades web basado en
[_fuzzing_][]. En la última versión, [2.2.1][], permite detectar
vulnerabilidades referente a:

-   Errores de gestión de ficheros (include/require local y remoto,
    fopen, readfile...)
-   Database Injection (PHP/JSP/ASP SQL Injections y XPath Injections)
-   XSS (Cross Site Scripting) Injection
-   LDAP Injection
-   Command Execution detection (eval(), system(), passtru()...)
-   CRLF Injection (HTTP Response Splitting, session fixation...)

Sin embargo, si usamos Ubuntu Natty Narwhal, la versión de los
repositorios es la 1.1.6, por lo que es posible que nos encontremos el
siguiente error al escanear páginas que contengan [caracteres no
ASCII][]. Por ejemplo:

```bash
$ wapiti http://127.0.0.1/ -v 1 -m GET_XSS -u
Wapiti-1.1.6 (wapiti.sourceforge.net)
Traceback (most recent call last):
  File "/usr/bin/wapiti", line 943, in
    wap.browse()
  File "/usr/bin/wapiti", line 123, in browse
    self.myls.go()
  File "/usr/share/wapiti/lswww.py", line 396, in go
    if self.browse(lien):
  File "/usr/share/wapiti/lswww.py", line 207, in browse
    p.feed(htmlSource)
  File "/usr/lib/python2.7/HTMLParser.py", line 108, in feed
    self.goahead(0)
  File "/usr/lib/python2.7/HTMLParser.py", line 148, in goahead
    k = self.parse_starttag(i)
  File "/usr/lib/python2.7/HTMLParser.py", line 252, in parse_starttag
    attrvalue = self.unescape(attrvalue)
  File "/usr/lib/python2.7/HTMLParser.py", line 393, in unescape
    return re.sub(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));", replaceEntities, s)
  File "/usr/lib/python2.7/re.py", line 151, in sub
    return _compile(pattern, flags).sub(repl, string, count)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc2 in position 0: ordinal not in range(128)
```

Parece ser que este error está [solucionado en la versión en
desarrollo][], por lo que lo mejor sería [probar la última versión][].

Aún así, podemos evitarlo modificando el fichero
`vim /usr/share/wapiti/lswww.py`, y cambiando las ocurrencias de:

```python
p.feed(htmlSource)
```

por:

```python
p.feed(htmlSource.decode("utf-8", "replace"))
```

  [Wapiti]: http://wapiti.sourceforge.net/
    "Wapiti"
  [_fuzzing_]: http://omniumpotentior.wordpress.com/2011/05/18/fuzzing-web-con-wapiti/
    "_fuzzing_"
  [2.2.1]: http://wapiti.sourceforge.net/README
    "2.2.1"
  [caracteres no ASCII]: http://wiki.python.org/moin/UnicodeDecodeError
    "caracteres no ASCII"
  [solucionado en la versión en desarrollo]: http://sourceforge.net/tracker/index.php?func=detail&aid=2828777&group_id=168625&atid=847490
    "solucionado en la versión en desarrollo"
  [probar la última versión]: http://sourceforge.net/projects/wapiti/
    "probar la última versión"
