Title: Abrir enlaces externos en una ventana nueva en segundo plano usando jQuery
Date: 2012-05-13 00:58
Author: Nacho Cano
Tags: chromium, firefox, javascript, jQuery, target, xhtml strict
Slug: abrir-enlaces-externos-en-una-ventana-nueva-en-segundo-plano-usando-jquery

Si queremos que nuestros enlaces se abran en una ventana nueva podemos
utilizar el atributo `target` para las etiquetas `<a>`. Sin embargo, si
utilizamos un esquema XHTML Strict este atributo no es válido para
ninguna etiqueta. El motivo es separar la presentación del contenido del
comportamiento, y el atributo `target` modifica el comportamiento.

Una alternativa es utilizar Javascript para conseguir el mismo efecto.
Si Javascript no está disponible simplemente se abrirá en la misma
ventana. Con Javascript, además, podemos conseguir que la ventana se
abra en segundo plano, aunque sólo en algunos navegadores, como por
ejemplo Chromium. [En Firefox es necesario modificar un parámetro][] que
viene desactivado por defecto.

Para activarlo en Firefox, vamos a Herramientas > Opciones. En
Contenido debe estar activado Habilitar Javascript, y en opciones
Avanzadas de Javascript se debe marcar "Abrir o cerrar ventanas".

Para distinguir los enlaces que queramos que se abran en segundo plano
de los que no, por ejemplo enlaces internos, tenemos varias
alternativas. Podemos utilizar el atributo `rel="external"` o asignarles
una clase, y luego utilizar un selector jQuery para seleccionarlos. Algo
así:

```bash
$('a[class="targetclass"]')
```

Otra forma es [aplicar un filtro][] para seleccionar sólo los enlaces
cuya dirección no contenga nuestro dominio.

```javascript
$('a').filter(function() {
    return this.hostname &&
        this.hostname !== location.hostname &&
        this.hostname.indexOf('.'+location.hostname) == -1;
})
```

Este filtro dejaría fuera enlaces cuya ruta contenga nuestro dominio,
algo como `http://example.com/must/see/www.mydomain.com`, aunque lo peor
que sucedería es que el enlace se abriría en la misma ventana.

Una vez que hemos seleccionado los enlaces que queremos, para abrir el
enlace en una ventana en segundo plano, obligamos a que el foco se pase
a la ventana padre:

```javascript
window.open(url);
window.focus();
```

Otra forma es que la ventana hija pierda el foco:

```javascript
var win = window.open(url);
win.blur();
```

Todo junto, utilizando la función `$` de jQuery, que permite ejecutar el
código cuando la página haya cargado:

```javascript
$(function() {
$('a').filter(function() {
        return this.hostname &&
            this.hostname !== location.hostname &&
            this.hostname.indexOf('.'+location.hostname) == -1;
      }).click(function() {
        var win = window.open(this.href);
        win.blur();
        window.focus();
        return false;
    });
});
```

  [En Firefox es necesario modificar un parámetro]: http://stackoverflow.com/questions/2533305/window-focus-self-focus-not-working-in-firefox/2533335#2533335
    "En Firefox es necesario modificar un parámetro"
  [aplicar un filtro]: http://stackoverflow.com/questions/2326872/how-to-match-external-links-with-javascript-but-ignore-subdomains/2326990#2326990
    "aplicar un filtro"
