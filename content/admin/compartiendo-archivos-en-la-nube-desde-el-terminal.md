Title: Compartiendo archivos en la nube desde el terminal
Date: 2014-09-06 17:45
Author: Nacho Cano
Tags: compartir, curl, gpg, phantomjs, webkit
Slug: compartiendo-archivos-en-la-nube-desde-el-terminal

Hay muchas maneras de compartir archivos, pero con [curl.io][] podemos
hacerlo directamente desde el terminal usando `curl`, permitiéndonos
archivos hasta 5 GB y durante 4 horas, tiempo tras el cual será
eliminados.

Por ejemplo, para compartir el archivo `/tmp/test`:

```bash
$ curl -F "file=@/tmp/test" http://curl.io/send/nzdqxcmf


File successfully received.

You can download test from this url:

http://curl.io/get/nzdqxcmf/90571b24cf847434a171d41cb2043d6a561cb85b
```

Para recuperarlo:

```bash
$ curl -o test http://curl.io/get/nzdqxcmf/90571b24cf847434a171d41cb2043d6a561cb85b
```

Tal como nos sugieren en su web, también podemos enviarlo cifrado con
`gpg`:

```bash
$ gpg -c "/tmp/test" && curl -F "file=@/tmp/test.gpg" http://curl.io/send/nzdqxcmf
```

Para recuperarlo y descifrarlo:

```bash
curl http://curl.io/get/nzdqxcmf/90571b24cf847434a171d41cb2043d6a561cb85b | gpg -o test
```

Absolutamente todo desde el terminal
------------------------------------

El hecho de poder compartir archivos en la nube desde el terminal está
muy bien, pero no deja de ser un engorro tener que recurrir al navegador
para poder obtener la URL de envío. Descargar el código fuente de la
página no nos sirve porque la URL se genera por javascript y en la web
se comprueba que el código de la URL sea válido (no sirve enviar
cualquier cosa, aunque sí parece que se pueden reutilizar URLs válidas).

Afortunadamente, podemos utilizar [phantomjs][]. Mediante el siguiente
_script_, `curlio.js`, podremos obtener una URL de envío válida:

```javascript
var page  = require('webpage').create(),
  address = "http://curl.io";

page.open(address, function(status) {
  if (status !== 'success') {
    console.log('Error loading address');
  } else {
    var url = page.evaluate(function() {
      return document.getElementsByClassName('command')[0].innerHTML.replace(/^.*/, "");
    });
    console.log(url);
  }
  phantom.exit();
});
```

Un ejemplo de uso:

```bash
$ phantomjs curlio.js
http://curl.io/send/fgmnwl2e
```

  [curl.io]: http://curl.io/
    "curl.io"
  [phantomjs]: http://phantomjs.org/
    "phantomjs"
