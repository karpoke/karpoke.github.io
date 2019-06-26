Title: urlencode y urldecode
Date: 2011-03-06 17:45
Author: Nacho Cano
Tags: alias, ASCII, escape, perl, rfc3986, sed, uri, uri_escape, url, urldec, urlenc
Slug: urlencode-y-urldecode

Los siguientes caracteres [son los únicos que se pueden utilizar][] en
una URL:

```bash
[a-zA-Z0-9-._~]
```

El resto, se deben codificar usando el prefijo `%` seguido del valor
ASCII hexadecimal del carácter. Por ejemplo:

```bash
( = %28
) = %29
/ = %2F
+ = %2B
...
```

Para [codificar la URL][] podemos utilizar la función `uri_escape` del
módulo `URI` de Perl.

```bash
alias urlenc='furlenc() { perl -MURI::Escape -e "print uri_escape(\"$1\").\"\n\";"; }; furlenc'
```

```bash
$ urlenc http://www.google.com
http%3A%2F%2Fwww.google.com
```

Para la [decodificación de la URL][], podemos hacer uso de `sed`:

```bash
alias urldec='furldec() { echo "$1" | sed -e'\''s/%\([0-9A-F][0-9A-F]\)/\\\\\x\1/g'\'' | xargs echo -e; }; furldec'
```

```bash
$ urldec http%3A%2F%2Fwww.google.com
http://www.google.com
```

  [son los únicos que se pueden utilizar]: http://tools.ietf.org/html/rfc3986#section-2.3
    "son los únicos que se pueden utilizar"
    "rfc3986"
  [codificar la URL]: http://stackoverflow.com/questions/296536/urlencode-from-a-bash-script/298258#298258
    "codificar la URL"
  [decodificación de la URL]: http://www.commandlinefu.com/commands/view/2285/urldecoding
    "decodificación de la URL"
